# Sagelite macOS arm64 CPython 3.13 Validation

## 2026-07-16 MeatAxe Post1 Binary Tables

Exact pushed source `5e95484667db6d37d7c214935e559c692c1230d2`
(`10.9.post44`) fixes the deterministic MeatAxe failure from the `post43`
strict gate. The retained `sagelite-meataxe-runtime==10.9` wheel was only
17,637 bytes because all 69 purported multiplication tables were 26--28 byte
text fixtures of the form `synthetic table for GF(...)`. They came from the
generic companion CI job, whose file-presence-only build and smoke checks let
the fixture wheel enter the macOS closure. SharedMeatAxe then diagnosed a
corrupt table in `kernel-0.c` and segfaulted when native code consumed it.

The companion now validates the SharedMeatAxe 1.0.2 binary contract at build
time and runtime: each table is 139,364 bytes, declares the expected field and
characteristic, and uses format version 6. Companion CI builds the
repository-pinned SharedMeatAxe source and generates real tables with `zcv`.
The selftest validates and confirms the active companion directory before it
constructs a native matrix. The corrected artifact uses a new versioned
filename, and the primary requirement now excludes the fixture version:

```text
sagelite_meataxe_runtime-10.9.post1-py3-none-macosx_14_0_arm64.whl
  1,251,006 bytes
  fff1a3ee7f903896c8bb9d579a537626543188f0d8663f17158e57c4f814d317
```

The exact committed source was transferred with `git archive` and built from
the retained `post43` native prefix. All 69 wheel payloads are byte-identical
to that prefix's generated tables. A fresh CPython 3.13 venv installed the
companion wheel alone using `--no-index --no-deps`, passed `pip check`, and
passed its complete runtime table validator. Installing that exact artifact
into the already-failed `post43` diagnostic venv was not acceptance evidence,
but it proved native integration: one MeatAxe matrix over every supported
field from GF(2) through GF(251) succeeded.

A complete selftest invocation also reached and passed the MeatAxe probe, and
lrslib passed on this invocation. It then exposed the next independent
failures. Sympow could not find `P02L` in `param_data` and returned an
unexpected result. QEPCAD subsequently crashed, restarted, and hung with a
Singular child; after a process snapshot, only that invocation's process tree
was terminated, so the recorded exit 143 is not a selftest-pass claim. The
strict short gate was not rerun, the full gate was not started, and nothing
was published.

The public `dev/manifest.json` remains unchanged at 177 wheels generated on
2026-07-09, including fourteen primary wheels. Durable exact-source artifacts
are under the following matching builder and controller paths:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-meataxe-20260716-034452-5e95484667d/
/scratch/sagelite-automation/macos-arm64-cp313-meataxe-20260716-034452-5e95484667d/
```

The directory contains the source archive extraction, build log, wheel and
SHA-256 inventory, payload audit, fresh install and `pip check`, runtime smoke,
and the all-field diagnostic result. The earlier non-authoritative diagnostic
run retains the complete selftest log and process snapshot. Its failed,
diagnostically modified 19 GiB venv was removed after preserving that evidence.
`m1` now has 99 GiB free, still just below the 100 GiB threshold for a coherent
`post44` primary rebuild but above the threshold for focused companion and
test-only work.

## 2026-07-16 Post43 Unified ECL Runtime and Strict Short Gate

Exact pushed source `d75dd63d01100c3051596137cdaa60a210078dbd`
(`10.9.post43`) makes the Maxima companion own the one installed ECL runtime.
The primary-wheel repair excludes ECL from general delocation and rewrites
every primary consumer to the companion's exact loader-relative
`libecl.24.5.dylib`; the redundant `sagelite.libs/libecl` copy is absent.
The macOS selftest now enumerates loaded images through dyld instead of the
Linux-only `/proc/self/maps` path. Focused controller validation passed 46
tests, and an exploratory repair of the retained `post42` input audited 1,176
dependencies across 637 Mach-O files with the intended single ECL path.

An exact controller archive with SHA-256
`21b501e91a9b62f6908271c7b160eebb8624a8dca594dd5112fa6b65fd3976c9`
reproduced source tree `69bc5914ecf36be524e8edae4c2fa97442786776` on
`m1`. The first native build reached 1,791 of 1,795 steps before a transient
Maxima external-project failure; a preserved retry from the same source and
native prefix passed Maxima and completed. The repaired primary is:

```text
sagelite-10.9.post43-cp313-cp313-macosx_26_0_arm64.whl
  97,422,309 bytes
  3088fa8d8b8ee7056731f5a99a845df5ddba41c45c677c6fe3590cff4dd6bc2d
```

Repair rewrote 23 companion dependencies in 16 Mach-O files and audited 1,176
dependencies across all 637 Mach-O files. The complete strict closure contains
179 wheels: one primary, 68 Sagelite companions, and 110 third-party wheels.
Its exact staged byte count is 13,889,866,225 and its inventory digest is
`8da88028c2ebd64c0797fb91c73cbcbc33d6b4c85b3239a306adbb2ff8e62724`.
Strict macOS preflight accepted every wheel, and a fresh CPython 3.13.14 venv
installed `sagelite[all-needed-extras]==10.9.post43` solely from that closure.
`pip check` passed, all runtime-leak counters were zero, all required native
imports passed, and `sage.all` imported. Crucially, Maxima library mode returned
`2` and symbolic integration returned `-cos(x)`, proving the duplicate-ECL
abort from `post42` fixed.

The strict short gate is not a pass. It exited 21 after 1,943 seconds. Selftest
returned `-11`: `lrsnash` first exited through SIGTRAP on its trivial feature
input, then the MeatAxe probe reported a corrupt table in `kernel-0.c` line 336
and segfaulted. The lrslib result is intermittent rather than an established
wheel defect: the same installed executable and input passed 100 consecutive
isolated probes and passed when probed after each preceding selftest stage,
while two complete selftest invocations reproduced SIGTRAP. The MeatAxe failure
is deterministic and is the next coherent runtime class to diagnose.

The installed `--optional=sage --short 600 -p 8` sweep saw 3,955 modules and
reported 36 failed. Two were direct failed examples: the ECL pre-`sig_on`
SIGINT test raised `RuntimeError: Aborted` instead of `KeyboardInterrupt`, and
the Singular interrupt probe returned false. The other 34 processes were
killed by segmentation fault; reduced analysis labels these as timeouts, but
the raw log explicitly records the signals. Five QEPCAD processes and their
Singular children were observed after escaping their doctest workers; four
remained active for more than ten minutes. After an exact process snapshot,
only those run-owned QEPCAD processes were terminated so the reducer could
finish. Packaged pytest then passed 212 tests with 5 skips. These signal,
interrupt, and teardown findings remain independent follow-up classes; the
full gate was not started.

The public preview manifest remains unchanged at 177 wheels generated on
2026-07-09, including fourteen primary wheels. Nothing was published. Durable
controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260716-021120-d75dd63d011/
```

