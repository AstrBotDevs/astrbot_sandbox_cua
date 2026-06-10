import asyncio
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest


import sys
import types


class _DummyLogger:
    def warning(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass


astrbot = types.ModuleType("astrbot")
astrbot_api = types.ModuleType("astrbot.api")
astrbot_api.logger = _DummyLogger()
astrbot_api.FunctionTool = type("FunctionTool", (), {})
astrbot_api_event = types.ModuleType("astrbot.api.event")
astrbot_api_event.filter = SimpleNamespace(command=lambda *a, **k: lambda f: f)
astrbot_api_star = types.ModuleType("astrbot.api.star")
astrbot_api_star.Context = type("Context", (), {})
astrbot_api_star.Star = type("Star", (), {"__init__": lambda self, context: None})
astrbot_api_star.register = lambda *a, **k: lambda cls: cls
astrbot_core = types.ModuleType("astrbot.core")
astrbot_agent = types.ModuleType("astrbot.core.agent")
astrbot_agent_run_context = types.ModuleType("astrbot.core.agent.run_context")
astrbot_agent_run_context.ContextWrapper = type(
    "ContextWrapper", (), {"__class_getitem__": classmethod(lambda cls, item: cls)}
)
astrbot_agent_tool = types.ModuleType("astrbot.core.agent.tool")
astrbot_agent_tool.ToolExecResult = type("ToolExecResult", (), {})
astrbot_astr_agent_context = types.ModuleType("astrbot.core.astr_agent_context")
astrbot_astr_agent_context.AstrAgentContext = type("AstrAgentContext", (), {})
astrbot_computer = types.ModuleType("astrbot.core.computer")
astrbot_sandbox_tool_binding = types.ModuleType(
    "astrbot.core.computer.sandbox_tool_binding"
)
astrbot_sandbox_tool_binding.sandbox_provider_tool = lambda *a, **k: lambda cls: cls
astrbot_computer_client = types.ModuleType("astrbot.core.computer.computer_client")
astrbot_computer_client.cleanup_sandbox_provider = None
astrbot_computer_client.detach_sandbox_provider = None
astrbot_computer_client.register_sandbox_provider = lambda *a, **k: None
astrbot_computer_client.get_booter = None
astrbot_computer_client.sync_skills_to_active_sandboxes = lambda *a, **k: None
astrbot_olayer = types.ModuleType("astrbot.core.computer.olayer")
for component in (
    "BrowserComponent",
    "FileSystemComponent",
    "GUIComponent",
    "PythonComponent",
    "ShellComponent",
):
    setattr(astrbot_olayer, component, type(component, (), {}))
astrbot_booters = types.ModuleType("astrbot.core.computer.booters")
astrbot_booters_base = types.ModuleType("astrbot.core.computer.booters.base")
astrbot_booters_base.ComputerBooter = type("ComputerBooter", (), {})
astrbot_sandbox_timeouts = types.ModuleType("astrbot.core.computer.sandbox_timeouts")
astrbot_sandbox_timeouts.resolve_sandbox_timeout = (
    lambda config, key, aliases=(), default=0: config.get(
        key, config.get(aliases[0], default) if aliases else default
    )
)
astrbot_message_result = types.ModuleType("astrbot.core.message.message_event_result")
astrbot_message_result.MessageChain = type("MessageChain", (), {})
astrbot_tools_util = types.ModuleType("astrbot.core.tools.computer_tools.util")
astrbot_tools_util.check_admin_permission = lambda *a, **k: True
astrbot_path = types.ModuleType("astrbot.core.utils.astrbot_path")
astrbot_path.get_astrbot_temp_path = lambda: "/tmp"
astrbot_star = types.ModuleType("astrbot.core.star")
astrbot_star_context = types.ModuleType("astrbot.core.star.context")
astrbot_star_context.Context = type("Context", (), {})
mcp = types.ModuleType("mcp")

PACKAGE = types.ModuleType("astrbot_sandbox_cua")
PACKAGE.__path__ = [str(Path(__file__).resolve().parent)]
BOOTERS_PACKAGE = types.ModuleType("astrbot_sandbox_cua.booters")
BOOTERS_PACKAGE.__path__ = [str(Path(__file__).resolve().parent / "booters")]
TOOLS_PACKAGE = types.ModuleType("astrbot_sandbox_cua.tools")
TOOLS_PACKAGE.__path__ = [str(Path(__file__).resolve().parent / "tools")]
TOOLS_PACKAGE.CuaKeyboardTypeTool = type("CuaKeyboardTypeTool", (), {})
TOOLS_PACKAGE.CuaMouseClickTool = type("CuaMouseClickTool", (), {})

for name, module in {
    "astrbot": astrbot,
    "astrbot.api": astrbot_api,
    "astrbot.api.event": astrbot_api_event,
    "astrbot.api.star": astrbot_api_star,
    "astrbot.core": astrbot_core,
    "astrbot.core.agent": astrbot_agent,
    "astrbot.core.agent.run_context": astrbot_agent_run_context,
    "astrbot.core.agent.tool": astrbot_agent_tool,
    "astrbot.core.astr_agent_context": astrbot_astr_agent_context,
    "astrbot.core.computer": astrbot_computer,
    "astrbot.core.computer.sandbox_tool_binding": astrbot_sandbox_tool_binding,
    "astrbot.core.computer.computer_client": astrbot_computer_client,
    "astrbot.core.computer.olayer": astrbot_olayer,
    "astrbot.core.computer.booters": astrbot_booters,
    "astrbot.core.computer.booters.base": astrbot_booters_base,
    "astrbot.core.computer.sandbox_timeouts": astrbot_sandbox_timeouts,
    "astrbot.core.message.message_event_result": astrbot_message_result,
    "astrbot.core.tools.computer_tools.util": astrbot_tools_util,
    "astrbot.core.utils.astrbot_path": astrbot_path,
    "astrbot.core.star": astrbot_star,
    "astrbot.core.star.context": astrbot_star_context,
    "astrbot_sandbox_cua": PACKAGE,
    "astrbot_sandbox_cua.booters": BOOTERS_PACKAGE,
    "astrbot_sandbox_cua.tools": TOOLS_PACKAGE,
    "mcp": mcp,
}.items():
    sys.modules.setdefault(name, module)

from astrbot_sandbox_cua import provider as provider_module  # noqa: E402
from astrbot_sandbox_cua import main as plugin_main  # noqa: E402
from astrbot_sandbox_cua.booters import cua as cua_module  # noqa: E402
from astrbot_sandbox_cua.booters.cua import (  # noqa: E402
    CuaBooter,
    _write_base64_via_shell,
)


def install_fake_import(monkeypatch, modules: dict[str, object]) -> None:
    original_import = __import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in modules:
            return modules[name]
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", fake_import)


@pytest.mark.asyncio
async def test_cua_booter_uses_persistent_create_and_disconnects_on_shutdown(
    monkeypatch,
):
    calls = []

    class FakeSandbox:
        def __init__(self, name: str):
            self.name = name
            self.shell = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.python = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.filesystem = SimpleNamespace()
            self.mouse = SimpleNamespace(click=lambda *args, **kwargs: None)
            self.keyboard = SimpleNamespace(type=lambda *args, **kwargs: None)

        async def disconnect(self):
            calls.append(("disconnect", self.name))

    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        @staticmethod
        async def create(image, *, name=None, local=False, **kwargs):
            calls.append(("create", image, {"name": name, "local": local, **kwargs}))
            return FakeSandbox(name)

        @staticmethod
        def ephemeral(*args, **kwargs):
            raise AssertionError("persistent mode must not use Sandbox.ephemeral")

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
    )

    await booter.boot("ignored-session")
    await booter.shutdown()

    assert calls[0] == (
        "create",
        "linux-image",
        {
            "name": "cua-persistent-1",
            "local": True,
        },
    )
    assert calls[1] == ("disconnect", "cua-persistent-1")


