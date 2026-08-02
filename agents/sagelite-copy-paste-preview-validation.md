# Sagelite Copy-Paste Preview Validation

This records fresh installs using the public developer-preview command shape
from `SAGELITE.md`:

```bash
python3.12 -m venv sagelite-test
. sagelite-test/bin/activate
python -m pip install --upgrade pip
python -m pip install --extra-index-url https://sagelite.sagemath.org/dev/simple/ "sagelite==10.9.post64"
python -c "from sage.all import *; x = polygen(QQ); print((x**4 - 1).factor()); print(gap.eval('2+2'))"
```

## Current Release-Gate Result

The `10.9.post64` preview was also tested with the stronger binary-only
release-gate install:

```bash
tools/validate-sagelite-public-install.sh python3.14 /bulk/output/path
```

That installs `sagelite[all-needed-extras]==10.9.post64` into a fresh virtual
environment directly from the public index, runs `pip check`, collects and
self-compares a clean-environment runtime manifest, rejects any of the five
runtime leak classes, runs all packaged selftests, and exercises
factorization, matrix arithmetic, and GAP. Results for all nine supported
platform/Python combinations are recorded below.

| Platform | Python | Installed KiB | Result | Durable evidence |
|---|---:|---:|---|---|
| Linux `x86_64` | 3.12 | 21,699,472 | pass | `/mnt/cocalc-scratch/sagelite-public-validation-20260802/linux-x86_64-cp312` |
| Linux `x86_64` | 3.13 | 21,688,044 | pass | `/mnt/cocalc-scratch/sagelite-public-validation-20260802/linux-x86_64-cp313` |
| Linux `x86_64` | 3.14 | 21,685,624 | pass | `/mnt/cocalc-scratch/sagelite-public-validation-20260802/linux-x86_64-cp314` |
| Linux `aarch64` | 3.12 | 21,886,860 | pass | `/home/sage.guest/sagelite-public-validation-20260802/linux-aarch64-cp312` |
| Linux `aarch64` | 3.13 | 21,878,424 | pass | `/home/sage.guest/sagelite-public-validation-20260802/linux-aarch64-cp313` |
| Linux `aarch64` | 3.14 | 21,875,200 | pass | `/home/sage.guest/sagelite-public-validation-20260802/linux-aarch64-cp314` |
| macOS arm64 | 3.12 | 19,941,432 | pass | `/Volumes/sage/sagelite-public-validation-20260802/macos-arm64-cp312-r1` |
| macOS arm64 | 3.13 | 19,933,816 | pass | `/Volumes/sage/sagelite-public-validation-20260802/macos-arm64-cp313-r1` |
| macOS arm64 | 3.14 | 19,932,400 | pass | `/Volumes/sage/sagelite-public-validation-20260802/macos-arm64-cp314-r1` |

Every row has a durable zero `exit-code`, 102 successful selftest checks, zero
entries in each of the five isolation-leak classes, and successful smoke
output. The temporary download directories and successful virtual
environments were removed after the evidence files were written.

## Historical Copy-Paste Result

| Platform | Python | Result | Log |
|---|---:|---|---|
| Linux `x86_64` | 3.12 | pass | `/scratch/sagelite-copy-paste-validation/20260708-052422-linux-x86_64-cp312/base-install.log` |
| macOS arm64 | 3.12 | pass | `/Volumes/sage/sagelite-copy-paste-validation/20260708-052423-macos-arm64-cp312/base-install.log` |
| Linux `aarch64` | 3.12 | pass | `/mnt/cocalc/sagelite-matrix-validation/copy-paste/20260708-052509-linux-aarch64-cp312/base-install.log` |

All three installs selected:

- `sagelite==10.9.post6`
- `sagelite-graphviz-runtime==10.9.post3`

The smoke command printed the factorization of `x^4 - 1` over `QQ` and
`gap.eval("2+2") == 4` on all three platforms.

## Graphviz Runtime Refresh

`sagelite-graphviz-runtime==10.9.post3` is a metadata/content refresh of the
existing platform wheels. It adds a Linux startup preload hook for the copied
Graphviz runtime libraries so the third-party `pygraphviz` wheel can import in
minimal Linux containers without setting `LD_LIBRARY_PATH`.

Focused public-index validation:

| Platform | Python | Result | Log |
|---|---:|---|---|
| Linux `aarch64` | 3.12 | `pygraphviz` imports with no `LD_LIBRARY_PATH` | `/mnt/cocalc/sagelite-matrix-validation/graphviz-post3-public/20260708-053546-linux-aarch64-cp312/pygraphviz-import.log` |
