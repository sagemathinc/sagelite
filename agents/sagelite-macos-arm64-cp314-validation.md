# Sagelite macOS arm64 CPython 3.14 Validation

## 2026-07-23 Post64 Short Standard Sweep Passed

Read-only reconciliation at `2026-07-23T03:03:37Z` found the guarded fresh
short gate still healthy under tmux session `sagelite_cp314_post64_watch`.
Strict preflight accepted all 168 staged wheels and all 68 requested companion
projects. The fresh binary-only
`sagelite[all-needed-extras]==10.9.post64` installation and `pip check`
passed, the runtime summary reported zero source, Python-path, dependency,
GAP-host-path, or host-executable leaks, and all 102 selftest checks passed.
The installed `--optional=sage` sweep then passed all 3,953 standard modules
with zero failures in 493.5 seconds.

Packaged pytest was still active. Its nested Sage test process was consuming
CPU and the durable log had advanced through 69% of 229 collected items, so
the run was left untouched. `/Volumes/sage` retained 86,640,256 KiB free,
above the 30 GiB test-only threshold. No short-gate exit code or reduced
analysis existed yet, and the separate fresh full gate remains guarded on a
zero short-gate exit. No short or full pass, cell acceptance, or publication
is claimed.

The same reconciliation reached `host` as native Linux `x86_64`, but the
assigned `/mnt/cocalc-scratch` run remained invisible because that path
resolved to the 24,883,167,232-byte root filesystem with only
14,581,669,888 bytes free. The separate `/mnt/cocalc` volume had
78,033,121,280 bytes free, below the binary 100 GiB heavy-build threshold.
The inaccessible authoritative run was left untouched and no duplicate was
launched. A direct public-manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post64` artifact.

## 2026-07-23 Post64 Wheel Built And Strict Validation Started

The exact native build from pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` completed with exit code zero at
`2026-07-23T02:30:50Z`. It produced this repaired primary:

```text
sagelite-10.9.post64-cp314-cp314-macosx_26_0_arm64.whl
  102,367,424 bytes
  3cd67f291d16db570fd642512220daac52a43c9c0135b3e22a00b68d2fb3fc27
```

Repair injected 2,079 native headers, rewrote 23 companion dependencies in
16 Mach-O files, and audited 1,176 dependencies across 637 Mach-O files. The
deterministic closure completed with exit code zero at
`2026-07-23T02:32:42Z`. It contains 168 wheels: one primary, 68 companions,
and 99 third-party wheels totaling 13,890,637,078 bytes. The SHA256 of its
`SHA256SUMS` inventory is
`cc1c05424f3fd1fe6f1904b91abc4f72d9c51e046ab2c717e488be0630175f1e`.
Strict preflight recorded the same wheel count and total bytes, found zero
invalid wheel filenames, and accepted all requested companion projects.

The guarded fresh short gate started immediately under tmux session
`sagelite_cp314_post64_watch`. At the latest `2026-07-23T02:36:23Z`
reconciliation it had created its fresh CPython 3.14 environment, passed
strict wheelhouse preflight, installed the exact binary-only
`sagelite[all-needed-extras]==10.9.post64` closure, and passed `pip check`.
Runtime-manifest collection was active. The separate fresh full gate remains
guarded on a zero short-gate exit. No short or full pass, cell acceptance, or
publication is claimed yet.

The same iteration reached `host` as native Linux `x86_64`, but the assigned
run remained invisible because `/mnt/cocalc-scratch` resolved to the
24,883,167,232-byte root filesystem with 14,570,610,688 bytes free. The
separate `/mnt/cocalc` volume had 78,029,946,880 bytes free, below the binary
100 GiB threshold. The inaccessible authoritative run was left untouched and
no duplicate was launched. The directly fetched public manifest remains the
177-wheel set generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen
Sagelite primary wheels and no `post64` artifact.

## 2026-07-23 Post64 Exact Rebuild Started

