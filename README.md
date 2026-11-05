# devsnap

[![PyPI](https://img.shields.io/pypi/v/devsnap)](https://pypi.org/project/devsnap/)
[![CI](https://github.com/gptfei/devsnap/actions/workflows/ci.yml/badge.svg)](https://github.com/gptfei/devsnap/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/devsnap)](https://pypi.org/project/devsnap/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Snapshot and diff your development environment — end "works on my machine" debugging.**

`devsnap` is a zero-dependency Python CLI that captures your OS, Python,
tool versions (git, node, docker, go, rust, ...), installed packages and
selected environment variables into one shareable JSON snapshot. Secrets
are masked automatically, so a snapshot is safe to paste into a bug report.
Diff two snapshots and see exactly what differs between two machines.

## Install

```bash
pip install devsnap
# or from source:
pip install git+https://github.com/gptfei/devsnap
```

Requires Python 3.9+. No third-party dependencies.

## Usage

```bash
# Take a snapshot on machine A
devsnap snap -o machine-a.json

# Take one on machine B, then compare
devsnap snap -o machine-b.json
devsnap diff machine-a.json machine-b.json
```

Example diff output:

```text
[python]
  ~ version: 3.11.4 -> 3.12.3

[tools]
  ~ git: git version 2.40.1 -> git version 2.43.0
  + docker = Docker version 25.0.3
```

`devsnap diff` exits with code 1 when environments differ, so CI can gate
on environment drift. Run `devsnap snap` without `-o` to print a readable
report instead of JSON.

As a library:

```python
from devsnap import collect_snapshot, diff_snapshots

mine = collect_snapshot()
print(mine.to_json())
```

## Why

"It works on my machine" bugs burn hours because the difference between
two environments is invisible. Existing answers are heavy (full system
inventory tools) or manual (copying `pip freeze` output around). devsnap
is the small middle ground: one command, one file, one diff.

## Contributing

Contributions are welcome — and designed to be easy:

- **Add a tool** to `collectors/tools.py` (one line, alphabetical).
- **Add a collector** for a stack we miss (Java, .NET, PHP, databases...).
  Copy any collector in `src/devsnap/collectors/`, see `base.py`.
- **Report** a machine where a snapshot comes out wrong.

Read [CONTRIBUTING.md](CONTRIBUTING.md), and look for issues labelled
`good first issue`.

## 中文简介

`devsnap` 是一个零依赖的 Python 命令行工具：一键把操作系统、Python、
常用工具版本、已装包和（自动打码后的）环境变量拍成一份 JSON 快照，
可以安全地贴进 issue 里。两份快照一 diff，“在我机器上能跑”的差异
立刻现形。

## See also

- **[llmparse](https://github.com/gptfei/llmparse)** — parse the JSON
  your LLM meant to send: extraction and repair for raw LLM output.

## License

MIT — see [LICENSE](LICENSE).
