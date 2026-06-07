# Sagelite

`sagelite` is the wheel-first distribution of Sage from this repository.

The distribution package name is `sagelite`. The Python import namespace
remains `sage`.

```bash
uv pip install sagelite
uv add sagelite
python -c "import sage.all"
```

## Purpose

The purpose of `sagelite` is to make a large, useful subset of Sage available
through standard Python packaging tools on modern systems without requiring a
traditional Sage source build or a full Sage runtime prefix.

The long-term user-facing goal is that `pip install sage` can install a
complete, practical Sage environment using ordinary Python packaging. In that
model, the `sage` distribution on PyPI should be a small metapackage that
depends on `sagelite[full]` or an equivalent complete extra, while `sagelite`
continues to provide the actual `sage` Python import namespace.

The strategy is not to reproduce Sage's traditional prefix as one monolithic
artifact. Instead, `sagelite` provides the core in-process library runtime, and
companion wheels provide optional executables, runtime files, and datasets.

## North Star

The north star for this project is:

> upstream merging is a first-class invariant.

This is not only a maintenance preference. It is a core product constraint.
`sagelite` should remain close enough to upstream Sage that each new official
Sage release can be merged, packaged, tested, and released without turning the
merge itself into a separate research project.

This constraint shapes the technical strategy:

- keep the `sage` Python package and source tree as close to upstream Sage as
  practical
- prefer additive packaging metadata, companion packages, and runtime discovery
  helpers over invasive source restructuring
- keep wheel-specific behavior explicit and easy to audit
- avoid changes that make ordinary upstream Sage development harder to merge
- when a fix is generally useful, prefer a form that could plausibly be sent
  upstream

The wheel-first packaging work is valuable only if it can keep moving as Sage
itself moves. A packaging strategy that works once but makes future Sage
release merges expensive is not successful for `sagelite`.

## Relationship To Passagemath

`passagemath` is a pip-installable modularized fork of SageMath with a closely
related goal: make Sage functionality available through ordinary Python
packaging and binary wheels. It is important prior art for `sagelite`.

Technically, `passagemath` demonstrates that a wheel-first Sage distribution is
viable. It has already explored many areas that matter to `sagelite`, including
modular package boundaries, PyPI-published metapackages, installed-wheel
doctesting, known-failure tracking, GAP package splitting, native runtime
packaging, macOS wheels, and platform-specific wheel repair.

The main difference is product shape. `passagemath` deeply modularizes Sage
into many `sagemath-*` and `passagemath-*` distributions. This gives it fine
grained package boundaries and independently installable pieces, but it also
creates a large structural delta from upstream Sage.

`sagelite` should learn from `passagemath`, but it should not adopt deep
modularization as an automatic default. The preferred `sagelite` shape is:

- one core distribution that provides the `sage` import namespace
- optional companion wheels for heavyweight runtimes and datasets
- a future `sage` metapackage that installs the broad supported stack
- minimal source-tree divergence from official Sage

That difference matters because upstream mergeability is a first-class
invariant for `sagelite`. Borrowing ideas, metadata patterns, CI techniques,
wheel repair methods, package splits, and compatible code from `passagemath`
can save substantial work. But changes should be evaluated against the cost
they add to future merges from official Sage.

## Product Contract

`sagelite` guarantees the following:

- The `sage` Python package imports in a supported environment.
- In-process Python, C, C++, and Cython functionality that depends on bundled
  or wheel-installed native libraries is part of the supported surface.
- Core arithmetic, algebra, combinatorics, modular forms, and related library
  features are in scope when they run entirely in-process.
- The wheel should install and work using standard Python tooling such as
  `pip` and `uv`.

The base `sagelite` wheel does not guarantee the following:

- Bundled standalone executables such as `gap`, `Singular`, `maxima`, or `gp`.
- A traditional Sage filesystem layout or runtime prefix.
- Optional databases or data packages unless explicitly installed.
- Feature parity with every aspect of the full Sage distribution.

Those features are still in scope for the overall wheel-first Sage product when
they are provided by optional companion packages or by a future `sage`
metapackage.

