# systemd_pydantic.ServiceUnitConfiguration

### *pydantic model* systemd_pydantic.ServiceUnitConfiguration

Bases: `_SystemdConfiguration`

#### section_order *: ClassVar[tuple[str, ...]]* *= ('unit', 'service', 'install')*

#### *field* unit *: [UnitConfiguration](systemd_pydantic.UnitConfiguration.md#systemd_pydantic.UnitConfiguration) | None* *= None*

#### *field* service *: [ServiceConfiguration](systemd_pydantic.ServiceConfiguration.md#systemd_pydantic.ServiceConfiguration)* *[Required]*

#### *field* install *: [InstallConfiguration](systemd_pydantic.InstallConfiguration.md#systemd_pydantic.InstallConfiguration) | None* *= None*