The matching `m1` directory retains the exact source, persistent native build,
wheelhouse, failed clean-install validation, and focused diagnostics. Important
files include `short-exit-code`, `short-command.log`, the validation summary,
runtime summary, selftest log, reduced analysis, the selftest retry and lrslib
state-transition logs, and the QEPCAD leaked-process snapshot. Free space was
80 GiB after retaining this latest unresolved run.

## 2026-07-16 Post42 Strict Short Gate

Exact pushed source `7827eb8b2f489bf4db4a71e1adfd4de341203276`
produced the coherent `post42` primary after rebuilding the repository-pinned
FFLAS-FFPACK 2.5.0 source with the same Homebrew Clang 22 toolchain used for
Sagelite. The repaired wheel is:

```text
sagelite-10.9.post42-cp313-cp313-macosx_26_0_arm64.whl
  98,566,869 bytes
  77e16b5bd077becd5ee557ce3e0bbc74e02816e5af4c79ae793384bb8b16b1af
```

Repair audited 1,180 load dependencies across 638 Mach-O files and rewrote 23
companion paths in 16 files. The rebuilt bundled `libffpack.1.dylib` exports
the exact C++ symbol required by `sage.libs.linbox.linbox_flint_interface`.
A focused neutral-environment probe imported that module and computed the
determinant of `[[1, 2], [3, 4]]` as `-2`, proving that this iteration fixed
the primary FFPACK ABI failure exposed by `post41`.

The complete local wheelhouse contained 179 valid wheels: one primary, 68
Sagelite companions, and 110 third-party wheels. Its staged size was
13,891,010,785 bytes and its inventory digest was
`66e7064c0d6096354178cb2875fefa13cf90a43488340b2ff7ccb8853fe8b196`.
Exact pushed validator source
`883d55cadd48578c26c3056c1bca262c5eff6221` normalized the macOS `arm64`
platform suffix to the host's `aarch64` alias; all 44 validator tests passed.
The authoritative strict gate then accepted every filename and tag, installed
`sagelite[all-needed-extras]==10.9.post42` into a fresh CPython 3.13.14 venv
using only that wheelhouse, and passed `pip check`. Runtime collection found no
dependency, executable, Python-path, source-path, or GAP host leak. All 17
required native imports, `sage.all`, integer factorization, and the repaired
LinBox path passed.

The strict short gate nevertheless failed with exit code 250 after 1,465
seconds. Its first remaining coherent failure class is Maxima/ECL runtime
selection on macOS. `sagelite-selftest` reported that `maxima.fas` requires
`FEstack_advance` but found no loaded ECL library, then the symbolic integration
probe aborted. The diagnostic itself is incomplete on macOS because
`_loaded_libecl_paths()` only examines Linux `/proc/self/maps`: direct symbol
audits prove that the ECL libraries bundled by `sagelite-ecl-runtime`,
`sagelite-maxima-runtime`, and `cypari2` all export `FEstack_advance`. A focused
neutral symbolic-integration run still aborted with status 134, and its dyld
trace showed both the `cypari2` and Maxima companion ECL paths being selected.
The next iteration must make ECL selection coherent and make the selftest
inspect loaded dylibs correctly on macOS before rebuilding the primary.

The aborted installed sweep reached 3,955 modules. Reduced analysis classified
609 as failed: 606 timeouts caused by the abort, two optional-native findings,
and one independently actionable core failure where a runtime Cython example
could not find `gsl/gsl_cblas.h`. These are not a short-pass claim and should
be re-evaluated only after the earlier Maxima/ECL class is fixed. The full gate
was not started, and nothing was published.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
Durable controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260716-010555-7827eb8b2f4/
```

The matching `m1` directory retains the exact source/build inputs, complete
wheelhouse, and validation evidence. The 19 GiB disposable failed-install venv
was removed after its artifacts were copied; free space returned to 101 GiB.

## 2026-07-15 Portable ImageMagick Companion

Exact pushed source `b4fb12e6c624c184367d0a1f5e668f3925b7f253`
made the ImageMagick companion portable on macOS. The package builder now
discovers Homebrew's unversioned ImageMagick module layout, scans the main
executables and every coder and filter module for their complete recursive
non-system dylib closure, rewrites all Mach-O load paths relative to their
packaged locations, and ad-hoc signs the repaired binaries. The packaged
libtool modules use relocatable uninstalled metadata and `.libs` storage so
they no longer redirect runtime loading to the Homebrew Cellar. The Linux
`ldd` packaging path and its explicit `LD_LIBRARY_PATH` wrapper remain
unchanged, while the macOS wrapper needs no library-path environment variable.
Focused repository validation passed 2 tests. The complete companion metadata
file had 256 passes and the same 3 pre-existing failures involving generated
Flatter egg-info and the Regina dependency expectation.

The exact pushed revision packaged Homebrew ImageMagick 7.1.2-27 and produced:

```text
sagelite_imagemagick_runtime-10.9.post3-py3-none-macosx_26_0_arm64.whl
  8,614,326 bytes
  a61df79f206166ed9c94841c3218f4868b18c9174f8a2dc3b4a50eef715776f1
