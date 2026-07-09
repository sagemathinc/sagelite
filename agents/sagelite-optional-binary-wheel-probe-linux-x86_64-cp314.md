# Sagelite Optional Binary-Wheel Probe

This generated report probes not-yet-packaged Sage optional packages for binary-wheel or pure-Python wheel availability.

The probe command shape is:

```bash
python -m pip download --only-binary=:all: --no-deps <requirement>
```

Scratch output: `/scratch/sagelite-optional-probes-cp314/binary-wheel-probe-20260708-175929`

## Summary

- Probed packages: 14
- Wheel-ready packages: 4
- Missing/source-only packages: 10

## Install-Smoke Outcome

The next low-risk metadata batch selected from this probe and a small manual
second-batch check is:

- `highspy >=1.13.1`
- `joblib >=1.5.3`

Validation:

- Dry-run binary-only dependency resolution passed on Linux `x86_64`,
  CPython 3.14, with `--only-binary=:all:` for both packages.
- A real install into a fresh CPython 3.14 venv with
  `sagelite==10.9.post8`, `joblib`, and `highspy` passed `pip check`.
- The runtime smoke imports `joblib`, imports `highspy`, runs basic Sage
  matrix arithmetic, and optimizes a tiny HiGHS model through `highspy`.
- These packages are included in the published `10.9.post9`
  `sagelite[optional-wheel-ready]` metadata. The public-index smoke at
  `/scratch/sagelite-r2-work/smoke-public-post9-cp314-x86_64-20260709-171841`
  passed with `sagelite[optional-wheel-ready]==10.9.post9`, `pip check`,
  Sage import, `joblib` import, `highspy` import, and a tiny HiGHS solve.

Rejected or deferred from the top-level wheel table:

- `pyppeteer`: dependency resolution still fails because no compatible
  `websockets` wheel satisfies `websockets<11`.
- `rst2ipynb`: dependency resolution still fails because `notedown` requires
  `pandoc-attributes`, which has no compatible distribution.
- `sage-flatsurf`: dependency resolution still fails because
  `surface-dynamics` has no compatible wheel.
- `snappy`: dependency resolution still fails because `PyX` has no compatible
  wheel on CPython 3.14; it also remains a larger packaging decision because
  its wheel stack pulls separate PARI-related dependencies.

## Wheel-Ready

| Sage package | Requirement | Artifact | Notes |
|---|---|---|---|
| `pyppeteer` | `pyppeteer` | `pyppeteer-2.0.0-py3-none-any.whl` | pip-style package metadata |
| `rst2ipynb` | `rst2ipynb >=0.2.2` | `rst2ipynb-0.2.3-py3-none-any.whl` | pip package with Sage install wrapper |
| `sage_flatsurf` | `sage-flatsurf` | `sage_flatsurf-0.8.0-py3-none-any.whl` | pip-style package metadata |
| `snappy` | `snappy` | `snappy-3.3.2-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl` | pip-style package metadata |

## Missing Or Source-Only

| Sage package | Requirement | Result | Likely next action |
|---|---|---|---|
| `gap_jupyter` | `gap_jupyter >=0.9` | no wheel | ERROR: No matching distribution found for gap_jupyter>=0.9 |
| `jupymake` | `jupymake >=0.9` | no wheel | ERROR: No matching distribution found for jupymake>=0.9 |
| `ore_algebra` | `ore_algebra @ git+https://github.com/mkauers/ore_algebra` | no wheel |   Running command git clone --filter=blob:none --quiet https://github.com/mkauers/ore_algebra /tmp/pip-download-dt95x4le/ore-algebra_7904fe1be92946c389082ba220a3db18 |
| `pandoc_attributes` | `pandoc_attributes >=8bc82f6d` | no wheel |                       ~~~~^ |
| `pari_jupyter` | `pari_jupyter >=1.3.2` | no wheel | ERROR: No matching distribution found for pari_jupyter>=1.3.2 |
| `pysingular` | `pysingular >=0.9.5` | no wheel | ERROR: No matching distribution found for pysingular>=0.9.5 |
| `pyx` | `PyX` | no wheel | ERROR: No matching distribution found for PyX |
| `singular_jupyter` | `singular_jupyter >=0.9.7` | no wheel | ERROR: No matching distribution found for singular_jupyter>=0.9.7 |
| `slabbe` | `slabbe` | no wheel | ERROR: No matching distribution found for slabbe |
| `surface_dynamics` | `surface_dynamics` | no wheel | ERROR: No matching distribution found for surface_dynamics |
