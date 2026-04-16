#!/usr/bin/env bash

set -euxo pipefail

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

python_includes="$(python-config --includes)"
ext_suffix="$(python - <<'PY'
import sysconfig
print(sysconfig.get_config_var("EXT_SUFFIX") or ".so")
PY
)"
cc ${python_includes} -fPIC -c "${tmpdir}/sanity.c" -o "${tmpdir}/sanity.o"
cc -shared "${tmpdir}/sanity.o" -o "${tmpdir}/sanity${ext_suffix}"

echo "Build environment snapshot:"
env | sort | grep -E '^(CYTHON|PATH|LD_LIBRARY_PATH|LIBRARY_PATH|CPATH|PKG_CONFIG_PATH|CMAKE_PREFIX_PATH|PIP_CONSTRAINT|PIP_FIND_LINKS)=' || true
