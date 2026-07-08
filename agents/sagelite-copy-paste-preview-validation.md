# Sagelite Copy-Paste Preview Validation

This records fresh installs using the public developer-preview command shape
from `SAGELITE.md`:

```bash
python3.12 -m venv sagelite-test
. sagelite-test/bin/activate
python -m pip install --upgrade pip
python -m pip install --extra-index-url https://sagelite.sagemath.org/dev/simple/ "sagelite==10.9.post6"
python -c "from sage.all import *; x = polygen(QQ); print((x**4 - 1).factor()); print(gap.eval('2+2'))"
```

## Result

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
