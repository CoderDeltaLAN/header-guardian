#!/usr/bin/env zsh
mkdir -p "$PWD/.logs"
LOG="$PWD/.logs/preflight.log"; : > "$LOG"
r() { print -r -- "\n$ $*" | tee -a "$LOG"; eval "$*" 2>&1 | tee -a "$LOG"; }
python3 -m venv .venv && . .venv/bin/activate
r "python -m pip install -U pip wheel build"
r "pip install -U ruff black mypy pytest"
r "pip install -e ."
r "ruff check ."
r "ruff format --check ."
r "black --check ."
r "pytest -q"
r "mypy ."
r "python -m build"
deactivate
print -r -- "\nLog completo: $LOG"