@pytest.mark.asyncio
async def test_cua_terminate_detaches_even_if_cleanup_fails(monkeypatch):
    calls = []

    class FakeProvider:
        provider_id = "cua"

    async def fake_cleanup(provider_id):
        calls.append(("cleanup", provider_id))
        raise RuntimeError("cleanup failed")

    def fake_detach(provider_id):
        calls.append(("detach", provider_id))

    monkeypatch.setattr(plugin_main, "cleanup_sandbox_provider", fake_cleanup)
    monkeypatch.setattr(plugin_main, "detach_sandbox_provider", fake_detach)

    plugin = plugin_main.CuaSandboxRuntimePlugin.__new__(
        plugin_main.CuaSandboxRuntimePlugin
    )
    plugin.provider = FakeProvider()

    with pytest.raises(RuntimeError, match="cleanup failed"):
        await plugin.terminate()

    assert calls == [("cleanup", "cua"), ("detach", "cua")]


@pytest.mark.asyncio
async def test_cua_terminate_noops_when_provider_missing(monkeypatch):
    calls = []

    def fake_detach(provider_id):
        calls.append(("detach", provider_id))

    monkeypatch.setattr(plugin_main, "detach_sandbox_provider", fake_detach)

    plugin = plugin_main.CuaSandboxRuntimePlugin.__new__(
        plugin_main.CuaSandboxRuntimePlugin
    )
    plugin.provider = None

    await plugin.terminate()

    assert calls == []


