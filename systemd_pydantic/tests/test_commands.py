from pathlib import Path
from unittest.mock import Mock, patch

from systemd_pydantic import ServiceConfiguration, ServiceUnitConfiguration, SystemdConvenienceConfiguration, UnitInfo
from systemd_pydantic.convenience.commands import (
    _load_or_pass,
    check_services,
    remove_systemd_config,
    restart_services,
    start_services,
    stop_services,
    write_systemd_config,
)


def configuration(tmp_path: Path) -> SystemdConvenienceConfiguration:
    return SystemdConvenienceConfiguration(
        service={"worker": ServiceUnitConfiguration(service=ServiceConfiguration(exec_start="/usr/bin/worker"))},
        unit_dir=tmp_path / "units",
        working_dir=tmp_path / "state",
    )


def test_load_or_pass(tmp_path: Path):
    config = configuration(tmp_path)
    config._write_self()

    assert _load_or_pass(config) is config
    assert _load_or_pass(config.model_dump_json()) == config
    assert _load_or_pass(config._pydantic_path) == config


def test_lifecycle_commands(tmp_path: Path):
    config = configuration(tmp_path)
    running = UnitInfo(name="worker.service", active_state="active", sub_state="running")
    stopped = UnitInfo(name="worker.service", active_state="inactive", sub_state="dead", result="success", exec_main_status=0)
    client = Mock()
    client.start_services.return_value = {running.name: running}
    client.restart_services.return_value = {running.name: running}
    client.get_all_service_info.return_value = {running.name: running}
    client.stop_services.return_value = {stopped.name: stopped}
    client.stop_timers.return_value = {}

    with patch("systemd_pydantic.convenience.commands.SystemdClient", return_value=client):
        assert write_systemd_config(config.model_dump_json(), _exit=False)
        assert start_services(config._pydantic_path, _exit=False)
        assert check_services(config._pydantic_path, check_running=True, _exit=False)
        assert restart_services(config._pydantic_path, _exit=False)
        assert stop_services(config._pydantic_path, _exit=False)
        assert remove_systemd_config(config._pydantic_path, _exit=False)

    client.daemon_reload.assert_called()
    assert not config._pydantic_path.exists()