The scheduled matrix iteration first reconciled the higher-priority Linux
`x86_64` builder. The `host` alias reached native Linux `x86_64`, but the
required `/mnt/cocalc-scratch` run remained invisible because that path
resolved to the 24,883,167,232-byte root filesystem with only
14,571,065,344 bytes free. The authoritative CPython 3.12 `post64` run was
left untouched, no result was inferred from inactive service properties on
the currently reached machine, and no duplicate x86_64 build was started.
The separate `/mnt/cocalc` volume had 78,018,404,352 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact.

Independent preflight found native macOS and its Linux aarch64 guest idle.
`/Volumes/sage` had 110,031,936 KiB free immediately after the guarded launch,
and the guest had 107,212,017,664 bytes free. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` is now building natively with
Homebrew CPython 3.14.6 under tmux session
`sagelite_cp314_post64_build`; the fail-fast watcher is active as
`sagelite_cp314_post64_watch`. Durable artifacts are at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260723-021858-014ae4bf443
```

The build reuses the intact CPython-independent native prefix from the
accepted CPython 3.13 `post51` run. Its exact 144,131,658-byte source archive
has SHA256
`8029bc4e83392f3ac4a5bed0865511f664b16871350eba2d56be60a8c9f65311`,
and its independently materialized clean tree matches committed tree
`08c39ac15ef341f68af0676dfb4f9b61de0010db`. The recorded environment is
Darwin `arm64` with CPython 3.14.6. At `2026-07-23T02:20:00Z`, both durable
processes remained active and the build log had entered native sdist
configuration. The closure will reuse compatible wheels from the accepted
`post64` CPython 3.13 wheelhouse and will resolve only the incompatible ABI
replacements before independent fresh short and full gates.

This is build-start evidence only. No `post64` CPython 3.14 wheel, validation
pass, cell acceptance, or publication is claimed yet. Before this evidence
edit, the canonical checkout, local tracking ref, and directly queried
`origin/develop` ref were synchronized at
`cbb6cfebdeec3ba48618deb7cbb952aeec0ef4e6`.

## 2026-07-19 Post63 Full Acceptance

The scheduled matrix iteration first reconciled the higher-priority Linux
`x86_64` builder. The `host` alias is reachable and reports native Linux
`x86_64`, but `/mnt/cocalc-scratch` still resolves to its 24 GB root
filesystem with only 15,089,299,456 bytes free. The recorded CPython 3.12
`post60` build and watcher services are inactive with successful service
status, but their bulk run root remains invisible. No x86_64 result was
inferred and no build was started there. The directly fetched public manifest
remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` artifact.

Independent preflight found native macOS and its Linux aarch64 guest idle. A
complete SHA256 recheck of the accepted CPython 3.13 wheelhouse and exact
source archive preceded removal of only that completed run's disposable
source, build, cache, and temporary trees; its strict wheelhouse, archive,
logs, and full-pass evidence remain. This restored 111,792,904 KiB free on
`/Volumes/sage`.

An initial guarded CPython 3.14 launch stopped before compilation because the
superseded `post54` run no longer retained the native-prefix directory named
in its historical metadata. Both build and watcher exited 1, no wheel was
created, and the concise failure evidence is preserved at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260719-060446-16d6d78012a
```

The exact fresh replacement uses the intact CPython-independent native prefix
from the accepted CPython 3.13 `post51` build. Exact pushed `post63` source
`16d6d78012a` then built natively for macOS arm64 CPython 3.14 under tmux
session `sagelite_cp314_post63_build` at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260719-060814-16d6d78012a
```

The exact 144,034,365-byte source archive has verified SHA256
`2c8e167e60ba6d84fbb58fc4e3602f4097d3555aee78a2d29ff3d14017df0a44`.
The materialized source tree matches committed tree
`2f95f24b66612b95bf8b5dc7329dbc1621eb657d`, and the recorded environment is
Darwin `arm64` with CPython 3.14.6. The build completed with exit code zero
and produced this repaired primary:

```text
sagelite-10.9.post63-cp314-cp314-macosx_26_0_arm64.whl
  102,366,502 bytes
  34c1362c36408083be0dfee830af7aad609a708a96f18ed65aa1b8a0e4e63373
