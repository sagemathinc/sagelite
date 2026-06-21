# Sagelite pip runtime parity plan

Date: 2026-06-21

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
- Original checkpoint commits:
  - `7ae08cca620 sagelite: stabilize installed doctest runtime`
  - `d6f056f1c51 sagelite: guard repaired native extension coverage`
- Newer parity-tooling commits now on `develop` include:
  - `8061aef7ae1 tools: infer sagelite wheels in installed doctest summaries`
  - `dde53d7e217 sagelite: summarize runtime smoke failures`
  - `6b4b4421285 sagelite: add runtime manifest smoke probes`
  - `f12d8dab6e3 tools/sagelite: broaden runtime manifest executable probes`
  - `f763daa6160 sagelite: report Python path leaks in runtime manifest diffs`
  - `399cf2263ed sagelite: smoke test repaired native imports`
  - `e489fcc4bcf sagelite: centralize native wheel catalog`
  - `288b6184a48 env: prefer sagelite GAP runtime over host roots`
  - `1ec2914d7de tools/sagelite: use resolved GAP roots for program probes`
  - `b2255c5ba76 sagelite: include fplll data in runtime extras`
  - `dacd7aa6e56 tools/sagelite: report bootstrapped fplll strategy paths`
  - `87c66e699ab tools/sagelite: sanitize installed runtime environment`
  - `5c3da77019c env: repair stale fplll strategy environment`
  - `d00d1fa4b82 sagelite: add installed validation extras`
  - `b6636950a33 sagelite: require eclib runtime in repaired wheels`
  - `9e7ae43f54d sagelite: keep selftest collecting runtime failures`
  - `388ab1af72c sagelite: reject host GUAVA feature programs`
  - `3cab3756b32 sagelite: smoke test GUAVA Leon runtime`
  - `dec22cbd620 sagelite: refine source path leak classification`
  - `3be3d150a82 sagelite: include fplll data in validation extras`
  - `3da976f920f agents: refresh sagelite parity checkpoint`
  - `e70692e91fb tools/sagelite: report native wheel coverage in runtime summaries`
  - `55ddb91b4e0 sagelite: reject build-tree source metadata in selftest`
  - `fad57c422fe tools/sagelite: classify fpylll strategy path leaks`
  - `c9164a34cb5 tools/sagelite: map missing native modules in doctest analysis`
  - `04418370406 tools/sagelite: smoke test cypari2 PARI packaging`
  - `87a9f451537 tools/sagelite: classify native library load failures`
  - `9e47d758cf9 tools/sagelite: refine representative doctest fingerprints`
  - `26faf89070b tools/sagelite: collect runtime summaries for staged index tests`
  - `e7a725d42fd agents: refresh sagelite parity checkpoint`
  - `299f3685afe tools/sagelite: smoke test fplll strategy data`
  - `a32ce89fad7 tools/sagelite: smoke test msolve variety runtime`
  - `40712df1cc0 sagelite: smoke test GAP3 runtime behavior`
  - `c15358e5974 tools/sagelite: capture selftest in installed doctest runs`
  - `8b058c7515e tools/sagelite: summarize selftest failures in runtime reports`
  - `0e8c14a2b41 tools/sagelite: add wheelhouse validation wrapper`
  - `64b5b91c395 tools/sagelite: record wheelhouse validation install metadata`
  - `c1a038d58b7 tools/sagelite: record wheelhouse validation step results`
  - `effa06ddccd agents: refresh sagelite parity checkpoint`
  - `848a8bd6c36 tools/sagelite: classify wheelhouse validation inputs`
  - `4fe2b1380d0 tools/sagelite: record repaired-wheel preflight failures`
  - `6bf2b7afc28 tools/sagelite: summarize wheelhouse validation artifacts`
  - `45e46663f1c tools/sagelite: reject ambiguous repaired-wheel validation inputs`
  - `16c8e209822 tools/sagelite: record validation host Python context`
