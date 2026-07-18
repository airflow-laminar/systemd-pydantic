from __future__ import annotations

import inspect
import os
from getpass import getuser
from pathlib import Path
from tempfile import gettempdir
from typing import TYPE_CHECKING, Literal, Self

from hydra import compose, initialize_config_dir
from hydra.utils import instantiate
from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..models import ServiceUnitConfiguration, TimerUnitConfiguration

SystemdScope = Literal["system", "user"]

if TYPE_CHECKING:
    from ..client import UnitInfo


def _calling_file(offset: int) -> str:
    return inspect.stack()[offset].filename


def _unit_filename(name: str, suffix: str) -> str:
    if "/" in name or name in {"", ".", ".."}:
        raise ValueError(f"invalid unit name: {name!r}")
    if name.endswith(suffix):
        return name
    if "." in name:
        raise ValueError(f"unit {name!r} must end in {suffix}")
    return f"{name}{suffix}"


class SystemdConfiguration(BaseModel):
    """Named collection of systemd service and timer unit files."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    service: dict[str, ServiceUnitConfiguration]
    timer: dict[str, TimerUnitConfiguration] = Field(default_factory=dict)
    unit_dir: Path | None = None
    working_dir: Path | None = None
    scope: SystemdScope = "system"

    @model_validator(mode="after")
    def _set_paths(self) -> SystemdConfiguration:
        names = sorted([*self.service, *self.timer])
        label = "-".join(names) or "units"
        if self.working_dir is None:
            object.__setattr__(self, "working_dir", Path(gettempdir()).resolve() / f"systemd-{getuser()}-{label}")
        if self.unit_dir is None:
            object.__setattr__(
                self,
                "unit_dir",
                Path("/etc/systemd/system") if self.scope == "system" else Path.home() / ".config/systemd/user",
            )
        for name in self.service:
            _unit_filename(name, ".service")
        for name in self.timer:
            _unit_filename(name, ".timer")
        return self

    def to_cfg(self) -> dict[str, str]:
        rendered = {_unit_filename(name, ".service"): config.to_cfg() for name, config in self.service.items()}
        rendered.update({_unit_filename(name, ".timer"): config.to_cfg() for name, config in self.timer.items()})
        return rendered

    @property
    def service_names(self) -> list[str]:
        return [_unit_filename(name, ".service") for name in self.service]

    @property
    def timer_names(self) -> list[str]:
        return [_unit_filename(name, ".timer") for name in self.timer]

    @property
    def unit_paths(self) -> list[Path]:
        assert self.unit_dir is not None
        return [self.unit_dir / name for name in self.to_cfg()]

    def write(self) -> list[Path]:
        assert self.unit_dir is not None
        self.unit_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for filename, contents in self.to_cfg().items():
            path = self.unit_dir / filename
            path.write_text(contents)
            paths.append(path)
        return paths

    def rmdir(self) -> None:
        for path in self.unit_paths:
            path.unlink(missing_ok=True)
        assert self.working_dir is not None
        if self.working_dir.exists() and not any(self.working_dir.iterdir()):
            self.working_dir.rmdir()

    @classmethod
    def _find_parent_config_folder(
        cls,
        config_dir: str = "config",
        config_name: str = "",
        *,
        basepath: str = "",
        _offset: int = 2,
    ) -> tuple[Path, Path, Path | str]:
        if basepath:
            calling_file = Path(basepath) if basepath.endswith((".py", ".yml", ".yaml")) else Path(basepath) / "dummy.py"
        else:
            calling_file = Path(_calling_file(_offset))
        folder = calling_file.parent.resolve()

        while True:
            candidate = folder / config_dir
            if not config_name and candidate.exists():
                return folder, candidate.resolve(), ""
            for suffix in (".yml", ".yaml"):
                path = candidate / f"{config_name}{suffix}"
                if config_name and path.exists():
                    return folder, candidate.resolve(), path.resolve()
            if str(folder) == os.path.abspath(os.sep):
                raise FileNotFoundError(f"could not find {config_name or config_dir!r} from {calling_file}")
            folder = folder.parent

    @classmethod
    def load(
        cls,
        config_dir: str = "config",
        config_name: str = "",
        overrides: list[str] | None = None,
        *,
        basepath: str = "",
        _offset: int = 3,
    ) -> Self:
        overrides = overrides or []
        hydra_dir = Path(__file__).resolve().parent / "hydra"
        with initialize_config_dir(config_dir=str(hydra_dir), version_base=None):
            if config_dir:
                hydra_folder, resolved_config_dir, _ = cls._find_parent_config_folder(
                    config_dir=config_dir,
                    config_name=config_name,
                    basepath=basepath,
                    _offset=_offset,
                )
                base = compose(config_name="base", return_hydra_config=True)
                searchpaths = list(base["hydra"]["searchpath"])
                searchpaths.extend([str(hydra_folder), str(resolved_config_dir)])
                if config_name:
                    overrides = [f"+config={config_name}", *overrides, f"hydra.searchpath=[{','.join(searchpaths)}]"]
                else:
                    overrides = [*overrides, f"hydra.searchpath=[{','.join(searchpaths)}]"]
            config = instantiate(compose(config_name="base", overrides=overrides))
        if isinstance(config, cls):
            return config
        if isinstance(config, BaseModel):
            config = config.model_dump(exclude_unset=True)
        return cls.model_validate(config)

    def start(self) -> dict[str, UnitInfo]:
        from ..client import SystemdClient

        return SystemdClient(self).start_services()

    def running(self) -> bool:
        from ..client import SystemdClient

        return all(info.running() for info in SystemdClient(self).get_all_service_info().values())

    def stop(self) -> dict[str, UnitInfo]:
        from ..client import SystemdClient

        return SystemdClient(self).stop_services()

    def kill(self) -> dict[str, UnitInfo]:
        from ..client import SystemdClient

        return SystemdClient(self).kill_services()


load_config = SystemdConfiguration.load
