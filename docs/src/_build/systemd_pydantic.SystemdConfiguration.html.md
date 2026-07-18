# systemd_pydantic.SystemdConfiguration

### *pydantic model* systemd_pydantic.SystemdConfiguration

Bases: `BaseModel`

Named collection of systemd service and timer unit files.

#### *field* service *: dict[str, [ServiceUnitConfiguration](systemd_pydantic.ServiceUnitConfiguration.md#systemd_pydantic.ServiceUnitConfiguration)]* *[Required]*

#### *field* timer *: dict[str, [TimerUnitConfiguration](systemd_pydantic.TimerUnitConfiguration.md#systemd_pydantic.TimerUnitConfiguration)]* *[Optional]*

#### *field* unit_dir *: Path | None* *= None*

#### *field* working_dir *: Path | None* *= None*

#### *field* scope *: SystemdScope* *= 'system'*

#### to_cfg() → dict[str, str]

#### *property* service_names *: list[str]*

#### *property* timer_names *: list[str]*

#### *property* unit_paths *: list[Path]*

#### write() → list[Path]

#### rmdir() → None

#### *classmethod* load(config_dir: str = 'config', config_name: str = '', overrides: list[str] | None = None, , basepath: str = '', \_offset: int = 3) → Self

#### start() → dict[str, [UnitInfo](systemd_pydantic.UnitInfo.md#systemd_pydantic.UnitInfo)]

#### running() → bool

#### stop() → dict[str, [UnitInfo](systemd_pydantic.UnitInfo.md#systemd_pydantic.UnitInfo)]

#### kill() → dict[str, [UnitInfo](systemd_pydantic.UnitInfo.md#systemd_pydantic.UnitInfo)]
