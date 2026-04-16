#!/usr/bin/env bash

set -euxo pipefail

python_bin="$1"
output_dir="$2"
source_dir="$3"

dump_meson_logs() {
  find "${source_dir}" -path '*/.mesonpy-*/meson-logs/meson-log.txt' -print0 | while IFS= read -r -d '' logfile; do
    echo "===== ${logfile} ====="
    cat "${logfile}"
  done
}

if ! "${python_bin}" -m cibuildwheel --output-dir "${output_dir}" "${source_dir}"; then
  dump_meson_logs
  exit 1
fi
