"""Operating system and shell information."""

from __future__ import annotations

import os
import platform

from .base import Collector


class SystemCollector(Collector):
    name = "system"

    def collect(self) -> dict[str, str]:
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "architecture": platform.architecture()[0] or "unknown",
            "shell": os.environ.get("SHELL", "unknown"),
            "terminal": os.environ.get("TERM", "unknown"),
            "locale": os.environ.get("LANG", "unknown"),
            "timezone": os.environ.get("TZ", "system default"),
            "cpu_count": str(os.cpu_count() or "unknown"),
        }