```

The first closure attempt stopped immediately because its script tested for
an empty `wheelhouse-resolved` directory before the script's own `mkdir`.
The orchestration wrapper lacked fail-fast behavior and therefore invoked the
short validator against the lone primary; strict preflight rejected all 68
missing companion projects before installation. That rejected attempt remains
preserved as `short-neutral-preclosure-rejected-20260719-062015`.

A guarded resume created the expected empty staging directory and linked 155
compatible wheels, then stopped because the closure command unconditionally
asked pip to download optional `pycryptosat`. Neither PyPI nor the preview
index has a CPython 3.14 wheel for it. The accepted CPython 3.13 closure omits
that project, and deterministic `all-needed-extras` resolution does not select
it. A second guarded resume therefore omitted only that unnecessary download.
It selected a strict closure of 168 wheels: one primary, 68 companions, and 99
third-party wheels totaling 13,890,636,156 bytes. The inventory SHA256 is
`3954c9a2c7ab75ef0b2833b50399025718a44d16c0baac8f4ab371c4f115af12`.

The fresh short gate passed strict macOS wheelhouse preflight with all 68
requested companion projects present, binary-only installation, `pip check`,
runtime isolation with zero leaks, all 102 selftest checks, all 3,953 installed
`--optional=sage` modules with zero failures, and the packaged pytest tests.
The standard sweep took 494.8 seconds, its independent reducer reported zero
failed modules, and the validator exited zero after 1,938.567 seconds. The
separate fresh full gate repeated that contract. Its unrestricted sweep passed
all 3,953 installed modules with zero failures in 788.7 seconds, packaged
pytest passed with 226 passes and 5 skips, and the independent reducer reported
zero failed modules. The full validator exited zero after 2,196.042 seconds;
the full-gate, watcher, and final resume exit artifacts all record zero.

Exact pushed `post63` source `16d6d78012a` is therefore accepted locally for
macOS arm64 CPython 3.14 as the sixth synchronized full-pass cell for this
release-candidate revision. A complete SHA256 recheck passed before deliberate
cleanup removed only the two completed validation installs and homes plus the
disposable source, build, cache, and temporary trees. The strict wheelhouse,
exact source archive, logs, summaries, runtime evidence, and reducer artifacts
remain at the authoritative run path above. Cleanup restored 111,571,288 KiB
free on `/Volumes/sage`.

The Linux x86_64 bulk mount remains absent. The public R2 manifest is still the
177-wheel set generated on 2026-07-09, with no `post63` artifact; nothing was
published by this validation.

## 2026-07-16 Post54 Strict Short And Full Pass

Exact pushed `post54` source `cf0c58f71315735cea2084e026bea6a2e283b27e`,
committed tree `479a86cba51685d4a0b7e7f11740c20900b57d3a`, produced
this repaired CPython 3.14 primary:

```text
sagelite-10.9.post54-cp314-cp314-macosx_26_0_arm64.whl
  102,365,990 bytes
  e893f5be4456e61b15cb7f4fa744da805eae47f4441bb511b1a6326a2a2d786d
