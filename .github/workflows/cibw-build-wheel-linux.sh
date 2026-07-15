#!/usr/bin/env bash

set -euxo pipefail

python_bin="$1"
output_dir="$2"
source_dir="$3"
companion_output_dir="$(pwd)/sagelite-companion-wheelhouse"

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

rm -rf "${companion_output_dir}"
mkdir -p "${companion_output_dir}"

if ! "${python_bin}" -m cibuildwheel --output-dir "${output_dir}" "${source_dir}"; then
  dump_meson_logs
  exit 1
fi

shopt -s nullglob
companion_wheels=("${companion_output_dir}"/*.whl)
if [ "${#companion_wheels[@]}" -eq 0 ]; then
  echo "repair completed without producing companion wheels" >&2
  exit 1
fi
mkdir -p "${output_dir}"
mv "${companion_wheels[@]}" "${output_dir}/"
rm -rf "${companion_output_dir}"