- Scratch install state:
  - Install metadata: `/scratch/sagelite-r2-work/current-install-latest.env`
  - Current raw proof wheel:
    `/scratch/sagelite-r2-work/current-wheel-20260618-235326/raw/sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl`
  - Partial installed doctest log:
    `/scratch/sagelite-r2-work/current-validation/doctest-installed-no-fplll-symlink-clean-env-full-20260619-002757.log`
  - Partial analysis:
    `/scratch/sagelite-r2-work/current-validation/doctest-installed-no-fplll-symlink-clean-env-full-20260619-002757.partial.analysis.md`
  - Current manifest diff:
    `/scratch/sagelite-r2-work/runtime-manifest-diff-refresh-20260620-feature-collection-fix.md`
  - Latest ad hoc current manifest:
    `/scratch/sagelite-r2-work/current-validation/sagelite-runtime-manifest-codex-current.json`
  - Fresh raw-wheel baseline:
    `/scratch/sagelite-r2-work/validation-raw-baseline-20260620-154330/README.md`
  - Scheduled raw-wheel validation:
    `/scratch/sagelite-r2-work/validation-scheduled-20260620-103219/README.md`

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
- The tooling foundation is now much stronger than when this plan was written:
  runtime manifests, manifest diffs, native wheel catalogs, repaired-wheel
  native import smoke checks, sanitized installed doctest runs, runtime
  summaries, and analyzer actionable buckets all exist.
- The actual pip runtime is still not close to final acceptance. The latest
  partial installed doctest analysis recorded 59 failed modules out of 62 seen.
- The latest manifest diff still shows real parity gaps:
  - feature collection for the reference manifest was not clean, so a fresh
    self-contained baseline must be regenerated before treating feature
    differences as authoritative;
  - candidate GAP still leaks host paths such as `/usr/share/gap`;
  - `sage_getfile_relative()` still reports build-tree paths for representative
    compiled modules;
  - `sage.libs.braiding` imports but fails with an undefined symbol in the
    current raw-wheel validation environment;
  - Maxima still points at build-prefix or host ECL state in some fields;
  - fpylll still reports `/project/local/share/fplll/strategies` paths.
- A fresh raw-wheel baseline on 2026-06-20 proved that a wheel-only install can
  be assembled in a fresh Python 3.12 venv after filling the scratch wheelhouse
  with third-party dependency wheels, and that `pip check` passes. However,
  `import sage.all` fails immediately from `/scratch` because
  `sage.libs.ntl.error` cannot resolve `libntl.so.45`. The native wheel catalog
  now treats `sage/libs/ntl/error.`, `libntl`, and `sage.libs.ntl.error` as
  required repaired-wheel surface area so manylinux repair validation catches
  this before companion runtime work.
- A scheduled raw-wheel validation on 2026-06-20 reached manifest collection
  but `sage.cli.selftest` stopped at the PARI packaging check because cypari2
  was installed with a private auditwheel PARI runtime. The manifest recorded
  required native import failures for missing or unresolved repaired-wheel
  libraries and also showed inherited host runtime variables. The installed
  doctest runner now strips inherited Sage, Sagelite, Maxima, GAP, FriCAS,
  Aldor, and fplll runtime environment variables before collecting manifests
  or running doctests.
- Since that raw-wheel validation, selftest has been changed to keep collecting
  runtime failures after early packaging failures; GAP companion root ordering
  and GUAVA Leon smoke coverage have been tightened; stale fpylll strategy
  paths can be repaired from `sagelite-fplll-data`; and the native catalog now
  includes the eclib runtime surface that failed in the raw-wheel proof.
  These changes still need a manylinux/CIBW repaired-wheel validation cycle.
- The installed doctest analyzer now separates stale fpylll strategy-data path
  leaks from generic stale build paths, so fresh logs should point that bucket
  at `sagelite-fplll-data` or a rebuilt fpylll runtime.
- The runtime manifest now has smoke probes for private cypari2 PARI wheels,
  fplll strategy-data relocation, and a basic msolve variety computation.
  `sagelite-selftest` now also probes GAP3 prompt parsing, help output,
  1-based list indexing, and LaTeX formatting when `sagelite-gap3-runtime` is
  installed.
- `tools/validate-sagelite-wheelhouse.py` now writes
  `install-metadata.json` into each validation directory before running the
  install commands, so successful and interrupted validation runs record their
  fresh install path, wheelhouse inputs, package requirement, command sequence,
  and sanitized environment.
- `tools/validate-sagelite-wheelhouse.py` now applies the same broad runtime
  environment sanitization policy as the installed doctest runner before
  creating the fresh venv, installing wheels, running `pip check`, and invoking
  validation. The metadata records the removed runtime keys and prefixes so
  CIBW/manylinux validation artifacts make inherited host leakage auditable.