```

The exact source archive SHA-256 is
`15007bd65bb35f08e9a1a1208fe3dc3256d4664bfabf5b2c9dab0587e893fb8c`.
Build and repair exited zero after injecting 2,079 headers, rewriting 23
companion-library references, and auditing 1,176 dependencies across 637
Mach-O files. The deterministic strict closure has 168 wheels: one primary,
68 companions, and 99 third-party wheels totaling 13,890,635,644 bytes. Its
inventory digest is
`a7b168c35f613d5506ec8e97ad235fd3f2fc9e19de022a95de00e2307472054c`.

The independent neutral-environment strict short gate passed in a fresh
wheel-only installation. Strict preflight found all 168 wheels compatible,
installation and `pip check` passed, the runtime manifest and every selftest
probe completed, and an explicit isolation assertion found no build path in
the Sage prefix hierarchy. `KENZO_FAS` was correctly `None` while Maxima and
generic ECL configuration resolved to their fresh companion packages. All
3,953 installed `--optional=sage` modules passed with zero failures in 491.5
seconds. Packaged pytest also passed 226 tests with 5 skips.

The required independent full gate then passed from another fresh wheel-only
installation under tmux session `sagelite_cp314_post54_full`. Strict macOS
preflight, installation, `pip check`, the runtime manifest, and every selftest
probe passed. Its explicit neutral-environment assertion found `SAGE_ROOT`
unset, the entire Sage prefix hierarchy inside the fresh installation, no
build paths, and `KENZO_FAS` unset. The unrestricted installed
`--optional=sage` sweep passed all 3,953 modules with zero failures in 791.8
seconds (4,511.6 CPU seconds and 4,463.9 cumulative wall seconds). Packaged
pytest passed 226 tests with 5 skips and 15 warnings in 269.55 seconds. The
validator recorded `Status: passed`, exit code 0, and 2,186.243 seconds total
elapsed time.

Both strict gates used eight threads and
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`. Their authoritative run path is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-202742-cf0c58f71315/
```

This exact `post54` build and its deterministic closure are accepted for the
local macOS arm64 CPython 3.14 matrix cell. Both fresh validation installs and
their evidence remain preserved; 59 GiB remained free after the full gate. No
publication was attempted.

## 2026-07-16 Post53 Kenzo Isolation Rejection And Post54 Repair

Exact pushed `post53` source `36d6058514b8a5eb1bae773626cfe5ed0dcdb584`
produced a repaired CPython 3.14 primary and deterministic strict closure. The
primary was:

```text
sagelite-10.9.post53-cp314-cp314-macosx_26_0_arm64.whl
  102,365,076 bytes
  97c102ea0f52254745f18e61072a92115cd67d344d707bdbf171d1648df9633a
```

The build and repair exited zero after injecting 2,079 headers, rewriting 23
companion-library references, and auditing 1,176 dependencies across 637
Mach-O files. The 168-wheel closure contains one primary, 68 companions, and
99 third-party wheels totaling 13,890,634,730 bytes; its inventory digest is
`e43168929153c42f5e2b470ad32a6230c9c540fd6199ff020a0572f31a5e1031`.

The strict fresh wheel-only install and `pip check` passed. Its neutral-path
diagnostic also proved that `SAGE_LOCAL`, `SAGE_SHARE`, `SAGE_DOC`,
`SAGE_SRC`, and `SAGE_LIB` now resolve within the fresh installation rather
than the build venv. The gate was nevertheless rejected during runtime
manifest collection because `KENZO_FAS` still fell back to the generated
build-time path when the Kenzo companion was incompatible with the active ECL
support directory. The automation stopped the gate and preserved its partial
validation evidence under:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-200221-36d6058514b/
```

The compatibility guard itself is necessary. Maxima activates its packaged
ECL support directory, which is a distinct filesystem entry from the generic
ECL companion directory. Explicitly forcing the Kenzo companion FAS with that
active directory reproduced an ECL abort with status 134. `post54` therefore
does not weaken the guard: for an installed wheel it preserves an explicit
`KENZO_FAS`, uses a compatible companion selected by bootstrap, or reports
Kenzo as unavailable instead of consulting generated build configuration.
Source-build configuration remains unchanged. Three focused tests cover the
installed, source-build, and explicit-environment cases; the complete focused
environment test file passes 125 tests. The primary and both strict gates must
be rebuilt from the exact committed `post54` source.

## 2026-07-16 Post52 Isolation Rejection And Post53 Force Repair

The `post52` strict gate passed wheelhouse preflight, fresh wheel-only
installation, and `pip check`, but a neutral-path diagnostic during runtime
manifest collection proved that `SAGE_LOCAL` still resolved to the new build
venv. The automation stopped the invalid gate and preserved its installation,
summary, and partial runtime artifacts. No selftest, short, or full result is
claimed.

