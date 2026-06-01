import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = types.ModuleType("astrbot_sandbox_cua")
PACKAGE.__path__ = [str(ROOT)]
BOOTERS_PACKAGE = types.ModuleType("astrbot_sandbox_cua.booters")
BOOTERS_PACKAGE.__path__ = [str(ROOT / "booters")]


class _DummyLogger:
    def warning(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass


astrbot = types.ModuleType("astrbot")
astrbot_api = types.ModuleType("astrbot.api")
astrbot_api.logger = _DummyLogger()
astrbot_core = types.ModuleType("astrbot.core")
astrbot_computer = types.ModuleType("astrbot.core.computer")
astrbot_olayer = types.ModuleType("astrbot.core.computer.olayer")
astrbot_booters = types.ModuleType("astrbot.core.computer.booters")
astrbot_booters_base = types.ModuleType("astrbot.core.computer.booters.base")
astrbot_star = types.ModuleType("astrbot.core.star")
astrbot_star_context = types.ModuleType("astrbot.core.star.context")


class _ComputerBooter:
    pass


class _Context:
    pass


for component in (
    "BrowserComponent",
    "FileSystemComponent",
    "GUIComponent",
    "PythonComponent",
    "ShellComponent",
):
    setattr(astrbot_olayer, component, type(component, (), {}))

astrbot_booters_base.ComputerBooter = _ComputerBooter
astrbot_star_context.Context = _Context

sys.modules.setdefault("astrbot", astrbot)
sys.modules.setdefault("astrbot.api", astrbot_api)
sys.modules.setdefault("astrbot.core", astrbot_core)
sys.modules.setdefault("astrbot.core.computer", astrbot_computer)
sys.modules.setdefault("astrbot.core.computer.olayer", astrbot_olayer)
sys.modules.setdefault("astrbot.core.computer.booters", astrbot_booters)
sys.modules.setdefault("astrbot.core.computer.booters.base", astrbot_booters_base)
sys.modules.setdefault("astrbot.core.star", astrbot_star)
sys.modules.setdefault("astrbot.core.star.context", astrbot_star_context)
sys.modules.setdefault("astrbot_sandbox_cua", PACKAGE)
sys.modules.setdefault("astrbot_sandbox_cua.booters", BOOTERS_PACKAGE)

from astrbot_sandbox_cua.provider import CuaSandboxProvider  # noqa: E402


def test_provider_declares_persistent_reconnect():
    provider = CuaSandboxProvider()

    assert provider.supports_persistent_reconnect is True


def test_build_connect_info_uses_stable_sandbox_id_for_persistent_name():
    provider = CuaSandboxProvider()

    connect_info = provider.build_connect_info(
        "display name",
        {"sandbox_id": "cua-abcd", "local": True, "image": "linux"},
    )

    assert connect_info["name"] == "display name"
    assert connect_info["persistent_name"] == "cua-abcd"


def test_renaming_sandbox_preserves_persistent_name():
    provider = CuaSandboxProvider()

    connect_info = provider.update_connect_info(
        {"sandbox_id": "cua-abcd", "connect_info": {"persistent_name": "cua-abcd"}},
        sandbox_name="new display name",
    )

    assert connect_info["name"] == "new display name"
    assert connect_info["persistent_name"] == "cua-abcd"