```

Its embedded name, version, and wheel tag match the filename. An exhaustive
audit covered all 149 Mach-O files and 1,150 load dependencies and found no
disallowed, unresolved, or escaping load path. A fresh CPython 3.13.14 venv
installed the wheel using only its local wheelhouse and passed `pip check`.
The shared companion smoke resolved both packaged entry points, reported the
bundled ImageMagick version, and converted a generated PPM image through PNG
to GIF from a neutral environment with no inherited library path.

The exploratory build first exposed Homebrew's `lib/ImageMagick/modules-*`
layout, then showed that installed libtool metadata would load modules and a
second MagickCore from absolute Cellar paths even after Mach-O repair. Those
diagnostics are preserved separately; the authoritative exact-source run
completed with exit code zero.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
This artifact was not published. Every previously missing
`all-needed-extras` companion distribution now has a compatible local wheel,
but they were built from successive exact commits. No strict complete-Sagelite
installation, `sagelite-selftest`, short run, full run, or publication result
is claimed. Final cell validation must rebuild the primary from the selected
current coherent revision, assemble its complete closure, and run the named
strict short and full gates.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-imagemagick-20260715-234707-b4fb12e6c62/
```

The matching `m1` directory retains the exact detached source, Homebrew input,
wheel, clean install, unpacked audit tree, and build log. Important successful
evidence includes `wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`,
`validation/strict-macho-audit.txt`, the install, `pip-check`, and smoke
outputs, `run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable FriCAS Companion

Exact pushed source `a754d6ae457c7e23a89f884da0eb7194855926a5`
made the FriCAS companion portable on macOS. The package builder now scans
the complete FriCAS runtime tree for Mach-O files, bundles every non-system
dylib in their recursive closure, rewrites load paths relative to the
packaged files, and ad-hoc signs the repaired binaries. FriCAS' `FRICASsys`
executable has a saved SBCL core appended after its Mach-O image; its repair
temporarily detaches the core while Apple tooling processes the Mach-O prefix
and then consumes existing alignment padding so the core retains its original
absolute file offset. Focused repository validation passed 4 tests. The
complete companion metadata file had 256 passes and the same 3 pre-existing
failures involving generated Flatter egg-info and the Regina dependency
expectation.

The exact pushed revision reused the native FriCAS input built by exact source
`24b5e7aec6db357933703de8a425f10ab4fb0e79` and produced:

```text
sagelite_fricas_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  41,691,889 bytes
  a489f14bacd1d42a860f555163869e4ce37cafaaccf85fea210f220e6c76e56c
```

Its embedded name, version, and wheel tag match the filename. An exhaustive
audit covered all 24 Mach-O files and 76 load dependencies and found no
disallowed, unresolved, or escaping load path. A fresh CPython 3.13.14 venv
installed the wheel using only its local wheelhouse and passed `pip check`.
The shared companion smoke resolved the packaged command, and a neutral
functional smoke started the bundled FriCAS 1.3.12 runtime and factored
`x^2 - 1` as `(x - 1)(x + 1)` with exit code zero.

The first exploratory build established that unmodified Apple tooling rejects
the appended-core executable because `__LINKEDIT` does not cover the physical
end of the file. The first exact-source wheel then passed its strict Mach-O
audit, installation, `pip check`, and shared smoke, but the stronger
arithmetic smoke found that growing the repaired Mach-O prefix had shifted the
aligned SBCL core. Both failed runs are preserved; the final exact-source run
kept the core offset and completed with exit code zero.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
This artifact was not published. The remaining `all-needed-extras` companion
closure is now one distribution: `sagelite-imagemagick-runtime`. No strict
Sagelite installation, `sagelite-selftest`, short run, full run, or
publication result is claimed. Final cell validation must still build the
ImageMagick companion and rebuild the primary from the selected coherent
revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-fricas-20260715-231810-a754d6ae457/
```

The matching `m1` directory retains the exact detached source, native input,
wheel, clean install, audit tree, and diagnostic runs. Important successful
evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/strict-macho-audit.txt`, the
install, `pip-check`, shared-smoke, and arithmetic-smoke outputs,
`run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable GNU Info Companion

Exact pushed source `af6c607fe0a648aa5771abd503c2a564371cc27a`
made the GNU Info companion portable on macOS. The package builder now
discovers the complete non-system dylib closure of the Info executable, copies
that closure beside the executable, rewrites dependencies and install IDs to
loader-relative paths, and ad-hoc signs all modified Mach-O files. The Linux
`ldd` packaging path remains unchanged. Focused repository validation passed
5 tests. The complete companion metadata file had 255 passes and the same 3
pre-existing failures involving generated Flatter egg-info and the Regina
dependency expectation.

The exact pushed revision used the native arm64 Info executable built by exact
source `24b5e7aec6db357933703de8a425f10ab4fb0e79`. It paired that executable
with the platform-independent documentation payload from the hash-verified
public aarch64 `10.9` companion and produced:

```text
sagelite_info_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  3,688,282 bytes
  6cc8fc5fc9ad607d4e62b7bfd40e34936dd0f6fe49de26b5f76bfc8eee72a89c
```

Its embedded name, version, and wheel tag match the filename. An exhaustive
audit covered its arm64 Mach-O executable and both load dependencies, finding
only allowed system libraries and no disallowed, unresolved, or escaping load
path. A fresh CPython 3.13.14 venv installed the wheel using only its local
wheelhouse and passed `pip check`. The shared companion smoke resolved the
packaged executable and documentation directory and successfully rendered the
Singular `groebner` Info node from a neutral environment.

The first durable launcher encountered the macOS `nohup` console-detach error
before cloning began. The recovered zsh-disowned process ran the unchanged
script to completion, and the final run exit code is zero. The diagnostic and
recovery are both preserved in the command log and run metadata.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
This artifact was not published. The remaining `all-needed-extras` companion
closure is now two distributions: `sagelite-fricas-runtime` and
`sagelite-imagemagick-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those two companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-info-20260715-223419-af6c607fe0a/
```

