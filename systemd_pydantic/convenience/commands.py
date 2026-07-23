from pathlib import Path
from typing import Annotated

from typer import Argument, Exit, Option, Typer

from ..client import SystemdClient
from ..config import SystemdConvenienceConfiguration
from .common import SystemdTaskStep

ConfigInput = str | Path | SystemdConvenienceConfiguration


def _raise_or_exit(value: bool, exit: bool):
    if exit:
        raise Exit(int(not value))
    return value


def _load_or_pass(cfg: ConfigInput) -> SystemdConvenienceConfiguration:
    if isinstance(cfg, Path):
        cfg = cfg.read_text()
    if isinstance(cfg, str):
        return SystemdConvenienceConfiguration.model_validate_json(cfg)
    if not isinstance(cfg, SystemdConvenienceConfiguration):
        raise NotImplementedError
    return cfg


def write_systemd_config(cfg_json: str, _exit: Annotated[bool, Argument(hidden=True)] = True):
    cfg = _load_or_pass(cfg_json)
    cfg._write_self()
    client = SystemdClient(cfg)
    client.daemon_reload()
    return _raise_or_exit(True, _exit)


def start_services(
    cfg: Annotated[Path, Option(exists=True, file_okay=True, dir_okay=False, readable=True)] = Path("pydantic.json"),
    restart: bool = False,
    _exit: Annotated[bool, Argument(hidden=True)] = True,
):
    config = _load_or_pass(cfg)
    client = SystemdClient(config)
    result = client.restart_services() if restart else client.start_services()
    ok = all(info.ok(config.success_exit_status) for info in result.values())
    return _raise_or_exit(ok, _exit)


def check_services(
    cfg: Annotated[Path, Option(exists=True, file_okay=True, dir_okay=False, readable=True)] = Path("pydantic.json"),
    check_running: bool = False,
    check_done: bool = False,
    _exit: Annotated[bool, Argument(hidden=True)] = True,
):
    config = _load_or_pass(cfg)
    infos = SystemdClient(config).get_all_service_info().values()
    if check_running:
        ok = all(info.running() for info in infos)
    elif check_done:
        ok = all(info.done(config.success_exit_status) for info in infos)
    else:
        ok = all(info.ok(config.success_exit_status) for info in infos)
    return _raise_or_exit(ok, _exit)


def stop_services(
    cfg: Annotated[Path, Option(exists=True, file_okay=True, dir_okay=False, readable=True)] = Path("pydantic.json"),
    _exit: Annotated[bool, Argument(hidden=True)] = True,
):
    config = _load_or_pass(cfg)
    infos = SystemdClient(config).stop_services().values()
    return _raise_or_exit(all(info.stopped() for info in infos), _exit)


def restart_services(
    cfg: Annotated[Path, Option(exists=True, file_okay=True, dir_okay=False, readable=True)] = Path("pydantic.json"),
    _exit: Annotated[bool, Argument(hidden=True)] = True,
):
    config = _load_or_pass(cfg)
    infos = SystemdClient(config).restart_services().values()
    return _raise_or_exit(all(info.ok(config.success_exit_status) for info in infos), _exit)


def remove_systemd_config(
    cfg: Annotated[Path, Option(exists=True, file_okay=True, dir_okay=False, readable=True)] = Path("pydantic.json"),
    _exit: Annotated[bool, Argument(hidden=True)] = True,
):
    config = _load_or_pass(cfg)
    client = SystemdClient(config)
    client.stop_timers()
    client.stop_services()
    config.rmdir()
    client.daemon_reload()
    return _raise_or_exit(True, _exit)


def _add_to_typer(app: Typer, command: SystemdTaskStep, function) -> None:
    app.command(command)(function)


def main() -> None:
    app = Typer()
    _add_to_typer(app, "configure-systemd", write_systemd_config)
    _add_to_typer(app, "start-services", start_services)
    _add_to_typer(app, "check-services", check_services)
    _add_to_typer(app, "restart-services", restart_services)
    _add_to_typer(app, "stop-services", stop_services)
    _add_to_typer(app, "unconfigure-systemd", remove_systemd_config)
    app()
