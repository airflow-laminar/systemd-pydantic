# systemd_pydantic.SystemdClient

### *class* systemd_pydantic.SystemdClient(cfg: [SystemdConfiguration](systemd_pydantic.SystemdConfiguration.html.md#systemd_pydantic.SystemdConfiguration), runner: [CommandRunner](systemd_pydantic.CommandRunner.html.md#systemd_pydantic.CommandRunner) | None = None)[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#SystemdClient)

Bases: `object`

#### \_\_init_\_(cfg: [SystemdConfiguration](systemd_pydantic.SystemdConfiguration.html.md#systemd_pydantic.SystemdConfiguration), runner: [CommandRunner](systemd_pydantic.CommandRunner.html.md#systemd_pydantic.CommandRunner) | None = None)[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#SystemdClient.__init__)

### Methods

| [`__init__`](#systemd_pydantic.SystemdClient.__init__)(cfg[, runner])   |    |
|-------------------------------------------------------------------------|----|
| `daemon_reload`()                                                       |    |
| `disable_units`([names])                                                |    |
| `enable_units`([names])                                                 |    |
| `get_all_service_info`()                                                |    |
| `get_all_timer_info`()                                                  |    |
| `get_unit_info`(name)                                                   |    |
| `get_units_info`(names)                                                 |    |
| `kill_services`()                                                       |    |
| `kill_units`(names)                                                     |    |
| `restart_services`()                                                    |    |
| `restart_units`(names)                                                  |    |
| `start_services`()                                                      |    |
| `start_timers`()                                                        |    |
| `start_units`(names)                                                    |    |
| `stop_services`()                                                       |    |
| `stop_timers`()                                                         |    |
| `stop_units`(names)                                                     |    |