The matching `m1` directory retains the exact detached source, reconstructed
native input, wheel, clean install, and audit tree. Important evidence includes
`wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`,
`validation/macho-inventory.txt`, `validation/strict-macho-audit.txt`, the
install, `pip-check`, and shared-smoke outputs, `run-metadata.txt`,
`command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable Kenzo Companion

Exact pushed source `d0f1d2296ea6102fded60a0bfedc97f0fd2cde82`
made the Kenzo companion portable on macOS. The package builder now discovers
the complete non-system dylib closure of `kenzo.fas`, copies the ECL, GMP, and
garbage-collector libraries beside the image, rewrites every dependency and
install ID to a loader-relative path, and ad-hoc signs all modified Mach-O
files. The Linux packaging path remains unchanged. Focused repository
validation passed 2 tests. The complete companion metadata file had 254 passes
and the same 3 pre-existing failures involving generated Flatter egg-info and
the Regina dependency expectation.

The exact pushed revision reused the Kenzo native input built by exact source
`24b5e7aec6db357933703de8a425f10ab4fb0e79` and produced:

```text
sagelite_kenzo_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  1,939,066 bytes
  e8e08c74b79756e4e41d7ce2489df7327909c8b182ab7cae71454ec8e59155af
```

Its embedded name, version, and wheel tag match the filename. An exhaustive
audit covered all 4 Mach-O files and 14 load dependencies and found no
absolute, unresolved, or escaping load path. A fresh CPython 3.13.14 venv
installed the wheel using only its local wheelhouse and passed `pip check`.
The shared companion smoke resolved the installed Kenzo image, and a second
neutral-environment functional smoke successfully loaded both the bundled ECL
library and `kenzo.fas` with `dlopen`.

The initial durable wrapper completed the build and audit but gave pip a wheel
basename relative to the wrong directory. The recovered fresh install used the
unchanged hash-verified absolute wheel path. Its first smoke invocation also
omitted the shared script's required import selector; rerunning that smoke
against the unchanged install completed successfully. Both wrapper diagnostics
are preserved, and the final run exit code is zero.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
This artifact was not published. The remaining `all-needed-extras` companion
closure is now three distributions: `sagelite-fricas-runtime`,
`sagelite-imagemagick-runtime`, and `sagelite-info-runtime`. No strict Sagelite
installation, `sagelite-selftest`, short run, full run, or publication result
is claimed. Final cell validation must still build those three companions and
rebuild the primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-kenzo-20260715-220513-d0f1d2296ea/
```

The matching `m1` directory retains the exact detached source, native input,
wheel, clean install, and audit tree. Important evidence includes
`wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`,
`validation/macho-inventory.txt`, `validation/strict-macho-audit.txt`, the
install, `pip-check`, shared-smoke, and `dlopen` outputs, `run-metadata.txt`,
`command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable 4D Polytope Database Companion

Exact pushed source `b70bf3d81af5422508b5fb255b3c6560eb44fadf`
produced the platform-independent 4D reflexive-polytope database wheel:

```text
sagelite_database_polytopes_4d-10.9-py3-none-any.whl
  9,100,370,523 bytes
  e22d60ebd324d848871f0980a7e48226396b5ed5ebecab23f8e1b5482b6438f2
```

Its embedded name, version, and `py3-none-any` wheel tag match the filename.
The inventory contains 17,981 members, including 17,975 non-directory files
under `Hodge4d`. A fresh CPython 3.13.14 venv installed the wheel using only
its local wheelhouse and passed `pip check`. A neutral-environment functional
smoke imported `sagelite_database_polytopes_4d`, resolved all three packaged
data paths, found a populated `Hodge4d` directory, and confirmed the
`reflexive_polytopes` Sage data-path entry point.

The recovered durable launcher had completed the wheel build and installation
but initially stopped before recording an exit code: it passed
`SAGELITE_COMPANION_IMPORT` instead of the smoke script's required
`SAGELITE_COMPANION_IMPORT_NAME`, and its zsh exit trap assigned the read-only
name `status`. The smoke was resumed against the unchanged installed wheel,
and the run now has exit code `0`; the failed wrapper diagnostic remains in
`command.log` and the recovery is recorded in `run-metadata.txt`.

The directly fetched public `dev/manifest.json` remains unchanged at 177
wheels generated on 2026-07-09, including fourteen Sagelite primary wheels.
This artifact was not published. The remaining `all-needed-extras` companion
closure is now four distributions: `sagelite-fricas-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`, and
`sagelite-kenzo-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those four companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-polytopes4d-20260715-203227-b70bf3d81af/
```

The matching `m1` directory retains the exact source, native input, 8.5 GiB
wheel, clean install, and complete build log. The controller copy retains the
source archive and concise evidence, including `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, the install, `pip-check`, and smoke outputs,
`run-metadata.txt`, disk records, and `exit-code` (`0`).

## 2026-07-15 Portable lrslib, msolve, and QEPCAD Companions

Exact pushed source `300764eac33f8e21cbcf24fddb2edcf241272ea7`
made the lrslib, msolve, and QEPCAD companion builders portable on macOS. The
builders now discover each executable's recursive non-system Mach-O closure,
copy the required dylibs, rewrite executable and dylib references to
loader-relative paths, assign portable install IDs, and ad-hoc sign every
modified Mach-O file. The Linux `ldd` paths are unchanged. Focused repository
validation passed the four portability tests. The complete companion metadata
file had 253 passes and the same 3 pre-existing failures
involving generated Flatter egg-info and the Regina dependency expectation.

The lrslib and msolve wheels reused native inputs built from exact source
`24b5e7aec6db357933703de8a425f10ab4fb0e79`. Their packaging source and the
final exact QEPCAD source `55949b5b79a40e49f69332b186d3a7e1348c1801`
produced:

```text
sagelite_lrslib_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  361,593 bytes
  d5e014b27968214dd0b5ba52921787122c63bb0702c756e86b60ea7ad5f0255c
sagelite_msolve_runtime-10.9.post2-py3-none-macosx_26_0_arm64.whl
  5,276,828 bytes
  382b07cb8bc1719949a44feb5c23e52b3abf6753b75e0e58e021c1f4058475fb
sagelite_qepcad_runtime-10.9.post3-py3-none-macosx_26_0_arm64.whl
  527,740 bytes
  4c17e33df1a16d8b4cc6df6a20a62caf651baced655c19d15bdfc4ee77a5f081
```

