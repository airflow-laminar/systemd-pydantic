from datetime import timedelta

import pytest
from pydantic import ValidationError

from systemd_pydantic import (
    InstallSection,
    ServiceSection,
    SystemdServiceConfiguration,
    SystemdTimerConfiguration,
    TimerSection,
    UnitSection,
)


def test_service_unit_file():
    config = SystemdServiceConfiguration(
        unit=UnitSection(description="Airflow worker", after=["network-online.target"], wants=["network-online.target"]),
        service=ServiceSection(
            type="exec",
            exec_start="/opt/jobs/worker --queue long-running",
            restart="on-failure",
            restart_sec=timedelta(seconds=5),
            user="airflow",
            working_directory="/opt/jobs",
            environment={"MODE": "production", "LABEL": 'long running "job"'},
            kill_mode="control-group",
        ),
        install=InstallSection(wanted_by=["multi-user.target"]),
    )

    assert (
        config.to_unit_file()
        == """[Unit]
Description=Airflow worker
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
ExecStart=/opt/jobs/worker --queue long-running
Restart=on-failure
RestartSec=5s
User=airflow
WorkingDirectory=/opt/jobs
Environment=\"MODE=production\"
Environment=\"LABEL=long running \\\"job\\\"\"
KillMode=control-group

[Install]
WantedBy=multi-user.target
"""
    )
    assert config.to_cfg() == config.to_unit_file()


def test_timer_unit_file_and_json_round_trip():
    config = SystemdTimerConfiguration(
        unit={"description": "Run cleanup"},
        timer={
            "on_boot_sec": timedelta(minutes=15),
            "on_calendar": ["daily", "Mon *-*-* 09:00:00"],
            "randomized_delay_sec": "30min",
            "persistent": True,
            "unit": "cleanup.service",
        },
        install={"wanted_by": ["timers.target"]},
    )

    assert (
        config.to_unit_file()
        == """[Unit]
Description=Run cleanup

[Timer]
OnBootSec=900s
OnCalendar=daily
OnCalendar=Mon *-*-* 09:00:00
RandomizedDelaySec=30min
Unit=cleanup.service
Persistent=yes

[Install]
WantedBy=timers.target
"""
    )
    assert SystemdTimerConfiguration.model_validate_json(config.model_dump_json()) == config


def test_oneshot_allows_multiple_start_commands():
    service = ServiceSection(type="oneshot", exec_start=["/usr/bin/prepare", "/usr/bin/run"], restart_sec=timedelta(microseconds=1))

    assert service.to_unit_file() == "[Service]\nType=oneshot\nExecStart=/usr/bin/prepare\nExecStart=/usr/bin/run\nRestartSec=0.000001s"


@pytest.mark.parametrize(
    "service",
    [
        {"type": "exec"},
        {"type": "exec", "exec_start": ["/usr/bin/one", "/usr/bin/two"]},
        {"type": "dbus", "exec_start": "/usr/bin/dbus-job"},
    ],
)
def test_invalid_service_configuration(service):
    with pytest.raises(ValidationError):
        ServiceSection.model_validate(service)


def test_timer_requires_trigger():
    with pytest.raises(ValidationError):
        TimerSection()
