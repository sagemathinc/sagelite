# Sagelite

`sagelite` is the wheel-first distribution of Sage from this repository.

The package name is `sagelite`. The Python import namespace remains `sage`.

```bash
uv pip install sagelite
uv add sagelite
python -c "import sage.all"
```

## Purpose

The purpose of `sagelite` is to make a large, useful subset of Sage available
through standard Python packaging tools on modern systems without requiring a
traditional Sage source build or a full Sage runtime prefix.

`sagelite` is not intended to be a drop-in replacement for every part of the
traditional Sage distribution. It is intended to provide a strong in-process
library runtime first.

## Product Contract

`sagelite` guarantees the following:

- The `sage` Python package imports in a supported environment.
- In-process Python, C, C++, and Cython functionality that depends on bundled
  or wheel-installed native libraries is part of the supported surface.
- Core arithmetic, algebra, combinatorics, modular forms, and related library
  features are in scope when they run entirely in-process.
- The wheel should install and work using standard Python tooling such as
  `pip` and `uv`.

`sagelite` does not guarantee the following:

- Bundled standalone executables such as `gap`, `Singular`, `maxima`, or `gp`.
- A traditional Sage filesystem layout or runtime prefix.
- Optional databases or data packages unless explicitly installed.
- Feature parity with every aspect of the full Sage distribution.

## Optional Integrations

Some Sage features rely on external programs or optional datasets.

For `sagelite`, these are treated as optional integrations rather than part of
the core package contract.

### External executables

Examples include:

- GAP
- Singular
- Maxima
- GP/Pari

Policy:

- `sagelite` does not bundle these executables.
- If a compatible executable is already installed on the user's `PATH`,
  related functionality may work.
- If not present, the feature should fail clearly and lazily, not break import
  or unrelated in-process functionality.

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
- Knot databases
- other large or specialized datasets

Policy:

- Optional data is not bundled into the core `sagelite` wheel by default.
- Missing data should surface as an explicit missing-feature or missing-data
  condition.
- Companion packages are the preferred delivery mechanism for data that is
  useful to many users but too large or specialized for the core wheel.

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

### Phase 3

- Linux `aarch64`

This matters for servers, cloud VMs, and Apple Silicon Linux environments, but
it comes after Linux `x86_64` and macOS `arm64` are stable.

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

These do not necessarily block a `sagelite` release:

- missing external executables
- missing optional data packages
- unsupported optional native components
- failures in features that are explicitly outside the `sagelite` contract

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

### Installed-wheel doctests

Broad doctest sweeps should be run against the installed wheel, not the source
tree.

The purpose of these runs is:

- identify core regressions
- identify optional external/data assumptions
- quantify the remaining unsupported surface

These doctest runs should be summarized using the reducer in
`tools/analyze-doctest-log.py`.

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

## Companion Packages

The preferred way to grow `sagelite` is through small, explicit companion
packages rather than by turning the core wheel into a monolith.

Examples:

- `sagelite-cremona-mini`
- future `sagelite-data-*` packages

This keeps the base installation small and makes optional capabilities
discoverable.

## Repository Policy

The current repository remains a fork of upstream Sage.

That is intentional:

- the `sagelite` contract is still being defined
- some fixes are source-level, not only packaging-level
- keeping changes in a fork makes upstream comparison and rebasing easier than
  a patch queue on top of a submodule checkout

If packaging and release infrastructure eventually dominates the work, a
separate thin packaging repository may make sense later. For now, the source
fork remains the right home for `sagelite`.

## Current Working Definition

At the current stage, `sagelite` should be understood as:

> a wheel-distributed core Sage runtime for standard Python environments,
> focused on in-process functionality, with optional interoperability for
> external executables and optional datasets when they are installed separately

That is the working contract used to judge packaging, testing, and release
readiness.
