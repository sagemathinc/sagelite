#!/usr/bin/env bash

set -euxo pipefail

export PATH="$(pwd)/build/bin:$PATH"
SPKGS="${SPKGS:-_bootstrap _prereq}"
TARGETS_PRE="${TARGETS_PRE:-gmp mpfr mpc mpfi openblas gsl libgd pari flint m4ri m4rie brial ecm fflas_ffpack linbox gap gap_packages singular ecl maxima lcalc eclib libbraiding libhomfly nauty symmetrica cliquer planarity glpk bliss coxeter3 mcqd meataxe sirocco tdlib}"
SAGE_PYTHON="${SAGE_PYTHON:-/opt/python/cp312-cp312/bin/python3}"
sage_python_version="$("${SAGE_PYTHON}" - <<'PY'
import sysconfig

print(sysconfig.get_python_version())
PY
)"
sage_site_packages="/host/sage-${AUDITWHEEL_PLAT}/lib/python${sage_python_version}/site-packages"
export PYTHONPATH="${sage_site_packages}${PYTHONPATH:+:${PYTHONPATH}}"

cat > build/bin/cython <<EOF
#!/usr/bin/env bash
exec "${SAGE_PYTHON}" -m cython "\$@"
EOF
chmod +x build/bin/cython
ln -sf cython build/bin/cython3

env -u PIP_CONSTRAINT "${SAGE_PYTHON}" -m ensurepip --upgrade || true
env -u PIP_CONSTRAINT "${SAGE_PYTHON}" -m pip install --upgrade \
  pip \
  setuptools \
  wheel \
  cython \
  'cysignals>=1.12.1'

echo "Installing bootstrap prerequisites inside cibuildwheel container"
(
  $(sage-print-system-package-command debian --yes --no-install-recommends install $(sage-get-system-packages debian $SPKGS))
) || (
  $(sage-print-system-package-command fedora --yes --no-install-recommends install $(sage-get-system-packages fedora $SPKGS | sed s/pkg-config/pkgconfig/))
) || (
  $(sage-print-system-package-command alpine --yes --no-install-recommends install $(sage-get-system-packages alpine $SPKGS))
) || (
  echo "No known package manager path succeeded" >&2
  exit 1
)

echo "Installing ccache inside cibuildwheel container"
if command -v apt-get >/dev/null 2>&1; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y ccache
elif command -v dnf >/dev/null 2>&1; then
  dnf install -y ccache
elif command -v yum >/dev/null 2>&1; then
  yum install -y ccache
elif command -v apk >/dev/null 2>&1; then
  apk add --no-cache ccache
else
  echo "No known package manager available for installing ccache" >&2
  exit 1
fi

mkdir -p "${CCACHE_DIR:?CCACHE_DIR must be set}"
ccache --version

# fflas-ffpack autotuning can throw FFPACK::CharpolyFailed in CI.
# The installed library works with default thresholds; avoid making wheel
# builds depend on a benchmarking pass.
export SAGE_FFLAS_FFPACK_SKIP_AUTOTUNE=yes

if cp "/host/sage-${AUDITWHEEL_PLAT}/config.status" . 2>/dev/null; then
  chmod +x config.status
fi

if [ -x ./config.status ]; then
  ./config.status
else
  ./configure --disable-doc --enable-build-as-root --with-python="${SAGE_PYTHON}" --prefix="/host/sage-${AUDITWHEEL_PLAT}"
  cp config.status prefix/
fi

sage_prefix="/host/sage-${AUDITWHEEL_PLAT}"
if [ -x "${sage_prefix}/bin/python3" ] && ! "${sage_prefix}/bin/python3" -m pip --version >/dev/null 2>&1; then
  echo "Removing stale pip install markers from ${sage_prefix}"
  rm -f "${sage_prefix}"/var/lib/sage/installed/pip-*
fi

# Python SPKG builds in TARGETS_PRE inherit PIP_CONSTRAINT from CIBW_ENVIRONMENT.
# Prepare the constraints file before make starts so build isolation can use it.
printf 'sage_setup @ file://%s/pkgs/sage-setup\n' "$(pwd)" > constraints.txt
echo "Prepared constraints.txt:"
cat constraints.txt

MAKE="make -j6" make V=0 ${TARGETS_PRE}