Their embedded names, versions, and wheel tags match the filenames. The
exhaustive audits covered 4 Mach-O files and 11 dependencies for lrslib, 6 and
23 for msolve, and 2 and 6 for QEPCAD: 12 Mach-O files and 40 dependencies in
total, with no absolute, unresolved, or escaping load path. Fresh CPython
3.13.14 venvs installed each wheel using only its local wheelhouse and passed
`pip check`. Neutral-environment functional smokes located both `lrs` and
`lrsnash`, exercised `msolve`, and started QEPCAD three independent times,
requiring its banner and first prompt after piped input reached EOF. The final
QEPCAD validation exit code is zero.

QEPCAD required a native input correction in addition to wheel repair. Its
legacy character reader redirected EOF to `/dev/tty`; with piped input it
could wait on a controlling terminal or recursively read an invalid terminal
descriptor. The patched `1.74.p10` input path preserves EOF for noninteractive
standard input, guards a failed terminal open, preserves integer EOF sentinels
in the configuration parsers, and exits before SACLIB's newline discard loop.
The final patch passed both GNU `patch --fuzz=0` and macOS BSD `patch` checks.
The preceding per-SHA runs preserve the initial timeout, unsafe teardown,
terminal-fallback, patch-context, and missing-declaration diagnostics rather
than treating intermittent crashes as successful smokes.

The public manifest was rechecked with a pip user agent and remains unchanged:
generated 2026-07-09, 177 wheels, and fourteen Sagelite primary wheels. These
artifacts were not published. This reduces the missing `all-needed-extras`
companion closure from 8 distributions to 5:
`sagelite-database-polytopes-4d`, `sagelite-fricas-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`, and
`sagelite-kenzo-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-native-command-20260715-183617-300764eac33/
/scratch/sagelite-automation/macos-arm64-cp313-qepcad-eof-20260715-200855-55949b5b79a/
```

The matching `m1` directories retain the exact sources, native inputs, wheels,
clean installs, audits, smokes, and intermediate diagnostic runs. Important
successful evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/strict-macho-audit.txt`, the
install and `pip-check` files, the companion smoke files, `run-metadata.txt`,
`command.log`, and `exit-code`. The native-command packaging run and final
QEPCAD run both have exit code `0`; the superseded combined validation exit
code remains `1` because it records the original QEPCAD timeout after the
lrslib and msolve validations had passed.

## 2026-07-15 Portable Giac Companion

Exact pushed source `4075521634d7ec628c3dca2c158066a47261f7f6`
made the Giac companion portable on macOS. The builder now discovers Giac's
complete non-system Mach-O closure, including Homebrew GCC dependencies
expressed through `@rpath`, copies that closure, rewrites executable and dylib
references to loader-relative paths, assigns portable install IDs, and ad-hoc
signs every modified Mach-O file. The Linux `ldd` path is unchanged. The
shared companion smoke now accepts Giac's numeric-only macOS version output
and requires a successful arithmetic calculation. Focused repository
validation passed 4 tests. The complete companion metadata file had 252
passes and the same 3 pre-existing failures involving generated Flatter
egg-info and the Regina dependency expectation.

The exact pushed revision reused the Giac native input built by exact source
`24b5e7aec6d` and produced:

```text
sagelite_giac_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  25,360,869 bytes
  15c8ba839d67bd64b00f0e0a17a45627484e362fbe1b5799838662e7c651557f
```

Its metadata and wheel tag match the filename. An exhaustive audit covered
all 20 Mach-O files and 71 load dependencies and found no absolute,
unresolved, or escaping load path. A fresh CPython 3.13.14 venv installed the
wheel using only the local wheelhouse, passed `pip check`, and completed the
version and arithmetic smokes from a neutral environment with no inherited
Sage or Homebrew path. The validation exit code is zero. The public manifest
was rechecked with a pip user agent and remains unchanged at 177 wheels and
fourteen Sagelite primary wheels; this artifact was not published.

This reduces the missing `all-needed-extras` companion closure from 9
distributions to 8: `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-imagemagick-runtime`,
`sagelite-info-runtime`, `sagelite-kenzo-runtime`,
`sagelite-lrslib-runtime`, `sagelite-msolve-runtime`, and
`sagelite-qepcad-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-giac-20260715-180928-4075521634d/
```

The matching `m1` directory retains the exact detached source checkout,
native input reference, wheel, clean install, and audit tree. Important
evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/strict-macho-audit.txt`,
`validation/install.txt`, `validation/pip-check.txt`,
`validation/smoke.txt`, `run-metadata.txt`, `command.log`, and `exit-code`
(`0`).

## 2026-07-15 Portable CSDP Companion

Exact pushed source `099c31b802a9d02557076228f6651afbb2af60ad`
made the CSDP companion portable on macOS. The package builder now discovers
the complete non-system Mach-O closure of `theta`, including Homebrew GCC
runtime dependencies expressed through `@rpath`, copies that closure, rewrites
all executable and dylib references to loader-relative paths, assigns portable
install IDs, and ad-hoc signs every modified Mach-O file. The existing Linux
`ldd` path is unchanged. Focused repository validation passed 2 tests; the
complete companion metadata file had 251 passes and the same 3 pre-existing
failures involving generated Flatter egg-info and the Regina dependency
expectation.

The exact pushed revision reused the CSDP native input built by exact source
`24b5e7aec6d` and produced:

```text
sagelite_csdp_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  827,120 bytes
  a5ba39d47c55ceec24ce841983405dbb4f1ac12dd790e817b1b7d127a786ecaf
```

Its metadata and wheel tag match the filename. An exhaustive audit covered all
5 Mach-O files and found no absolute, unresolved, or escaping load path. A
fresh CPython 3.13.14 venv installed the wheel using only the local wheelhouse,
passed `pip check`, and completed a functional Lovasz theta-number smoke from
a neutral directory with no inherited Sage or Homebrew path. The validation
exit code is zero. The public manifest was rechecked with a pip user agent and
remains unchanged at 177 wheels and fourteen Sagelite primary wheels; this
artifact was not published.

