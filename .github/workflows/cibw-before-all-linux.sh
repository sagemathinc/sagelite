#!/usr/bin/env bash

set -euxo pipefail

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

if cp "/host/sage-${AUDITWHEEL_PLAT}/config.status" . 2>/dev/null; then
  chmod +x config.status
fi

if [ -x ./config.status ]; then
  ./config.status
else
  ./configure --enable-build-as-root --prefix="/host/sage-${AUDITWHEEL_PLAT}"
  cp config.status prefix/
fi

MAKE="make -j6" make V=0 ${TARGETS_PRE}

printf 'sage_setup @ file://%s/pkgs/sage-setup\n' "$(pwd)" > constraints.txt
echo "Prepared constraints.txt:"
cat constraints.txt
