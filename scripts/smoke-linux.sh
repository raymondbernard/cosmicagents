#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-}

if [ -z "$PYTHON_BIN" ]; then
  if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
    PYTHON_BIN="$VIRTUAL_ENV/bin/python"
  elif [ -x "$ROOT_DIR/.venv/bin/python" ]; then
    PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
  elif [ -x "$ROOT_DIR/.venv/Scripts/python.exe" ]; then
    PYTHON_BIN="$ROOT_DIR/.venv/Scripts/python.exe"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  else
    echo "python3 is required" >&2
    exit 127
  fi
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m pytest -q tests/cli/test_entrypoints.py
