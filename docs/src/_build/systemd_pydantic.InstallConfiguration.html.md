# systemd_pydantic.InstallConfiguration

### *pydantic model* systemd_pydantic.InstallConfiguration

Bases: `_Section`

Enablement settings from a systemd `[Install]` section.

#### section_name *: ClassVar[str]* *= 'Install'*

#### directives *: ClassVar[dict[str, str]]* *= {'alias': 'Alias', 'also': 'Also', 'default_instance': 'DefaultInstance', 'required_by': 'RequiredBy', 'upheld_by': 'UpheldBy', 'wanted_by': 'WantedBy'}*

#### space_separated *: ClassVar[frozenset[str]]* *= frozenset({'alias', 'also', 'required_by', 'upheld_by', 'wanted_by'})*

#### *field* alias *: list[str]* *[Optional]*

#### *field* wanted_by *: list[str]* *[Optional]*

#### *field* required_by *: list[str]* *[Optional]*

#### *field* upheld_by *: list[str]* *[Optional]*

#### *field* also *: list[str]* *[Optional]*

#### *field* default_instance *: str | None* *= None*
