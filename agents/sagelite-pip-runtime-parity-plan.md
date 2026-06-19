# Sagelite pip runtime parity plan

Date: 2026-06-19

Goal: make the pip-installable `sagelite` distribution behave like the
self-contained Sage runtime closely enough that installed doctests fail only
for legitimate code defects, not packaging drift, missing runtime data, or
host-system leakage.

This plan deliberately does not use broad `# random` or blanket doctest
masking. Doctests should be changed only after the pip runtime has been made
equivalent to the self-contained Sage runtime, and only for mathematically
acceptable output variants, tolerances, or ordering differences.

## Current checkpoint

- Repository branch: `develop`.
- Relevant commits:
  - `7ae08cca620 sagelite: stabilize installed doctest runtime`
  - `d6f056f1c51 sagelite: guard repaired native extension coverage`
- Scratch install state:
  - Install metadata: `/scratch/sagelite-r2-work/current-install-latest.env`
  - Current raw proof wheel:
    `/scratch/sagelite-r2-work/current-wheel-20260618-235326/raw/sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl`
  - Partial installed doctest log:
    `/scratch/sagelite-r2-work/current-validation/doctest-installed-no-fplll-symlink-clean-env-full-20260619-002757.log`
  - Partial analysis:
    `/scratch/sagelite-r2-work/current-validation/doctest-installed-no-fplll-symlink-clean-env-full-20260619-002757.partial.analysis.md`

Known facts from the latest investigation:

- A local raw wheel can be built with `sage.libs.braiding` and
  `sage.rings.polynomial.pbori.pbori` included when `brial` and
  `libbraiding` are enabled.
- Local `auditwheel repair` cannot produce a usable manylinux wheel on this
  host because the local toolchain emits too-new glibc symbols. Repaired wheel
  validation must happen in the manylinux/CIBW environment.
- The full installed doctest run is not close to passing yet. A partial clean
  run showed failures across external runtimes, missing native extensions,
  path discovery, numeric tolerances, symbolic output, and algorithmic
  representative choices.
- The previous passing installed run was narrower and still depended on manual
  runtime adjustments, including manually copied extensions and narrow
  `LD_LIBRARY_PATH`.

## Guiding principles

1. Use `/scratch` for build, wheelhouse, and test environments.
2. Test only fresh pip-installed environments when validating packaging.
3. Runtime tests should not require `LD_LIBRARY_PATH`, manual copied extension
   modules, or symlinks under `/project/local`.
4. Prefer making runtime discovery deterministic over editing doctests.
5. Make CI fail at wheel repair time when a required extension or bundled
   shared library is missing.
6. Treat self-contained Sage as the runtime contract. First compare and close
   parity gaps, then decide which doctest outputs are acceptable variants.

## Phase 1: establish reproducible parity manifests

Create a manifest script that can be run in both environments:

- self-contained Sage from the source build;
- fresh pip-installed sagelite from local wheelhouse.

The manifest should be machine-readable JSON and include:

- Python executable, version, `sys.path`, `site.getsitepackages()`, and
  `sysconfig` platform tags.
- Sage version, `SAGE_ROOT`, `SAGE_LOCAL`, `SAGE_SHARE`, `SAGE_EXTCODE`,
  `SAGE_VENV`, and all sagelite-specific env overrides.
- Installed Python packages from `importlib.metadata`.
- Sage feature detection results for all features used by doctests.
- Paths and versions for external executables:
  `gap`, `gap3`, `maxima`, `giac`, `fricas`, `singular`, `qepcad`, `latte-count`,
  `count`, `integrate`, `msolve`, `dot`, `neato`, `fdp`, `twopi`, `pdf2svg`,
  `dvipng`, `gfan`, `4ti2`, `palp`, and other companion executables.
- GAP root paths, GAP package paths, and GAP workspace path.
- Maxima library/executable mode details, including `MAXIMA_PREFIX`,
  `MAXIMA_USERDIR`, Lisp implementation, and available Lisp modules.
- FriCAS executable path, Aldor/FriCAS environment variables, and Lisp backend.
- `fpylll` and `fplll` strategy-data paths.
- For every compiled `sage/**/*.so`, record:
  - wheel-relative path;
  - `ldd` dependencies;
  - RPATH/RUNPATH from `readelf -d`;
  - whether any dependency resolves outside the venv/wheel or platform policy.
- For selected compiled modules, record `inspect.getsourcefile()` and
  `sage_getfile_relative()` output to catch build-tree path leakage.

Deliverables:

- `tools/sagelite_runtime_manifest.py`
- A focused test for the manifest script.
- Manifest JSON artifacts in `/scratch` for self-contained and pip-installed
  environments.
- A generated diff report identifying host leakage and missing runtime assets.

Success gate:

- The diff report explains every known doctest failure bucket before any broad
  doctest edits are made.

## Phase 2: build and repair wheel parity

Make the wheel build request the same native surface area as the self-contained
runtime.

Actions:

- Audit Meson options used in release/CIBW against Sage optional native
  libraries and the self-contained Sage build.
- Maintain a required native-extension catalog for Linux sagelite wheels.
  Start with the extensions already known to matter:
  - `sage/libs/braiding.`
  - `sage/rings/polynomial/pbori/pbori.`
  - `sage/libs/coxeter3/coxeter.`
  - `sage/libs/homfly.`
  - native wrappers for `bliss`, `mcqd`, `meataxe`, `sirocco`, and `tdlib` when
    their features are expected to be detected.
- Extend `.github/workflows/repair-wheel-linux.sh` validation so repaired
  wheels fail if any required extension or bundled runtime library is absent.
- Extend metadata tests to cover the required native-extension catalog.
- In the manylinux build, enable required Meson options explicitly instead of
  relying on `auto` for release-critical native features.
- Verify auditwheel bundles runtime libraries for non-policy dependencies:
  `libbrial`, `libbrial_groebner`, `libbraiding`, `libhomfly`, `libcoxeter`,
  and similar libraries required by the native-extension catalog.
- Verify repaired wheels do not contain build-tree absolute paths in generated
  extension metadata where Sage inspection expects package-relative paths.

Success gate:

- A fresh venv can install the repaired sagelite wheel without source-tree
  copying.
- `python -c "import sage.all"` succeeds from outside the repository.
- Native feature smoke tests pass for every required native extension.
- `pip check` passes.
- No `LD_LIBRARY_PATH` is required.

## Phase 3: companion runtime package parity

For each sagelite companion package, compare against self-contained Sage and
ensure Sage discovers companion assets before host-system assets.

### GAP and GAP packages

Observed issues:

- GUAVA was installed, but `weight_distribution(algorithm='leon')` looked for
  `/usr/share/gap/pkg/guava//bin/wtdist`.
- The GUAVA companion wheel contained GAP package data but not the expected
  `bin/wtdist` program.
- Some GAP paths still went through `/usr/bin/gap` and `/usr/share/gap`.

Actions:

- Ensure `sage.env` and GAP feature discovery prepend sagelite companion GAP
  roots before system GAP roots.
- Build and package GUAVA program binaries such as `wtdist`, or mark the
  feature unavailable when the binary is absent.
- Add a GUAVA smoke test that runs:
  - `libgap.LoadPackage("guava")`;
  - `libgap.DirectoriesPackagePrograms("guava")`;
  - existence and executability of `wtdist`;
  - one Sage `C.weight_distribution(algorithm="leon")` example.
- Ensure GAP package companion metadata includes all required data and binaries.
- Audit GAP workspace generation so it is created from the pip runtime, not a
  source-tree or host-system workspace.

Success gate:

- GUAVA doctests no longer use `/usr/share/gap/pkg/guava`.
- GAP package features are detected only when the corresponding companion
  package is complete.

### GAP3

Observed issues:

- GAP3 examples returned different errors, blank output, wrong indexing, and
  different LaTeX formatting.

Actions:

- Compare GAP3 version, startup files, package path, prompt handling, and
  command echoing against self-contained Sage.
- Add a smoke test for `Gap3._execute_line`, `Gap3.help`, indexing, and LaTeX.
- Fix the interface if the pip runtime prompt/output parsing differs.

Success gate:

- `sage.interfaces.gap3` doctests pass or have only documented upstream-output
  variants.

### Maxima

Observed issues:

- Help/example commands failed with `Module error: Don't know how to REQUIRE
  SB-BSD-SOCKETS`.
- Symbolic integration often returned `cases(...)`, `+Infinity`, or expanded
  antiderivatives where self-contained Sage expected constraints or simpler
  forms.

Actions:

- Compare Maxima executable, Lisp implementation, `MAXIMA_PREFIX`,
  `MAXIMA_USERDIR`, `maxima-init.mac`, and compiled Lisp modules against
  self-contained Sage.
- Ensure the maxima runtime package includes all Lisp modules needed for help,
  examples, sockets, and library mode.
- Ensure Sage loads the sagelite Maxima runtime and its ECL/SBCL libraries, not
  a host Maxima or host Lisp module set.
