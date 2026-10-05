#!/usr/bin/env bash
set -euo pipefail

printf '\nRAVEN v0.1 foundation bootstrap\n'
printf '%s\n' '--------------------------------'

if [[ ! -f README.md ]]; then
  echo 'ERROR: run this from the RAVEN repository root (README.md was not found).' >&2
  exit 1
fi

if [[ ! -d .git ]]; then
  echo 'ERROR: this directory is not a Git working tree.' >&2
  echo 'Clone the collaboration repository first, then re-run bootstrap.sh.' >&2
  exit 1
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 12):
    raise SystemExit(f"Python 3.12+ required; found {sys.version.split()[0]}")
print(f"Python {sys.version.split()[0]} OK")
PY

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev]'

printf '\n[1/4] Validating authorization/configuration gates...\n'
raventest validate-config configs/example.yaml

printf '\n[2/4] Running unit/integration tests...\n'
pytest -q

printf '\n[3/4] Running lint checks...\n'
ruff check .

printf '\n[4/4] Proving the local baseline pipeline...\n'
raventest run --target mock --suite baseline --config configs/example.yaml

printf '\nFoundation validation complete.\n'
printf '%s\n' 'Review the working tree before committing:'
git status --short
