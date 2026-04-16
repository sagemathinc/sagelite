#!/usr/bin/env bash

set -euxo pipefail

python_bin="$1"
output_dir="$2"
source_dir="$3"

dump_meson_logs() {
  local source_name found=0 root logfile

  source_name="$(basename "${source_dir}")"
  for root in "${source_dir}" "/project/unpacked/${source_name}" "/project"; do
    [ -d "${root}" ] || continue
    while IFS= read -r -d '' logfile; do
      found=1
      echo "===== ${logfile} ====="
      cat "${logfile}"
    done < <(find "${root}" -path '*/.mesonpy-*/meson-logs/meson-log.txt' -print0)
  done

  if [ "${found}" -eq 0 ]; then
    echo "No meson-log.txt files found under ${source_dir} or /project"
  fi
}

if ! "${python_bin}" -m cibuildwheel --output-dir "${output_dir}" "${source_dir}"; then
  dump_meson_logs
  exit 1
fi