- Add smoke tests for:
  - `maxima.help("gcd")`;
  - `maxima.example("arrays")`;
  - `maxima_lib.sr_integral` cases involving assumptions;
  - one calculus doctest that currently returns `cases(...)`.
- Only after runtime parity is achieved, evaluate whether remaining symbolic
  differences are acceptable doctest variants.

Success gate:

- Maxima help/example tests pass.
- Maxima/Sage symbolic integration behavior matches self-contained Sage for the
  existing doctest examples, or differences are explained by an intentional
  version update.

### FriCAS

Observed issues:

- FriCAS Sage conversion segfaulted or failed with missing `UnaryExport`.

Actions:

- Compare FriCAS executable, Lisp backend, startup files, and environment
  variables against self-contained Sage.
- Add a runtime smoke test for:
  - factorization converted back to Sage;
  - `fricas("sol.basis").sage()`;
  - `fricas_translator` polynomial ring and factorization conversions.
- Fix packaging of FriCAS libraries or startup environment before editing
  doctests.

Success gate:

- FriCAS conversion smoke tests pass without crashes.

### fpylll and fplll data

Observed issues:

- fpylll had a compiled-in strategy path under `/project/local`.
- `shortest_vector()` now falls back to PARI when exact SVP cannot open the
  strategy file.
- Other LLL paths still encountered `fpylll.util.ReductionError: b'infinite
  loop in babai'`.

Actions:

- Determine whether fpylll can be configured at runtime to use the
  `sagelite-fplll-data` strategy directory.
- If yes, set that path centrally during Sage initialization.
- If not, decide whether sagelite must build/publish its own fpylll wheel with
  portable data paths.
- Add fallback behavior for implicit LLL calls only when fpylll raises known
  portability failures and PARI/fplll alternatives are available.
- Add focused doctests for the projective rational point failures that raised
  `infinite loop in babai`.

Success gate:

- No symlink under `/project/local` is required.
- Known fpylll LLL/SVP doctests pass in a fresh pip environment.

### msolve

Observed issues:

- Most failures were dictionary key-order printing.
- Some failures were parser errors when msolve emitted extra lines such as
  `Restarting with another random linear form` or emitted empty/non-Sage
  output before the data.

Actions:

- Capture raw msolve stdout/stderr for failing examples.
- Make the parser robust against diagnostic lines if self-contained Sage accepts
  them, or suppress diagnostics in the msolve wrapper.
- Fix `UnboundLocalError` so unsupported output raises a useful error with the
  raw output.
- Update doctests to compare sorted normalized items only after parser behavior
  is correct.

Success gate:

- `sage.rings.polynomial.msolve` doctests pass or fail only on acceptable
  ordering differences.

### LattE, qepcad, graphviz/dot2tex, Normaliz

Actions:

- Normalize companion executable paths in verbose output only where the
  self-contained Sage already abstracts paths.
- For qepcad, stop assuming command strings are based on `SAGE_LOCAL`; use the
  resolved sagelite runtime executable path.
- For dot2tex/graphviz, compare executable versions and output formats against
  self-contained Sage.
- For Normaliz/polyhedron numeric results, determine whether differences come
  from version drift or floating precision. Prefer tolerance-based doctests only
  after version parity is understood.

Success gate:

- External verbose-output doctests do not fail solely because pip paths contain
  venv or companion package locations.

## Phase 4: path-discovery and host-leakage cleanup

Observed issues:

- `sage_getfile_relative()` returned absolute build-tree paths such as
  `/scratch/sagelite-r2-work/current-source-.../src/sage/rings/rational.pyx`.
- Some subprocesses invoked host tools or host Python when the environment was
  not sanitized.

Actions:

- Ensure wheel builds do not preserve source-tree paths in a way that breaks
  Sage inspection.
- Add installed-wheel tests for `sage_getfile_relative()` on representative
  compiled modules.
- Ensure `sage`, `python`, and `python3` subprocesses inside doctests resolve
  to the venv interpreter where appropriate.
- Make installed doctest runner enforce:
  - `PATH="$venv/bin:$PATH"`;
  - `PYTHONNOUSERSITE=1`;
  - no inherited `PYTHONPATH`;
  - explicit runtime env variables for companion packages.
- Add a smoke test that runs from `/scratch`, not the repository root, to avoid
  source-tree shadowing.

Success gate:

- Installed doctest self-tests do not import editable/source sagelite.
- Source inspection returns package-relative paths where expected.

## Phase 5: installed test runner and triage improvements

The current analyzer under-classifies many failures as `unknown`.

