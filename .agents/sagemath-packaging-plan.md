# SageMath Packaging And Distribution Plan

## Goal

Make `pip install sagemath` a real, supported install path for end users.

The primary user experience should be:

1. Create a normal Python environment.
2. Run `pip install sagemath` or `uv add sagemath`.
3. Import Sage or run `sage` immediately, without a local source build.

Source builds should remain supported, but as the developer path, not the default user path.

## What This Plan Assumes

- Sage already has modern Python packaging pieces:
  - `pyproject.toml` with `meson-python`
  - a real `project.name = "sagemath"`
  - wheel targets in `build/make/Makefile.in`
  - a disabled wheel workflow in `.github/workflows/release.yml`
- The hard part is not architecture from scratch.
- The hard part is finishing and operationalizing binary distribution.

## Recommendation In One Sentence

Ship one official, fat, vendored binary wheel first, on one platform, and only split or generalize after that works well.

## Non-Goals For The First Iteration

- Native Windows support
- Perfect distro integration
- Minimal wheel size
- Solving every optional package and dataset
- Preserving every historical system-package choice

The first release should optimize for install success, not elegance.

## Product Decision

Treat Sage like PyTorch, not like a distro meta-package.

- Official binary wheels are the primary product.
- GitHub releases and PyPI are the primary channels.
- Conda-forge is a downstream channel, not the source of truth.
- Debian/Ubuntu/Fedora packaging is opportunistic and downstream.
- Source builds remain available for developers and packagers.

## Packaging Strategy

### Phase 1: One Big Wheel

Start with a single `sagemath` wheel that contains:

- the Python package
- the compiled extension modules
- the native shared libraries Sage depends on
- the executable tools Sage shells out to or links against
- the runtime metadata needed to find those tools and libraries

This wheel should target:

- Linux `x86_64`
- CPython 3.12
- glibc-based `manylinux`

This is intentionally narrow. The first milestone is one install path that works reliably.

### Why A Fat Wheel First

- It avoids early debates about package boundaries.
- It prevents "system package found, but not actually usable" failures.
- It matches how users think: Sage is one thing.
- It makes CI, debugging, and support much simpler.

Only after this works should the project consider splitting out optional components or data packages.

## Architecture

### Package Layout

Initial version:

- `sagemath`
  - ships everything needed for a standard Sage session
  - exposes the `sage` console entry point
  - bundles required native programs and libraries inside the wheel

Possible later split, only if justified:

- `sagemath`
  - thin top-level package
- `sagemath-runtime`
  - bundled native closure
- `sagemath-databases`
  - large optional databases
- `sagemath-extra`
  - optional interfaces and less common dependencies

I would not start with the split.

### Runtime Behavior

At runtime, Sage should resolve bundled resources relative to the installed package location.

That means:

- locating bundled shared libraries without relying on the system
- locating bundled executables like GAP, PARI/GP, Singular, Maxima, etc.
- setting any required environment variables from Python entry points automatically
- avoiding assumptions that the install tree is a source checkout

If needed, add a small runtime bootstrap module that computes the internal prefix from `import sage`.

## Build Strategy

### Reuse Existing Infrastructure

Use the current Sage build system to build the closure, then package the result as a wheel.

Start from:

- `pyproject.toml`
- `build/make/Makefile.in`
- `.github/workflows/release.yml`

The existing disabled `build_wheels` job is the obvious launch point.

### Rule For Official Wheels

For official wheels, prefer vendoring over system detection.

That means:

- do not rely on distro packages during the final wheel build except for toolchain/bootstrap prerequisites
- bundle the known-good versions of the native dependencies Sage requires
- make the official wheel path deterministic and self-contained

For source builds, keep the current system-package integration.

## Concrete Milestones

### Milestone 0: Make The Repo Honest

- Update docs so they stop implying that archived or unmaintained binary paths are the recommended answer.
- Document two paths clearly:
  - official binary install
  - source build for developers
- Add a short "current packaging status" page.

### Milestone 1: Nightly Linux Wheel

Target:

- `manylinux_x86_64`
- CPython 3.12
- publish nightly wheel artifacts to GitHub Actions artifacts and GitHub Releases

Tasks:

- Narrow `.github/workflows/release.yml` to a single wheel target first.
- Remove `if: false` and make the job build exactly one platform.
- Force vendored builds for the native closure used in that wheel.
- Add wheel repair using `auditwheel`.
- Install the resulting wheel in a fresh venv and run smoke tests.

Smoke tests:

- `python -c "import sage; from sage.all import ZZ; print(ZZ(2)^10)"`
- `sage -c "print(factor(2^61 - 1))"`
- `sage -c "gap('Size(SymmetricGroup(8))')"`
- `sage -c "singular('ring r = 0,(x,y),dp; ideal I = x2+y2; I;')"`
- `sage -c "from sage.all import prime_pi; print(prime_pi(10^6))"`
- `sage --version`

### Milestone 2: Public Preview On PyPI

Target:

- publish preview wheels to TestPyPI first
- then publish preview wheels to PyPI for beta releases

Tasks:

- make `pip install sagemath` prefer wheels and fail fast if no wheel exists
- do not silently fall back to source build for normal users
- add a clear error message when an unsupported platform has no wheel

### Milestone 3: Additional Platforms

Add in this order:

1. macOS `arm64`
2. Linux `aarch64`
3. macOS `x86_64`

I would only consider Windows after the Linux/macOS story is stable, and likely via WSL first.

### Milestone 4: Optional Splitting

After the fat wheel is stable:

- identify very large optional data packages
- move them into explicit extras or companion packages
- keep core algebra/number theory/group theory functionality in the main install

## First Engineering Tasks

These are the first concrete tickets I would create.

1. Re-enable the wheel workflow for one target in `.github/workflows/release.yml`.
2. Add a clean-room install test job that starts from an empty venv and installs only the built wheel.
3. Add a runtime self-check command, e.g. `sage --self-test-runtime`, that verifies bundled executables and libraries are discoverable.
4. Audit which executables and libraries must be shipped for a standard Sage session.
5. Patch runtime path resolution so installed wheels do not assume a source tree layout.
6. Remove stale references to archived binary packaging guidance from README and install docs.
7. Publish nightly wheel artifacts even before they are declared supported.

## Known Risks

- Shared library relocation issues
- Executable discovery for subprocess-backed interfaces
- Wheel size
- Licensing review for bundled components
- Platform-specific toolchain quirks
- Optional packages that accidentally become mandatory in the bundled build

None of these are conceptual blockers. They are packaging engineering work.

## How Codex Helps

This is the part I would explicitly use Codex for.

- Generate and maintain the dependency inventory from `build/pkgs` and `pyproject.toml`.
- Continuously triage CI failures and cluster them by root cause.
- Propose small patches for broken detection logic and runtime path issues.
- Maintain the smoke test matrix.
- Keep docs synchronized with the actual state of released artifacts.
- Produce focused PRs that march the wheel job from red to green.

The most important operational rule is this:

Use Codex to finish the existing packaging transition, not to design a brand-new packaging system.

## Success Criteria

This plan is working when all of the following are true:

- `pip install sagemath` works in a fresh Linux `x86_64` venv without compiling Sage
- the installed package can run a normal Sage session
- the wheel build runs in CI on every release branch
- nightly artifacts exist and are easy for users to test
- unsupported platforms fail clearly instead of attempting a surprise source build

## Short Version

Do not start by splitting Sage into ten elegant packages.

Start by shipping one ugly, reliable, official wheel.

Once that exists, refine it.
