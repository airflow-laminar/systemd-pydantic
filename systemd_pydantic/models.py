from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ServiceType = Literal["simple", "exec", "forking", "oneshot", "dbus", "notify", "notify-reload", "idle"]
RestartPolicy = Literal["no", "on-success", "on-failure", "on-abnormal", "on-watchdog", "on-abort", "always"]
KillMode = Literal["control-group", "mixed", "process", "none"]
TimeSpan = str | timedelta


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _format_time_span(value: timedelta) -> str:
    microseconds = ((value.days * 86_400) + value.seconds) * 1_000_000 + value.microseconds
    if microseconds % 1_000_000 == 0:
        return f"{microseconds // 1_000_000}s"
    return f"{microseconds / 1_000_000:.6f}".rstrip("0") + "s"


class _Section(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    section_name: ClassVar[str]
    directives: ClassVar[dict[str, str]]
    repeated: ClassVar[frozenset[str]] = frozenset()
    space_separated: ClassVar[frozenset[str]] = frozenset()

    def to_unit_file(self) -> str:
        lines = [f"[{self.section_name}]"]
        for field_name, value in self:
            if value is None or value == [] or value == {}:
                continue
            directive = self.directives[field_name]
            if field_name == "environment":
                lines.extend(f"{directive}={_quote(f'{key}={item}')}" for key, item in value.items())
            elif isinstance(value, list):
                if field_name in self.repeated:
                    lines.extend(f"{directive}={self._format(item)}" for item in value)
                elif field_name in self.space_separated:
                    lines.append(f"{directive}={' '.join(self._format(item) for item in value)}")
            else:
                lines.append(f"{directive}={self._format(value)}")
        return "\n".join(lines)

    @staticmethod
    def _format(value: object) -> str:
        if isinstance(value, bool):
            return "yes" if value else "no"
        if isinstance(value, timedelta):
            return _format_time_span(value)
        return str(value)


class UnitSection(_Section):
    """Common settings from a systemd unit's ``[Unit]`` section."""

    section_name = "Unit"
    directives = {
        "description": "Description",
        "documentation": "Documentation",
        "wants": "Wants",
        "requires": "Requires",
        "requisite": "Requisite",
        "binds_to": "BindsTo",
        "part_of": "PartOf",
        "upholds": "Upholds",
        "conflicts": "Conflicts",
        "before": "Before",
        "after": "After",
        "on_failure": "OnFailure",
    }
    space_separated = frozenset(directives.keys() - {"description"})

    description: str | None = None
    documentation: list[str] = Field(default_factory=list)
    wants: list[str] = Field(default_factory=list)
    requires: list[str] = Field(default_factory=list)
    requisite: list[str] = Field(default_factory=list)
    binds_to: list[str] = Field(default_factory=list)
    part_of: list[str] = Field(default_factory=list)
    upholds: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    before: list[str] = Field(default_factory=list)
    after: list[str] = Field(default_factory=list)
    on_failure: list[str] = Field(default_factory=list)


class ServiceSection(_Section):
    """Process supervision settings from a systemd ``[Service]`` section."""

    section_name = "Service"
    directives = {
        "type": "Type",
        "exec_condition": "ExecCondition",
        "exec_start_pre": "ExecStartPre",
        "exec_start": "ExecStart",
        "exec_start_post": "ExecStartPost",
        "exec_reload": "ExecReload",
        "exec_stop": "ExecStop",
        "exec_stop_post": "ExecStopPost",
        "restart": "Restart",
        "restart_sec": "RestartSec",
        "restart_steps": "RestartSteps",
        "restart_max_delay_sec": "RestartMaxDelaySec",
        "restart_randomized_delay_sec": "RestartRandomizedDelaySec",
        "timeout_start_sec": "TimeoutStartSec",
        "timeout_stop_sec": "TimeoutStopSec",
        "runtime_max_sec": "RuntimeMaxSec",
        "watchdog_sec": "WatchdogSec",
        "remain_after_exit": "RemainAfterExit",
        "guess_main_pid": "GuessMainPID",
        "pid_file": "PIDFile",
        "bus_name": "BusName",
        "user": "User",
        "group": "Group",
        "supplementary_groups": "SupplementaryGroups",
        "working_directory": "WorkingDirectory",
        "environment": "Environment",
        "environment_file": "EnvironmentFile",
        "umask": "UMask",
        "standard_output": "StandardOutput",
        "standard_error": "StandardError",
        "kill_mode": "KillMode",
        "kill_signal": "KillSignal",
        "send_sigkill": "SendSIGKILL",
        "success_exit_status": "SuccessExitStatus",
        "restart_prevent_exit_status": "RestartPreventExitStatus",
        "restart_force_exit_status": "RestartForceExitStatus",
    }
    repeated = frozenset(
        {
            "exec_condition",
            "exec_start_pre",
            "exec_start",
            "exec_start_post",
            "exec_reload",
            "exec_stop",
            "exec_stop_post",
            "environment_file",
        }
    )
    space_separated = frozenset({"supplementary_groups", "success_exit_status", "restart_prevent_exit_status", "restart_force_exit_status"})

    type: ServiceType | None = None
    exec_condition: list[str] = Field(default_factory=list)
    exec_start_pre: list[str] = Field(default_factory=list)
    exec_start: list[str] = Field(default_factory=list)
    exec_start_post: list[str] = Field(default_factory=list)
    exec_reload: list[str] = Field(default_factory=list)
    exec_stop: list[str] = Field(default_factory=list)
    exec_stop_post: list[str] = Field(default_factory=list)
    restart: RestartPolicy | None = None
    restart_sec: TimeSpan | None = None
    restart_steps: int | None = Field(default=None, ge=0)
    restart_max_delay_sec: TimeSpan | None = None
    restart_randomized_delay_sec: TimeSpan | None = None
    timeout_start_sec: TimeSpan | Literal["infinity"] | None = None
    timeout_stop_sec: TimeSpan | Literal["infinity"] | None = None
    runtime_max_sec: TimeSpan | Literal["infinity"] | None = None
    watchdog_sec: TimeSpan | None = None
    remain_after_exit: bool | None = None
    guess_main_pid: bool | None = None
    pid_file: Path | None = None
    bus_name: str | None = None
    user: str | None = None
    group: str | None = None
    supplementary_groups: list[str] = Field(default_factory=list)
    working_directory: Path | str | None = None
    environment: dict[str, str] = Field(default_factory=dict)
    environment_file: list[Path | str] = Field(default_factory=list)
    umask: str | None = None
    standard_output: str | None = None
    standard_error: str | None = None
    kill_mode: KillMode | None = None
    kill_signal: str | None = None
    send_sigkill: bool | None = None
    success_exit_status: list[int | str] = Field(default_factory=list)
    restart_prevent_exit_status: list[int | str] = Field(default_factory=list)
    restart_force_exit_status: list[int | str] = Field(default_factory=list)

    @field_validator(
        "restart_sec",
        "restart_max_delay_sec",
        "restart_randomized_delay_sec",
        "timeout_start_sec",
        "timeout_stop_sec",
        "runtime_max_sec",
        "watchdog_sec",
        mode="before",
    )
    @classmethod
    def _normalize_time_span(cls, value: object) -> object:
        if isinstance(value, timedelta):
            return _format_time_span(value)
        return value

    @field_validator(
        "exec_condition",
        "exec_start_pre",
        "exec_start",
        "exec_start_post",
        "exec_reload",
        "exec_stop",
        "exec_stop_post",
        "environment_file",
        mode="before",
    )
    @classmethod
    def _coerce_repeated_value(cls, value: object) -> object:
        if isinstance(value, (str, Path)):
            return [value]
        return value

    @model_validator(mode="after")
    def _validate_commands(self) -> ServiceSection:
        if not self.exec_start and not (self.remain_after_exit and self.exec_stop):
            raise ValueError("a service requires ExecStart, or RemainAfterExit=yes with ExecStop")
        if self.type != "oneshot" and len(self.exec_start) > 1:
            raise ValueError("multiple ExecStart commands require Type=oneshot")
        if self.type == "dbus" and not self.bus_name:
            raise ValueError("Type=dbus requires BusName")
        return self


class TimerSection(_Section):
    """Activation settings from a systemd ``[Timer]`` section."""

    section_name = "Timer"
    directives = {
        "on_active_sec": "OnActiveSec",
        "on_boot_sec": "OnBootSec",
        "on_startup_sec": "OnStartupSec",
        "on_unit_active_sec": "OnUnitActiveSec",
        "on_unit_inactive_sec": "OnUnitInactiveSec",
        "on_calendar": "OnCalendar",
        "accuracy_sec": "AccuracySec",
        "randomized_delay_sec": "RandomizedDelaySec",
        "fixed_random_delay": "FixedRandomDelay",
        "randomized_offset_sec": "RandomizedOffsetSec",
        "defer_reactivation": "DeferReactivation",
        "on_clock_change": "OnClockChange",
        "on_timezone_change": "OnTimezoneChange",
        "unit": "Unit",
        "persistent": "Persistent",
        "wake_system": "WakeSystem",
        "remain_after_elapse": "RemainAfterElapse",
    }
    repeated = frozenset({"on_active_sec", "on_boot_sec", "on_startup_sec", "on_unit_active_sec", "on_unit_inactive_sec", "on_calendar"})

    on_active_sec: list[TimeSpan] = Field(default_factory=list)
    on_boot_sec: list[TimeSpan] = Field(default_factory=list)
    on_startup_sec: list[TimeSpan] = Field(default_factory=list)
    on_unit_active_sec: list[TimeSpan] = Field(default_factory=list)
    on_unit_inactive_sec: list[TimeSpan] = Field(default_factory=list)
    on_calendar: list[str] = Field(default_factory=list)
    accuracy_sec: TimeSpan | None = None
    randomized_delay_sec: TimeSpan | None = None
    fixed_random_delay: bool | None = None
    randomized_offset_sec: TimeSpan | None = None
    defer_reactivation: bool | None = None
    on_clock_change: bool | None = None
    on_timezone_change: bool | None = None
    unit: str | None = None
    persistent: bool | None = None
    wake_system: bool | None = None
    remain_after_elapse: bool | None = None

    @field_validator(
        "on_active_sec",
        "on_boot_sec",
        "on_startup_sec",
        "on_unit_active_sec",
        "on_unit_inactive_sec",
        "on_calendar",
        mode="before",
    )
    @classmethod
    def _coerce_trigger(cls, value: object) -> object:
        if isinstance(value, timedelta):
            return [_format_time_span(value)]
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [_format_time_span(item) if isinstance(item, timedelta) else item for item in value]
        return value

    @field_validator("accuracy_sec", "randomized_delay_sec", "randomized_offset_sec", mode="before")
    @classmethod
    def _normalize_time_span(cls, value: object) -> object:
        if isinstance(value, timedelta):
            return _format_time_span(value)
        return value

    @model_validator(mode="after")
    def _require_trigger(self) -> TimerSection:
        triggers = (
            self.on_active_sec,
            self.on_boot_sec,
            self.on_startup_sec,
            self.on_unit_active_sec,
            self.on_unit_inactive_sec,
            self.on_calendar,
            self.on_clock_change,
            self.on_timezone_change,
        )
        if not any(triggers):
            raise ValueError("a timer requires at least one trigger")
        return self


class InstallSection(_Section):
    """Enablement settings from a systemd ``[Install]`` section."""

    section_name = "Install"
    directives = {
        "alias": "Alias",
        "wanted_by": "WantedBy",
        "required_by": "RequiredBy",
        "upheld_by": "UpheldBy",
        "also": "Also",
        "default_instance": "DefaultInstance",
    }
    space_separated = frozenset({"alias", "wanted_by", "required_by", "upheld_by", "also"})

    alias: list[str] = Field(default_factory=list)
    wanted_by: list[str] = Field(default_factory=list)
    required_by: list[str] = Field(default_factory=list)
    upheld_by: list[str] = Field(default_factory=list)
    also: list[str] = Field(default_factory=list)
    default_instance: str | None = None


class _SystemdConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    section_order: ClassVar[tuple[str, ...]]

    def to_unit_file(self) -> str:
        sections = [getattr(self, name) for name in self.section_order]
        return "\n\n".join(section.to_unit_file() for section in sections if section is not None) + "\n"

    def to_cfg(self) -> str:
        """Compatibility alias for configuration generators in related projects."""

        return self.to_unit_file()


class SystemdServiceConfiguration(_SystemdConfiguration):
    section_order = ("unit", "service", "install")

    unit: UnitSection | None = None
    service: ServiceSection
    install: InstallSection | None = None


class SystemdTimerConfiguration(_SystemdConfiguration):
    section_order = ("unit", "timer", "install")

    unit: UnitSection | None = None
    timer: TimerSection
    install: InstallSection | None = None