The new selector was present and returned the correct fresh-install
`sys.prefix` when called after import. The remaining defect was in `var()`:
its documented `force=True` mode skipped the process environment but still
consulted generated `sage.config` before considering the forced fallback.
`post53` makes the implementation match its documentation by bypassing both
the environment and generated build configuration in forced mode. A focused
regression test supplies conflicting values from both sources and requires the
fallback. The CPython 3.14 primary and strict gates must be rebuilt again from
the exact committed `post53` source.

## 2026-07-16 Post51 Isolation Rejection And Post52 Repair

The strict `post51` short gate completed its fresh wheel-only installation and
`pip check`, but its runtime manifest made the run invalid before the short
doctest sweep could become evidence. With an initially empty environment, the
installed `sage.config` supplied this still-existing build prefix:

```text
SAGE_LOCAL=/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-183608-bd3d4c40efe4/build/venv
```

The derived `SAGE_SHARE`, `SAGE_DOC`, and package-install paths reused the same
tree, the doctest runner reported that build venv as `SAGE_LOCAL`, and selftest
loaded Kenzo from its `lib/ecl/kenzo.fas` instead of the installed companion.
The automation stopped the invalid doctest sweep with `KeyboardInterrupt` and
preserved its runtime manifest, summary, selftest log, and partial doctest log
under the authoritative run path. No install, selftest, short, or full result
is claimed from this gate.

The `post52` source repair initializes `SAGE_ROOT` before the prefix hierarchy
and selects `sys.prefix` for `SAGE_LOCAL` when Sage is installed without a
source tree. An explicit `SAGE_LOCAL` environment override and the configured
prefix of an ordinary source build remain unchanged. Focused tests cover all
three cases. Exact pushed source
`b2350b4d3d412af1f88d09de15d5a4097c7b73f7`, materialized as tree
`9261e66905c4b595f1b18458dbe6cf571bc9348f`, produced this repaired primary:

```text
sagelite-10.9.post52-cp314-cp314-macosx_26_0_arm64.whl
  102,366,234 bytes
  ee8c095e498d0d7e59f1acc2650b94fce34f0d54415f225d773784492102ca9a
```

The build and macOS repair exited zero after injecting 2,079 native headers,
rewriting 23 companion-library references, and auditing 1,176 dependencies
across 637 Mach-O files. The wheel contains the new installed-prefix runtime
logic. Its deterministic CPython 3.14 closure has 168 compatible wheels: one
primary, 68 companions, and 99 third-party wheels totaling 13,890,635,888
bytes. The inventory digest is
`9736fc5b8999c5c66f511d620bbc69e1cce2f2b2bc69c218299560337aa7eaff`.

With 98 GiB free, the independent neutral-environment strict short gate
started durably under tmux session `sagelite_cp314_post52_short`. It uses
explicit `--optional=sage --short 600`, eight threads, and
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`. The authoritative run path is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-194003-b2350b4d3d4/
```

This is build, closure, and short-gate-start evidence only. A successful fresh
install, selftest, short sweep, and independent full gate are still required;
the rejected `post51` wheel must not be repaired in place or retagged as
acceptance evidence.

## 2026-07-16 Post51 Wheel, Closure, And Strict Short Start

The durable native build from exact pushed `10.9.post51` source
`bd3d4c40efe4bfa4556f88cdb657b347f9fd6eb4` completed successfully on
Darwin arm64 with Homebrew CPython 3.14. The source archive and materialized
tree remain the exact inputs recorded below. The build exited zero at
`2026-07-16T18:52:48Z` and produced the repaired primary:

```text
sagelite-10.9.post51-cp314-cp314-macosx_26_0_arm64.whl
  102,366,925 bytes
  6a4086d1cc5c82589331b18926ec8c35525df7888cac1b4adf2a6329c6bcfceb
```