@pytest.mark.asyncio
async def test_cua_booter_resumes_persistent_runtime_when_resume_enabled(monkeypatch):
    calls = []

    class FakeSandbox:
        def __init__(self, name: str):
            self.name = name
            self.shell = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.python = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.filesystem = SimpleNamespace()
            self.mouse = SimpleNamespace(click=lambda *args, **kwargs: None)
            self.keyboard = SimpleNamespace(type=lambda *args, **kwargs: None)

        async def disconnect(self):
            calls.append(("disconnect", self.name))

    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        connect = None

        @staticmethod
        async def resume(name, **kwargs):
            calls.append(("resume", name, kwargs))
            return FakeSandbox(name)

        @staticmethod
        async def create(*args, **kwargs):
            raise AssertionError("resume path must not create a new sandbox")

        @staticmethod
        def ephemeral(*args, **kwargs):
            raise AssertionError("resume path must not use Sandbox.ephemeral")

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
        resume=True,
    )

    await booter.boot("ignored-session")

    assert calls == [("resume", "cua-persistent-1", {"local": True})]


@pytest.mark.asyncio
async def test_cua_provider_passes_persistent_runtime_name_for_persistent_sandbox(
    monkeypatch,
):
    recorded = {}

    class FakeBooter:
        def __init__(self, **kwargs):
            recorded.update(kwargs)

        async def boot(self, session_id: str):
            recorded["boot_session_id"] = session_id

        async def shutdown(self):
            return None

    monkeypatch.setattr(
        provider_module, "cua_booter", SimpleNamespace(CuaBooter=FakeBooter)
    )

    provider = provider_module.CuaSandboxProvider()
    booter = await provider.create_booter(
        context=object(),
        session_id="dashboard",
        sandbox_id="cua-123",
        config={
            "image": "linux",
            "os_type": "linux",
            "local": True,
            "persistent": True,
            "persistent_name": "cua-123",
        },
    )

    assert recorded["persistent"] is True
    assert recorded["persistent_name"] == "cua-123"
    assert recorded["resume"] is False
    assert (
        recorded["boot_session_id"] == uuid.uuid5(uuid.NAMESPACE_DNS, "dashboard").hex
    )
    assert getattr(booter, "sandbox_id") == "cua-123"