Actions:

- Improve `tools/analyze-doctest-log.py` fingerprints for:
  - symbolic expression variants;
  - numeric tolerance failures;
  - external executable path differences;
  - GAP/GAP3/Maxima/FriCAS runtime errors;
  - msolve parser diagnostics;
  - fpylll reduction failures;
  - build-tree source path leakage;
  - optional native extension missing.
- Make the installed doctest runner optionally emit:
  - manifest path;
  - environment summary;
  - exact wheel filenames installed;
  - companion package list;
  - feature list.
- Add a "top actionable buckets" report that groups failures by root cause
  rather than by module.

Success gate:

- A failed installed doctest run produces a compact report that points to
  packaging/runtime fixes first and doctest robustness fixes second.

## Phase 6: doctest robustness after parity

Only after phases 1-5 close packaging and runtime parity gaps, update doctests
that are genuinely brittle.

Permitted doctest changes:

- Numeric output: use existing Sage tolerance syntax when the result is
  numerically equivalent and the dependency version legitimately changes the
  last bits.
- Symbolic output: compare by simplification, derivative, substitution, or
  invariant properties instead of exact pretty-printed antiderivatives.
- Ordering: sort results or compare sets/dictionaries structurally.
- External verbose output: use ellipses for absolute executable paths and
  timing lines when the command behavior is what matters.
- Representative choices: test mathematical invariants when multiple reduced
  bases, uniformizers, monodromy labels, or character table row orderings are
  valid.

Forbidden doctest changes:

- Do not mark broad blocks `# random` merely to suppress failures.
- Do not mark examples optional if the dependency is installed and expected to
  work.
- Do not convert real runtime crashes, missing binaries, missing extensions, or
  parser errors into tolerated output.

Success gate:

- Each doctest edit has a short rationale tied to a validated acceptable
  variant, not to a packaging defect.

## Phase 7: final clean install validation

For each validation cycle:

1. Build or download repaired sagelite and all companion wheels into
   `/scratch/sagelite-r2-work/wheelhouse-<stamp>`.
2. Create a fresh venv under `/scratch/sagelite-r2-work/install-<stamp>`.
3. Install sagelite and all intended companion packages from the wheelhouse.
4. Run `pip check`.
5. Run the runtime manifest and compare it to self-contained Sage.
6. Run smoke tests for native extensions and external runtimes.
7. Run targeted doctests for recently fixed buckets.
8. Run full installed doctests with a clean environment.
9. Analyze logs and commit only coherent, validated change sets.

Fresh install command shape:

```bash
python3 -m venv /scratch/sagelite-r2-work/install-<stamp>
/scratch/sagelite-r2-work/install-<stamp>/bin/python -m pip install -U pip
/scratch/sagelite-r2-work/install-<stamp>/bin/python -m pip install \
    --no-index \
    --find-links /scratch/sagelite-r2-work/wheelhouse-<stamp> \
    'sagelite[all-needed-extras]'
/scratch/sagelite-r2-work/install-<stamp>/bin/python -m pip check
```

Installed doctest command shape:

```bash
export PATH="/scratch/sagelite-r2-work/install-<stamp>/bin:$PATH"
export PYTHONNOUSERSITE=1
unset PYTHONPATH
/scratch/sagelite-r2-work/install-<stamp>/bin/python \
    tools/run-installed-wheel-doctests.py \
    --python /scratch/sagelite-r2-work/install-<stamp>/bin/python \
    --output-dir /scratch/sagelite-r2-work/validation-<stamp> \
    --label full \
    --full \
    --nthreads 4
```

Final acceptance criteria:

- Fresh pip install succeeds from wheels only.
- `pip check` passes.
- No manual file copying, `/project/local` symlinks, or `LD_LIBRARY_PATH` are
  required.
- All required native extension imports pass.
- All companion executable smoke tests pass.
- Full installed doctests pass, or remaining failures are documented as
  intentionally unsupported optional features with feature detection preventing
  their doctests from running by default.

## Suggested implementation order

1. Runtime manifest and clean installed runner environment.
2. Required native extension catalog, starting with `coxeter3`.
3. GAP/GUAVA path and `wtdist` packaging.
4. Maxima runtime help/example and integration parity.
5. FriCAS conversion crashes.
6. fpylll strategy-data and LLL fallback coverage.
7. msolve parser diagnostics.
8. Source-path leakage in compiled modules.
9. LattE/qepcad/graphviz verbose path behavior.
10. Doctest robustness edits for numeric, symbolic, and ordering variants.
