# Sagelite Optional Wheel-Ready Matrix Validation

This records the public-index validation of
`sagelite[optional-wheel-ready]==10.9.post6`.

The validation command shape was:

```bash
python -m pip install --no-cache-dir --only-binary=:all: \
  --extra-index-url https://sagelite.sagemath.org/dev/simple/ \
  "sagelite[optional-wheel-ready]==10.9.post6"
python -m pip check
python - <<'PY'
from sage.all import QQ, gap, matrix, polygen
x = polygen(QQ)
print((x**4 - 1).factor())
print(gap.eval("2+2"))
print(matrix(QQ, [[1, 2], [3, 5]]).det())
PY
```

The optional import smoke also imports `admcycles`, `biopython`, `clarabel`,
`GitPython`, `nibabel`, `osqp`, `pybtex`, `pygraphviz`, `python-flint`,
`qdldl`, `scs`, `SQLAlchemy`, and `texttable` where selected by environment
markers.

## Result

| Platform | Python | Result | Log |
|---|---:|---|---|
| Linux `x86_64` | 3.12 | pass | `/scratch/sagelite-matrix-validation/20260708-043658-linux-x86_64-post6/cp312/install-smoke.log` |
| Linux `x86_64` | 3.13 | pass | `/scratch/sagelite-matrix-validation/20260708-043658-linux-x86_64-post6/cp313/install-smoke.log` |
| Linux `x86_64` | 3.14 | pass | `/scratch/sagelite-matrix-validation/20260708-043658-linux-x86_64-post6/cp314/install-smoke.log` |
| macOS arm64 | 3.12 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-044450-macos-arm64-post6/cp312/install-smoke.log` |
| macOS arm64 | 3.13 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-044450-macos-arm64-post6/cp313/install-smoke.log` |
| macOS arm64 | 3.14 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-044450-macos-arm64-post6/cp314/install-smoke.log` |
| Linux `aarch64` | 3.12 | install and `pip check` pass; optional import smoke passes with caveats | `/mnt/cocalc/sagelite-matrix-validation/20260708-044819-linux-aarch64-cp312-post6/smoke-with-system-git-and-graphviz-ldpath.log` |

## Metadata Refresh

`10.9.post5` failed binary-only resolution for these targets because `ecos`
has no compatible wheel there:

- Linux `x86_64`, CPython 3.13
- Linux `x86_64`, CPython 3.14
- Linux `aarch64`, CPython 3.12

`10.9.post6` makes `ecos` conditional:

```toml
ecos >=2.0.14; sys_platform == "darwin" or (sys_platform == "linux" and platform_machine == "x86_64" and python_version < "3.13")
```

This keeps `ecos` enabled on the tested platforms where compatible wheels were
available and skips it elsewhere.

## Linux Aarch64 Caveats

Linux `aarch64` was validated under qemu/binfmt in a
`python:3.12-slim-bookworm` container on the Linux build host.

The binary-only install and `pip check` passed without system packages in:

`/mnt/cocalc/sagelite-matrix-validation/20260708-044819-linux-aarch64-cp312-post6/install-smoke.log`

That first smoke then exposed two runtime expectations:

- `GitPython` needs a `git` executable on `PATH`.
- `pygraphviz` imports on Debian slim after
  `LD_LIBRARY_PATH` includes the Sagelite Graphviz runtime library directory,
  for example:

```bash
export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/sagelite_graphviz/data/lib:$LD_LIBRARY_PATH"
```

The passing follow-up smoke with those conditions is:

`/mnt/cocalc/sagelite-matrix-validation/20260708-044819-linux-aarch64-cp312-post6/smoke-with-system-git-and-graphviz-ldpath.log`
