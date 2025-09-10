# header-guardian

CLI to enforce standardized **file headers** (SPDX license identifiers, copyright lines, or custom templates) across your codebase.  
Built for an **Always Green** workflow and clean open‑source repos.

[![CI](https://github.com/CoderDeltaLAN/header-guardian/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/header-guardian/actions/workflows/ci.yml)
[![CodeQL](https://github.com/CoderDeltaLAN/header-guardian/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/header-guardian/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-0070ba?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW) 

---

## Why

Compliance and consistency suffer when source files **lack headers** (SPDX/copyright) or they are **inconsistent**.  
`header-guardian` standardizes headers from day one — locally and in CI.

## Features

- Validates and inserts `SPDX-License-Identifier: <ID>` at the top of source files.
- Optional **copyright** header: `Copyright (c) <YEAR> <AUTHOR>`.
- Supports **custom templates** via `--template` (prepended verbatim).
- **Idempotent fixes**: re-running does not duplicate headers.
- Clear **exit codes** for CI gating.
- Fast, **zero‑config defaults** with sensible ignores.
- Current focus: **Python** files (`.py`). (Roadmap could expand via comment‑style detection.)

## Installation

### From PyPI (when published)
```bash
pip install header-guardian
```

### From source (local checkout)
```bash
# inside the project root
pip install .
# or using Poetry build artifact
poetry build && pip install dist/*.whl
```

## Quick Start

```bash
# Show help
header-guardian --help

# Check that all .py files have the expected header(s) (no changes)
header-guardian --path . --ext .py --mode check

# Insert headers where missing (SPDX + optional copyright)
header-guardian --path . --ext .py --mode fix --license-id MIT --author "CoderDeltaLAN"
```

> Ignored by default: `.git`, `.venv`, `venv`, `env`, `dist`, `build`, `__pycache__`, `.mypy_cache`, `.pytest_cache`.

## CLI Reference

```
Usage: header-guardian [OPTIONS]

Options:
  --path PATH                     Root directory to scan. [default: .]
  --ext TEXT                      File extension to validate. Repeat for multiple. [default: .py]
  --mode [check|fix]              "check" only validates; "fix" inserts headers. [default: check]
  --license-id TEXT               SPDX License Identifier to enforce. [default: MIT]
  --author TEXT                   Author to render in copyright line when --mode=fix.
  --template FILE                 Optional path to a custom header template to prepend.
  --help                          Show this message and exit.
```

### Exit codes
- `0`: All good.
- `1`: Missing/invalid headers.

## Examples

Check only:
```bash
header-guardian --path . --ext .py --mode check
```

Fix headers with SPDX + author:
```bash
header-guardian --path . --ext .py --mode fix --license-id MIT --author "CoderDeltaLAN"
```

Use a custom template file:
```bash
header-guardian --path . --ext .py --mode fix --template ./header.template
```

Scan a specific subtree:
```bash
header-guardian --path ./src --ext .py --mode check
```

## CI Usage (GitHub Actions snippet)

```yaml
- run: poetry run header-guardian --path . --ext .py --mode check
```
Combine with **required status checks** to keep `main` always green.

## Contributing

Use **Poetry** for local setup. Run the local gate before any push:
```bash
poetry run ruff check . --fix
poetry run ruff format .
poetry run black .
PYTHONPATH=src poetry run pytest -q
poetry run mypy .
```
Conventional Commits recommended. Small, atomic PRs. CI must be green.

See `SECURITY.md` for vulnerability reporting.

## 🔍 SEO Keywords

AI code analyzer, Python linter, bug detection CLI, refactor AI code, Python static analysis, clean code automation, catch bugs early, developer productivity tools, SPDX headers, license compliance, header templates, OSS tooling, developer workflow, continuous integration.

## 💖 Donations & Sponsorship

Support open-source: your donations keep projects clean, secure, and evolving for the global community.  
[![Donate](https://img.shields.io/badge/Donate-PayPal-0070ba?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW)

## 👤 Author

**CoderDeltaLAN (Yosvel)**  
📧 `coderdeltalan.cargo784@8alias.com`  
🐙 https://github.com/CoderDeltaLAN

## 📄 License

Licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

