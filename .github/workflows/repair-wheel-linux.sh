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

pruned_dir="$tmpdir/pruned-wheel"
packed_dir="$tmpdir/packed-wheel"

# Cython sources and declarations are useful for source builds but are not
# needed at runtime.  Dropping them buys several MB of PyPI size headroom.
env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade wheel
env -u PIP_CONSTRAINT "$python_bin" -m wheel unpack "$tmpdir/${raw_wheel##*/}" -d "$pruned_dir"
find "$pruned_dir" -type f \( -name '*.pyx' -o -name '*.pxd' -o -name '*.pxi' \) -delete
mkdir -p "$packed_dir"
env -u PIP_CONSTRAINT "$python_bin" -m wheel pack "$pruned_dir"/* -d "$packed_dir"
repaired_input="$(find "$packed_dir" -name '*.whl' -print -quit)"
if [ -z "$repaired_input" ]; then
  echo "failed to repack pruned wheel" >&2
  exit 1
fi

if command -v ccache >/dev/null 2>&1; then
  echo "Compiler cache stats after wheel build:"
  ccache -s || true
fi

auditwheel repair -w "$dest_dir" "$repaired_input"
