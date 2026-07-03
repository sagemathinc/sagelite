#!/usr/bin/env bash

set -euxo pipefail

export PATH="$(pwd)/build/bin:$PATH"
SPKGS="${SPKGS:-_bootstrap _prereq}"
TARGETS_PRE="${TARGETS_PRE:-gmp mpfr mpc mpfi openblas gsl libgd pari pari_elldata pari_galdata pari_galpol pari_nftables pari_seadata flint m4ri m4rie brial ecm frobby fflas_ffpack linbox gap gap_packages gap3 gfan giac singular ecl maxima fricas jmol kenzo lcalc eclib libbraiding libhomfly nauty palp 4ti2 rubiks symmetrica cliquer planarity qepcad glpk bliss coxeter3 mcqd meataxe sirocco tdlib glucose kissat graphviz dvipng poppler flatter imagemagick sympow topcom csdp benzene buckygen msolve fplll latte_int lrslib lie pdf2svg plantri tachyon tides}"
SAGE_PYTHON="${SAGE_PYTHON:-/opt/python/cp312-cp312/bin/python3}"
# Some Sage package names describe system tools and cannot be built as SPKGs.
system_spkgs=($SPKGS)
system_tool_targets=()
native_targets=()
for target in $TARGETS_PRE; do
  case "${target}" in
    graphviz|dvipng|flatter|imagemagick|pdf2svg|poppler)
      system_tool_targets+=("${target}")
      ;;
    *)
      native_targets+=("${target}")
      ;;
  esac
done
echo "System-package SPKGs: ${system_spkgs[*]}"
echo "System tool targets: ${system_tool_targets[*]:-(none)}"
echo "Native Sage targets: ${native_targets[*]}"
sage_python_version="$("${SAGE_PYTHON}" - <<'PY'
import sysconfig

print(sysconfig.get_python_version())
PY
)"
sage_site_packages="/host/sage-${AUDITWHEEL_PLAT}/lib/python${sage_python_version}/site-packages"
sage_prefix="/host/sage-${AUDITWHEEL_PLAT}"

cat > build/bin/cython <<EOF
#!/usr/bin/env bash
exec "${SAGE_PYTHON}" -m cython "\$@"
EOF
chmod +x build/bin/cython
ln -sf cython build/bin/cython3

env -u PIP_CONSTRAINT -u PYTHONPATH "${SAGE_PYTHON}" -m ensurepip --upgrade || true
env -u CYTHON -u PIP_CONSTRAINT -u PYTHONPATH "${SAGE_PYTHON}" -m pip install --upgrade \
  pip \
  setuptools \
  wheel \
  cython \
  'cysignals>=1.12.1'

echo "Installing bootstrap prerequisites inside cibuildwheel container"
(
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    $(sage-print-system-package-command debian --yes --no-install-recommends install $(sage-get-system-packages debian "${system_spkgs[@]}"))
) || (
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    $(sage-print-system-package-command fedora --yes --no-install-recommends install $(sage-get-system-packages fedora "${system_spkgs[@]}" | sed s/pkg-config/pkgconfig/) | sed 's/^dnf install -y /dnf install -y --setopt=install_weak_deps=False /')
) || (
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    $(sage-print-system-package-command alpine --yes --no-install-recommends install $(sage-get-system-packages alpine "${system_spkgs[@]}"))
) || (
  echo "No known package manager path succeeded" >&2
  exit 1
)

tool_packages_debian=(ccache curl)
tool_packages_fedora=(ccache curl)
tool_packages_alpine=(ccache curl)
for target in "${system_tool_targets[@]}"; do
  case "${target}" in
    graphviz)
      tool_packages_debian+=(graphviz)
      tool_packages_fedora+=(graphviz)
      tool_packages_alpine+=(graphviz)
      ;;
    dvipng)
      tool_packages_debian+=(dvipng)
      tool_packages_fedora+=(texlive-dvipng)
      tool_packages_alpine+=(texlive-dvipng)
      ;;
    flatter)
      tool_packages_debian+=(libeigen3-dev)
      tool_packages_fedora+=(eigen3-devel)
      tool_packages_alpine+=(eigen-dev)
      ;;
    imagemagick)
      tool_packages_debian+=(imagemagick)
      tool_packages_fedora+=(ImageMagick)
      tool_packages_alpine+=(imagemagick)
      ;;
    pdf2svg)
      tool_packages_debian+=(pdf2svg)
      tool_packages_fedora+=(git gcc pkgconf-pkg-config poppler-glib-devel cairo-devel glib2-devel)
      tool_packages_alpine+=(pdf2svg)
      ;;
    poppler)
      tool_packages_debian+=(poppler-utils)
      tool_packages_fedora+=(poppler-utils)
      tool_packages_alpine+=(poppler-utils)
      ;;
  esac
done