The closure assembly reused only wheels whose tags are compatible with the
CPython 3.14 interpreter. It fetched exact-version CPython 3.14 replacements
for the 24 non-primary CPython 3.13-only projects, then used pip in
`--dry-run --ignore-installed --no-index` mode to resolve the complete local
`sagelite[all-needed-extras]==10.9.post51` graph. Eleven unrelated third-party
wheels retained by the CPython 3.13 wheelhouse were not selected and were
excluded. The resulting closure has 168 compatible wheels: one primary, 68
companions, and 99 third-party wheels totaling 13,890,636,579 bytes. Its
inventory digest is
`b0cf14807fb69722f54d308ea41b024be3de93727954f4b9136336694252f2b7`.
Closure assembly and its interpreter-tag checks exited zero at
`2026-07-16T19:07:22Z`.

With 98 GiB free on `/Volumes/sage`, the named strict macOS short gate started
durably at `2026-07-16T19:08:09Z` under tmux session
`sagelite_cp314_post51_short`, with recorded PID 90654. It uses a neutral
`/usr/bin:/bin` base path, explicit
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`, a fresh wheel-only install of
`sagelite[all-needed-extras]==10.9.post51`, strict macOS preflight, explicit
`--optional=sage --short 600`, and eight test threads. Its authoritative path
is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-183608-bd3d4c40efe4/
```

This is wheel-built, compatible-closure, and short-gate-start evidence. No
fresh install, `pip check`, selftest, short, full-suite, or publication result
is claimed yet. The public preview manifest remains the 177-wheel set
generated on 2026-07-09 with fourteen `post8` and `post9` primary wheels.

## 2026-07-16 Post51 Exact Rebuild Start

The scheduled matrix iteration first retried the two higher-priority Linux
`x86_64` cells. The required `host` SSH alias again timed out during
connection, so no x86_64 build or validation was started. The public preview
manifest remained the 177-wheel set generated on 2026-07-09, with fourteen
public Sagelite primary wheels split between `10.9.post8` and `10.9.post9`.

The independent macOS arm64 CPython 3.14 cell then passed builder preflight on
`m1`: the host reported Darwin arm64, Homebrew CPython 3.14 was available, and
no Sagelite build or validator process was active. `/Volumes/sage` initially
had only 48 GiB free. Removing only the completed fresh-install venvs from the
accepted CPython 3.13 `post51` run and source, build, wheelhouse, and install
content from the superseded CPython 3.13 `post50` run restored 103 GiB free.
The accepted `post51` wheelhouse, reusable native dependency prefix, metadata,
and complete controller evidence copy were retained.

An exact archive of pushed `develop` source
`bd3d4c40efe4bfa4556f88cdb657b347f9fd6eb4` was transferred in bounded
chunks and reconstructed on `m1`. The controller and builder both verified
archive SHA-256
`cd8eb7b883d56b065fe7a36d267346d975800c4f60fbff491d9d52d2a601ffc3`.
The archive materializes committed tree
`d556af41ea4a78e51fa90e8daa14145e3cbeab7f`, and `origin/develop` was
verified at the same source commit before launch.

The native Darwin arm64 `10.9.post51` CPython 3.14 build is active under the
durable tmux session `sagelite_cp314_post51`, with recorded PID 51388. It
started at `2026-07-16T18:41:29Z`, verified the exact source input, and reached
CPython 3.14 build-dependency installation. The run reuses the accepted
CPython-independent native dependency prefix from the preceding `post51`
CPython 3.13 build. Its authoritative remote path is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp314-20260716-183608-bd3d4c40efe4/
```

This is build-start evidence only. No CPython 3.14 primary wheel, strict
closure, install, smoke, or full-suite result is claimed yet. After the
repaired primary completes, the next step is to assemble a CPython
3.14-compatible closure rather than copy CPython 3.13 ABI wheels, then run the
strict fresh short and full macOS gates with explicit `--optional=sage` and
`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`.
