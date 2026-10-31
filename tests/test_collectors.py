import sys

sys.path.insert(0, "src")

from devsnap.collectors.base import run_version
from devsnap.collectors.env import mask_value
from devsnap.collectors.tools import TOOLS


def test_run_version_missing_tool():
    assert run_version(["definitely-not-a-real-tool-xyz", "--version"]) == "not found"


def test_run_version_real_tool():
    assert run_version(["git", "--version"]).startswith("git version")


def test_secrets_are_masked():
    assert mask_value("API_TOKEN", "abc123") == "***masked***"
    assert mask_value("AWS_SECRET_ACCESS_KEY", "abc123") == "***masked***"
    assert mask_value("EDITOR", "vim") == "vim"


def test_tools_are_alphabetical_and_unique():
    assert list(TOOLS) == sorted(TOOLS)
