from pathlib import Path

from pydantic import ValidationError
from pytest import raises

from systemd_pydantic import (
    ServiceConfiguration,
    ServiceUnitConfiguration,
    SystemdConfiguration,
    SystemdConvenienceConfiguration,
    TimerUnitConfiguration,
)


def service_unit(command: str = "/usr/bin/true") -> ServiceUnitConfiguration:
    return ServiceUnitConfiguration(service=ServiceConfiguration(type="exec", exec_start=command))


def test_configuration_render_write_remove_and_round_trip(tmp_path: Path):
    config = SystemdConfiguration(
        service={"worker": service_unit()},
        timer={"worker": TimerUnitConfiguration(timer={"on_calendar": "hourly"})},
        unit_dir=tmp_path / "units",
        working_dir=tmp_path / "state",
    )

    assert set(config.to_cfg()) == {"worker.service", "worker.timer"}
    assert config.write() == [tmp_path / "units" / "worker.service", tmp_path / "units" / "worker.timer"]
    assert all(path.exists() for path in config.unit_paths)
    assert SystemdConfiguration.model_validate_json(config.model_dump_json()) == config

    config.rmdir()
    assert not any(path.exists() for path in config.unit_paths)


def test_convenience_defaults_and_persistence(tmp_path: Path):
    config = SystemdConvenienceConfiguration(
        service={"worker": service_unit()},
        unit_dir=tmp_path / "units",
        working_dir=tmp_path / "state",
    )

    service = config.service["worker"].service
    assert service.restart == "no"
    assert service.timeout_stop_sec == "30s"
    assert service.kill_mode == "control-group"
    assert service.kill_signal == "SIGTERM"
    assert service.success_exit_status == [0]

    config._write_self()
    assert config._pydantic_path.exists()
    assert SystemdConvenienceConfiguration.model_validate_json(config._pydantic_path.read_text()) == config
    config.rmdir()
    assert not config._pydantic_path.exists()


def test_user_scope_default_unit_dir():
    config = SystemdConfiguration(service={"worker": service_unit()}, scope="user")

    assert config.unit_dir == Path.home() / ".config/systemd/user"


def test_invalid_unit_name():
    with raises(ValidationError):
        SystemdConfiguration(service={"bad/name": service_unit()})
