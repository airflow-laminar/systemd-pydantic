from pytest import raises

from systemd_pydantic import (
    CommandResult,
    ServiceConfiguration,
    ServiceUnitConfiguration,
    SystemdClient,
    SystemdCommandError,
    SystemdConfiguration,
    SystemdScope,
)


class FakeRunner:
    def __init__(self):
        self.commands: list[list[str]] = []
        self.states: dict[str, str] = {}

    def run(self, command: list[str], timeout: int) -> CommandResult:
        self.commands.append(command)
        action_index = 2 if "--user" in command else 1
        action = command[action_index]
        names = [value for value in command[action_index + 1 :] if not value.startswith("--")]
        if action in {"start", "restart"}:
            self.states.update({name: "active" for name in names})
        elif action in {"stop", "kill"}:
            self.states.update({name: "inactive" for name in names})
        if action == "show":
            name = names[0]
            active = self.states.get(name, "inactive")
            sub_state = "running" if active == "active" else "dead"
            stdout = f"LoadState=loaded\nActiveState={active}\nSubState={sub_state}\nResult=success\nExecMainCode=exited\nExecMainStatus=0\n"
            return CommandResult(command, 0, stdout)
        return CommandResult(command, 0)


class FailingRunner:
    def run(self, command: list[str], timeout: int) -> CommandResult:
        return CommandResult(command, 1, stderr="permission denied")


def configuration(scope: SystemdScope = "system") -> SystemdConfiguration:
    return SystemdConfiguration(
        service={"worker": ServiceUnitConfiguration(service=ServiceConfiguration(exec_start="/usr/bin/worker"))},
        scope=scope,
    )


def test_service_lifecycle_and_state():
    runner = FakeRunner()
    client = SystemdClient(configuration(), runner)

    assert client.start_services()["worker.service"].running()
    assert client.restart_services()["worker.service"].ok()
    assert client.stop_services()["worker.service"].done()
    assert client.kill_services()["worker.service"].stopped()
    assert [command[1] for command in runner.commands if command[1] != "show"] == ["start", "restart", "stop", "kill"]


def test_user_scope_and_management_commands():
    runner = FakeRunner()
    client = SystemdClient(configuration("user"), runner)

    client.daemon_reload()
    client.enable_units()
    client.disable_units()

    assert runner.commands == [
        ["systemctl", "--user", "daemon-reload"],
        ["systemctl", "--user", "enable", "worker.service"],
        ["systemctl", "--user", "disable", "worker.service"],
    ]


def test_command_error():
    with raises(SystemdCommandError, match="permission denied"):
        SystemdClient(configuration(), FailingRunner()).daemon_reload()
