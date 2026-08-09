# systemd_pydantic.UnitConfiguration

### *pydantic model* systemd_pydantic.UnitConfiguration[[source]](../../../_modules/systemd_pydantic/models.html.md#UnitConfiguration)

Bases: `_Section`

Common settings from a systemd unit’s `[Unit]` section.

#### section_name *: ClassVar[str]* *= 'Unit'*

#### directives *: ClassVar[dict[str, str]]* *= {'after': 'After', 'before': 'Before', 'binds_to': 'BindsTo', 'conflicts': 'Conflicts', 'description': 'Description', 'documentation': 'Documentation', 'on_failure': 'OnFailure', 'part_of': 'PartOf', 'requires': 'Requires', 'requisite': 'Requisite', 'upholds': 'Upholds', 'wants': 'Wants'}*

#### space_separated *: ClassVar[frozenset[str]]* *= frozenset({'after', 'before', 'binds_to', 'conflicts', 'documentation', 'on_failure', 'part_of', 'requires', 'requisite', 'upholds', 'wants'})*

#### *field* description *: str | None* *= None*

#### *field* documentation *: list[str]* *[Optional]*

#### *field* wants *: list[str]* *[Optional]*

#### *field* requires *: list[str]* *[Optional]*

#### *field* requisite *: list[str]* *[Optional]*

#### *field* binds_to *: list[str]* *[Optional]*

#### *field* part_of *: list[str]* *[Optional]*

#### *field* upholds *: list[str]* *[Optional]*

#### *field* conflicts *: list[str]* *[Optional]*

#### *field* before *: list[str]* *[Optional]*

#### *field* after *: list[str]* *[Optional]*

#### *field* on_failure *: list[str]* *[Optional]*
