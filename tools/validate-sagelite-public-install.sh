#!/usr/bin/env bash

set -Eeuo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "usage: $0 PYTHON OUTPUT_DIR [VERSION]" >&2
  exit 2
fi

python_bin="$1"
output_dir="$2"
version="${3:-10.9.post64}"
index_url="${SAGELITE_SIMPLE_INDEX_URL:-https://sagelite.sagemath.org/dev/simple/}"
script_dir="$(cd "$(dirname "$0")" && pwd)"
manifest_tool="${SAGELITE_RUNTIME_MANIFEST_TOOL:-${script_dir}/sagelite_runtime_manifest.py}"
venv="${output_dir}/venv"
temp_dir="${output_dir}/tmp"
log="${output_dir}/validation.log"

mkdir -p "${output_dir}"
if [ -e "${venv}" ]; then
  echo "refusing to reuse existing environment: ${venv}" >&2
  exit 2
fi
if [ ! -f "${manifest_tool}" ]; then
  echo "runtime manifest tool not found: ${manifest_tool}" >&2
  exit 2
fi

exec > >(tee "${log}") 2>&1

mkdir -p "${temp_dir}"
export TMPDIR="${temp_dir}"

finish() {
  status="$?"
  printf '%s\n' "${status}" > "${output_dir}/exit-code"
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "${output_dir}/finished-at.txt"
  rm -rf "${temp_dir}"
  if [ "${status}" -eq 0 ] && [ "${SAGELITE_KEEP_PUBLIC_INSTALL:-0}" != "1" ]; then
    rm -rf "${venv}"
  fi
  exit "${status}"
}
trap finish EXIT

date -u '+%Y-%m-%dT%H:%M:%SZ' > "${output_dir}/started-at.txt"
{
  echo "python=${python_bin}"
  echo "version=${version}"
  echo "index_url=${index_url}"
  echo "uname=$(uname -a)"
  "${python_bin}" -VV
} | tee "${output_dir}/metadata.txt"

"${python_bin}" -m venv "${venv}"
venv_python="${venv}/bin/python"
"${venv_python}" -m pip install --upgrade pip
"${venv_python}" -m pip install \
  --no-cache-dir \
  --only-binary=:all: \
  --retries 20 \
  --timeout 60 \
  --extra-index-url "${index_url}" \
  "sagelite[all-needed-extras]==${version}"
"${venv_python}" -m pip check | tee "${output_dir}/pip-check.log"
"${venv_python}" -m pip freeze --all > "${output_dir}/pip-freeze.txt"
"${venv_python}" -m pip show sagelite > "${output_dir}/sagelite-package.txt"
du -sk "${venv}" > "${output_dir}/installed-size-kib.txt"

clean_path="${venv}/bin:/usr/bin:/bin"
env \
  -u PYTHONPATH \
  -u LD_LIBRARY_PATH \
  -u DYLD_LIBRARY_PATH \
  -u SAGE_ROOT \
  -u SAGE_LOCAL \
  -u SAGE_SRC \
  -u SAGE_VENV \
  PATH="${clean_path}" \
  PYTHONNOUSERSITE=1 \
  "${venv_python}" "${manifest_tool}" collect \
    --label public-${version} \
    --output "${output_dir}/runtime-manifest.json"

"${venv_python}" "${manifest_tool}" compare \
  --reference "${output_dir}/runtime-manifest.json" \
  --candidate "${output_dir}/runtime-manifest.json" \
  --json-output "${output_dir}/runtime-isolation.json" \
  --md-output "${output_dir}/runtime-isolation.md"

"${venv_python}" - "${output_dir}/runtime-isolation.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
keys = [
    "candidate_executable_host_leaks",
    "candidate_python_path_leaks",
    "candidate_dependency_leaks",
    "candidate_source_path_leaks",
    "candidate_gap_host_leaks",
]
counts = {key: len(data.get(key, [])) for key in keys}
print("runtime isolation:", counts)
if any(counts.values()):
    raise SystemExit("runtime isolation leaks detected")
PY

env \
  -u PYTHONPATH \
  -u LD_LIBRARY_PATH \
  -u DYLD_LIBRARY_PATH \
  -u SAGE_ROOT \
  -u SAGE_LOCAL \
  -u SAGE_SRC \
  -u SAGE_VENV \
  PATH="${clean_path}" \
  PYTHONNOUSERSITE=1 \
  "${venv_python}" -m sage.cli.selftest | tee "${output_dir}/selftest.log"

env \
  -u PYTHONPATH \
  -u LD_LIBRARY_PATH \
  -u DYLD_LIBRARY_PATH \
  -u SAGE_ROOT \
  -u SAGE_LOCAL \
  -u SAGE_SRC \
  -u SAGE_VENV \
  PATH="${clean_path}" \
  PYTHONNOUSERSITE=1 \
  "${venv_python}" - "${version}" <<'PY' | tee "${output_dir}/smoke.log"
import sys
from importlib.metadata import version

from sage.all import GF, QQ, gap, matrix, polygen

x = polygen(QQ)
factorization = (x**4 - 1).factor()
determinant = matrix(GF(7), [[1, 2], [3, 4]]).det()
gap_value = gap.eval("2+2")
expected_version = sys.argv[1]
print("sagelite", version("sagelite"))
print("factorization", factorization)
print("determinant", determinant)
print("gap", gap_value)
assert version("sagelite") == expected_version
assert factorization.prod() == x**4 - 1
assert determinant == 5
assert gap_value == "4"
PY

echo "public install validation passed"
