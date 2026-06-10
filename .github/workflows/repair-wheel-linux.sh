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

build_gap3_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local gap3_root="$prefix/gap3/latest/gap3"
  if [ ! -x "$gap3_root/bin/gap.sh" ] ||
     [ ! -f "$gap3_root/lib/init.g" ]; then
    echo "GAP3 runtime not found under $gap3_root; searched prefix contents:" >&2
    find "$prefix" -maxdepth 6 \( -name gap.sh -o -name init.g \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-gap3-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "GAP3 runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_GAP3_ROOT="$gap3_root" \
  SAGELITE_GAP3_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_gfan_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local gfan_bindir="$prefix/bin"
  if [ ! -x "$gfan_bindir/gfan" ] || [ ! -x "$gfan_bindir/gfan_bases" ]; then
    echo "gfan executables not found under $gfan_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name gfan -o -name gfan_bases -o -name gfan_groebnercone \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-gfan-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "gfan runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_GFAN_BINDIR="$gfan_bindir" \
  SAGELITE_GFAN_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_ecm_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local ecm_bindir="$prefix/bin"
  if [ ! -x "$ecm_bindir/ecm" ] && [ ! -x "$ecm_bindir/gmp-ecm" ]; then
    echo "ecm executable not found under $ecm_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name ecm -o -name gmp-ecm \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-ecm-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "ECM runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_ECM_BINDIR="$ecm_bindir" \
  SAGELITE_ECM_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_frobby_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local frobby_bindir="$prefix/bin"
  if [ ! -x "$frobby_bindir/frobby" ]; then
    echo "frobby executable not found under $frobby_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name frobby -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-frobby-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "Frobby runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_FROBBY_BINDIR="$frobby_bindir" \
  SAGELITE_FROBBY_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_mwrank_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local mwrank_bindir="$prefix/bin"
  if [ ! -x "$mwrank_bindir/mwrank" ]; then
    echo "mwrank executable not found under $mwrank_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name mwrank -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-mwrank-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "mwrank runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_MWRANK_BINDIR="$mwrank_bindir" \
  SAGELITE_MWRANK_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_sympow_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local sympow_bindir="$prefix/bin"
  if [ ! -x "$sympow_bindir/sympow" ]; then
    echo "sympow executable not found under $sympow_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name sympow -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-sympow-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "SYMPOW runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_SYMPOW_BINDIR="$sympow_bindir" \
  SAGELITE_SYMPOW_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_topcom_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local topcom_bindir="$prefix/bin"
  if { [ ! -x "$topcom_bindir/points2allfinetriangs" ] && [ ! -x "$topcom_bindir/topcom-points2allfinetriangs" ]; } ||
     { [ ! -x "$topcom_bindir/points2placingtriang" ] && [ ! -x "$topcom_bindir/topcom-points2placingtriang" ]; }; then
    echo "TOPCOM executables not found under $topcom_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name points2allfinetriangs -o -name topcom-points2allfinetriangs -o -name points2placingtriang -o -name topcom-points2placingtriang -o -name chiro2alltriangs -o -name topcom-chiro2alltriangs \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-topcom-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "TOPCOM runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_TOPCOM_BINDIR="$topcom_bindir" \
  SAGELITE_TOPCOM_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_four_ti_2_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local four_ti_2_bindir="$prefix/bin"
  if { [ ! -x "$four_ti_2_bindir/hilbert" ] && [ ! -x "$four_ti_2_bindir/4ti2-hilbert" ]; } ||
     { [ ! -x "$four_ti_2_bindir/zsolve" ] && [ ! -x "$four_ti_2_bindir/4ti2-zsolve" ]; } ||
     { [ ! -x "$four_ti_2_bindir/qsolve" ] && [ ! -x "$four_ti_2_bindir/4ti2-qsolve" ]; } ||
     { [ ! -x "$four_ti_2_bindir/groebner" ] && [ ! -x "$four_ti_2_bindir/4ti2-groebner" ]; }; then
    echo "4ti2 executables not found under $four_ti_2_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name hilbert -o -name 4ti2-hilbert -o -name zsolve -o -name 4ti2-zsolve -o -name qsolve -o -name 4ti2-qsolve -o -name groebner -o -name 4ti2-groebner \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-4ti2-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "4ti2 runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_4TI2_BINDIR="$four_ti_2_bindir" \
  SAGELITE_4TI2_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_cddlib_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local cddlib_bindir="$prefix/bin"
  if [ ! -x "$cddlib_bindir/cddexec" ] ||
     [ ! -x "$cddlib_bindir/cddexec_gmp" ] ||
     [ ! -x "$cddlib_bindir/redcheck_gmp" ] ||
     [ ! -x "$cddlib_bindir/scdd" ] ||
     [ ! -x "$cddlib_bindir/scdd_gmp" ]; then
    echo "cddlib executables not found under $cddlib_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name cddexec -o -name cddexec_gmp -o -name redcheck_gmp -o -name scdd -o -name scdd_gmp \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-cddlib-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "cddlib runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_CDDLIB_BINDIR="$cddlib_bindir" \
  SAGELITE_CDDLIB_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_csdp_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local csdp_bindir="$prefix/bin"
  if [ ! -x "$csdp_bindir/theta" ]; then
    echo "CSDP theta executable not found under $csdp_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name theta -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-csdp-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "CSDP runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_CSDP_BINDIR="$csdp_bindir" \
  SAGELITE_CSDP_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_benzene_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local benzene_bindir="$prefix/bin"
  if [ ! -x "$benzene_bindir/benzene" ]; then
    echo "benzene executable not found under $benzene_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name benzene -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-benzene-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "benzene runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_BENZENE_BINDIR="$benzene_bindir" \
  SAGELITE_BENZENE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_buckygen_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local buckygen_bindir="$prefix/bin"
  if [ ! -x "$buckygen_bindir/buckygen" ]; then
    echo "buckygen executable not found under $buckygen_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name buckygen -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-buckygen-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "buckygen runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_BUCKYGEN_BINDIR="$buckygen_bindir" \
  SAGELITE_BUCKYGEN_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_glucose_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local glucose_bindir="$prefix/bin"
  if [ ! -x "$glucose_bindir/glucose" ] ||
     [ ! -x "$glucose_bindir/glucose-syrup" ]; then
    echo "Glucose executables not found under $glucose_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name glucose -o -name glucose-syrup \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-glucose-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "Glucose runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_GLUCOSE_BINDIR="$glucose_bindir" \
  SAGELITE_GLUCOSE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_kissat_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local kissat_bindir="$prefix/bin"
  if [ ! -x "$kissat_bindir/kissat" ]; then
    echo "kissat executable not found under $kissat_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name kissat -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-kissat-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "kissat runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_KISSAT_BINDIR="$kissat_bindir" \
  SAGELITE_KISSAT_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_msolve_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local msolve_bindir="$prefix/bin"
  if [ ! -x "$msolve_bindir/msolve" ]; then
    echo "msolve executable not found under $msolve_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name msolve -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-msolve-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "msolve runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_MSOLVE_BINDIR="$msolve_bindir" \
  SAGELITE_MSOLVE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_flatter_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local flatter_bindir="$prefix/bin"
  if [ ! -x "$flatter_bindir/flatter" ]; then
    echo "flatter executable not found under $flatter_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name flatter -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-flatter-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "flatter runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_FLATTER_BINDIR="$flatter_bindir" \
  SAGELITE_FLATTER_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_latte_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local latte_bindir="$prefix/bin"
  if [ ! -x "$latte_bindir/count" ] ||
     [ ! -x "$latte_bindir/integrate" ]; then
    echo "LattE executables not found under $latte_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name count -o -name integrate \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-latte-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "LattE runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_LATTE_BINDIR="$latte_bindir" \
  SAGELITE_LATTE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_lcalc_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local lcalc_bindir="$prefix/bin"
  if [ ! -x "$lcalc_bindir/lcalc" ]; then
    echo "lcalc executable not found under $lcalc_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name lcalc -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-lcalc-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "lcalc runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_LCALC_BINDIR="$lcalc_bindir" \
  SAGELITE_LCALC_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_lrslib_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local lrslib_bindir="$prefix/bin"
  if [ ! -x "$lrslib_bindir/lrs" ] ||
     [ ! -x "$lrslib_bindir/lrsnash" ]; then
    echo "lrslib executables not found under $lrslib_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name lrs -o -name lrsnash \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-lrslib-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "lrslib runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_LRSLIB_BINDIR="$lrslib_bindir" \
  SAGELITE_LRSLIB_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_lie_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local lie_bindir="$prefix/bin"
  local lie_info_dir="$prefix/lib/LiE"
  if [ ! -x "$lie_bindir/lie" ] ||
     [ ! -f "$lie_info_dir/INFO.0" ] ||
     [ ! -f "$lie_info_dir/INFO.3" ]; then
    echo "LiE runtime not found under $prefix; searched prefix contents:" >&2
    find "$prefix" -maxdepth 5 \( -name lie -o -name INFO.0 -o -name INFO.3 \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-lie-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "LiE runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_LIE_BINDIR="$lie_bindir" \
  SAGELITE_LIE_INFO_DIR="$lie_info_dir" \
  SAGELITE_LIE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_plantri_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local plantri_bindir="$prefix/bin"
  if [ ! -x "$plantri_bindir/plantri" ]; then
    echo "plantri executable not found under $plantri_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name plantri -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-plantri-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "plantri runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_PLANTRI_BINDIR="$plantri_bindir" \
  SAGELITE_PLANTRI_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_planarity_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local planarity_bindir="$prefix/bin"
  if [ ! -x "$planarity_bindir/planarity" ]; then
    echo "planarity executable not found under $planarity_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name planarity -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-planarity-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "planarity runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_PLANARITY_BINDIR="$planarity_bindir" \
  SAGELITE_PLANARITY_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_qepcad_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local qepcad_root="$prefix"
  if [ ! -x "$qepcad_root/bin/qepcad" ] ||
     [ ! -f "$qepcad_root/share/qepcad/qepcad.help" ] ||
     [ ! -f "$qepcad_root/etc/default.qepcadrc" ]; then
    echo "QEPCAD runtime not found under $qepcad_root; searched prefix contents:" >&2
    find "$prefix" -maxdepth 5 \( -name qepcad -o -name qepcad.help -o -name default.qepcadrc \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-qepcad-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "QEPCAD runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_QEPCAD_ROOT="$qepcad_root" \
  SAGELITE_QEPCAD_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_tachyon_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local tachyon_bindir="$prefix/bin"
  if [ ! -x "$tachyon_bindir/tachyon" ]; then
    echo "tachyon executable not found under $tachyon_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 -name tachyon -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-tachyon-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "tachyon runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_TACHYON_BINDIR="$tachyon_bindir" \
  SAGELITE_TACHYON_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
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

  local repaired_sagelite_wheel ecl_soname
  repaired_sagelite_wheel="$(find "$dest_dir" -maxdepth 1 -type f -name 'sagelite-*.whl' -print -quit)"
  if [ -z "$repaired_sagelite_wheel" ]; then
    echo "repaired sagelite wheel not found in $dest_dir" >&2
    exit 1
  fi
  ecl_soname="$(
    "$python_bin" - "$repaired_sagelite_wheel" <<'PY'
import os
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1]) as wheel:
    matches = sorted(
        os.path.basename(name)
        for name in wheel.namelist()
        if name.startswith("sagelite.libs/libecl") and name.endswith(".so.24.5.10")
    )
if len(matches) != 1:
    raise SystemExit(f"expected one bundled libecl, found {matches}")
print(matches[0])
PY
  )"

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_MAXIMA_PREFIX="$maxima_prefix" \
  SAGELITE_MAXIMA_FAS="$maxima_fas" \
  SAGELITE_MAXIMA_IMAGESDIR="$maxima_imagesdir" \
  SAGELITE_MAXIMA_ECLDIR="$maxima_ecldir" \
  SAGELITE_MAXIMA_LIBDIR="$prefix/lib" \
  SAGELITE_MAXIMA_ECL_SONAME="$ecl_soname" \
  SAGELITE_MAXIMA_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_meataxe_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac
  case "$AUDITWHEEL_PLAT" in
    manylinux*_x86_64) ;;
    *) return 0 ;;
  esac

  local meataxe_dir="$prefix/share/meataxe"
  local zcv="$prefix/bin/zcv"
  if [ ! -f "$meataxe_dir/p009.zzz" ] && [ ! -x "$zcv" ]; then
    echo "MeatAxe tables and zcv were not found under $prefix; searched prefix contents:" >&2
    find "$prefix" -maxdepth 5 \( -name 'p009.zzz' -o -name zcv \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-meataxe-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "MeatAxe runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  if [ -f "$meataxe_dir/p009.zzz" ]; then
    SAGELITE_MEATAXE_DIR="$meataxe_dir" \
    SAGELITE_MEATAXE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
      env -u PIP_CONSTRAINT "$python_bin" -m build \
        --wheel \
        --no-isolation \
        --outdir "$output_dir" \
        "$companion_dir"
  else
    SAGELITE_MEATAXE_ZCV="$zcv" \
    SAGELITE_MEATAXE_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
      env -u PIP_CONSTRAINT "$python_bin" -m build \
        --wheel \
        --no-isolation \
        --outdir "$output_dir" \
        "$companion_dir"
  fi
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

build_rubiks_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local rubiks_bindir="$prefix/bin"
  if [ ! -x "$rubiks_bindir/cu2" ] || [ ! -x "$rubiks_bindir/cubex" ] ||
     [ ! -x "$rubiks_bindir/dikcube" ] || [ ! -x "$rubiks_bindir/mcube" ] ||
     [ ! -x "$rubiks_bindir/optimal" ] || [ ! -x "$rubiks_bindir/size222" ]; then
    echo "Rubiks executables not found under $rubiks_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name cu2 -o -name cubex -o -name dikcube -o -name mcube -o -name optimal -o -name size222 \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-rubiks-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "Rubiks runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_RUBIKS_BINDIR="$rubiks_bindir" \
  SAGELITE_RUBIKS_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
    env -u PIP_CONSTRAINT "$python_bin" -m build \
      --wheel \
      --no-isolation \
      --outdir "$output_dir" \
      "$companion_dir"
  ls -lh "$output_dir"
}

