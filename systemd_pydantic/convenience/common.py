from typing import Literal

SystemdTaskStep = Literal[
    "configure-systemd",
    "start-services",
    "check-services",
    "restart-services",
    "stop-services",
    "unconfigure-systemd",
]

__all__ = ("SystemdTaskStep",)
