"""Selected environment variables, with secrets masked.

Only a small allow-list of development-relevant variables is captured,
and any variable whose name looks secret-bearing is masked. Snapshots
are meant to be pasted into bug reports, so they must be safe to share.
"""

from __future__ import annotations

import os

from .base import Collector

CAPTURED = [
    "CI",
    "EDITOR",
    "HOME",
    "LANG",
    "PATH",
    "PWD",
    "SHELL",
    "TERM",
    "TZ",
    "USER",
    "VIRTUAL_ENV",
    "CONDA_DEFAULT_ENV",
    "NODE_ENV",
    "PYTHONPATH",
]

SECRET_MARKERS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL")


def mask_value(name: str, value: str) -> str:
    if any(marker in name.upper() for marker in SECRET_MARKERS):
        return "***masked***"
    return value


class EnvCollector(Collector):
    name = "env"

    def collect(self) -> dict[str, str]:
        return {
            name: mask_value(name, os.environ[name])
            for name in CAPTURED
            if name in os.environ
        }