def test_cua_provider_build_connect_info_uses_sandbox_id_for_persistent_name():
    provider = provider_module.CuaSandboxProvider()

    info = provider.build_connect_info(
        "display-name",
        {"sandbox_id": "cua-runtime-1", "local": True},
    )

    assert info["name"] == "display-name"
    assert info["persistent_name"] == "cua-runtime-1"


def test_cua_provider_update_connect_info_preserves_persistent_name():
    provider = provider_module.CuaSandboxProvider()
    record = {
        "sandbox_id": "cua-123",
        "connect_info": {
            "name": "old-display-name",
            "persistent_name": "cua-runtime-1",
        },
    }

    updated = provider.update_connect_info(record, sandbox_name="new-display-name")

    assert updated["name"] == "new-display-name"
    assert updated["persistent_name"] == "cua-runtime-1"


def test_cua_provider_update_connect_info_adds_missing_persistent_name_from_sandbox_id():
    provider = provider_module.CuaSandboxProvider()
    record = {
        "sandbox_id": "cua-runtime-1",
        "connect_info": {"name": "old-display-name"},
    }

    updated = provider.update_connect_info(record, sandbox_name="new-display-name")

    assert updated["name"] == "new-display-name"
    assert updated["persistent_name"] == "cua-runtime-1"


@pytest.mark.asyncio
async def test_cua_provider_resume_repairs_legacy_display_name_persistent_name(
    monkeypatch,
):
    recorded = {}

    class FakeBooter:
        def __init__(self, **kwargs):
            recorded.update(kwargs)

        async def boot(self, session_id: str):
            recorded["boot_session_id"] = session_id

        async def shutdown(self):
            return None

    class FakeSandboxState:
        @staticmethod
        def load(name):
            if name == "cua-123":
                return {"name": name, "status": "running"}
            return None

    fake_state_module = SimpleNamespace(sandbox_state=FakeSandboxState)

    install_fake_import(monkeypatch, {"cua_sandbox": fake_state_module})
    monkeypatch.setattr(
        provider_module, "cua_booter", SimpleNamespace(CuaBooter=FakeBooter)
    )

    provider = provider_module.CuaSandboxProvider()
    await provider.create_booter(
        context=object(),
        session_id="dashboard",
        sandbox_id="cua-123",
        config={
            "local": True,
            "persistent_name": "display-name",
            "resume": True,
        },
    )

    assert recorded["persistent_name"] == "cua-123"
    assert recorded["resume"] is True


@pytest.mark.asyncio
async def test_cua_provider_does_not_trust_stale_local_state(monkeypatch):
    class FakeSandboxState:
        @staticmethod
        def load(name):
            if name == "cua-stale":
                return {"name": name, "status": "running"}
            return None

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            raise RuntimeError(f"no local sandbox named {name}")

        @staticmethod
        async def resume(name, **kwargs):
            raise RuntimeError(f"no local sandbox named {name}")

    install_fake_import(
        monkeypatch,
        {
            "cua": SimpleNamespace(Sandbox=FakeSandboxApi),
            "cua_sandbox": SimpleNamespace(sandbox_state=FakeSandboxState),
        },
    )

    provider = provider_module.CuaSandboxProvider()
    exists = await provider.check_persistent_sandbox_exists(
        {"sandbox_id": "cua-stale", "connect_info": {"local": True}}
    )

    assert exists is False


@pytest.mark.asyncio
async def test_cua_booter_available_probes_runtime(monkeypatch):
    class StaleShell:
        async def exec(self, command):
            raise RuntimeError("connection refused")

    booter = CuaBooter(local=True, persistent=True, persistent_name="cua-stale")
    booter._runtime = SimpleNamespace(shell=StaleShell())

    assert await booter.available() is False


@pytest.mark.asyncio
async def test_cua_booter_available_times_out_unresponsive_runtime(monkeypatch):
    class HangingShell:
        async def exec(self, command):
            await asyncio.sleep(60)
            return {"success": True}

    monkeypatch.setattr(cua_module, "_CUA_HEALTH_CHECK_TIMEOUT_SECONDS", 0.01)
    booter = CuaBooter(local=True, persistent=True, persistent_name="cua-stale")
    booter._runtime = SimpleNamespace(shell=HangingShell())

    assert await booter.available() is False


