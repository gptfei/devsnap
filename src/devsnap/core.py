"""Snapshot collection, serialisation and diffing."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .collectors import ALL_COLLECTORS

FORMAT_VERSION = 1


@dataclass
class Snapshot:
    created_at: str
    sections: dict[str, dict[str, str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "format": FORMAT_VERSION,
            "created_at": self.created_at,
            "sections": self.sections,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Snapshot":
        if data.get("format") != FORMAT_VERSION:
            raise ValueError(f"unsupported snapshot format: {data.get('format')!r}")
        return cls(created_at=data["created_at"], sections=data["sections"])

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "Snapshot":
        return cls.from_dict(json.loads(text))


def collect_snapshot(only: list[str] | None = None) -> Snapshot:
    sections: dict[str, dict[str, str]] = {}
    for collector in ALL_COLLECTORS:
        if only and collector.name not in only:
            continue
        try:
            sections[collector.name] = collector.collect()
        except Exception as exc:  # one bad collector must not lose the snapshot
            sections[collector.name] = {"error": f"{type(exc).__name__}: {exc}"}
    return Snapshot(
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        sections=sections,
    )


def diff_snapshots(old: Snapshot, new: Snapshot) -> dict[str, dict[str, tuple[str | None, str | None]]]:
    """Return ``{section: {key: (old_value, new_value)}}`` for changed keys only.

    ``None`` marks a key that is absent on that side.
    """
    diff: dict[str, dict[str, tuple[str | None, str | None]]] = {}
    for section in sorted(set(old.sections) | set(new.sections)):
        old_items = old.sections.get(section, {})
        new_items = new.sections.get(section, {})
        changes = {}
        for key in sorted(set(old_items) | set(new_items)):
            before, after = old_items.get(key), new_items.get(key)
            if before != after:
                changes[key] = (before, after)
        if changes:
            diff[section] = changes
    return diff


def render_snapshot(snapshot: Snapshot) -> str:
    lines = [f"devsnap snapshot — {snapshot.created_at}", ""]
    for section, items in snapshot.sections.items():
        lines.append(f"[{section}]")
        for key in sorted(items):
            lines.append(f"  {key} = {items[key]}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_diff(diff: dict) -> str:
    if not diff:
        return "No differences.\n"
    lines = []
    for section, changes in diff.items():
        lines.append(f"[{section}]")
        for key, (before, after) in changes.items():
            if before is None:
                lines.append(f"  + {key} = {after}")
            elif after is None:
                lines.append(f"  - {key} = {before}")
            else:
                lines.append(f"  ~ {key}: {before} -> {after}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
