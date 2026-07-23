from pathlib import Path

from pydantic import Field, PrivateAttr, model_validator

from ..models import KillMode, RestartPolicy, TimeSpan
from .systemd import SystemdConfiguration


class SystemdConvenienceConfiguration(SystemdConfiguration):
    """Systemd defaults and persisted state used by convenience commands."""

    _pydantic_path: Path = PrivateAttr(default=Path("pydantic.json"))

    restart: RestartPolicy = "no"
    timeout_stop_sec: TimeSpan = "30s"
    kill_mode: KillMode = "control-group"
    kill_signal: str = "SIGTERM"
    success_exit_status: list[int | str] = Field(default_factory=lambda: [0])
    command_timeout: int = Field(default=60, ge=1)

    @model_validator(mode="after")
    def _set_convenience_defaults(self) -> "SystemdConvenienceConfiguration":
        for unit in self.service.values():
            service = unit.service
            service.restart = service.restart or self.restart
            service.timeout_stop_sec = service.timeout_stop_sec or self.timeout_stop_sec
            service.kill_mode = service.kill_mode or self.kill_mode
            service.kill_signal = service.kill_signal or self.kill_signal
            service.success_exit_status = service.success_exit_status or self.success_exit_status
        assert self.working_dir is not None
        self._pydantic_path = self.working_dir / "pydantic.json"
        return self

    def _write_self(self) -> None:
        assert self.working_dir is not None
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.write()
        self._pydantic_path.write_text(self.model_dump_json(exclude_unset=True))

    def rmdir(self) -> None:
        self._pydantic_path.unlink(missing_ok=True)
        super().rmdir()


load_convenience_config = SystemdConvenienceConfiguration.load
