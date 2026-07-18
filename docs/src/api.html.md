# API reference

The public API is re-exported from `systemd_pydantic`.

## Unit models

| [`UnitConfiguration`](_build/systemd_pydantic.UnitConfiguration.md#systemd_pydantic.UnitConfiguration)                      | Common settings from a systemd unit's `[Unit]` section.          |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| [`ServiceConfiguration`](_build/systemd_pydantic.ServiceConfiguration.md#systemd_pydantic.ServiceConfiguration)             | Process supervision settings from a systemd `[Service]` section. |
| [`TimerConfiguration`](_build/systemd_pydantic.TimerConfiguration.md#systemd_pydantic.TimerConfiguration)                   | Activation settings from a systemd `[Timer]` section.            |
| [`InstallConfiguration`](_build/systemd_pydantic.InstallConfiguration.md#systemd_pydantic.InstallConfiguration)             | Enablement settings from a systemd `[Install]` section.          |
| [`ServiceUnitConfiguration`](_build/systemd_pydantic.ServiceUnitConfiguration.md#systemd_pydantic.ServiceUnitConfiguration) |                                                                  |
| [`TimerUnitConfiguration`](_build/systemd_pydantic.TimerUnitConfiguration.md#systemd_pydantic.TimerUnitConfiguration)       |                                                                  |

## Configuration and lifecycle

| [`SystemdConfiguration`](_build/systemd_pydantic.SystemdConfiguration.md#systemd_pydantic.SystemdConfiguration)                                  | Named collection of systemd service and timer unit files.          |
|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`SystemdConvenienceConfiguration`](_build/systemd_pydantic.SystemdConvenienceConfiguration.md#systemd_pydantic.SystemdConvenienceConfiguration) | Systemd defaults and persisted state used by convenience commands. |
| [`SystemdClient`](_build/systemd_pydantic.SystemdClient.md#systemd_pydantic.SystemdClient)(cfg[, runner])                                        |                                                                    |
| [`UnitInfo`](_build/systemd_pydantic.UnitInfo.md#systemd_pydantic.UnitInfo)                                                                      |                                                                    |
| [`CommandResult`](_build/systemd_pydantic.CommandResult.md#systemd_pydantic.CommandResult)(command, returncode[, stdout, ...])                   |                                                                    |
| [`CommandRunner`](_build/systemd_pydantic.CommandRunner.md#systemd_pydantic.CommandRunner)(\*args, \*\*kwargs)                                   |                                                                    |
| [`SubprocessCommandRunner`](_build/systemd_pydantic.SubprocessCommandRunner.md#systemd_pydantic.SubprocessCommandRunner)()                       |                                                                    |
| [`SSHCommandRunner`](_build/systemd_pydantic.SSHCommandRunner.md#systemd_pydantic.SSHCommandRunner)(host[, runner])                              |                                                                    |
| [`SystemdCommandError`](_build/systemd_pydantic.SystemdCommandError.md#systemd_pydantic.SystemdCommandError)(result)                             |                                                                    |
| [`load_config`](_build/systemd_pydantic.load_config.md#systemd_pydantic.load_config)([config_dir, config_name, ...])                             |                                                                    |
| [`load_convenience_config`](_build/systemd_pydantic.load_convenience_config.md#systemd_pydantic.load_convenience_config)([config_dir, ...])      |                                                                    |