This reduces the missing `all-needed-extras` companion closure from 10
distributions to 9: `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-giac-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`,
`sagelite-kenzo-runtime`, `sagelite-lrslib-runtime`,
`sagelite-msolve-runtime`, and `sagelite-qepcad-runtime`. No strict Sagelite
installation, `sagelite-selftest`, short run, full run, or publication result
is claimed. Final cell validation must still build those companions and
rebuild the primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-csdp-20260715-173818-099c31b802a/
```

The matching `m1` directory retains the exact detached source checkout, native
input reference, wheel, clean install, and audit tree. Important evidence
includes `wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`,
`validation/macho-inventory.txt`, `validation/strict-macho-audit.txt`,
`validation/install.txt`, `validation/pip-check.txt`, `validation/smoke.txt`,
`run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Giac System-BLAS Build Ordering

Exact pushed source `24b5e7aec6db357933703de8a425f10ab4fb0e79`
fixes the first failure in the remaining-native-companion batch. Giac's
package metadata did not declare either the selected BLAS implementation or
the conditional system pkg-config facade targets, even though Giac configure
unconditionally requires `lapack.pc`. On this Homebrew system, explicit
`make giac` therefore bypassed the facade that maps the accepted system
OpenBLAS installation to BLAS, CBLAS, and LAPACK pkg-config names.

The fix declares both `$(BLAS)` and `$(PCFILES)`. In a fresh exact-source run,
the generated dependency graph retained both abstractions, created
`prefix/lib/pkgconfig/lapack.pc` as a symlink to Homebrew's `openblas.pc`, and
built and installed Giac 1.9.0.15p0 successfully. The preceding failed run at
exact pushed source `15a6f69795d9169cc02e95b6b768a8ad16e87609`
is preserved and shows the original `Package 'lapack' not found` configure
failure. The public manifest was rechecked with a pip user agent and remains
unchanged at 177 wheels and fourteen Sagelite primary wheels.

This resolves the native Giac build blocker only. No Giac companion wheel,
Mach-O repair, isolated smoke, strict Sagelite installation, short run, full
run, or publication result is claimed yet. The exact-source native-input run
continues durably under:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-remaining-native-20260715-170825-24b5e7aec6d/
```

Important completed evidence includes `run-metadata.txt`,
`validation/source-status.txt`,
`validation/giac-generated-dependencies.txt`, `validation/lapack-pc.txt`,
`validation/lapack-pc-target.txt`, `validation/giac-built-at.txt`, and
`command.log`. The ten-distribution macOS companion closure count is unchanged
until repaired wheels pass their audits and isolated smokes.

## 2026-07-15 Portable Command Companion Batch

Exact pushed source `2df580c98da3f01a41ad4232542c91673cbc33d2`
made the LiE companion portable on macOS by copying its non-system Readline
dylib, rewriting both the executable dependency and dylib install ID to
loader-relative paths, and ad-hoc signing the modified Mach-O files. Focused
repository validation passed five tests. The native inputs from the preceding
exact-source command build at `5e6a45e7160` were then packaged into six native
macOS arm64 wheels:

```text
sagelite_gap3_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  20,585,435 bytes
  ffc08bcb43eae2e1ee8bac604ffd8af95f0517b09e4812ff093382af8e203883
sagelite_glucose_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  137,687 bytes
  98b4f1d1fdb7ae344dca4688a0d3dbc361f7fde2f8ecf654febe14643dc79e67
sagelite_kissat_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  123,174 bytes
  e4a3737d3157279797647f3b6d14d6e4b43b908cd1bd7ba595f1287e50cfae5d
sagelite_lie_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  889,476 bytes
  701f8da3b95cab38a44f5ad6455d070ce90798b96cde7f314311882452cdb023
sagelite_plantri_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  116,195 bytes
  334cd5e2c06d14ef9a399d17e021116366437712157f7574b2d593a74848568c
sagelite_rubiks_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  192,609 bytes
  b09f6a4ebef1f402c11dbb45eef744c6eff07f5ba1a5da36c1d261b2e31daa40
```

Their embedded metadata and wheel tags match the filenames. An exhaustive
audit covered 97 Mach-O files and found no absolute, unresolved, or escaping
load path. The initial smoke exposed two validation defects rather than wheel
defects: Glucose rejects `-help` and directs callers to `--help`, and the
shared smoke script had no handlers for LiE or GAP3. Exact pushed sources
`701ebbdc8471b8fa42e5eea779be921809ae901d` and
`dd2cf612b014b9973cc68f522ad24efd8fff6827` corrected those protocols and
added deterministic arithmetic probes for LiE and GAP3. Focused repository
validation then passed seven tests.

Exact validation source `dd2cf612b01` installed the unchanged, hash-verified
wheel bytes into six separate fresh CPython 3.13.14 venvs with a neutral
runtime `PATH`. All six isolated smokes passed, including both Glucose
executables, Plantri, Kissat, two Rubiks commands, and arithmetic through LiE
and GAP3. The validation exit code is zero. The public manifest remains
unchanged at 177 wheels; no artifact from this batch was published.

Together with the previously completed Maxima and Planarity wheels, this batch
reduces the missing `all-needed-extras` closure from 16 distributions to 10:
`sagelite-csdp-runtime`, `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-giac-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`,
`sagelite-kenzo-runtime`, `sagelite-lrslib-runtime`,
`sagelite-msolve-runtime`, and `sagelite-qepcad-runtime`. No strict Sagelite
installation, `pip check`, selftest, short run, full run, or publication result
is claimed. Final cell validation must still build those companions and rebuild
the primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-command-companions-20260715-160338-2df580c98da/
/scratch/sagelite-automation/macos-arm64-cp313-command-smoke-20260715-161127-dd2cf612b01/
```

The matching `m1` directories retain the exact source checkouts and fresh
smoke venvs. Important evidence includes both `wheelhouse/SHA256SUMS` files,
the wheel metadata inventory, `validation/macho-inventory.txt`, the empty
`validation/strict-macho-audit.txt`, all six `validation/smoke-*.txt` files,
`run-metadata.txt`, `command.log`, and the final validation `exit-code` (`0`).

## 2026-07-15 Portable Planarity Companion

