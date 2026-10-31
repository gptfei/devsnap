import json

from devsnap.cli import main
from devsnap.core import Snapshot


def test_snap_to_file(tmp_path):
    out = tmp_path / "snap.json"
    assert main(["snap", "-o", str(out), "--only", "system"]) == 0
    data = json.loads(out.read_text())
    assert data["sections"]["system"]["os"]


def test_diff_exit_codes(tmp_path):
    old = Snapshot(created_at="t1", sections={"tools": {"git": "2.40"}})
    new = Snapshot(created_at="t2", sections={"tools": {"git": "2.43"}})
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    a.write_text(old.to_json())
    b.write_text(new.to_json())
    assert main(["diff", str(a), str(b)]) == 1
    assert main(["diff", str(a), str(a)]) == 0
