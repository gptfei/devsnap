"""Versions of common external development tools.

Each tool is one line here. Adding a tool the community uses is a
welcome contribution — please keep the list alphabetical.
"""

from __future__ import annotations

from .base import Collector, run_version

# tool name -> argv used to ask it for its version
TOOLS: dict[str, list[str]] = {
    "bun": ["bun", "--version"],
    "cargo": ["cargo", "--version"],
    "cmake": ["cmake", "--version"],
    "deno": ["deno", "--version"],
    "docker": ["docker", "--version"],
    "git": ["git", "--version"],
    "go": ["go", "version"],
    "java": ["java", "--version"],
    "kubectl": ["kubectl", "version", "--client"],
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "pnpm": ["pnpm", "--version"],
    "ruby": ["ruby", "--version"],
    "rustc": ["rustc", "--version"],
    "yarn": ["yarn", "--version"],
}


class ToolsCollector(Collector):
    name = "tools"

    def collect(self) -> dict[str, str]:
        return {name: run_version(argv) for name, argv in sorted(TOOLS.items())}