- `tools/validate-sagelite-wheelhouse.py` now rewrites `install-metadata.json`
  after each completed command with the overall run status, exit code, and
  per-step command result records. Failed scheduled validations should now show
  whether the run stopped during venv creation, pip upgrade, wheel install,
  `pip check`, or installed doctest validation without opening the raw CI log.
- `tools/validate-sagelite-wheelhouse.py --require-repaired-sagelite-wheel`
  now writes `install-metadata.json` for raw-wheel preflight rejection, so an
  accidentally staged raw Linux wheelhouse still leaves auditable validation
  input classification instead of failing before artifact creation.
- `tools/validate-sagelite-wheelhouse.py` now also writes
  `validation-summary.md` beside the install metadata. Scheduled CIBW or
  scratch validation artifacts expose the overall status, exit code, wheelhouse
  classification, preflight error, and completed step commands without requiring
  a JSON viewer.
- `tools/validate-sagelite-wheelhouse.py` now records validation host context
  in both artifacts, including the controller Python version/platform and the
  requested base Python used to create the fresh venv. This should make CIBW
  multi-ABI artifacts auditable when a repaired-wheel validation uses the wrong
  interpreter or runs under an unexpected controller Python.
- The current tree already contains the first msolve parser hardening from this
  plan: `src/sage/rings/polynomial/msolve.py` ignores diagnostic lines before
  the Sage-readable payload and raises `NotImplementedError` with raw msolve
  output instead of leaking `UnboundLocalError`.

Scheduled audit on 2026-06-21:

- No repaired Linux sagelite wheelhouse is staged under
  `/scratch/sagelite-r2-work`; only raw Linux diagnostic wheelhouses are
  available locally. Authoritative parity validation still requires a fresh
  manylinux/CIBW repaired-wheel artifact.
- Older Cloudflare release artifacts are present under
  `/scratch/sagelite-r2-work/cloudflare-wheel-artifacts/release-26987879340`,
  but they contain three primary repaired sagelite wheels for Python 3.12,
  3.13, and 3.14. They are stale relative to the current tooling and are not a
  valid single-interpreter validation input.
- The combined R2 wheelhouse under
  `/scratch/sagelite-r2-work/cloudflare-wheel-artifacts/combined-r2/wheels`
  contains multiple raw Linux primary sagelite wheels, so it is also not a
  valid repaired-wheel validation input.
- Repaired-wheel preflight artifacts from this scheduled run:
  - `/scratch/sagelite-r2-work/validation-scheduled-20260621-release-preflight/validation-summary.md`
    records the stale multi-Python repaired release wheelhouse rejection.
  - `/scratch/sagelite-r2-work/validation-scheduled-20260621-combined-preflight/validation-summary.md`
    records the combined raw-wheel wheelhouse rejection.
- The raw baseline wheelhouse from 2026-06-20 is known to fail immediately at
  `import sage.all` because `sage.libs.ntl.error` cannot resolve
  `libntl.so.45`; rerunning that old raw wheel would not produce new parity
  evidence.
- Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
  - `PYTHONNOUSERSITE=1 PYTHONPATH=src .venv/bin/python -m pytest --confcutdir=src/sage/misc src/sage/misc/sageinspect_test.py -q`
- Follow-up scheduled tooling validation added host/interpreter context to
  wheelhouse validation metadata and summaries. Focused local validation passed
  with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Host `/usr/bin/python3` is Python 3.14 and cannot run the project tests
  cleanly: with user-site enabled it finds a stale editable sagelite loader
  pointing at `/tmp/sage-wheel-prefix/bin/python3`; with
  `PYTHONNOUSERSITE=1`, `pytest` is not installed. Use the repository `.venv`
  for local pure-Python tooling tests.
- Follow-up scheduled tooling work added the native wheel catalog to
  `tools/validate-sagelite-wheelhouse.py` artifacts. Future CIBW/manylinux
  validation directories now record the required Meson options, native import
  module surface, and native library prefixes in `install-metadata.json` and
  summarize the catalog in `validation-summary.md`.
