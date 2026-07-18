from __future__ import annotations

from dataclasses import dataclass
from subprocess import run
from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from ..config import SystemdConfiguration


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str = ""
    stderr: str = ""


class CommandRunner(Protocol):
    def run(self, command: list[str], timeout: int) -> CommandResult: ...


class SubprocessCommandRunner:
    def run(self, command: list[str], timeout: int) -> CommandResult:
        result = run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return CommandResult(command=command, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)


class SSHCommandRunner:
    def __init__(self, host: str, runner: CommandRunner | None = None):
        self.host = host
        self.runner = runner or SubprocessCommandRunner()

    def run(self, command: list[str], timeout: int) -> CommandResult:
        return self.runner.run(["ssh", self.host, *command], timeout)


class SystemdCommandError(RuntimeError):
    def __init__(self, result: CommandResult):
        self.result = result
        detail = result.stderr.strip() or result.stdout.strip()
        super().__init__(f"command failed ({result.returncode}): {' '.join(result.command)}{': ' + detail if detail else ''}")


class UnitInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    load_state: str = ""
    active_state: str = ""
    sub_state: str = ""
    result: str = ""
    exec_main_code: str = ""
    exec_main_status: int | None = None

    def running(self) -> bool:
        return self.active_state in {"active", "activating", "reloading"}

    def stopped(self) -> bool:
        return self.active_state in {"inactive", "deactivating"}

    def done(self, ok_exitstatuses: list[int | str] | None = None) -> bool:
        statuses = {str(value) for value in (ok_exitstatuses or [0])}
        return self.stopped() and self.result in {"", "success"} and str(self.exec_main_status or 0) in statuses

    def ok(self, ok_exitstatuses: list[int | str] | None = None) -> bool:
        return self.running() or self.done(ok_exitstatuses)

    def bad(self, ok_exitstatuses: list[int | str] | None = None) -> bool:
        return self.active_state == "failed" or (self.stopped() and not self.done(ok_exitstatuses))


class SystemdClient:
    _SHOW_PROPERTIES = ("LoadState", "ActiveState", "SubState", "Result", "ExecMainCode", "ExecMainStatus")

    def __init__(self, cfg: SystemdConfiguration, runner: CommandRunner | None = None):
        self.cfg = cfg
        self.runner = runner or SubprocessCommandRunner()
        self.timeout = getattr(cfg, "command_timeout", 60)

    def _run(self, *args: str, check: bool = True) -> CommandResult:
        command = ["systemctl"]
        if self.cfg.scope == "user":
            command.append("--user")
        result = self.runner.run([*command, *args], self.timeout)
        if check and result.returncode != 0:
            raise SystemdCommandError(result)
        return result

    def daemon_reload(self) -> CommandResult:
        return self._run("daemon-reload")

    def enable_units(self, names: list[str] | None = None) -> CommandResult:
        return self._run("enable", *(names if names is not None else [*self.cfg.service_names, *self.cfg.timer_names]))

    def disable_units(self, names: list[str] | None = None) -> CommandResult:
        return self._run("disable", *(names if names is not None else [*self.cfg.service_names, *self.cfg.timer_names]))

    def start_units(self, names: list[str]) -> dict[str, UnitInfo]:
        if names:
            self._run("start", *names)
        return self.get_units_info(names)

    def stop_units(self, names: list[str]) -> dict[str, UnitInfo]:
        if names:
            self._run("stop", *names)
        return self.get_units_info(names)

    def restart_units(self, names: list[str]) -> dict[str, UnitInfo]:
        if names:
            self._run("restart", *names)
        return self.get_units_info(names)

    def kill_units(self, names: list[str]) -> dict[str, UnitInfo]:
        if names:
            self._run("kill", "--signal=SIGKILL", *names)
        return self.get_units_info(names)

    def start_services(self) -> dict[str, UnitInfo]:
        return self.start_units(self.cfg.service_names)

    def stop_services(self) -> dict[str, UnitInfo]:
        return self.stop_units(self.cfg.service_names)

    def restart_services(self) -> dict[str, UnitInfo]:
        return self.restart_units(self.cfg.service_names)

    def kill_services(self) -> dict[str, UnitInfo]:
        return self.kill_units(self.cfg.service_names)

    def start_timers(self) -> dict[str, UnitInfo]:
        return self.start_units(self.cfg.timer_names)

    def stop_timers(self) -> dict[str, UnitInfo]:
        return self.stop_units(self.cfg.timer_names)

    def get_unit_info(self, name: str) -> UnitInfo:
        properties = [f"--property={value}" for value in self._SHOW_PROPERTIES]
        result = self._run("show", name, *properties, check=False)
        values = {}
        for line in result.stdout.splitlines():
            key, separator, value = line.partition("=")
            if separator:
                values[key] = value
        status = values.get("ExecMainStatus", "")
        return UnitInfo(
            name=name,
            load_state=values.get("LoadState", "not-found" if result.returncode else ""),
            active_state=values.get("ActiveState", "failed" if result.returncode else ""),
            sub_state=values.get("SubState", ""),
            result=values.get("Result", ""),
            exec_main_code=values.get("ExecMainCode", ""),
            exec_main_status=int(status) if status.lstrip("-").isdigit() else None,
        )

    def get_units_info(self, names: list[str]) -> dict[str, UnitInfo]:
        return {name: self.get_unit_info(name) for name in names}

    def get_all_service_info(self) -> dict[str, UnitInfo]:
        return self.get_units_info(self.cfg.service_names)

    def get_all_timer_info(self) -> dict[str, UnitInfo]:
        return self.get_units_info(self.cfg.timer_names)
