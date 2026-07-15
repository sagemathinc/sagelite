#!/usr/bin/env bash

set -euxo pipefail

python - <<'PY'
import sys

if sys.version_info.releaselevel != "final":
    raise SystemExit(
        "refusing to build a release wheel with a prerelease Python: "
        f"{sys.version.split()[0]}"
    )
PY

python -m pip install --upgrade \
  build \
  meson \
  meson-python \
  ninja \
  'cython>=3.1.0' \
  'cysignals>=1.12.1' \
  'gmpy2>=2.1.5' \
  jinja2 \
  memory_allocator \
  'numpy>=2.2.4' \
  'cypari2>=2.2.1'

if command -v ccache >/dev/null 2>&1; then
  echo "Compiler cache:"
  ccache --version
  ccache --show-config | grep -E '^(cache_dir|max_size|compiler_check|base_dir|hash_dir)' || true
  ccache -z || true
fi

echo "Build Python:"
which python
python --version

echo "Configured CYTHON: ${CYTHON:-<unset>}"
if [ -n "${CYTHON:-}" ]; then
  "${CYTHON}" --version
else
  which cython
  cython --version
fi

tmpdir="$(mktemp -d)"
trap 'rm -rf "${tmpdir}"' EXIT
cat > "${tmpdir}/sanity.pyx" <<'EOF'
def answer():
    return 42
EOF

if [ -n "${CYTHON:-}" ]; then
  "${CYTHON}" "${tmpdir}/sanity.pyx"
else
  cython "${tmpdir}/sanity.pyx"
fi

python_includes="$(python - <<'PY'
import sysconfig

seen = set()
for key in ("INCLUDEPY", "CONFINCLUDEPY"):
    path = sysconfig.get_config_var(key)
    if path and path not in seen:
        seen.add(path)
        print(f"-I{path}")
PY
)"
ext_suffix="$(python - <<'PY'
import sysconfig
print(sysconfig.get_config_var("EXT_SUFFIX") or ".so")
PY
)"
cc ${python_includes} -fPIC -c "${tmpdir}/sanity.c" -o "${tmpdir}/sanity.o"
cc -shared "${tmpdir}/sanity.o" -o "${tmpdir}/sanity${ext_suffix}"

echo "Build environment snapshot:"
env | sort | grep -E '^(CYTHON|PATH|LD_LIBRARY_PATH|LIBRARY_PATH|CPATH|PKG_CONFIG_PATH|CMAKE_PREFIX_PATH|PIP_CONSTRAINT|PIP_FIND_LINKS)=' || true

meson_probe_dir="$(mktemp -d)"
trap 'rm -rf "${tmpdir}" "${meson_probe_dir}"' EXIT
cat > "${meson_probe_dir}/meson.build" <<'EOF'
project('cython-probe', 'cython')
EOF

if ! meson setup "${meson_probe_dir}/build" "${meson_probe_dir}/" --wipe; then
  find "${meson_probe_dir}" -path '*/meson-logs/meson-log.txt' -print0 | while IFS= read -r -d '' logfile; do
    echo "===== ${logfile} ====="
    cat "${logfile}"
  done
  exit 1
fi
