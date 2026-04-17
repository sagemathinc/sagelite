#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 RAW_WHEEL DEST_DIR" >&2
  exit 2
fi

raw_wheel="$1"
dest_dir="$2"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

if [ -z "${AUDITWHEEL_PLAT:-}" ]; then
  echo "AUDITWHEEL_PLAT is not set" >&2
  exit 1
fi

prefix="/host/sage-${AUDITWHEEL_PLAT}"
if [ ! -d "$prefix" ]; then
  echo "bootstrap prefix not found: $prefix" >&2
  exit 1
fi

python_bin="${PYTHON:-python3}"
vendored_site="$tmpdir/cypari-site"

# Build cypari2 from source against the same PARI that Sage linked against.
# Installing the prebuilt wheel would reintroduce a second bundled libpari.
env -u PIP_CONSTRAINT "$python_bin" -m pip install \
  --no-deps \
  --no-binary cypari2 \
  --target "$vendored_site" \
  cypari2

"$python_bin" .github/workflows/vendor-cypari-wheel.py \
  --wheel "$raw_wheel" \
  --prefix "$vendored_site" \
  --out "$tmpdir/${raw_wheel##*/}"

if command -v ccache >/dev/null 2>&1; then
  echo "Compiler cache stats after wheel build:"
  ccache -s || true
fi

auditwheel repair -w "$dest_dir" "$tmpdir/${raw_wheel##*/}"