Exact pushed source `7d63944caeb9c4c0fdcf4c2463db95d7ee97c1a3`
fixed the first failure recovered from the macOS command-companion batch. The
planarity wheel builder had unconditionally invoked Linux `ldd`; on Darwin it
now discovers `libplanarity` with `otool`, copies the dylib, rewrites the
executable dependency and dylib install ID to loader-relative paths, and
ad-hoc signs both modified Mach-O files. The Linux packaging path remains
unchanged. Focused repository validation passed 7 tests; the complete
companion metadata file had 248 passes and 3 pre-existing failures involving
ignored generated egg-info and the separately inconsistent Regina dependency
expectation.

The exact pushed revision then built this native companion wheel on `m1`:

```text
sagelite_planarity_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  95,228 bytes
  5911d9dc3d634ecef7033b71af50988f8cda815472cfd1431ec41756ec236632
```

Its native input was reused from the immediately preceding exact-source
command-companion run at `5e6a45e7160`; that source differs from the wheel's
source only by this packaging repair and its test. The resulting wheel has two
Mach-O files. An exhaustive load-path and install-ID audit found no absolute,
unresolved, or escaping dependency, and a separate fresh CPython 3.13.14 venv
installed the wheel and passed the planarity executable smoke with an empty
environment apart from the required neutral `PATH` and smoke selectors.

This adds one of the 17 previously missing `all-needed-extras` companion
distributions, leaving 16. It does not establish a strict Sagelite install,
`pip check`, selftest, short run, full run, or publication result. Final cell
validation must still assemble all remaining companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-planarity-20260715-153510-7d63944caeb/
```

The matching `m1` directory retains the exact source checkout, build venv, and
unpacked audit tree. Important evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/macho-inventory.txt`, the empty
`validation/strict-macho-audit.txt`, `validation/smoke.txt`, `command.log`,
and `exit-code` (`0`).

## 2026-07-15 Portable Base Companion Batch

Exact pushed source `cc8d999d436a256a42ff70d51963fc4f04bb836b`
completed a native macOS arm64 build of the three base companions that were
missing or below the `post39` primary's dependency floors. The resulting
`macosx_26_0_arm64` wheels are:

```text
sagelite_flatter_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  13,936,429 bytes
  20c09b5c7118a4aa8aa7a309ed6ddf70cfb98c206dced84938b9f15874aa8878
sagelite_graphviz_runtime-10.9.post4-py3-none-macosx_26_0_arm64.whl
  11,651,031 bytes
  ed8300dc724f217f52b0129da7d79a983dc72f225ed41ce19408a37a7757f0a8
sagelite_maxima_runtime-10.9.post15-py3-none-macosx_26_0_arm64.whl
  23,470,010 bytes
  4fc54eeff0d301f74aaac937fee1be2c8626f3d939c9f10b93d5fe7922e0b981
```

All three were installed into separate fresh CPython 3.13.14 venvs with no
inherited Sage or Homebrew path, then passed their companion smoke. Flatter
ran help and lattice-reduction probes, Graphviz ran its executable and plugin
probes, and Maxima evaluated its arithmetic probe through the bundled ECL
image. An exhaustive audit of every Mach-O file in all three wheels found no
non-system absolute load path. The repair work covers recursive Darwin dylib
discovery, Homebrew alias handling, plugin install IDs, loader-relative
Maxima/ECL/GMP/GC references, and the `ecl_min` helper. Focused repository
validation passed 24 tests.

This removes all three base-companion compatibility gaps recorded for
`post39`. It does not complete the cell: 17 distinct `all-needed-extras`
companion distributions still lack compatible macOS wheels. Also, the retained
portable primary was built from `c6c8d1b6665`, so final coherent-revision
validation must rebuild the primary from the selected then-current commit
before strict installation. No clean-install, `pip check`, selftest, short,
full, or publication claim is made. The public manifest remains unchanged at
177 wheels and fourteen primary wheels.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-base-companions-20260715-123539-84b84caad68/
```

The matching `m1` directory retains the build tree. Important evidence
includes `wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`, the three
`validation/smoke-*.txt` files, the empty strict-audit result,
`run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable Primary Wheel and Companion-Closure Blocker

Exact pushed source `c6c8d1b666516434e24793bee92ff57430575442`
(`10.9.post39`) completed a fresh native build on `m1`. The controller-created
source archive had SHA-256
`49783ef08ceaa378c397a8d50001510fd52009f9818fe12e3b3df15edcd99656`.
The controller and `m1` independently reproduced its materialized source tree
`e51552e11c63ee82dad1caedb29550cc1cacc3aa`. An initial source guard compared
that materialized archive tree with the unexported commit tree and stopped
before building; the guard and preserved failure log were corrected to compare
the independently reproduced archive tree before the same archive was used.

The committed general macOS repair now succeeds. The resulting primary wheel
is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-20260715-114613-c6c8d1b6665/wheelhouse/sagelite-10.9.post39-cp313-cp313-macosx_26_0_arm64.whl
```

It is 98,560,684 bytes with SHA-256
`92742b66f1155e8518d8b01103dcd76709fd0b819880f7166b30a66133cb5d8c`.
Its metadata and wheel tag are `10.9.post39` and
`cp313-cp313-macosx_26_0_arm64`. The wheel has 4,986 members, including 638
Mach-O files and 51 general bundled dylibs. The final repair rewrote 23
companion-owned PARI/GMP/MPFR/Singular dependencies in 16 Mach-O files and
audited 1,178 load dependencies across all 638 Mach-O files. The audit found
only system libraries, wheel-contained loader-relative libraries, and the
exact allowed companion-relative library paths; it rejected absolute,
unresolved `@rpath`, and escaping paths. Delocate's permissive scan still logs
expected missing-companion diagnostics before that independent strict audit,
because those companion libraries deliberately do not live in the primary
wheel.

The primary-wheel portability blocker is therefore fixed, but the cell cannot
yet start its required strict clean installation. A CPython 3.13.14 native-tag
probe of the public dev index found no compatible release satisfying 3 of 45
base companion requirements:

```text
sagelite-flatter-runtime >=10.9.post1,<10.10
sagelite-graphviz-runtime >=10.9.post4,<10.10
sagelite-maxima-runtime >=10.9.post15,<10.10
```

The public index has older macOS wheels for each, respectively `10.9`,
`10.9.post3`, and `10.9.post14`. A separate probe found 18 of the 33 Sagelite
companions in `all-needed-extras` without a compatible public wheel. Most have
only Linux wheels; `sagelite-database-polytopes-4d` has no public simple-index
entry, and the Maxima gap overlaps the base set. There are 20 distinct missing
base-or-extra companion distributions. The incomplete 3.7 GiB download probe
was removed after its logs and compatibility inventories were preserved.

No clean-install, `pip check`, selftest, short-doctest, full-doctest, or
publication claim is made. The next macOS CPython 3.13 iteration should build
the 20 missing compatible companion distributions from committed source,
assemble the complete wheelhouse around this primary, and run the named strict
short and full `--optional=sage` gates. Durable controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-114613-c6c8d1b6665/
```

