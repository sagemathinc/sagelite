# Sagelite macOS arm64 CPython 3.14 Validation

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
