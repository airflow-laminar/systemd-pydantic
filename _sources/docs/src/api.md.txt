# API reference

The public API is re-exported from `systemd_pydantic`.

## Unit models

```{eval-rst}
.. currentmodule:: systemd_pydantic

.. autosummary::
   :toctree: _build

   UnitConfiguration
   ServiceConfiguration
   TimerConfiguration
   InstallConfiguration
   ServiceUnitConfiguration
   TimerUnitConfiguration
```

## Configuration and lifecycle

```{eval-rst}
.. currentmodule:: systemd_pydantic

.. autosummary::
   :toctree: _build

   SystemdConfiguration
   SystemdConvenienceConfiguration
   SystemdClient
   UnitInfo
   CommandResult
   CommandRunner
   SubprocessCommandRunner
   SSHCommandRunner
   SystemdCommandError
   load_config
   load_convenience_config
```