## Packaging Strategy

The core packaging rule is:

> keep the base wheel useful and importable, and put optional heavyweight
> payloads into explicit, testable companion wheels.

This uses ordinary Python packaging mechanisms:

- platform wheels for native extensions and bundled shared libraries
- package data for executable and dataset payloads
- console-script entry points for bundled commands
- Python entry points or runtime helper modules for data-path discovery
- extras such as `sagelite[gap]`, `sagelite[databases]`, `sagelite[runtime]`,
  and `sagelite[full]`

This is intentionally not a Conda-specific strategy. Conda remains useful as a
source of build dependencies, but the installation target is standard Python
wheel installation with `pip`, `uv`, or similar tools.

## Optional Integrations

Some Sage features rely on external programs or optional datasets.

For `sagelite`, these are treated as optional integrations rather than part of
the base package contract.

### External executables

Examples include:

- GAP
- Singular
- Maxima
- GP/Pari
- gfan
- 4ti2
- ECM
- mwrank

Policy for the base wheel:

- `sagelite` does not bundle large standalone executables directly.
- If a compatible executable is already installed on the user's `PATH`,
  related functionality may work.
- If not present, the feature should fail clearly and lazily, not break import
  or unrelated in-process functionality.

Policy for the wheel-first product:

- Redistributable executables should be packaged in companion wheels when doing
  so makes Sage functionality easier to install and test.
- Companion wheels may contain real executable payloads under package data, for
  example `sagelite_ecm/data/bin/ecm` or `sagelite_gfan/data/bin/gfan`.
- Companion wheels may expose console scripts that execute the bundled binary
  and Python helpers that return the executable path.
- Sage runtime discovery should prefer explicitly installed companion packages
  over stale build-time configuration.

### Optional native components

Some features depend on Sage modules or native libraries that are not included
in the initial `sagelite` core wheel.

Policy:

- Missing optional native components should be treated as unavailable features,
  not core installation failures.
- If they become important to users, they can be promoted into either the core
  wheel or separately distributed companion packages.

### Optional data packages

Examples include:

- Cremona databases
- graph databases
- reflexive polytope databases
- PARI data
- GAP package data
- other large or specialized datasets

Policy:

- Optional data is not bundled into the core `sagelite` wheel by default.
- Missing data should surface as an explicit missing-feature or missing-data
  condition.
- Companion packages are the preferred delivery mechanism for data that is
  useful to many users but too large or specialized for the core wheel.

## Companion Packages

The preferred way to grow `sagelite` is through small, explicit companion
packages rather than by turning the core wheel into a monolith.

This keeps the base installation small and makes optional capabilities
discoverable.

### Companion executable wheels

Executable companion packages bundle redistributable command-line runtimes used
by Sage interfaces or doctests.

Examples include:

- `sagelite-gap-runtime`
- `sagelite-gap3-runtime`
- `sagelite-benzene-runtime`
- `sagelite-buckygen-runtime`
- `sagelite-gfan-runtime`
- `sagelite-4ti2-runtime`
- `sagelite-d3js-runtime`
- `sagelite-ecm-runtime`
- `sagelite-jmol-runtime`
- `sagelite-kenzo-runtime`
- `sagelite-latte-runtime`
- `sagelite-lie-runtime`
- `sagelite-lrslib-runtime`
- `sagelite-mathjax-runtime`
- `sagelite-maxima-runtime`
- `sagelite-meataxe-runtime`
- `sagelite-mwrank-runtime`
- `sagelite-nauty-runtime`
- `sagelite-palp-runtime`
- `sagelite-plantri-runtime`
- `sagelite-rubiks-runtime`
- `sagelite-singular-runtime`
- `sagelite-sympow-runtime`
- `sagelite-threejs-runtime`
- `sagelite-topcom-runtime`

Most of these packages copy executable payloads into package data at build
time. Some also copy shared-library dependencies and arrange wrappers so the
runtime is relocatable inside a virtual environment.

### Companion data wheels