@pytest.mark.asyncio
async def test_cua_booter_available_propagates_cancellation():
    class CancellingShell:
        async def exec(self, command):
            raise asyncio.CancelledError

    booter = CuaBooter(local=True, persistent=True, persistent_name="cua-stale")
    booter._runtime = SimpleNamespace(shell=CancellingShell())

    with pytest.raises(asyncio.CancelledError):
        await booter.available()


@pytest.mark.asyncio
async def test_cua_booter_available_handles_missing_shell():
    booter = CuaBooter(local=True, persistent=True, persistent_name="cua-stale")
    booter._runtime = SimpleNamespace()

    assert await booter.available() is False


@pytest.mark.asyncio
async def test_cua_booter_destroy_disconnects_before_delete(monkeypatch):
    calls = []

    class FakeSandbox:
        def __init__(self, name: str):
            self.name = name
            self.shell = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.python = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.filesystem = SimpleNamespace()
            self.mouse = SimpleNamespace(click=lambda *args, **kwargs: None)
            self.keyboard = SimpleNamespace(type=lambda *args, **kwargs: None)

        async def disconnect(self):
            calls.append(("disconnect", self.name))

    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        @staticmethod
        async def create(image, *, name=None, local=False, **kwargs):
            return FakeSandbox(name)

        @staticmethod
        async def delete(name, **kwargs):
            calls.append(("delete", name, kwargs))

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
    )

    await booter.boot("ignored-session")
    await booter.destroy()

    assert calls == [
        ("disconnect", "cua-persistent-1"),
        ("delete", "cua-persistent-1", {"local": True}),
    ]


@pytest.mark.asyncio
async def test_cua_booter_destroy_ignores_missing_sandbox(monkeypatch):
    class FakeSandbox:
        def __init__(self, name: str):
            self.name = name
            self.shell = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.python = SimpleNamespace(exec=lambda *args, **kwargs: None)
            self.filesystem = SimpleNamespace()
            self.mouse = SimpleNamespace(click=lambda *args, **kwargs: None)
            self.keyboard = SimpleNamespace(type=lambda *args, **kwargs: None)

        async def disconnect(self):
            return None

    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        @staticmethod
        async def create(image, *, name=None, local=False, **kwargs):
            return FakeSandbox(name)

        @staticmethod
        async def delete(name, **kwargs):
            raise ValueError(f"No local sandbox named '{name}' found in state files.")

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
    )

    await booter.boot("ignored-session")
    await booter.destroy()


@pytest.mark.asyncio
async def test_cua_booter_resume_raises_unexpected_connect_error(monkeypatch):
    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            raise RuntimeError(f"permission denied for {name}")

        @staticmethod
        async def resume(*args, **kwargs):
            raise AssertionError("unexpected errors must not fall through to resume")

        @staticmethod
        async def create(*args, **kwargs):
            raise AssertionError("unexpected errors must not fall through to create")

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
        resume=True,
    )

    with pytest.raises(RuntimeError, match="permission denied"):
        await booter.boot("ignored-session")


