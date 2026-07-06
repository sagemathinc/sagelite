# Sagelite Optional Package Probe: Linux x86_64 CPython 3.12

This records an initial package-availability probe for the first-batch
candidates from `agents/sagelite-optional-package-inventory.md`.

Probe command shape:

```bash
python3.12 -m pip download --dest <scratch>/downloads --only-binary=:all: --no-deps <requirement>
```

The probe intentionally used `--no-deps`; it checks whether the candidate
package itself has a binary wheel or pure-Python wheel available for the Linux
`x86_64` CPython 3.12 baseline. Dependency closure and runtime smoke tests are
separate follow-up work.

Scratch output:

```text
/scratch/sagelite-optional-probes/linux-x86_64-cp312-20260706-060205
```

## Wheel-Ready Candidates

These packages downloaded wheel files with `--only-binary=:all:`:

| Sage package | Requirement used | Downloaded artifact |
|---|---|---|
| `admcycles` | `admcycles` | `admcycles-1.4-py3-none-any.whl` |
| `biopython` | `biopython` | `biopython-1.87-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` |
| `clarabel` | `clarabel` | `clarabel-0.11.1-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` |
| `ecos_python` | `ecos` | `ecos-2.0.14-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` |
| `gitpython` | `GitPython` | `gitpython-3.1.50-py3-none-any.whl` |
| `nibabel` | `nibabel` | `nibabel-5.4.2-py3-none-any.whl` |
| `osqp_python` | `osqp` | `osqp-1.1.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` |
| `pybtex` | `pybtex` | `pybtex-0.26.1-py3-none-any.whl` |
| `pygraphviz` | `pygraphviz` | `pygraphviz-2.0-cp312-cp312-manylinux_2_28_x86_64.whl` |
| `pyppeteer` | `pyppeteer` | `pyppeteer-2.0.0-py3-none-any.whl` |
| `python_flint` | `python-flint` | `python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` |
| `qdldl_python` | `qdldl` | `qdldl-0.1.9.post1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` |
| `rst2ipynb` | `rst2ipynb >=0.2.2` | `rst2ipynb-0.2.3-py3-none-any.whl` |
| `sage_flatsurf` | `sage-flatsurf` | `sage_flatsurf-0.8.0-py3-none-any.whl` |
| `scs` | `scs` | `scs-3.2.11-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` |
| `sqlalchemy` | `sqlalchemy` | `sqlalchemy-2.0.51-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl` |
| `texttable` | `texttable >=1.6.3` | `texttable-1.7.0-py2.py3-none-any.whl` |

These are the best first targets for Sagelite optional extras because they do
not require us to build new package wheels for the Linux `x86_64` CPython 3.12
baseline. The next check is installing each candidate into a fresh
`sagelite==10.9.post3` environment and running a small import/runtime smoke.

## Source-Only Or Missing Wheel Candidates

These did not produce a candidate wheel in this probe:

| Sage package | Requirement used | Result | Likely next action |
|---|---|---|---|
| `gap_jupyter` | `gap_jupyter >=0.9` | no matching distribution | package from Sage source or skip initially |
| `jupymake` | `jupymake >=0.9` | no matching distribution | package after `polymake` work |
| `pandoc_attributes` | `pandoc_attributes >=8bc82f6d` | invalid version requirement for pip | package from Sage tarball or normalize versioning |
| `pari_jupyter` | `pari_jupyter >=1.3.2` | no matching distribution | package from Sage source or skip initially |
| `pysingular` | `pysingular >=0.9.5` | no matching distribution | package from Sage source after Singular runtime checks |
| `pyx` | `pyx` | no binary distribution | build or vendor a pure-Python wheel if needed |
| `singular_jupyter` | `singular_jupyter >=0.9.7` | no matching distribution | package from Sage source after `pysingular` |
| `slabbe` | `slabbe` | no matching distribution | package from Sage source; likely Sage-dependent |
| `snappy` | first line in `requirements.txt` is a comment | probe input parsing failed | rerun with `snappy`; dependency policy needs review |
| `surface_dynamics` | `surface_dynamics` | no matching distribution | package from Sage source; depends on Sage Cython headers |

`ore_algebra` is a special case. Sage metadata points to a direct Git URL:

```text
ore_algebra @ git+https://github.com/mkauers/ore_algebra
```

`pip download` saved a source zip, not a wheel, even with
`--only-binary=:all:`. Treat it as source-only for Sagelite packaging.

## Suggested First Batch

Start with a small group that is wheel-ready and useful, but unlikely to
perturb the standard install:

- `biopython`
- `pybtex`
- `pyx` only after building or finding a pure-Python wheel
- `python_flint`
- `sqlalchemy`
- `texttable`

Then handle the optimization stack as a coordinated group because these
packages are dependencies of the existing `cvxpy` extra:

- `clarabel`
- `ecos_python`
- `osqp_python`
- `qdldl_python`
- `scs`

Sage-adjacent packages that depend on Sage internals or source headers should
be a separate workstream:

- `surface_dynamics`
- `sage_flatsurf`
- `slabbe`
- `snappy`
- `ore_algebra`
