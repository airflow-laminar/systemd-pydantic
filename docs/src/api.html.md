# API reference

The public API is re-exported from `systemd_pydantic`.

## Unit models

| [`UnitConfiguration`](_build/systemd_pydantic.UnitConfiguration.html.md#systemd_pydantic.UnitConfiguration)                      | Common settings from a systemd unit's `[Unit]` section.          |
|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`ServiceConfiguration`](_build/systemd_pydantic.ServiceConfiguration.html.md#systemd_pydantic.ServiceConfiguration)             | Process supervision settings from a systemd `[Service]` section. |
| [`TimerConfiguration`](_build/systemd_pydantic.TimerConfiguration.html.md#systemd_pydantic.TimerConfiguration)                   | Activation settings from a systemd `[Timer]` section.            |
| [`InstallConfiguration`](_build/systemd_pydantic.InstallConfiguration.html.md#systemd_pydantic.InstallConfiguration)             | Enablement settings from a systemd `[Install]` section.          |
| [`ServiceUnitConfiguration`](_build/systemd_pydantic.ServiceUnitConfiguration.html.md#systemd_pydantic.ServiceUnitConfiguration) |                                                                  |
| [`TimerUnitConfiguration`](_build/systemd_pydantic.TimerUnitConfiguration.html.md#systemd_pydantic.TimerUnitConfiguration)       |                                                                  |

## Configuration and lifecycle

| [`SystemdConfiguration`](_build/systemd_pydantic.SystemdConfiguration.html.md#systemd_pydantic.SystemdConfiguration)                                  | Named collection of systemd service and timer unit files.          |
|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`SystemdConvenienceConfiguration`](_build/systemd_pydantic.SystemdConvenienceConfiguration.html.md#systemd_pydantic.SystemdConvenienceConfiguration) | Systemd defaults and persisted state used by convenience commands. |
| [`SystemdClient`](_build/systemd_pydantic.SystemdClient.html.md#systemd_pydantic.SystemdClient)(cfg[, runner])                                        |                                                                    |
| [`UnitInfo`](_build/systemd_pydantic.UnitInfo.html.md#systemd_pydantic.UnitInfo)                                                                      |                                                                    |
| [`CommandResult`](_build/systemd_pydantic.CommandResult.html.md#systemd_pydantic.CommandResult)(command, returncode[, stdout, ...])                   |                                                                    |
| [`CommandRunner`](_build/systemd_pydantic.CommandRunner.html.md#systemd_pydantic.CommandRunner)(\*args, \*\*kwargs)                                   |                                                                    |
| [`SubprocessCommandRunner`](_build/systemd_pydantic.SubprocessCommandRunner.html.md#systemd_pydantic.SubprocessCommandRunner)()                       |                                                                    |
| [`SSHCommandRunner`](_build/systemd_pydantic.SSHCommandRunner.html.md#systemd_pydantic.SSHCommandRunner)(host[, runner])                              |                                                                    |
| [`SystemdCommandError`](_build/systemd_pydantic.SystemdCommandError.html.md#systemd_pydantic.SystemdCommandError)(result)                             |                                                                    |
| [`load_config`](_build/systemd_pydantic.load_config.html.md#systemd_pydantic.load_config)([config_dir, config_name, ...])                             |                                                                    |
| [`load_convenience_config`](_build/systemd_pydantic.load_convenience_config.html.md#systemd_pydantic.load_convenience_config)([config_dir, ...])      |                                                                    |
