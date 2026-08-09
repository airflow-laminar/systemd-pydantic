# systemd_pydantic.ServiceUnitConfiguration

### *pydantic model* systemd_pydantic.ServiceUnitConfiguration[[source]](../../../_modules/systemd_pydantic/models.html.md#ServiceUnitConfiguration)

Bases: `_SystemdConfiguration`

#### section_order *: ClassVar[tuple[str, ...]]* *= ('unit', 'service', 'install')*

#### *field* unit *: [UnitConfiguration](systemd_pydantic.UnitConfiguration.html.md#systemd_pydantic.UnitConfiguration) | None* *= None*

#### *field* service *: [ServiceConfiguration](systemd_pydantic.ServiceConfiguration.html.md#systemd_pydantic.ServiceConfiguration)* *[Required]*

#### *field* install *: [InstallConfiguration](systemd_pydantic.InstallConfiguration.html.md#systemd_pydantic.InstallConfiguration) | None* *= None*
