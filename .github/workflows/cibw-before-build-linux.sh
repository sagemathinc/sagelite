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
