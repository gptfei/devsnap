from devsnap.core import Snapshot, collect_snapshot, diff_snapshots, render_diff


def sample(sections):
    return Snapshot(created_at="2026-01-01T00:00:00+00:00", sections=sections)


def test_snapshot_json_roundtrip():
    snap = sample({"system": {"os": "Linux"}})
    assert Snapshot.from_json(snap.to_json()).sections == snap.sections


def test_collect_has_core_sections():
    snap = collect_snapshot()
    assert "system" in snap.sections
    assert "python" in snap.sections
    assert snap.sections["python"]["version"]


def test_collect_only_filter():
    snap = collect_snapshot(only=["system"])
    assert list(snap.sections) == ["system"]


def test_diff_detects_change_add_remove():
    old = sample({"tools": {"git": "git version 2.40", "node": "v18"}})
    new = sample({"tools": {"git": "git version 2.43", "docker": "Docker version 25"}})
    diff = diff_snapshots(old, new)
    assert diff["tools"]["git"] == ("git version 2.40", "git version 2.43")
    assert diff["tools"]["node"] == ("v18", None)
    assert diff["tools"]["docker"] == (None, "Docker version 25")


def test_diff_identical_is_empty_and_renders_so():
    snap = sample({"system": {"os": "Linux"}})
    assert diff_snapshots(snap, snap) == {}
    assert render_diff({}) == "No differences.\n"