@pytest.mark.asyncio
async def test_cua_booter_resume_does_not_create_when_persistent_sandbox_missing(
    monkeypatch,
):
    class FakeImage:
        @staticmethod
        def linux():
            return "linux-image"

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            raise ValueError(f"No local sandbox named '{name}' found in state files.")

        @staticmethod
        async def resume(name, **kwargs):
            raise ValueError(f"No local sandbox named '{name}' found in state files.")

        @staticmethod
        async def create(*args, **kwargs):
            raise AssertionError("resume path must not create a new sandbox")

    fake_module = SimpleNamespace(Image=FakeImage, Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    booter = CuaBooter(
        image="linux",
        os_type="linux",
        local=True,
        persistent_name="cua-persistent-1",
        persistent=True,
        resume=True,
    )

    with pytest.raises(RuntimeError, match="could not be resumed"):
        await booter.boot("ignored-session")


@pytest.mark.asyncio
async def test_cua_provider_shortens_docker_unavailable_errors(monkeypatch):
    class FakeBooter:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        async def boot(self, session_id):
            raise RuntimeError(
                "[900] Cannot connect to Docker Engine via "
                "unix:///Users/test/.docker/run/docker.sock"
            )

        async def shutdown(self):
            return None

    monkeypatch.setattr(provider_module.cua_booter, "CuaBooter", FakeBooter)

    provider = provider_module.CuaSandboxProvider()
    context = SimpleNamespace(
        get_config=lambda umo: {"provider_settings": {"sandbox": {}}}
    )
    config = provider.build_create_config(context, "session-a")

    with pytest.raises(
        RuntimeError, match="^Docker is not installed or not running$"
    ) as excinfo:
        await provider.create_booter(context, "session-a", "cua-1", config)

    cause = excinfo.value.__cause__
    assert isinstance(cause, RuntimeError)
    assert "Cannot connect to Docker Engine via" in str(cause)


def test_cua_provider_does_not_overmatch_docker_errors():
    assert not provider_module._is_docker_unavailable_error(
        RuntimeError("Failed to create Docker network using /var/run/docker.sock")
    )


@pytest.mark.asyncio
async def test_cua_provider_destroy_booter_ignores_non_callable_destroy():
    shutdown_calls = []

    class FakeBooter:
        destroy = True

        async def shutdown(self):
            shutdown_calls.append("shutdown")

    provider = provider_module.CuaSandboxProvider()

    await provider.destroy_booter(FakeBooter(), {"retention_policy": "temporary"})

    assert shutdown_calls == ["shutdown"]


@pytest.mark.asyncio
async def test_cua_provider_reports_persistent_sandbox_exists(monkeypatch):
    calls = []

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            calls.append((name, kwargs))

            class FakeSandbox:
                async def disconnect(self):
                    calls.append(("disconnect", name))

            return FakeSandbox()

    fake_module = SimpleNamespace(Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    provider = provider_module.CuaSandboxProvider()

    exists = await provider.check_persistent_sandbox_exists(
        {"connect_info": {"persistent_name": "cua-persistent-1", "local": True}}
    )

    assert exists is True
    assert calls == [
        ("cua-persistent-1", {"local": True}),
        ("disconnect", "cua-persistent-1"),
    ]


@pytest.mark.asyncio
async def test_cua_provider_reports_missing_persistent_sandbox(monkeypatch):
    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            raise ValueError(f"No local sandbox named '{name}' found in state files.")

    fake_module = SimpleNamespace(Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    provider = provider_module.CuaSandboxProvider()

    exists = await provider.check_persistent_sandbox_exists(
        {"connect_info": {"persistent_name": "cua-persistent-1", "local": True}}
    )

    assert exists is False


@pytest.mark.asyncio
async def test_cua_provider_checks_resume_before_reporting_missing_persistent_sandbox(
    monkeypatch,
):
    calls = []

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            calls.append(("connect", name, kwargs))
            raise ValueError(f"No local sandbox named '{name}' found in state files.")

        @staticmethod
        async def resume(name, **kwargs):
            calls.append(("resume", name, kwargs))

            class FakeSandbox:
                async def disconnect(self):
                    calls.append(("disconnect", name))

            return FakeSandbox()

    fake_module = SimpleNamespace(Sandbox=FakeSandboxApi)

    install_fake_import(monkeypatch, {"cua": fake_module})

    provider = provider_module.CuaSandboxProvider()

    exists = await provider.check_persistent_sandbox_exists(
        {"connect_info": {"persistent_name": "cua-persistent-1", "local": True}}
    )

    assert exists is True
    assert calls == [
        ("connect", "cua-persistent-1", {"local": True}),
        ("resume", "cua-persistent-1", {"local": True}),
        ("disconnect", "cua-persistent-1"),
    ]


@pytest.mark.asyncio
async def test_cua_provider_verifies_local_state_readiness(
    monkeypatch,
):
    class FakeSandboxState:
        @staticmethod
        def load(name):
            return {"name": name, "status": "running"}

    class FakeSandboxApi:
        @staticmethod
        async def connect(name, **kwargs):
            raise RuntimeError(f"no local sandbox named {name}")

    fake_cua_module = SimpleNamespace(Sandbox=FakeSandboxApi)
    fake_state_module = SimpleNamespace(sandbox_state=FakeSandboxState)

    install_fake_import(
        monkeypatch,
        {"cua": fake_cua_module, "cua_sandbox": fake_state_module},
    )

    provider = provider_module.CuaSandboxProvider()

    exists = await provider.check_persistent_sandbox_exists(
        {"connect_info": {"persistent_name": "cua-persistent-1", "local": True}}
    )

    assert exists is False


@pytest.mark.asyncio
async def test_cua_shell_upload_fallback_chunks_large_payloads(tmp_path):
    commands = []

    class FakeShell:
        async def exec(self, command, **kwargs):
            commands.append((command, kwargs))
            return {"stdout": "", "stderr": "", "exit_code": 0, "success": True}

    target_path = "/tmp/uploaded.bin"
    data = b"a" * 200_000

    result = await _write_base64_via_shell(FakeShell(), target_path, data)

    assert result["success"] is True
    assert len(commands) > 2
    assert all(len(command) < 100_000 for command, _kwargs in commands)
    assert commands[0][0].startswith("mkdir -p ")
    assert any(command.startswith("python3 - ") for command, _kwargs in commands)
    assert any(" <<'PY'" in command for command, _kwargs in commands)
    assert str(Path(target_path).parent) in commands[0][0]
    assert commands[-1][0].startswith("rm -f ")


@pytest.mark.asyncio
async def test_cua_shell_upload_fallback_cleans_encoded_file_on_decoder_error():
    commands = []

    class FakeShell:
        async def exec(self, command, **kwargs):
            commands.append((command, kwargs))
            if command.startswith("python3"):
                return {
                    "stdout": "",
                    "stderr": "decode failed",
                    "exit_code": 1,
                    "success": False,
                }
            return {"stdout": "", "stderr": "", "exit_code": 0, "success": True}

    result = await _write_base64_via_shell(FakeShell(), "/tmp/uploaded.bin", b"data")

    assert result["success"] is False
    assert any(command.startswith("python3") for command, _kwargs in commands)
    assert commands[-1][0].startswith("rm -f ")


@pytest.mark.asyncio
async def test_cua_shell_upload_fallback_allows_successful_stderr_warnings():
    commands = []

    class FakeShell:
        async def exec(self, command, **kwargs):
            commands.append((command, kwargs))
            return {
                "stdout": "",
                "stderr": "warning: harmless diagnostic",
                "exit_code": 0,
                "success": True,
            }

    result = await _write_base64_via_shell(FakeShell(), "/tmp/uploaded.bin", b"data")

    assert result["success"] is True
    assert any(command.startswith("python3") for command, _kwargs in commands)
    assert commands[-1][0].startswith("rm -f ")


@pytest.mark.asyncio
async def test_cua_shell_upload_fallback_ignores_stderr_without_status_fields():
    commands = []

    class FakeShell:
        async def exec(self, command, **kwargs):
            commands.append((command, kwargs))
            return {"stdout": "", "stderr": "warning: harmless diagnostic"}

    result = await _write_base64_via_shell(FakeShell(), "/tmp/uploaded.bin", b"data")

    assert result["stderr"] == "warning: harmless diagnostic"
    assert any(command.startswith("python3") for command, _kwargs in commands)
    assert commands[-1][0].startswith("rm -f ")