Data companion packages make optional Sage datasets installable without
bloating the base wheel.

Examples include:

- `sagelite-cunningham-tables`
- `sagelite-database-cremona-ellcurve`
- `sagelite-database-cremona-mini`
- `sagelite-database-ellcurves`
- `sagelite-database-graphs`
- `sagelite-database-jones-numfield`
- `sagelite-database-kohel`
- `sagelite-database-mutation-class`
- `sagelite-database-odlyzko-zeta`
- `sagelite-database-polytopes`
- `sagelite-database-polytopes-4d`
- `sagelite-database-stein-watkins-mini`
- `sagelite-database-symbolic-data`
- `sagelite-pari-data`

Data packages should expose their installed paths through small Python helper
APIs and, where useful, `sagemath.data_paths` entry points.

Companion packages should have their own smoke tests. A smoke test should prove
that the package imports, exposes the expected data or executable path, and can
perform one representative runtime action when feasible.

### GAP runtime splitting

GAP is large enough that it should not necessarily remain one companion wheel.
A typical GAP root contains a modest core plus large optional package data.
Large payloads such as `TransGrp`, `TomLib`, `CtblLib`, `PrimGrp`, and
`AtlasRep` are natural candidates for separate wheels.

A future split could look like:

- `sagelite-gap-runtime` for the GAP core
- `sagelite-gap-package-gapdoc`
- `sagelite-gap-package-smallgrp`
- `sagelite-gap-package-transgrp`
- `sagelite-gap-package-primgrp`
- `sagelite-gap-package-ctbllib`
- `sagelite-gap-package-tomlib`
- `sagelite-gap-package-atlasrep`

Sage and libgap already understand multiple GAP roots through
`GAP_ROOT_PATHS`, so multiple installed GAP companion packages can contribute
runtime roots. Splitting GAP keeps individual PyPI artifacts smaller and makes
missing optional GAP datasets easier to diagnose.

## `sage` Metapackage

The intended role of the `sage` PyPI distribution is a thin metapackage.

It should not ship a top-level `sage/` package of its own. Instead, it should
depend on `sagelite[full]` or a curated complete extra:

```toml
[project]
name = "sage"
dependencies = [
  "sagelite[full] >=10.9,<10.10",
]
```

This gives users the simple command:

```bash
pip install sage
python -c "import sage.all"
```

The distinction is:

- `sagelite` is the core import-providing distribution.
- `sagelite[...]` extras expose explicit optional installation profiles.
- `sage` is the broad, user-facing install target.

## Supported Platforms

The platform plan is phased.

### Phase 1

- Linux `x86_64`
- CPython `3.12`

This is the first platform that must be stable before broad release.

### Phase 2

- macOS `arm64`

This is the next high-value platform because it covers a large share of modern
developer laptops and does not require users to build Sage from source.

Homebrew is a reasonable macOS build dependency source. The intended user
experience should still be ordinary wheel installation, not a requirement that
users manually install a long list of Homebrew packages. In practice this means
building on macOS with Homebrew-provided dependencies, then using wheel repair
tooling such as `delocate` so the resulting wheels are relocatable.

### Phase 3

- Linux `aarch64`

This matters for servers, cloud VMs, and Apple Silicon Linux environments, but
it comes after Linux `x86_64` and macOS `arm64` are stable.

Windows is not a near-term target.

## Release Policy

The release policy should be driven by the `sagelite` contract rather than by
the traditional Sage distribution.

### Release blockers

These block a `sagelite` release:

- import failures in a supported environment
- crashes or signal-level failures in core-supported functionality
- broken bundled-library interactions in supported in-process code
- broad regressions in the supported core surface
- installation failures via standard Python packaging workflows

### Non-blockers

These do not necessarily block a base `sagelite` release:

- missing external executables
- missing optional data packages
- unsupported optional native components
- failures in features that are explicitly outside the `sagelite` contract

For a `sage` metapackage release, the bar is higher: the selected full
installation profile should install cleanly and the companion package smoke
tests should pass.

### Gray area

Some failures are not immediate blockers but need triage:

- slow or timing-sensitive doctests
- environment-specific failures
- modules that currently depend on optional features for historical reasons

These should be tracked and classified, but they should not automatically be
treated as proof that the core wheel is not releasable.

## Testing Strategy

Testing should be layered.

### Smoke tests

Every supported wheel build should at least verify:

- `import sage.all`
- core arithmetic functionality
- PARI interoperability paths such as `pari(ZZ(11))`
- representative higher-level features such as `ModularSymbols(11).dimension()`

Companion packages should additionally test one representative payload-specific
operation, such as loading a GAP package, running `ecm -h`, invoking `gfan`, or
opening a packaged database.

### Installed-wheel doctests

Broad doctest sweeps should be run against the installed wheel, not the source
tree.

The purpose of these runs is:

- identify core regressions
- identify optional external/data assumptions
- quantify the remaining unsupported surface

These doctest runs should be summarized using the reducer in
`tools/analyze-doctest-log.py`.

Traditional source-tree doctest results are still useful, but they do not
answer the wheel product question by themselves. Release decisions should track
the installed-wheel doctest score for:

- base `sagelite`
- `sagelite[runtime]`
- `sagelite[databases]`
- `sagelite[full]`
- the future `sage` metapackage

### Classification buckets

Doctest failures should be grouped into these buckets:

- `core-supported`
- `optional-external`
- `optional-data`
- `performance-only`
- `framework`
- `unknown`

This classification is part of the release process because `sagelite` needs a
clear product boundary.

## Publishing Strategy

Publishing is designed around GitHub Actions artifacts and explicit manual
promotion to PyPI.

The release workflow should:

- build the `sagelite` sdist
- build platform wheels for supported Python and platform combinations
- build companion wheels
- smoke-test the base wheel and installed companion wheels
- upload all artifacts for inspection
- publish to PyPI only when explicitly dispatched with publishing enabled

The workflows use `SAGEMATH_PYPI_API_TOKEN` and `pypa/gh-action-pypi-publish`
for upload. This keeps ordinary pushes and release artifact generation separate
from publishing.

For large companion wheels, especially GAP-related packages, artifact size
should be monitored. When a package approaches PyPI file-size limits, prefer
splitting the payload into smaller semantically meaningful wheels rather than
requesting a larger limit as the first response.

## Long-Term Scope

It is plausible for this approach to cover almost all redistributable,
open-source Sage functionality over time.

In scope:

- Sage Python modules
- Sage Cython extension modules
- bundled native libraries
- redistributable standalone executables
- optional open datasets
- command-line interfaces used by Sage
- Jupyter/kernel integration when it fits standard Python packaging

Not fully in scope:

- proprietary systems such as Magma, Mathematica, Maple, or MATLAB
- data or software that cannot be redistributed
- features that fundamentally depend on a user's local external service or
  site-specific installation
- exact preservation of every traditional `SAGE_LOCAL` filesystem assumption

The practical goal is therefore not "every historical optional interface works
without external software". The goal is:

> as much of the redistributable Sage distribution as possible should work from
> standard wheel installation, with optional proprietary or site-local systems
> detected lazily when the user has them installed.

## Repository Policy

The current repository remains a fork of upstream Sage.

That is intentional:

- the `sagelite` contract is still being defined
- some fixes are source-level, not only packaging-level
- keeping changes in a fork makes upstream comparison and rebasing easier than
  a patch queue on top of a submodule checkout

The fork should still behave like a close downstream of Sage, not like an
independent replacement project. Packaging work should be organized so that the
delta from upstream remains understandable, reviewable, and mergeable.

If packaging and release infrastructure eventually dominates the work, a
separate thin packaging repository may make sense later. For now, the source
fork remains the right home for `sagelite`.

## Current Working Definition

At the current stage, `sagelite` should be understood as:

> a wheel-distributed core Sage runtime for standard Python environments,
> focused on in-process functionality, with optional companion wheels for
> redistributable executables and datasets

That is the working contract used to judge packaging, testing, and release
readiness.
