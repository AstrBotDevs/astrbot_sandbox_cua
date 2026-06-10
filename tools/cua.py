from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from astrbot.api import FunctionTool
from astrbot.core.agent.run_context import ContextWrapper
from astrbot.core.agent.tool import ToolExecResult
from astrbot.core.astr_agent_context import AstrAgentContext
from astrbot.core.computer.computer_client import get_booter
from astrbot.core.computer.sandbox_tool_binding import sandbox_provider_tool
from astrbot.core.tools.computer_tools.util import check_admin_permission

_CUA_TOOL_CONFIG = {
    "provider_settings.computer_use_runtime": "sandbox",
    "provider_settings.sandbox.booter": "cua",
}


def _to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


def _exception_detail(error: Exception) -> str:
    return str(error) or type(error).__name__


async def _get_gui_component(context: ContextWrapper[AstrAgentContext]) -> Any:
    booter = await get_booter(
        context.context.context,
        context.context.event.unified_msg_origin,
    )
    gui = getattr(booter, "gui", None)
    if gui is None:
        raise RuntimeError(
            "Current sandbox booter does not support CUA GUI capability. "
            "Please switch sandbox booter to cua."
        )
    return gui


@sandbox_provider_tool("cua", config=_CUA_TOOL_CONFIG)
@dataclass
class CuaMouseClickTool(FunctionTool):
    name: str = "astrbot_cua_mouse_click"
    description: str = "Click a coordinate in the CUA sandbox desktop."
    parameters: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X coordinate."},
                "y": {"type": "integer", "description": "Y coordinate."},
                "button": {
                    "type": "string",
                    "description": "Mouse button, usually left, right, or middle.",
                    "default": "left",
                },
            },
            "required": ["x", "y"],
        }
    )

    async def call(
        self,
        context: ContextWrapper[AstrAgentContext],
        x: int,
        y: int,
        button: str = "left",
    ) -> ToolExecResult:
        if err := check_admin_permission(context, "Using CUA mouse"):
            return err
        try:
            gui = await _get_gui_component(context)
            return _to_json(await gui.click(x, y, button=button))
        except Exception as e:
            return f"Error clicking CUA desktop: {_exception_detail(e)}"


@sandbox_provider_tool("cua", config=_CUA_TOOL_CONFIG)
@dataclass
class CuaKeyboardTypeTool(FunctionTool):
    name: str = "astrbot_cua_keyboard_type"
    description: str = "Type text into the CUA sandbox desktop."
    parameters: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to type."},
            },
            "required": ["text"],
        }
    )

    async def call(
        self,
        context: ContextWrapper[AstrAgentContext],
        text: str,
    ) -> ToolExecResult:
        if err := check_admin_permission(context, "Using CUA keyboard"):
            return err
        try:
            gui = await _get_gui_component(context)
            return _to_json(await gui.type_text(text))
        except Exception as e:
            return f"Error typing in CUA desktop: {_exception_detail(e)}"
