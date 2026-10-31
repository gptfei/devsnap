"""Base class for collectors.

A collector inspects one slice of the development environment (Python,
Git, Node, Docker, ...) and returns a flat ``{key: value}`` mapping of
strings. Collectors must never raise: a missing tool is reported as
``"not found"`` so a snapshot always succeeds on any machine.

Want to add support for a new tool? Copy any existing collector, give it
a unique ``name``, and register it in ``collectors/__init__.py``.
See CONTRIBUTING.md — this is the easiest first contribution to devsnap.
"""

from __future__ import annotations

import shutil
import subprocess


class Collector:
    name: str = "base"

    def collect(self) -> dict[str, str]:
        raise NotImplementedError


def run_version(argv: list[str], timeout: float = 5.0) -> str:
    """Run a ``--version``-style command and return its first output line.

    Returns ``"not found"`` when the executable is missing and
    ``"unknown"`` when it exists but produces no usable output.
    """
    exe = shutil.which(argv[0])
    if exe is None:
        return "not found"
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    output = (proc.stdout or proc.stderr).strip().splitlines()
    return output[0].strip() if output else "unknown"
