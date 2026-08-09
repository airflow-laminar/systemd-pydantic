# systemd_pydantic.TimerUnitConfiguration

### *pydantic model* systemd_pydantic.TimerUnitConfiguration[[source]](../../../_modules/systemd_pydantic/models.html.md#TimerUnitConfiguration)

Bases: `_SystemdConfiguration`

#### section_order *: ClassVar[tuple[str, ...]]* *= ('unit', 'timer', 'install')*

#### *field* unit *: [UnitConfiguration](systemd_pydantic.UnitConfiguration.html.md#systemd_pydantic.UnitConfiguration) | None* *= None*

#### *field* timer *: [TimerConfiguration](systemd_pydantic.TimerConfiguration.html.md#systemd_pydantic.TimerConfiguration)* *[Required]*

#### *field* install *: [InstallConfiguration](systemd_pydantic.InstallConfiguration.html.md#systemd_pydantic.InstallConfiguration) | None* *= None*
