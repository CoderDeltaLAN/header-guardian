# header-guardian

> Multi-language header enforcer with auto-fix and SARIF-ready outputs. Always Green from day one.

![CI](https://github.com/CoderDeltaLAN/header-guardian/actions/workflows/ci.yml/badge.svg?branch=main)

## Author
**CoderDeltaLAN** — `coderdeltalan.cargo784@8alias.com`

## Quick start
```bash
pip install header-guardian
header-guardian --help
header-guardian --path . --ext .py --mode check
header-guardian --path . --ext .py --ext .ts --mode fix
```

## What it does
- Ensures a standard copyright + SPDX header.
- Supports multiple languages: .py, .sh, .js/.ts/.go/.rs/.c/.cpp/.h/.hpp, etc.
- `check` validates, `fix` inserts headers idempotently.
- Ignored dirs: .git, .venv, __pycache__, dist, build, node_modules, vendor.

## Donate
Support the project: PayPal — https://www.paypal.com/donate/\?hosted_button_id\=YVENCBNCZWVPW

## License
MIT — see [LICENSE](./LICENSE).