build_palp_runtime_companion() {
  case "$(basename "$raw_wheel")" in
    *-cp312-cp312-*) ;;
    *) return 0 ;;
  esac

  local palp_bindir="$prefix/bin"
  if [ ! -x "$palp_bindir/poly.x" ] || [ ! -x "$palp_bindir/nef.x" ]; then
    echo "PALP executables not found under $palp_bindir; searched prefix contents:" >&2
    find "$prefix" -maxdepth 4 \( -name 'poly.x' -o -name 'nef.x' -o -name 'class.x' -o -name 'cws.x' \) -print >&2 || true
    exit 1
  fi

  local project_dir="/project"
  local companion_dir="$project_dir/companion-packages/sagelite-palp-runtime"
  local output_dir="$dest_dir"
  if [ ! -d "$companion_dir" ]; then
    echo "PALP runtime companion package not found: $companion_dir" >&2
    exit 1
  fi

  env -u PIP_CONSTRAINT "$python_bin" -m pip install --upgrade build setuptools wheel
  mkdir -p "$output_dir"
  SAGELITE_PALP_BINDIR="$palp_bindir" \
  SAGELITE_PALP_RUNTIME_PLAT_NAME="$AUDITWHEEL_PLAT" \
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
     ! find "$singular_root/lib" "$singular_root/libexec" -ipath '*/singular/MOD/freealgebra.so' -print -quit 2>/dev/null | grep -q .; then
    echo "Singular runtime data not found under $singular_root; searched prefix contents:" >&2
    find "$prefix/share" "$prefix/lib" "$prefix/libexec" -maxdepth 5 \
      \( -name standard.lib -o -name freegb.lib -o -name all.lib \) \
      -print >&2 || true
    find "$prefix/lib" "$prefix/libexec" -maxdepth 5 -iname freealgebra.so -print >&2 || true
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
build_gap3_runtime_companion
build_gfan_runtime_companion
build_ecm_runtime_companion
build_frobby_runtime_companion
build_mwrank_runtime_companion
build_sympow_runtime_companion
build_topcom_runtime_companion
build_four_ti_2_runtime_companion
build_cddlib_runtime_companion
build_csdp_runtime_companion
build_benzene_runtime_companion
build_buckygen_runtime_companion
build_glucose_runtime_companion
build_kissat_runtime_companion
build_msolve_runtime_companion
build_flatter_runtime_companion
build_latte_runtime_companion
build_lcalc_runtime_companion
build_lrslib_runtime_companion
build_lie_runtime_companion
build_planarity_runtime_companion
build_plantri_runtime_companion
build_qepcad_runtime_companion
build_tachyon_runtime_companion
build_maxima_runtime_companion
build_meataxe_runtime_companion
build_nauty_runtime_companion
build_rubiks_runtime_companion
build_palp_runtime_companion
build_pari_data_companion
build_singular_runtime_companion
