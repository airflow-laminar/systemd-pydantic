# Why services and timers share one model

A systemd timer does not run a command by itself. It activates another unit,
normally a service with the same base name. Both files use the common `[Unit]`
and `[Install]` sections, live under the same manager scope, and participate in
the same enable/start/status lifecycle. Keeping timers in `systemd-pydantic`
preserves that relationship and avoids a second package duplicating systemd’s
unit concepts.

## Layers of the package

Section models map typed Python fields to systemd directives.
`ServiceUnitConfiguration` and `TimerUnitConfiguration` assemble those sections
into files. `SystemdConfiguration` names collections and controls persistence.
`SystemdClient` handles `systemctl` calls and returns typed `UnitInfo` state.

`SystemdConvenienceConfiguration` adds shared stop/restart defaults and persists
JSON state for the `_systemd_convenience` CLI. That layer exists for external
orchestrators such as
[airflow-systemd](https://github.com/airflow-laminar/airflow-systemd); ordinary
unit rendering does not require it.

## User and system scopes

System scope uses `/etc/systemd/system` and `systemctl`. User scope uses
`~/.config/systemd/user` and `systemctl --user`. The model changes paths and
commands, but it does not elevate permissions or create a user session manager.
Those remain deployment responsibilities.

## Relationship to cron and supervisord

[cron-pydantic](https://github.com/airflow-laminar/cron-pydantic) models a
scheduler that launches commands without retaining process ownership.
[supervisor-pydantic](https://github.com/airflow-laminar/supervisor-pydantic)
models a dedicated supervisord instance. Systemd combines activation,
supervision, logging, dependencies, and host lifecycle in the existing service
manager, which is why its configuration and runtime client are represented
together.
