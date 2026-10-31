"""devsnap — snapshot and diff your development environment."""

from .core import Snapshot, collect_snapshot, diff_snapshots, render_diff, render_snapshot

__version__ = "0.1.0"
__all__ = [
    "Snapshot",
    "collect_snapshot",
    "diff_snapshots",
    "render_diff",
    "render_snapshot",
    "__version__",
]
