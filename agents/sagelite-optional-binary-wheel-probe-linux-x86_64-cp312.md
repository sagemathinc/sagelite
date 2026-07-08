# Sagelite Optional Binary-Wheel Probe

This report records a generated probe of not-yet-packaged Sage optional packages for binary-wheel or pure-Python wheel availability, plus follow-up install-smoke results for candidates selected from the probe.

The probe command shape is:

```bash
python -m pip download --only-binary=:all: --no-deps <requirement>
```

Scratch output: `/scratch/sagelite-optional-probes/binary-wheel-probe-20260706-213913`

## Summary

- Probed packages: 18
- Wheel-ready packages: 8
- Missing/source-only packages: 10

## Install-Smoke Outcome

The second low-risk batch added to `sagelite[optional-wheel-ready]` is:

- `admcycles >=1.4`
- `GitPython >=3.1.50`
- `nibabel >=5.4.2`
- `pygraphviz >=2.0`

Validation:

- Public-index install: `sagelite[optional-wheel-ready]==10.9.post6`
- Install mode: `pip install --no-cache-dir --only-binary=:all: --extra-index-url https://sagelite.sagemath.org/dev/simple/`
- Passed on Linux `x86_64`, CPython 3.12, 3.13, and 3.14: `pip check`,
  Sage polynomial arithmetic, Sage matrix arithmetic, GAP invocation, and
  imports for all packages selected by `optional-wheel-ready`.
- Passed on macOS arm64, CPython 3.12, 3.13, and 3.14: `pip check`, Sage
  polynomial arithmetic, Sage matrix arithmetic, GAP invocation, and imports
  for all packages selected by `optional-wheel-ready`.
- Passed on Linux `aarch64`, CPython 3.12: binary-only install and
  `pip check`. The optional import smoke also passes in a Debian slim
  container after installing system `git` for `GitPython`. The earlier
  `pygraphviz` runtime-library-path issue is fixed by
  `sagelite-graphviz-runtime==10.9.post3`.
- `10.9.post6` is a metadata-only preview refresh from `10.9.post5` that makes
  `ecos` conditional. `ecos` remains enabled on macOS arm64 and Linux
  `x86_64` CPython 3.12, and is skipped where no compatible wheel was found:
  Linux `x86_64` CPython 3.13/3.14 and Linux `aarch64` CPython 3.12.

Deferred candidates from the wheel-ready table:

- `pyppeteer`: top-level wheel exists, but dependency resolution fails for CPython 3.12 under binary-only install because it requires `websockets<11` and no compatible wheel is available.
- `rst2ipynb`: top-level wheel exists, but dependency resolution fails because `notedown` requires `pandoc-attributes`, which is not available as a compatible distribution.
- `sage-flatsurf`: top-level wheel exists, but dependency resolution fails because `surface-dynamics` is not available as a compatible wheel.
- `snappy`: binary wheel exists, but it pulls `cypari` and its own PARI-linked stack rather than the Sagelite `cypari2`/PARI runtime path, so it needs a conscious packaging decision before adding to the low-risk extra.

## Wheel-Ready

| Sage package | Requirement | Artifact | Notes |
|---|---|---|---|
| `admcycles` | `admcycles` | `admcycles-1.4-py3-none-any.whl` | pip-style package metadata |
| `gitpython` | `GitPython` | `gitpython-3.1.50-py3-none-any.whl` | pip-style package metadata |
| `nibabel` | `nibabel` | `nibabel-5.4.2-py3-none-any.whl` | pip-style package metadata |
| `pygraphviz` | `pygraphviz` | `pygraphviz-2.0-cp312-cp312-manylinux_2_28_x86_64.whl` | pip-style package metadata |
| `pyppeteer` | `pyppeteer` | `pyppeteer-2.0.0-py3-none-any.whl` | pip-style package metadata |
| `rst2ipynb` | `rst2ipynb >=0.2.2` | `rst2ipynb-0.2.3-py3-none-any.whl` | pip package with Sage install wrapper |
| `sage_flatsurf` | `sage-flatsurf` | `sage_flatsurf-0.8.0-py3-none-any.whl` | pip-style package metadata |
| `snappy` | `snappy` | `snappy-3.3.2-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` | pip-style package metadata |

## Missing Or Source-Only

| Sage package | Requirement | Result | Likely next action |
|---|---|---|---|
| `gap_jupyter` | `gap_jupyter >=0.9` | no wheel | ERROR: No matching distribution found for gap_jupyter>=0.9 |
| `jupymake` | `jupymake >=0.9` | no wheel | ERROR: No matching distribution found for jupymake>=0.9 |
| `ore_algebra` | `ore_algebra @ git+https://github.com/mkauers/ore_algebra` | no wheel |   Running command git clone --filter=blob:none --quiet https://github.com/mkauers/ore_algebra /tmp/pip-download-1dvt5_p_/ore-algebra_f1c17604e4f341b6a4a018aff155426b |
| `pandoc_attributes` | `pandoc_attributes >=8bc82f6d` | no wheel |                       ~~~~^ |
| `pari_jupyter` | `pari_jupyter >=1.3.2` | no wheel | ERROR: No matching distribution found for pari_jupyter>=1.3.2 |
| `pysingular` | `pysingular >=0.9.5` | no wheel | ERROR: No matching distribution found for pysingular>=0.9.5 |
| `pyx` | `PyX` | no wheel | ERROR: No matching distribution found for PyX |
| `singular_jupyter` | `singular_jupyter >=0.9.7` | no wheel | ERROR: No matching distribution found for singular_jupyter>=0.9.7 |
| `slabbe` | `slabbe` | no wheel | ERROR: No matching distribution found for slabbe |
| `surface_dynamics` | `surface_dynamics` | no wheel | ERROR: No matching distribution found for surface_dynamics |
