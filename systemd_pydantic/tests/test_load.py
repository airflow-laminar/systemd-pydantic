from pathlib import Path

from systemd_pydantic import SystemdConfiguration, SystemdConvenienceConfiguration, load_config, load_convenience_config

BASE_PATH = str(Path(__file__).parent / "hydra" / "dag.py")


def test_load_config():
    config = load_config("config", "systemd", basepath=BASE_PATH)

    assert isinstance(config, SystemdConfiguration)
    assert config.scope == "user"
    assert config.service_names == ["worker.service"]


def test_load_convenience_config():
    config = load_convenience_config("config", "systemd", basepath=BASE_PATH)

    assert isinstance(config, SystemdConvenienceConfiguration)
    assert config.service["worker"].service.restart == "no"
