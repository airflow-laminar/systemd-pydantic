# Tutorial: render a service and timer

In this tutorial, we will model a oneshot service, schedule it with a timer, and
write both unit files to a local build directory.

## Install the package

```bash
pip install systemd-pydantic
```

## Create the units

Create `example.py`:

```python
from systemd_pydantic import (
    InstallConfiguration,
    ServiceConfiguration,
    ServiceUnitConfiguration,
    SystemdConfiguration,
    TimerConfiguration,
    TimerUnitConfiguration,
)

config = SystemdConfiguration(
    service={
        "daily-report": ServiceUnitConfiguration(
            unit={"description": "Build the daily report"},
            service=ServiceConfiguration(
                type="oneshot",
                exec_start="/opt/reports/build",
                environment={"REPORT_FORMAT": "html"},
            ),
        )
    },
    timer={
        "daily-report": TimerUnitConfiguration(
            unit={"description": "Run the daily report"},
            timer=TimerConfiguration(
                on_calendar="daily",
                persistent=True,
            ),
            install=InstallConfiguration(wanted_by=["timers.target"]),
        )
    },
    unit_dir="build/units",
    working_dir="build/state",
    scope="user",
)

for path in config.write():
    print(path)
```

Run it:

```bash
python example.py
```

The output lists two files:

```text
build/units/daily-report.service
build/units/daily-report.timer
```

## Inspect the files

Open `build/units/daily-report.service`. It contains:

```ini
[Unit]
Description=Build the daily report

[Service]
Type=oneshot
ExecStart=/opt/reports/build
Environment="REPORT_FORMAT=html"
```

Open `build/units/daily-report.timer`. It contains the calendar trigger and
`timers.target` installation metadata.

You have now rendered a related service/timer pair without writing to a systemd
unit directory or invoking `systemctl`.