if command -v apt-get >/dev/null 2>&1; then
  echo "Installing build tool packages inside cibuildwheel container: ${tool_packages_debian[*]}"
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH apt-get update
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${tool_packages_debian[@]}"
elif command -v dnf >/dev/null 2>&1; then
  echo "Installing build tool packages inside cibuildwheel container: ${tool_packages_fedora[*]}"
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    dnf install -y --setopt=install_weak_deps=False "${tool_packages_fedora[@]}"
elif command -v yum >/dev/null 2>&1; then
  echo "Installing build tool packages inside cibuildwheel container: ${tool_packages_fedora[*]}"
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    yum install -y "${tool_packages_fedora[@]}"
elif command -v apk >/dev/null 2>&1; then
  echo "Installing build tool packages inside cibuildwheel container: ${tool_packages_alpine[*]}"
  env -u PYTHONPATH -u PIP_CONSTRAINT -u PIP_FIND_LINKS -u LD_LIBRARY_PATH \
    apk add --no-cache "${tool_packages_alpine[@]}"
else
  echo "No known package manager available for installing build tool packages" >&2
  exit 1
fi

build_pdf2svg_system_tool() {
  local install_prefix="$1"
  if command -v pdf2svg >/dev/null 2>&1; then
    return 0
  fi
  if [ -x "$install_prefix/bin/pdf2svg" ]; then
    return 0
  fi

  local build_root source_dir
  build_root="$(mktemp -d)"
  source_dir="$build_root/pdf2svg-src"
  git clone https://github.com/dawbarton/pdf2svg.git "$source_dir"
  git -C "$source_dir" checkout 2371ca32926354227f58ce6cab18a7bd54136252
  mkdir -p "$install_prefix/bin"
  cc -O2 -o "$install_prefix/bin/pdf2svg" "$source_dir/pdf2svg.c" \
    $(pkg-config --cflags --libs poppler-glib cairo)
  rm -rf "$build_root"
}

for target in "${system_tool_targets[@]}"; do
  case "${target}" in
    pdf2svg)
      build_pdf2svg_system_tool "$sage_prefix"
      ;;
  esac
done

mkdir -p "${CCACHE_DIR:?CCACHE_DIR must be set}"
ccache --version
ccache_binary="$(command -v ccache)"
cat > build/bin/ccache <<EOF
#!/usr/bin/env bash

set -e

if [ -n "\${LD_LIBRARY_PATH:-}" ]; then
  sanitized_ld_library_path=""
  old_ifs="\${IFS}"
  IFS=:
  for library_path in \${LD_LIBRARY_PATH}; do
    case "\${library_path}" in
      /host/sage-*/lib|/project/prefix/lib)
        continue
        ;;
    esac
    if [ -z "\${sanitized_ld_library_path}" ]; then
      sanitized_ld_library_path="\${library_path}"
    else
      sanitized_ld_library_path="\${sanitized_ld_library_path}:\${library_path}"
    fi
  done
  IFS="\${old_ifs}"
  export LD_LIBRARY_PATH="\${sanitized_ld_library_path}"
fi

exec "${ccache_binary}" "\$@"
EOF
chmod +x build/bin/ccache

export PYTHONPATH="${sage_site_packages}${PYTHONPATH:+:${PYTHONPATH}}"

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
  ./configure --disable-doc --enable-experimental-packages --enable-build-as-root --with-python="${SAGE_PYTHON}" --prefix="/host/sage-${AUDITWHEEL_PLAT}"
  cp config.status prefix/
fi

if [ -x "${sage_prefix}/bin/python3" ] && ! env -u PYTHONPATH "${sage_prefix}/bin/python3" -m pip --version >/dev/null 2>&1; then
  echo "Removing stale pip install markers from ${sage_prefix}"
  rm -f "${sage_prefix}"/var/lib/sage/installed/pip-*
fi

python_module_available() {
  (
    cd /
    PYTHONPATH="${sage_site_packages}" "${sage_prefix}/bin/python3" - "$1" <<'PY'
import importlib.util
import sys

spec = importlib.util.find_spec(sys.argv[1])
if spec is None or spec.origin in (None, "namespace"):
    raise SystemExit(1)
PY
  )
}

if [ -x "${sage_prefix}/bin/python3" ]; then
  while IFS=: read -r spkg module; do
    if ! python_module_available "${module}" >/dev/null 2>&1; then
      echo "Removing stale ${spkg} install markers from ${sage_prefix}"
      rm -f "${sage_prefix}"/var/lib/sage/installed/"${spkg}"-*
    fi
  done <<'EOF'
flit_core:flit_core
meson:mesonbuild
meson_python:mesonpy
ninja_build:ninja
pyproject_metadata:pyproject_metadata
python_build:build
setuptools:setuptools
wheel:wheel
cypari:cypari2
cysignals:cysignals
cython:Cython
gmpy2:gmpy2
jupyter_core:jupyter_core
memory_allocator:memory_allocator
numpy:numpy
pkgconfig:pkgconfig
pplpy:ppl
requests:requests
typing_extensions:typing_extensions
EOF
fi

# Python SPKG builds in TARGETS_PRE inherit PIP_CONSTRAINT from CIBW_ENVIRONMENT.
# Prepare the constraints file before make starts so build isolation can use it.
printf 'sage_setup @ file://%s/pkgs/sage-setup\n' "$(pwd)" > constraints.txt
echo "Prepared constraints.txt:"
cat constraints.txt

if [ "${#native_targets[@]}" -gt 0 ]; then
  MAKE="make -j6" make V=0 "${native_targets[@]}"
fi
