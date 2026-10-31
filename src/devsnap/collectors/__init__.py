"""All collectors, in snapshot display order."""

from .base import Collector
from .env import EnvCollector
from .python import PythonCollector
from .system import SystemCollector
from .tools import ToolsCollector

ALL_COLLECTORS: list[Collector] = [
    SystemCollector(),
    PythonCollector(),
    ToolsCollector(),
    EnvCollector(),
]

__all__ = ["ALL_COLLECTORS", "Collector"]