- Follow-up scheduled tooling work now names each wheelhouse validation step in
  `install-metadata.json` command results and in `validation-summary.md`,
  preserving host/interpreter context in failure summaries. Focused local
  validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work now records sagelite companion/runtime/data
  wheels separately from the primary sagelite wheel in wheelhouse validation
  metadata and summaries, so future CIBW artifacts expose staged companion
  coverage without opening the full inventory JSON. Focused local validation
  passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work now normalizes companion sagelite wheel
  package names in wheelhouse validation metadata, records duplicate companion
  packages, and reports missing `all-needed-extras` sagelite companion wheels
  in both `install-metadata.json` and `validation-summary.md`. Focused local
  validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-all-needed-extra-sagelite-wheels`,
  which rejects incomplete companion/runtime/data wheelhouses before creating
  an install when a validation run is meant to prove the full
  `sagelite[all-needed-extras]` runtime. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --reject-duplicate-companion-sagelite-wheels`,
  which rejects ambiguous companion/runtime/data wheelhouses before creating
  an install when duplicate normalized sagelite companion package names are
  staged. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work now records Python and ABI tags for every
  wheelhouse wheel in validation inventory metadata and renders the primary
  sagelite wheel's Python, ABI, and platform tags in `validation-summary.md`,
  making multi-ABI CIBW artifacts easier to audit when the staged wheel does
  not match the requested validation interpreter. Focused local validation
  passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-primary-sagelite-wheel-python-tag`,
  which rejects a staged primary sagelite wheel whose Python tag does not match
  the requested validation interpreter. This turns stale multi-ABI repaired
  artifacts into an auditable preflight failure instead of a later install-time
  ambiguity. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-primary-sagelite-wheel-abi-tag`,
  which rejects a staged primary sagelite wheel whose ABI tag does not match
  the requested validation interpreter. This catches malformed or mixed-ABI
  CIBW artifacts before pip installation when paired with the existing Python
  tag and repaired-wheel preflights. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-primary-sagelite-wheel-platform-machine`,
  which rejects a staged primary sagelite wheel whose platform tag architecture
  does not match the validation host machine. This catches wrong-architecture
  manylinux artifacts before pip installation when paired with the existing
  repaired-wheel, Python-tag, and ABI-tag preflights. Focused local validation
  passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-primary-sagelite-wheel-compatible-platform-tag`,
  which rejects a staged primary sagelite wheel whose platform tag is not in
  the validation host's compatible platform tag set. This catches wrong
  manylinux/musllinux policy tags before installation even when the wheel's
  architecture, Python tag, and ABI tag otherwise match. Focused local
  validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work added
  `tools/validate-sagelite-wheelhouse.py --require-compatible-companion-sagelite-wheels`,
  which rejects staged sagelite companion/runtime/data wheels whose Python,
  ABI, or platform tags are incompatible with the requested validation
  interpreter or host. Validation summaries now also render companion wheel
  tags, so CIBW artifacts expose wrong-ABI or wrong-platform companion wheels
  without opening the JSON inventory. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py tools/test_sagelite_runtime_manifest.py tools/test_run_installed_wheel_doctests.py tools/test_analyze_doctest_log.py -q`
- Follow-up scheduled tooling work now records the inferred wheel validation
  contract in wheelhouse validation artifacts: expected primary/companion
  Python and ABI tags, normalized host machine, compatible platform tag sample,
  and enabled preflight flags. This makes CIBW preflight artifacts auditable
  without reconstructing the validation contract from the command line and host
  metadata. Focused local validation passed with:
  - `PYTHONNOUSERSITE=1 .venv/bin/python -m pytest --confcutdir=tools tools/test_validate_sagelite_wheelhouse.py -q`

## Reality status

Approximate status as of 2026-06-20:

- Phase 1, reproducible manifests: mostly implemented, but the reference
  self-contained manifest must be regenerated with the correct Sage Python.
- Phase 2, native wheel parity: CI/tooling checks are mostly implemented and
  the required native catalog has been broadened, but repaired-wheel proof must
  happen in manylinux/CIBW, not on this host.
- Phase 3, companion runtime parity: partially implemented. GAP/GUAVA, GAP3,
  fplll, and msolve have newer targeted runtime checks and bootstrapping fixes,
  while Maxima, FriCAS, GAP3, and msolve still need fresh repaired-wheel
  evidence.
- Phase 4, path discovery and host leakage: runner environment sanitization is
  implemented; source-path leak classification has been refined; installed
  wheel source-inspection selftest coverage and
  `sage_getfile_relative()` build-prefix normalization are present. Treat older
  scratch source-leak and GAP-host-leak reports as stale unless reproduced by a
  fresh run from current `develop`.
- Phase 5, installed test runner and triage: substantially implemented; the
  next full run should use `--runtime-summary` so the report is self-contained.
  The runner now sanitizes inherited runtime variables in addition to `PATH`,
  `PYTHONNOUSERSITE`, `PYTHONPATH`, and `LD_LIBRARY_PATH`.
- Phase 6, doctest robustness: mostly intentionally deferred.
- Phase 7, final clean install validation: not achieved.

Overall this is past the diagnostic/tooling stage, but not near acceptance.
The highest-value work is now to run a fresh manylinux/CIBW repaired-wheel
validation cycle with the current tooling. Local raw-wheel validation remains
useful for diagnostics, but native-library, PARI, and auditwheel conclusions
must come from the repaired-wheel environment.

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

Status: mostly implemented. The remaining Phase 1 work is operational: produce
a clean self-contained reference manifest with the right Sage Python, produce a
fresh pip-installed candidate manifest from the current wheelhouse, and compare
them after feature collection succeeds in both environments.

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

- Done: `tools/sagelite_runtime_manifest.py`
- Done: focused tests for the manifest script.
- Done but stale/needs refresh: manifest JSON artifacts in `/scratch` for
  self-contained and pip-installed environments.
- Done but needs a clean reference rerun: generated diff reports identifying
  host leakage and missing runtime assets.

Success gate:

- The diff report explains every known doctest failure bucket before any broad
  doctest edits are made.

## Phase 2: build and repair wheel parity

Status: tooling and CI checks are mostly implemented. The unresolved part is
proof: repaired wheels must be validated in the manylinux/CIBW environment.
Local repaired wheels from this host are not authoritative.

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

Status: incomplete. Many companion packages and extras are declared and many
feature helpers prefer sagelite companions, but the latest manifest/doctest
artifacts still show host leakage and runtime-behavior differences.

For each sagelite companion package, compare against self-contained Sage and
ensure Sage discovers companion assets before host-system assets.

### GAP and GAP packages

Current status: not clean. The manifest tooling can detect GUAVA program
availability, but the latest diff still shows `/usr/share/gap` and GUAVA host
paths in the candidate. Fix this before treating GUAVA doctest output as a
doctest robustness issue.

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

Current status: instrumented but not proven. `sagelite-selftest` now runs a
targeted GAP3 smoke probe when the companion runtime is installed, but the
installed doctest analysis still needs a fresh repaired-wheel rerun for
`sage.interfaces.gap3`.

Observed issues:

- GAP3 examples returned different errors, blank output, wrong indexing, and
  different LaTeX formatting.

Actions:

- Compare GAP3 version, startup files, package path, prompt handling, and
  command echoing against self-contained Sage.
- Done: add a smoke test for `Gap3._execute_line`, `Gap3.help`, indexing, and
  LaTeX.
- Fix the interface if the pip runtime prompt/output parsing differs.

Success gate:

- `sage.interfaces.gap3` doctests pass or have only documented upstream-output
  variants.

### Maxima

Current status: high-risk and still incomplete. There are tests and selftests
around companion Maxima/ECL state, but the latest manifest diff still shows
`MAXIMA_FAS`, `MAXIMA_PREFIX`, and `ECLDIR` differences. Resolve those before
editing symbolic doctests.

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

Current status: partially instrumented, not proven. The manifest and selftest
paths include FriCAS conversion smoke checks, but conversion crashes/errors
remain a known installed-runtime bucket.

Observed issues:

- FriCAS Sage conversion segfaulted or failed with missing `UnaryExport`.

Actions:

- Compare FriCAS executable, Lisp backend, startup files, and environment
  variables against self-contained Sage.
- Done: add a runtime smoke test for:
  - factorization converted back to Sage;
  - `fricas("sol.basis").sage()`;
  - `fricas_translator` polynomial ring and factorization conversions.
- Fix packaging of FriCAS libraries or startup environment before editing
  doctests.

Success gate:

- FriCAS conversion smoke tests pass without crashes.

### fpylll and fplll data

Current status: unresolved. The latest manifest still reports fpylll strategy
paths under `/project/local/share/fplll/strategies`.

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

Current status: partly fixed but not proven in an installed repaired-wheel
environment. The analyzer can recognize msolve diagnostic parser failures, and
the parser now skips diagnostic lines before the payload and reports unsupported
formats with raw output instead of `UnboundLocalError`. Fresh installed
doctests still need to prove whether remaining failures are only ordering
differences.

Observed issues:

- Most failures were dictionary key-order printing.
- Done: parser errors when msolve emitted extra lines such as
  `Restarting with another random linear form` now skip diagnostics before the
  payload and report empty/non-Sage output with raw-output context.

Actions:

- Done: capture raw msolve stdout in parser error messages for unsupported
  output.
- Done: make the parser robust against diagnostic lines before the
  Sage-readable payload.
- Done: fix `UnboundLocalError` so unsupported output raises a useful error
  with the raw output.
- Re-run the installed doctest examples in a fresh repaired-wheel environment.
- Update doctests to compare sorted normalized items only after parser behavior
  is correct.

Success gate:

- `sage.rings.polynomial.msolve` doctests pass or fail only on acceptable
  ordering differences.

### LattE, qepcad, graphviz/dot2tex, Normaliz

Current status: mixed. qepcad companion command construction has coverage, but
external verbose-path and numeric-output failures should be revisited only
after the fresh manifest and targeted smoke tests identify actual version/path
differences.

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

Status: partially complete. Installed doctest runs now sanitize `PATH`,
`PYTHONNOUSERSITE`, `PYTHONPATH`, and `LD_LIBRARY_PATH`, but compiled-module
source-path leakage remains visible in manifest diffs.

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

Status: substantially improved, but still expected to evolve. The analyzer now
has more runtime fingerprints and the runner can emit runtime summaries. The
next full installed run should use this path so the remaining `unknown` bucket
can be reduced with evidence from current logs.

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
    --runtime-summary \
    --manifest-compiled-limit 200 \
    --wheelhouse /scratch/sagelite-r2-work/wheelhouse-<stamp> \
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

## Next high-value execution plan

Do these in order. Do not spend time on broad doctest edits until items 1-8
are either fixed or explicitly ruled out as runtime parity issues.

1. Create a fresh authoritative validation baseline.
   - Build or download current repaired Linux wheels in the same style that
     release/CIBW uses. If only local raw wheels are available, label the run
     as raw-wheel proof and do not treat it as final acceptance evidence.
   - Create a new wheelhouse and fresh venv under `/scratch/sagelite-r2-work`.
   - Install from wheels only and run `pip check`.
   - Run `tools/sagelite_runtime_manifest.py collect` for:
     - a self-contained Sage reference using the actual Sage Python, not
       `/usr/bin/python3`;
     - the fresh pip-installed candidate.
   - Run `tools/sagelite_runtime_manifest.py compare`.
   - Run `tools/run-installed-wheel-doctests.py --runtime-summary` for targeted
     smoke/doctest buckets before attempting another full run.
   - Deliverable: one timestamped `/scratch/sagelite-r2-work/validation-<stamp>`
     directory containing install metadata, manifests, manifest diff, runtime
     summary, smoke logs, and targeted doctest analysis. The validation
     wrapper creates `install-metadata.json` automatically.

2. Prove or fix repaired-wheel native parity in manylinux/CIBW.
   - Verify the repaired wheel contains every prefix from
     `tools/sagelite_native_wheel_catalog.py`.
   - Verify every required native import module imports from outside the source
     tree with no `LD_LIBRARY_PATH`.
   - Investigate the current `sage.libs.braiding` undefined-symbol failure.
   - Confirm auditwheel bundles or policy-allows libraries including
     `libbrial`, `libbrial_groebner`, `libbraiding`, `libhomfly`,
     `libcoxeter3`, `libbliss`, `libcliquer`, `libmtx`, and `libsirocco`.
   - Stop here if this fails: companion runtime work is less useful until the
     core wheel imports reliably.

3. Fix compiled-module source-path leakage.
   - Use the manifest `source_inspection` failures for
     `sage.rings.integer`, `sage.rings.rational`, `sage.libs.homfly`, and
     similar modules as the starting set.
   - Determine whether the source paths come from Cython debug/source metadata,
     generated extension metadata, or Sage inspection assumptions.
   - Add or extend an installed-wheel test that runs from `/scratch` and asserts
     representative `sage_getfile_relative()` results are package-relative or
     otherwise intentionally normalized.

4. Fix GAP/GUAVA host leakage and completeness.
   - Ensure the pip runtime prepends sagelite GAP roots before system GAP roots.
   - Decide and implement one behavior for GUAVA:
     - package executable `wtdist` in the companion wheel; or
     - mark GUAVA unavailable when package data is present but `wtdist` is
       missing.
   - Targeted proof:
     - `libgap.LoadPackage("guava")`;
     - `libgap.DirectoriesPackagePrograms("guava")`;
     - executable check for `wtdist`;
     - one Sage `weight_distribution(algorithm="leon")` example.
   - Success means no `/usr/share/gap` or `/usr/lib/gap` paths appear in the
     candidate manifest unless they are deliberately allowed and documented.

5. Fix Maxima/ECL runtime parity before symbolic doctests.
   - Remove build-prefix leakage such as `current-build-prefix/lib/ecl/maxima.fas`
     from installed runtime state.
   - Ensure `MAXIMA_PREFIX`, `MAXIMA_FAS`, `MAXIMA_USERDIR`, `ECLDIR`, and
     library-mode lookup point at the installed sagelite companion runtime or at
     a documented system dependency, never a build tree.
   - Targeted proof:
     - `maxima.help("gcd")`;
     - `maxima.example("arrays")`;
     - `maxima_lib.sr_integral` examples involving assumptions;
     - the calculus examples that currently produce `cases(...)` or crash.

6. Fix fpylll/fplll strategy-data portability.
   - Determine definitively whether installed fpylll can be redirected to
     `sagelite-fplll-data` at runtime.
   - If yes, centralize that setup during Sage initialization and add a smoke
     test for the resolved strategy file.
   - If no, plan a sagelite-controlled fpylll wheel or another packaging-level
     fix. Do not rely on `/project/local` symlinks.
   - Then re-run the known LLL/SVP/projective rational point examples.

7. Fix FriCAS conversion runtime failures.
   - Compare executable, prefix, startup files, Lisp backend, and environment
     variables between self-contained and pip environments.
   - Targeted proof:
     - factorization converted back to Sage;
     - `fricas("sol.basis").sage()`;
     - `fricas_translator` polynomial ring and factorization conversions.

8. Prove msolve parser diagnostics and fix remaining ordering failures.
   - Done: parse through diagnostic lines such as
     `Restarting with another random linear form`.
   - Done: replace `UnboundLocalError` paths with useful errors that include
     raw output.
   - Re-run the current failing examples in a repaired-wheel environment.
   - Only then update doctests for ordering by comparing normalized structures.

9. Clean up remaining external verbose-path and numeric-version buckets.
   - qepcad: ensure command strings use the resolved sagelite executable path,
     not `SAGE_LOCAL` assumptions.
   - LattE/graphviz/dot2tex: compare versions and output formats against the
     reference manifest before changing doctests.
   - Normaliz/polyhedron numeric failures: decide whether differences are
     dependency-version drift or precision bugs, then use tolerances only for
     verified equivalent results.

10. Reduce analyzer `unknown` using the new full-run evidence.
    - Add fingerprints only for repeated root causes with clear evidence.
    - Keep the report focused on packaging/runtime fixes first and doctest
      robustness second.

11. Only after runtime parity gaps are closed, edit brittle doctests.
    - Prefer structural comparisons, sorted outputs, invariants, or tolerances.
    - Do not mark real missing runtimes, crashes, source leakage, or parser
      errors as acceptable doctest variance.

12. Final validation.
    - Fresh venv, wheels only, no repository cwd, no `LD_LIBRARY_PATH`, no
      manual file copying, no `/project/local` symlink.
    - `pip check`.
    - Manifest compare.
    - Native and companion smoke tests.
    - Targeted doctests for every recently fixed bucket.
    - Full installed doctests.

## Known hard problems

- Manylinux proof is mandatory. Local raw-wheel success is useful for debugging
  but cannot prove published-wheel parity.
- Maxima/ECL failures are high-risk because runtime packaging drift can look
  like harmless symbolic-output drift.
- fpylll strategy paths may require a packaging-level decision if upstream does
  not support reliable runtime relocation.
- Compiled-module source-path leakage may require build-system or Sage
  inspection changes rather than simple packaging metadata tweaks.
- GAP package data and GAP executable/program directories have multiple path
  layers; fixing only `GAP_ROOT_PATHS` may not be enough.
- Doctest robustness edits are easy to overuse. Keep them behind manifest and
  smoke-test evidence.