The matching `m1` run retains the wheel and build evidence. Important files
include `command.log`, `exit-code`, `wheelhouse/SHA256SUMS`,
`validation/base-companion-compatibility-probe.txt`, and
`validation/all-needed-companion-compatibility-probe.txt`.

## 2026-07-15 Native Build and Portability Blocker

The next scheduled iteration built exact pushed source
`c978063abdb6c3c14359784be591b635eca63783` (`10.9.post38`) on `m1` from a
controller-created `git archive`. The transferred archive had SHA-256
`471039880fafee2e8564694597c17291024ad910f3b849f2dd0d5fd4efaac5fa`, and
the temporary build repository reproduced canonical source tree
`86bc87b0b9f1a6492267d3db30e4c38945a9eab0`. This avoided building an
uncommitted or independently modified remote checkout.

The native CPython 3.13 compilation completed after two preserved diagnostic
attempts. The first identified five missing native build dependencies and led
to run-local builds of Bliss, Coxeter3, MCQD, MeatAxe, and TDLib. The second
found that an older CPython 3.14 prefix was preceding the CPython 3.13 virtual
environment in `PATH`; correcting that ordering selected NumPy 2.5.0 from the
build environment. The completed intermediate wheel is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-20260715-103605-c978063abdb6/wheelhouse/sagelite-10.9.post38-cp313-cp313-macosx_26_0_arm64.whl
```

It is 67,044,960 bytes with SHA-256
`54071f863141da72099fa71a04bd9ec56b6ac9dafc2dd8b6a6bdd818cc406d00`.
Its metadata has the expected `cp313-cp313-macosx_26_0_arm64` tag, and its
4,934 members include 585 extension modules. Existing Singular and PARI
companion-runtime repairs ran successfully.

This artifact is **not** an installable portable-wheel result. An exhaustive
Mach-O audit found no bundled dylibs and 30 distinct non-system absolute dylib
dependencies. They resolve into the run-local prefix, the older
`/Volumes/sage/sagelite-build/prefix`, or Homebrew. A subsequent standard
`delocate` attempt failed with `DelocationError: Could not find all
dependencies` because the existing companion repairs had already rewritten
PARI/GMP/MPFR references to `@loader_path` locations supplied by separate
companion wheels, which are absent while repairing the primary wheel alone.

The next implementation step is a macOS repair stage that bundles the general
native dependency closure while preserving one authoritative
PARI/GMP/MPFR/Singular runtime from the companion wheels. It must then reject
all remaining non-system absolute dependencies before strict preflight or
installation begins. Running generic delocation before the companion repairs
may duplicate those runtimes, so it is not accepted without an explicit
post-repair audit.

No wheel-built, install-passed, smoke-passed, full-passed, or publication claim
is made for this artifact. In particular, the public `post9` matrix entry
remains unchanged. Durable controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-103605-c978063abdb6/
```

The remote run and its build products remain under the matching path in
`/Volumes/sage/sagelite-automation`. Preserved evidence includes source and
archive hashes, run metadata, both failed build logs, the successful exit
code, the complete Mach-O dependency inventory, the 30-entry absolute
dependency inventory, the primary checksum and size, and the delocation
traceback.

## 2026-07-15 Strict-Profile Preparation

The scheduled matrix iteration first rechecked Linux `x86_64` CPython 3.14.
The required `host` alias still reached an `x86_64` machine without
`/mnt/cocalc-scratch`; `/` had 17 GiB free and `/mnt/cocalc` had 64 GiB free.
That leaves the existing x86_64 heavy-build blocker unchanged. No x86_64
build, validation, or publication was started.

Independent preflight for the next available work-order cell found `m1` idle,
native macOS `arm64`, running macOS 26.4, with Homebrew CPython 3.13 and 181 GiB
free on `/Volumes/sage`. Preserved macOS wheels and doctest logs are from the
earlier `post1`/`post3` work and do not match the current source or companion
dependency floors, so none were promoted to acceptance evidence.

Exact pushed source `718dba53d4005967543dc9e2e103e397b3852dc8`
(`10.9.post38`) adds `--strict-macos-wheelhouse-preflight` to
`tools/validate-sagelite-wheelhouse.py`. The profile requires a primary
`macosx` wheel and applies the complete closure, requested version, companion
version, interpreter, ABI, architecture, and host-compatible platform checks.
It deliberately omits the Linux-only manylinux repair requirement. The
validator also records `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` in install
metadata when the accepted macOS full-suite workaround is explicitly set.

Focused validation passed 43 tests. The commit was pushed to `origin/develop`
and the remote ref was verified at the exact SHA above. Durable controller
artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-100758-718dba53d400/
```

Important files include:

```text
run-metadata.txt
host-preflight.txt
m1-preflight.txt
public-manifest-summary.txt
validation/pytest-validator.log
```

The public manifest remained unchanged at 177 wheels generated on 2026-07-09,
including fourteen Sagelite primaries. No `post38` artifact is public.

No macOS CPython 3.13 wheel-built, install-passed, smoke-passed, or full-passed
claim is made. The cell remains `smoke only`. The next iteration should build
the exact then-current pushed source and its complete macOS arm64 CPython 3.13
wheel closure in a new `/Volumes/sage/sagelite-automation` run, then run the
named strict short gate and full `--optional=sage` sweep.
