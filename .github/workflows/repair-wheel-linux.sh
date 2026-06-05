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

build_gap_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local gap_roots
  gap_roots="$(
    {
      find "$prefix" -path '*/lib/init.g' -print |
        sed 's#/lib/init\.g$##'
      find "$prefix" -path '*/pkg/*/PackageInfo.g' -print |
        sed 's#/pkg/[^/]*/PackageInfo\.g$##'
    } | sort -u | paste -sd ';' -
  )"
  local has_gap_init
  has_gap_init="no"
  while IFS= read -r gap_root; do
    if [ -f "$gap_root/lib/init.g" ]; then
      has_gap_init="yes"
      break
    fi
  done < <(printf '%s' "$gap_roots" | tr ';' '\n')
  if [ -z "$gap_roots" ] || [ "$has_gap_init" != "yes" ]; then
    echo "GAP root not found under $prefix; searched prefix contents:" >&2
    find "$prefix" -maxdepth 5 \( -name init.g -o -name PackageInfo.g -o -name sysinfo.gap \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-gap-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "GAP runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_GAP_ROOTS="$gap_roots" \
  SAGELITE_GAP_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_maxima_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local maxima_prefix
  maxima_prefix="$(
    find "$prefix" -path '*/share/maxima*/*/src' -type d -print |
      sed 's#/src$##' |
      sort -V |
      tail -1
  )"
  local maxima_fas="$prefix/lib/ecl/maxima.fas"
  local maxima_imagesdir="$prefix/lib/maxima/$(basename "$maxima_prefix")"
  local maxima_ecldir
  maxima_ecldir="$(
    find "$prefix/lib" -maxdepth 1 -type d -name 'ecl-*' -print |
      sort -V |
      tail -1
  )"
  if [ -z "$maxima_prefix" ] || [ ! -d "$maxima_prefix/share" ] ||
     [ ! -f "$maxima_fas" ] ||
     [ ! -f "$maxima_imagesdir/binary-ecl/maxima" ] ||
     [ -z "$maxima_ecldir" ]; then
    echo "Maxima runtime not found under $prefix; searched prefix contents:" >&2
    find "$prefix" -maxdepth 6 \
      \( -name maxima.fas -o -path '*/share/maxima*/*/src' \
         -o -path '*/binary-ecl/maxima' -o -name 'ecl-*' \) \
      -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-maxima-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "Maxima runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_MAXIMA_PREFIX="$maxima_prefix" \
  SAGELITE_MAXIMA_FAS="$maxima_fas" \
  SAGELITE_MAXIMA_IMAGESDIR="$maxima_imagesdir" \
  SAGELITE_MAXIMA_ECLDIR="$maxima_ecldir" \
  SAGELITE_MAXIMA_LIBDIR="$prefix/lib" \
  SAGELITE_MAXIMA_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_nauty_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local nauty_bindir="$prefix/bin"
  if [ ! -x "$nauty_bindir/geng" ] || [ ! -x "$nauty_bindir/genposetg" ]; then
    echo "nauty executables not found under $nauty_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name geng -o -name genposetg -o -name genktreeg \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-nauty-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "nauty runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_NAUTY_BINDIR="$nauty_bindir" \
  SAGELITE_NAUTY_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_pari_data_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac
  case "$AUDITWHEEL_PLAT" in
    manylinux*_x86_64) ;;
    *) return 0 ;;
  esac

  local pari_root="$prefix/share/pari"
  if [ ! -d "$pari_root" ] || ! find "$pari_root" -maxdepth 1 -type d \
      \( -name galdata -o -name elldata -o -name seadata -o -name galpol -o -name nftables \) \
      -print -quit | grep -q .; then
    echo "PARI data not found under $pari_root; searched prefix contents:" >&2
    find "$prefix/share" -maxdepth 3 \
      \( -name galdata -o -name elldata -o -name seadata -o -name galpol -o -name nftables \) \
      -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-pari-data"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "PARI data companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_PARI_DATA_DIR="$pari_root" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_singular_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac
  case "$AUDITWHEEL_PLAT" in
    manylinux*_x86_64) ;;
    *) return 0 ;;
  esac

  local singular_root="$prefix"
  if [ ! -f "$singular_root/share/singular/LIB/standard.lib" ] ||
     [ ! -f "$singular_root/share/singular/LIB/freegb.lib" ] ||
     ! find "$singular_root/lib" "$singular_root/libexec" -path '*/singular/MOD/freealgebra.so' -print -quit 2>/dev/null | grep -q .; then
    echo "Singular runtime data not found under $singular_root; searched prefix contents:" >&2
    find "$prefix/share" "$prefix/lib" "$prefix/libexec" -maxdepth 5 \
      \( -name standard.lib -o -name freegb.lib -o -name all.lib \) \
      -print >&2 || true
    find "$prefix/lib" "$prefix/libexec" -maxdepth 5 -name freealgebra.so -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-singular-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "Singular runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_SINGULAR_ROOT="$singular_root" \
  SAGELITE_SINGULAR_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

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
build_gap_runtime_companion
build_maxima_runtime_companion
build_nauty_runtime_companion
build_pari_data_companion
build_singular_runtime_companion
