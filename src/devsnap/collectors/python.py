"""Python interpreter and installed packages."""

from __future__ import annotations

import importlib.metadata
import platform
import sys

from .base import Collector


class PythonCollector(Collector):
    name = "python"

    def collect(self) -> dict[str, str]:
        data = {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        }
        try:
            packages = sorted(
                f"{dist.metadata['Name']}=={dist.version}"
                for dist in importlib.metadata.distributions()
                if dist.metadata.get("Name")
            )
        except Exception:  # a snapshot must never fail on a broken env
            packages = []
        data["packages_count"] = str(len(packages))
        data["packages"] = ", ".join(packages)
        return data
