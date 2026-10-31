"""Command line interface: ``devsnap snap`` and ``devsnap diff``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import Snapshot, collect_snapshot, diff_snapshots, render_diff, render_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devsnap",
        description="Snapshot and diff your development environment.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snap", help="take a snapshot of this machine")
    snap.add_argument("-o", "--output", help="write JSON snapshot to this file")
    snap.add_argument(
        "--only",
        help="comma-separated collectors to run (system, python, tools, env)",
    )

    diff = sub.add_parser("diff", help="compare two snapshot JSON files")
    diff.add_argument("old", help="older snapshot JSON file")
    diff.add_argument("new", help="newer snapshot JSON file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "snap":
        only = [part.strip() for part in args.only.split(",")] if args.only else None
        snapshot = collect_snapshot(only=only)
        if args.output:
            Path(args.output).write_text(snapshot.to_json(), encoding="utf-8")
            print(f"Snapshot written to {args.output}")
        else:
            print(render_snapshot(snapshot), end="")
        return 0

    if args.command == "diff":
        old = Snapshot.from_json(Path(args.old).read_text(encoding="utf-8"))
        new = Snapshot.from_json(Path(args.new).read_text(encoding="utf-8"))
        changes = diff_snapshots(old, new)
        print(render_diff(changes), end="")
        # Non-zero exit when environments differ, so CI can gate on it.
        return 1 if changes else 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
