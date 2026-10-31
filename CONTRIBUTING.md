# Contributing to devsnap

Thanks for helping! This project is built so a first contribution takes
minutes, not days.

## Set up

```bash
git clone https://github.com/gptfei/devsnap
cd devsnap
pip install -e .
python -m pytest
python -m devsnap snap   # smoke test
```

## The easiest contributions

1. **Add a tool version check** — one line in
   `src/devsnap/collectors/tools.py`, e.g. `"php": ["php", "--version"]`.
   Keep the dict alphabetical and add nothing else.
2. **Add a collector** — for a runtime, database or cloud CLI we do not
   cover yet. Copy `collectors/system.py`, implement `collect()` so it
   returns `{str: str}` and never raises, register it in
   `collectors/__init__.py`, and add a test.
3. **Fix snapshot output** on an OS or shell we have not tested.

## Rules that keep reviews fast

- Zero third-party dependencies. Standard library only.
- A collector must never raise or hang (5s timeout on subprocess calls).
- Never capture a secret in clear text — when in doubt, mask it.
- New behaviour needs a test. Bug fixes need a regression test.
- Keep PRs small and single-purpose; describe the machine/OS you tested on.

## Pull request flow

Fork, branch (`feat/...` or `fix/...`), open the PR against `main`,
fill in the template, and make sure CI is green. A maintainer reviews
for correctness and safety of captured data — that is the whole bar.
