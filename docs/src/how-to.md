# How-to guides

These guides cover common systemd configuration and lifecycle tasks.

## How to load YAML with Hydra

Create `config/job.yaml`:

```yaml
# @package _global_
service:
  worker:
    unit:
      description: Background worker
    service:
      type: exec
      exec_start: /opt/jobs/worker
      restart: on-failure
scope: user
```

Load it relative to your calling script:

```python
from systemd_pydantic import SystemdConfiguration

config = SystemdConfiguration.load("config", "job")
```

Pass Hydra overrides with `overrides=["scope=system"]` when the deployment owns
the system manager.

## How to control units

Write units, reload the manager, then start services through one client:

```python
from systemd_pydantic import SystemdClient

config.write()
client = SystemdClient(config)
client.daemon_reload()
client.start_services()
```

Use `start_timers()` for timer activation. `enable_units()` and
`disable_units()` default to every configured service and timer, or accept an
explicit list of names.

## How to run commands over SSH

Inject an `SSHCommandRunner`:

```python
from systemd_pydantic import SSHCommandRunner, SystemdClient

client = SystemdClient(config, runner=SSHCommandRunner("jobs.example.com"))
client.get_all_service_info()
```

The remote host must already contain the unit files. For Airflow-managed SSH
configuration and lifecycle, use
[airflow-systemd](https://github.com/airflow-laminar/airflow-systemd).

## How to use the model with airflow-config

Use `SystemdTask` as an `airflow-pydantic` task target:

```yaml
dags:
  nightly-systemd:
    schedule: "@daily"
    tasks:
      run-job:
        _target_: airflow_systemd.SystemdTask
        cfg:
          scope: user
          service:
            nightly:
              service:
                type: exec
                exec_start: /opt/jobs/nightly
```

Load this with `airflow-config`; it instantiates the matching
`SystemdAirflowConfiguration` through the task model. Refer to the
[airflow-systemd tutorial](https://github.com/airflow-laminar/airflow-systemd/blob/main/docs/src/tutorial.md)
for the complete DAG lifecycle.
