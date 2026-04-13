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

"$python_bin" .github/workflows/vendor-cypari-wheel.py \
  --wheel "$raw_wheel" \
  --prefix "$prefix" \
  --out "$tmpdir/${raw_wheel##*/}"

auditwheel repair -w "$dest_dir" "$tmpdir/${raw_wheel##*/}"
