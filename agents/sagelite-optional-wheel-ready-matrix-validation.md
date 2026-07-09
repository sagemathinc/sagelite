# Sagelite Optional Wheel-Ready Matrix Validation

This records the public-index validation of
`sagelite[optional-wheel-ready]==10.9.post8`.

The validation command shape was:

```bash
python -m pip install --no-cache-dir --only-binary=:all: \
  --extra-index-url https://sagelite.sagemath.org/dev/simple/ \
  "sagelite[optional-wheel-ready]==10.9.post8"
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
`cvxpy`, `cylp`, `GitPython`, `nibabel`, `osqp`, `pybtex`, `pygraphviz`,
`pyscipopt`, `python-flint`, `qdldl`, `scs`, `SQLAlchemy`, and `texttable`
where selected by environment markers. It also solves a tiny `cvxpy` problem
with CLARABEL, instantiates `CyClpSimplex`, and optimizes a tiny PySCIPOpt
model.

## Result

| Platform | Python | Result | Log |
|---|---:|---|---|
| Linux `x86_64` | 3.12 | pass | `/scratch/sagelite-matrix-validation/20260708-062950-linux-x86_64-post8/python3.12/install-smoke.log` |
| Linux `x86_64` | 3.13 | pass | `/scratch/sagelite-matrix-validation/20260708-062950-linux-x86_64-post8/python3.13/install-smoke.log` |
| Linux `x86_64` | 3.14 | pass | `/scratch/sagelite-matrix-validation/20260708-062950-linux-x86_64-post8/python3.14/install-smoke.log` |
| macOS arm64 | 3.12 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-061620-macos-arm64-post8/python3.12/install-smoke.log` |
| macOS arm64 | 3.13 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-061620-macos-arm64-post8/python3.13/install-smoke.log` |
| macOS arm64 | 3.14 | pass | `/Volumes/sage/sagelite-matrix-validation/20260708-061620-macos-arm64-post8/python3.14/install-smoke.log` |
| Linux `aarch64` | 3.12 | install and `pip check` pass; optional import smoke passes with system `git` installed | `/mnt/cocalc/sagelite-matrix-validation/20260708-063616-linux-aarch64-cp312-post8/smoke-with-system-git.log` |

## Metadata Refresh

`10.9.post9` adds this optional batch:

- `highspy >=1.13.1`
- `joblib >=1.5.3`

The public `dev` simple index was refreshed from a merged 177-wheel wheelhouse
that keeps the existing `10.9.post8` primary wheels and adds `10.9.post9`
primary wheels for the same staged platforms. A fresh public-index smoke test
passed on Linux `x86_64`, CPython 3.14:

`/scratch/sagelite-r2-work/smoke-public-post9-cp314-x86_64-20260709-171841`

That smoke installed `sagelite[optional-wheel-ready]==10.9.post9`, ran
`pip check`, imported `sage.all`, `joblib`, and `highspy`, did basic Sage
matrix arithmetic, and solved a tiny HiGHS model through `highspy`.

`10.9.post5` failed binary-only resolution for these targets because `ecos`
has no compatible wheel there:

- Linux `x86_64`, CPython 3.13
- Linux `x86_64`, CPython 3.14
- Linux `aarch64`, CPython 3.12

`10.9.post6` made `ecos` conditional:

```toml
ecos >=2.0.14; sys_platform == "darwin" or (sys_platform == "linux" and platform_machine == "x86_64" and python_version < "3.13")
```

`10.9.post8` adds this optional batch:

- `cvxpy >=1.6.7`
- `cylp >=0.92.3`
- `pyscipopt >=5.1.1`

It also narrows `ecos` again because current macOS arm64 Homebrew Python
environments no longer resolve an `ecos>=2.0.14` binary wheel:

```toml
ecos >=2.0.14; sys_platform == "linux" and platform_machine == "x86_64" and python_version < "3.13"
```

## Linux Aarch64 Caveats

Linux `aarch64` was validated under qemu/binfmt in a
`python:3.12-slim-bookworm` container on the Linux build host.

For `10.9.post8`, the binary-only install and `pip check` passed without
system packages in:

`/mnt/cocalc/sagelite-matrix-validation/20260708-063616-linux-aarch64-cp312-post8/install-smoke.log`

That first smoke then exposed one runtime expectation:

- `GitPython` needs a `git` executable on `PATH`.

The passing follow-up smoke with system `git` installed is:

`/mnt/cocalc/sagelite-matrix-validation/20260708-063616-linux-aarch64-cp312-post8/smoke-with-system-git.log`

The `pygraphviz` issue is fixed by `sagelite-graphviz-runtime==10.9.post3`,
which adds a Linux startup preload hook. A focused public-index check passed
without `LD_LIBRARY_PATH`:

`/mnt/cocalc/sagelite-matrix-validation/graphviz-post3-public/20260708-053546-linux-aarch64-cp312/pygraphviz-import.log`
