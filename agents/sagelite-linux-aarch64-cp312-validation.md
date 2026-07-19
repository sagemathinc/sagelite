# Sagelite Linux aarch64 CPython 3.12 Validation

## 2026-07-19 Post63 Wheel And Strict Short/Full Passes

The exact pushed build recorded below completed with exit code zero and
produced 82 repaired primary and companion wheels totaling 4,623,984,743
bytes. The primary is:

```text
sagelite-10.9.post63-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,679,293 bytes
sha256: 498e1696cf81685ce816b5eb409fe4f05e8cbb5e93c97fa0303b2f663caab92a
```

The build-wheel `SHA256SUMS` file has SHA256
`ef47e662aa06f020648ca8596b3e53c0ff92eb24e9a9f19c24ff4c1c643c10ad`.
The guarded watcher combined those exact outputs with the accepted
ABI-specific supplements and portable companions, then resolved a
deterministic strict 191-wheel closure totaling 16,739,264,911 bytes. The
validator's staged-wheelhouse SHA256 is
`66ba3673f01d534d24c175c56d3fb84b9f3a79ed65b5d1e0f6ce6f0f20550779`;
the retained closure `SHA256SUMS` file has SHA256
`beea42a4a26e7b785e8a16116d0d557705805a38ae5420c4b73a85b52a66dc19`.

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post63` installation,
`python -m pip check`, runtime isolation with zero dependency, Python-path, or
source-path leaks, all 102 selftest checks, all 3,953 installed
`--optional=sage --short 600` modules with zero failures, and packaged pytest
with 229 passes and 2 skips. The standard sweep took 521.3 seconds, the
independent reducer reported 3,953 modules seen and zero failed modules, and
the validator exited zero after 1,258.151 seconds.

The separate fresh full gate repeated strict preflight, binary-only
installation, `pip check`, its independent zero-leak runtime scan, and all 102
selftests. Its unrestricted installed `--optional=sage` sweep passed all 3,953
modules with zero failures in 826.2 seconds. Packaged pytest passed with 229
passes, 2 skips, and 15 warnings in 289.28 seconds. The independent reducer
again reported 3,953 modules seen, zero failed modules, and no actionable
buckets. The full validator exited zero after 1,564.739 seconds. The durable
build, short, full, and watcher exit artifacts all contain zero.

Authoritative artifacts are retained at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260719-000623-16d6d78012a
```

Exact pushed `post63` source `16d6d78012a` is accepted locally for Linux
aarch64 CPython 3.12 as the third synchronized full-pass cell for this
release-candidate revision. Deliberate cleanup retained the 82-wheel build
output, strict 191-wheel closure, inventories, validation summaries, runtime
manifests, selftest logs, reduced analyses, and command logs. It removed only
the completed short/full install homes, disposable exact-source checkout, and
host validation venv, restoring 104,549,597,184 bytes free in the native
guest. The public manifest remains the 177-wheel set generated on 2026-07-09;
no artifact was published.

## 2026-07-19 Post63 Synchronized Build Start

The higher-priority Linux `x86_64` CPython 3.12 target was reachable, but its
required `/mnt/cocalc-scratch` bulk mount remained absent. That path resolved
to the 24 GB root filesystem with 15,139,332,096 bytes free. The recorded
`post60` build and watcher services were inactive with successful status, but
their bulk run root remained invisible. No result was inferred and no x86_64
build was started.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `10.9.post63` artifact. Independent preflight found the
outer `m1` host native Darwin `arm64`, the Lima guest native Linux `aarch64`,
and no active Sagelite service or Docker container. The outer
`/Volumes/sage` filesystem had 106,205,328 KiB free. The guest initially had
105,984,335,872 bytes free, below the binary 100 GiB heavy-build threshold.

Precise cleanup first archived a complete SHA256 inventory of the superseded
82-wheel `post61` CPython 3.12 build wheelhouse, whose wheels total
4,623,984,325 bytes, before removing only that wheel directory. Its archived
inventory SHA256 is
`6630bf4b4521932dbab19edfcf9f4c4235417941b45b7ab614043ef6b634beb8`.
Because those files were mostly hard-linked into newer closures, additional
cleanup archived and removed only the obsolete `post54` CPython 3.13 retry
closure. Its 83 wheels total 15,981,989,574 bytes, and its archived inventory
SHA256 is
`e440a77da0d97526cffc2bd33e492af71b23d6d1c6f21907fb463c77017c4e85`.
All concise validation evidence and the current `post62` CPython 3.12 and
`post63` CPython 3.13/3.14 closures remain. Guest capacity rose to
110,680,354,816 bytes.

Exact pushed release-candidate source is:

```text
source SHA: 16d6d78012a4971870e165e3ae948a24b8f7ed9c
version:    10.9.post63
bundle:     sagelite-16d6d78012a-depth1.bundle
size:       145,792,413 bytes
sha256:     89c36c7de5b51212c1d1dc386ead6dc85dbd3b39188f6cbe95ff463cf5a83e20
```

The bundle hash and exact head passed independently in the guest. All 191
hashes in the retained accepted `post62` CPython 3.12 seed closure also
passed; its inventory SHA256 is
`16edafdaad0f0ba0c9f4627622d85957c76d5a3aef852878b08f8f51f64298c5`.
The new native run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260719-000623-16d6d78012a
```

Its exact checkout reached pushed source `16d6d78012a497` and reports
`10.9.post63` from `VERSION.txt`. The actual manylinux container reports Linux
`aarch64` and CPython 3.12.13. This leg uses the repository Linux CIBW helpers
and will emit a synchronized platform companion set. The guarded watcher will
assemble a deterministic strict closure and run independent fresh short and
full gates only after a zero build exit.

The durable services are active as:

```text
sagelite-post63-arm-cp312-build.service  main PID 2249335
sagelite-post63-arm-cp312-watch.service  main PID 2249343
```

Script hashes are:

```text
766f1d113d08811fee2994645ad368a32460b7ac65e2e9f94123b8ceddf2b0b3  start-build.sh
fb7ce6c48c9b665495d734cfb781176c230995b10e3c398685afee9485ec873b  validate-after-build.sh
1ecd09f1175f8f626fa23678ec70bc16ed2d210eec280bd5bd7a4fdcc66a7a15  watch-and-validate.sh
```

This is exact-source build-start evidence only; no `post63` CPython 3.12
wheel, validation pass, cell acceptance, or publication is claimed yet.

## 2026-07-18 Post62 Wheel And Strict Short/Full Passes

The exact pushed build recorded below completed with exit code zero and
produced 82 repaired primary and companion wheels totaling 4,623,984,628
bytes. The primary is:

```text
sagelite-10.9.post62-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,679,178 bytes
sha256: 62e5c439081cd34af75e70176e7f765b712e4b8bac47dea15af19799ef4f11f1
```

The build-wheel inventory SHA256 is
`329a7d9a6cc3e34da92168ea3cd5a175b278b663a16ef8f63225246be80b508b`.
The guarded watcher combined those exact outputs with the accepted
ABI-specific supplements and portable companions, then resolved a
deterministic strict 191-wheel closure totaling 16,739,264,796 bytes. Its
inventory SHA256 is
`16edafdaad0f0ba0c9f4627622d85957c76d5a3aef852878b08f8f51f64298c5`.

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post62` installation,
`python -m pip check`, runtime isolation, all 102 selftest checks, all 3,953
installed `--optional=sage --short 600` modules with zero failures, and
packaged pytest with 229 passes and 2 skips. The standard sweep took 512.9
seconds, the independent reducer reported 3,953 modules seen and zero failed
modules, and the validator exited zero after 1,247.279 seconds.

The watcher then created a separate fresh install for the unrestricted full
gate. It repeated strict preflight, binary-only installation, `pip check`,
runtime isolation, and all 102 selftest checks. The unrestricted installed
`--optional=sage` sweep passed all 3,953 modules with zero failures in 825.9
seconds. Packaged pytest passed with 229 passes, 2 skips, and 15 warnings in
296.10 seconds. The independent reducer reported 3,953 modules seen, zero
failed modules, and no actionable buckets. The full validator exited zero
after 1,558.319 seconds, and the durable build, watcher, short, and full exit
artifacts all contain zero. Authoritative artifacts are retained at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260718-170343-b68997abc23
```

Exact pushed `post62` source `b68997abc23` is accepted locally for Linux
aarch64 CPython 3.12. Deliberate cleanup retained the exact strict closure,
wheel inventories, validation summaries, runtime manifests, selftest logs,
reduced analyses, and command logs. It removed only the completed fresh full
install, disposable exact-source checkout, and host validation venv, restoring
102,807,773,184 bytes free in the native guest. The directly fetched public
manifest remains the 177-wheel set generated on 2026-07-09; no artifact was
published.

## 2026-07-18 Post62 Synchronized Build Start

The higher-priority Linux `x86_64` CPython 3.12 target was reachable, but its
required `/mnt/cocalc-scratch` bulk mount remained absent. That path resolved
to the 24 GB root filesystem with 15,026,716,672 bytes free. The recorded
`post60` build and watcher services were inactive with successful service
status, but their bulk run root was not visible. No result was inferred and no
x86_64 build was started.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `10.9.post60`, `10.9.post61`, or `10.9.post62`
artifact. Independent preflight found the outer `m1` host native Darwin
`arm64`, the Lima guest native Linux `aarch64`, and no active Sagelite service
or Docker container. The outer `/Volumes/sage` filesystem had 108,794,488 KiB
free. The guest had 108,433,301,504 bytes free before launch, above the binary
100 GiB heavy-build threshold.

Exact pushed release-candidate source is:

```text
source SHA: b68997abc23abff78d8744ed7bb3cfa9c926b7c3
version:    10.9.post62
bundle:     sagelite-b68997abc23-depth1.bundle
size:       145,796,607 bytes
sha256:     323f23af946b83e059ce23f06887ea4f720c034db3ee54bc42f5462702d9cfc3
```

The retained bundle hash matches the previously verified Linux aarch64
CPython 3.14 source input. The new native run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260718-170343-b68997abc23
```

Its detached checkout is clean at the exact source SHA and reports
`10.9.post62` from `VERSION.txt`. The actual manylinux container reports Linux
`aarch64` and CPython 3.12.13. This CPython 3.12 leg uses the repository's
Linux CIBW helpers and emits a synchronized platform companion set. The
accepted `post61` CPython 3.12 strict closure is used only as a guarded source
of ABI-specific supplements and portable dependency wheels.

The durable services are active as:

```text
sagelite-post62-arm-cp312-build.service  main PID 1683637
sagelite-post62-arm-cp312-watch.service  main PID 1683846
```

Script hashes are:

```text
a97cb6ed7d642d08b680941d6ef0ef07c7016e50a31ccb9373f91b03d96d3a0b  start-build.sh
2f421f81722eb144228cc88071a12367891b02f7c2c7428b5da4e7e5c4d642d2  validate-after-build.sh
1ecd09f1175f8f626fa23678ec70bc16ed2d210eec280bd5bd7a4fdcc66a7a15  watch-and-validate.sh
```

The watcher will assemble a deterministic strict closure and run independent
fresh short and full gates only after a zero build exit. This is exact-source
build-start evidence only; no `post62` wheel, install, validation pass, or
publication is claimed yet.

## 2026-07-18 Post61 Wheel And Strict Short/Full Passes

The native build and guarded watcher from the exact pushed source recorded
below both completed with exit code zero.  The build produced 82 repaired
primary and companion wheels totaling 4,623,984,325 bytes.  The primary is:

```text
sagelite-10.9.post61-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,678,874 bytes
sha256: ffe510e0ed81fe05b38e511e29df3c9e21c3871d31e7c7379eba86e67b08a4f8
```

The build-wheel inventory SHA256 is
`36f5211b15a1b2d9934d72736cab5803ae39f56a926cafe6cbb01e3add35d9d2`.
The watcher combined those exact outputs with the accepted ABI-specific
supplements and portable companions, then resolved a deterministic strict
191-wheel closure totaling 16,739,264,493 bytes.  Its inventory SHA256 is
`362969114641358f4a31c65ab6a4dd7b5d4c2bbfd809fd30b3587eebc1d55d32`.

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post61` installation,
`python -m pip check`, runtime isolation with zero leaks, all 102 selftest
checks, and all 3,953 installed `--optional=sage --short 600` modules with
zero failures.  The standard sweep took 522.8 seconds, the independent
reducer reported 3,953 modules seen and zero failed modules, and the validator
exited zero after 1,247.0 seconds.

The separately named full gate created another fresh install from the same
strict closure.  It repeated the strict preflight, wheel-only installation,
`pip check`, zero-leak runtime scan, and all 102 selftests.  Its unrestricted
installed `--optional=sage` sweep passed all 3,953 modules with zero failures
in 901.0 seconds.  The independent reducer again reported 3,953 modules seen,
zero failed modules, and no actionable buckets.  The full validator exited
zero after 1,651.972 seconds.  The durable build, short, full, and watcher
exit-code files all contain zero.

Authoritative artifacts are retained at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260718-083928-33f8a4dae1d
```

Deliberate cleanup retained the verified exact-source bundle, new build and
strict wheelhouses, inventories, validation summaries, runtime manifests,
selftest logs, reduced analyses, and top-level command logs.  It removed only
the completed fresh-install tree, disposable checkout and host venv,
superseded CPython 3.12 wheel copies, and obsolete wheel outputs from rejected
CPython 3.13/3.14 investigations while preserving their inventories and
failure evidence.  Final guest capacity is 108,312,612,864 bytes, above the
binary 100 GiB heavy-build threshold.  Exact pushed `post61` source
`33f8a4dae1d` is accepted locally for Linux aarch64 CPython 3.12.  The directly
fetched public manifest remains the 177-wheel set generated on 2026-07-09;
no artifact was published.

## 2026-07-18 Post61 Synchronized Build Start

All three bounded attempts to reconcile the higher-priority Linux `x86_64`
CPython 3.12 `post60` job through the required `host` alias timed out before a
session was established.  That possibly surviving job was left untouched, and
no result was inferred.  The directly fetched public `dev/manifest.json`
remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `10.9.post60` or `10.9.post61` artifact.

Independent preflight on `m1` found the outer host native Darwin `arm64` and
the persistent Lima guest running Linux `aarch64`.  No Sagelite automation
service, validation process, tmux session, or Docker container was active.
The outer `/Volumes/sage` filesystem had 108,113,384 KiB free.  The guest
initially had 107,425,144,832 bytes free, only about 49 MiB above the binary
100 GiB heavy-build threshold.  Precise cleanup removed only a regenerated
closure from the rejected `post14` run, obsolete primary-wheel directories
from superseded `post10` through `post18` failure runs, and the already
recorded `post60` source bundle.  Accepted wheelhouses, validation summaries,
runtime manifests, reduced analyses, inventories, and current failure evidence
remain.  This restored 110,247,145,472 bytes free before source staging.

Exact pushed release-candidate source is:

```text
source SHA: 33f8a4dae1da1571b07b9bbf8adddfe07a41af6c
version:    10.9.post61
bundle:     sagelite-shallow-33f8a4dae1d.bundle
size:       145,788,566 bytes
sha256:     c2670796bf1b7a7254b7a9824f1caedd60dbb5295c2c08d658ce3bf5e00a4ab7
```

The bundle hash matched on the controller, outer Mac, and Linux guest.  The
new native run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260718-083928-33f8a4dae1d
```

Its checkout is clean at the exact source SHA and reports `10.9.post61` from
`VERSION.txt`.  The actual manylinux container reports Linux `aarch64` and
CPython 3.12.13.  Pre-launch guest capacity was 110,101,356,544 bytes.  The
build uses the repository Linux CIBW helpers with
`CIBW_BUILD=cp312-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the accepted
`post60` CPython 3.12 closure as the guarded source of ABI-specific supplements
and portable wheels.  This leg emits a synchronized platform companion set
before the watcher resolves a fresh strict closure and runs independent short
and full gates.

The durable services are active as:

```text
sagelite-post61-arm-cp312-build.service  main PID 1008691
sagelite-post61-arm-cp312-watch.service  main PID 1008698
```

Script hashes are:

```text
addb1ea883e18836e839588981f63be6397bb01eaf32f1dd5c37ad6f2c967deb  start-build.sh
14cb096a77ef48b77f6c4f1a739c9e517049f991c35a263cace77d340ef71bf7  validate-after-build.sh
1ecd09f1175f8f626fa23678ec70bc16ed2d210eec280bd5bd7a4fdcc66a7a15  watch-and-validate.sh
```

This is exact-source build-start evidence only.  No `post61` wheel, install,
short gate, full-suite pass, or publication is claimed yet.

## 2026-07-18 Post60 Wheel And Strict Short/Full Passes

All three bounded attempts to reconcile the higher-priority Linux `x86_64`
CPython 3.12 job through the required `host` alias timed out during SSH
connection. That possibly surviving job was left untouched. The public
`dev/manifest.json` remained the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels, so
no local `post60` artifact was assumed public.

The native Linux arm64 build and watcher described below completed from exact
pushed source `22a2cb56739940d7a9eb313e997fd0a004a9ea36`
(`10.9.post60`). The clean native `aarch64` build exited zero and produced 82
repaired primary and companion wheels totaling 4,623,974,563 bytes. The
primary is:

```text
sagelite-10.9.post60-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,678,592 bytes
sha256: 95ab03ac02865369c08ce3b6b2acb00f5cc54189404084ce4518f65ab7bcfd3b
```

The build-wheel inventory SHA256 is
`13bf345e42a91fa19c6452dc342eef0266202abf3a44bfd0362a569e6107a370`.
The watcher combined the new exact-build wheels with accepted ABI-specific
supplements and portable companions, then resolved a deterministic strict
191-wheel closure totaling 16,739,251,241 bytes. Its inventory SHA256 is
`e0bf111356e5848111a6b24d8b4f320dd62ea9d3411b2a4b6d664c4b425f6592`.

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post60` installation,
`python -m pip check`, runtime-manifest isolation, every selftest, all 3,953
installed `--optional=sage --short 600` modules with zero failures, and
packaged pytest with 229 passes, 2 skips, and 15 warnings. The doctest sweep
took 519.2 seconds, pytest took 295.89 seconds, and the validator exited zero
after 1,266.143 seconds. Its reduced-analysis JSON reports 3,953 modules seen,
zero failed modules, and no actionable buckets.

The separately named full gate created a second fresh install from the same
strict closure. Preflight, wheel-only installation, `pip check`, runtime
isolation, and every selftest passed again. The unrestricted installed
`--optional=sage` sweep reported `All tests passed` for all 3,953 modules in
888.6 seconds. Packaged pytest then passed 229 tests with 2 skips and 15
warnings in 298.02 seconds. The validator exited zero after 1,617.91 seconds,
and the independent reducer again reported 3,953 modules seen and zero failed
modules. The durable build, short, full, and watcher exit-code files all
contain zero.

Authoritative artifacts are retained at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260717-223804-22a2cb56739
```

Deliberate cleanup retained the exact strict closure, build inventory,
validation summaries, runtime manifests, selftest logs, reduced analyses, and
top-level command logs. It removed only completed install homes and build
venvs, inactive pushed-source checkouts, one resolved superseded closure, two
obsolete pre-post60 bundles, and the unused 2025 manylinux image. Final guest
capacity is 107,698,089,984 bytes free, above the binary 100 GiB heavy-build
threshold. No artifact was published.

## 2026-07-17 Post60 Synchronized Build Start

Three bounded attempts to reconcile the higher-priority Linux `x86_64`
CPython 3.12 job through the required `host` alias timed out during SSH
connection. That possibly surviving job was left untouched. The public
`dev/manifest.json` remained the 177-wheel set generated on 2026-07-09, so no
local `post60` artifact was assumed public.

Independent preflight on `m1` found the outer Darwin host native `arm64`, the
persistent Lima guest running Linux `aarch64`, and no active Sagelite build,
validator, or Docker container. The outer `/Volumes/sage` filesystem had
108,004,188,160 bytes free. The guest initially had 103,446,056,960 bytes
free, below the binary 100 GiB heavy-build threshold. Precise cleanup removed
only superseded regenerated closure links, eight inactive disposable source
checkouts, and six obsolete exact-source bundle inputs. Accepted wheelhouses,
validation evidence, logs, and the latest useful failure evidence remain.
This restored 108,706,050,048 bytes free in the guest before source staging.

Exact pushed release-candidate source is:

```text
source SHA: 22a2cb56739940d7a9eb313e997fd0a004a9ea36
version:    10.9.post60
bundle:     sagelite-shallow-22a2cb56739.bundle
size:       145,770,108 bytes
sha256:     84f2902d2051d598b04430d9ef95b4e9fe672f4d02a0701a653d2764b82285dc
```

The hash matched on the controller, outer Mac, and Linux guest. The new native
run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260717-223804-22a2cb56739
```

Its clean checkout was independently confirmed at the exact source SHA and
`10.9.post60`. The pre-launch guest capacity was 108,560,244,736 bytes. The
build uses the repository Linux CIBW helpers with
`CIBW_BUILD=cp312-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the accepted
CPython 3.12 closure as the guarded source of ABI-specific supplements and
portable wheels. This leg emits a synchronized platform companion set before
the watcher resolves a fresh strict closure and runs independent short and
full gates.

The durable services are active as:

```text
sagelite-post60-arm-cp312-build.service  main PID 432512
sagelite-post60-arm-cp312-watch.service  main PID 432520
```

Script hashes are:

```text
d9f70b4345cc933a5f86a8d95b2ce0f5f5c98a24ea61d93d27baac2fead48e86  start-build.sh
57805b8cd47d58ca7b20de0403c97bab5660df33646fc730d26d4f5c9b3f80b9  validate-after-build.sh
1ecd09f1175f8f626fa23678ec70bc16ed2d210eec280bd5bd7a4fdcc66a7a15  watch-and-validate.sh
```

The build completed exact-bundle checkout and entered native prerequisite
setup while the watcher remained active. No `post60` wheel, install, short
gate, full gate, or publication result is claimed yet.

## 2026-07-16 Post54 Wheel And Strict Short/Full Passes

The native build from exact pushed source
`9492b6cbf83875c024ef2c6760977707ef8065f2` completed with exit code zero.
It produced 82 repaired wheels: one primary and 81 companion runtime/data
wheels, including ABI-specific `pplpy`. The native `pycosat` and `cysignals`
supplements described below brought the build wheelhouse to 84. The primary is:

```text
sagelite-10.9.post54-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,678,292 bytes
sha256: ae629dc301f91273aec9eeb85ebe9625ff768f1d9fa7c411be35e9cfc9eaa2be
```

The first binary-only closure attempt correctly rejected the retained CPython
3.13 `pycosat` wheel and stopped before installation because no public CPython
3.12 aarch64 wheel exists. Native manylinux builds then supplied repaired
CPython 3.12 wheels for `pycosat 0.6.6` and `cysignals 1.12.6`. The matching
`cysignals` avoids the exported-C-function mismatch already established on
CPython 3.13. The failed resolution log and exit code remain preserved as
`validation-follow-r1.log` and `validation-follow-r1-exit-code`.

The resulting deterministic strict closure has 191 wheels totaling
16,739,248,783 bytes: one primary, 81 Sagelite companions, and 109 third-party
wheels. Its staged wheelhouse digest is
`cf8bef4b02173028cd2b1c7e9db8203c4d5b81df8c395d46eb464f480cbee675`,
and its inventory-file digest is
`4c94228fe9f9da854b1d9c5d19d2fd7b163cad97dd8e2382451d0cdef5b701af`.

The strict short gate then passed in a fresh CPython 3.12 wheel-only install.
All 191 wheel filenames and tags passed strict repaired-wheelhouse preflight;
all 68 requested Sagelite dependency projects were present. Installation,
`pip check`, runtime manifest collection, and every selftest probe passed. The
explicit installed `--optional=sage --short 600` sweep saw all 3,953 modules
and reduced to zero failures in 519.2 seconds. Packaged pytest passed 229 tests
with 2 skips and 15 warnings. The validator recorded `Status: passed`, exit
code 0, and 1,246.475 seconds total elapsed time.

After removing the short gate's fresh install, the same durable validation
service ran a separate fresh strict full gate from the identical wheel
contract. Strict preflight, wheel-only installation, `pip check`, runtime
manifest collection, and every selftest probe passed again. The unrestricted
installed `--optional=sage` sweep saw all 3,953 modules and reduced to zero
failures; its doctest runner reported `All tests passed` in 883.4 seconds.
Packaged pytest then passed 229 tests with 2 skips and 15 warnings in 306.60
seconds. The full validator recorded `Status: passed`, exit code 0, and
1,630.778 seconds total elapsed time.

The durable service completed successfully as:

```text
sagelite-post54-cp312-validate-r2.service
```

This is repaired-wheel, compatible-closure, independent fresh-install short
and full evidence. Both validation and follow-up exit-code files contain zero.
The cell is accepted as `full`. The completed full gate's disposable 21 GiB
install tree was removed after preserving the wheelhouses and validation
evidence, restoring 103,526,285,312 bytes free in the guest. No publication
was attempted.

## 2026-07-16 Post54 Native Build Start

The scheduled matrix iteration first retried the higher-priority Linux
`x86_64` CPython 3.14 cell. The required `host` SSH alias again timed out
during connection, so no x86_64 build or validation was started. The public
`dev/manifest.json` remained the 177-wheel set generated on 2026-07-09, with
fourteen public Sagelite primaries split between `10.9.post8` and
`10.9.post9`.

The independent Linux aarch64 CPython 3.12 cell then passed native backend
preflight on `m1`. The outer host reported Darwin `arm64`, and the persistent
Lima guest reported Linux `aarch64` with Docker running as `arm64`. No
Sagelite build, validator, or user service was active.

The outer filesystem initially had 59 GiB free and the guest had less than
100 GiB free. Cleanup removed only completed fresh-install venvs and
disposable build/source/cache content from accepted macOS runs, plus source,
venv, and wheelhouse content from superseded resolved-failure runs. It
retained the accepted macOS CPython 3.13 and 3.14 wheelhouses, their concise
short/full evidence, and the accepted Linux aarch64 CPython 3.13 and 3.14
wheelhouses and evidence. After cleanup and source staging, the outer volume
had 117,415,904 KiB free and the Linux guest had 110,081,482,752 bytes free,
both above the 100 GiB heavy-build threshold.

The exact pushed source is:

```text
source SHA: 9492b6cbf83875c024ef2c6760977707ef8065f2
version:    10.9.post54
bundle:     sagelite-shallow-9492b6cbf83.bundle
size:       145,745,628 bytes
sha256:     2c3d130ea8b058c6cd706e5c17523be666f724427bcaf397c9bce0f370647537
```

The bundle hash matched on the controller, outer Mac, and Linux guest. The
native build uses the repository CIBW helpers with
`CIBW_BUILD=cp312-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the CPython
3.12 manylinux interpreter. Its durable run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260716-221205-9492b6cbf83
```

The build and gated watcher are active as:

```text
sagelite-post54-cp312-build.service
sagelite-post54-cp312-validate.service
```

The watcher waits for the build's durable `exit-code`. After build success it
will assemble a CPython 3.12-compatible closure from the new repaired wheels,
accepted ABI-independent aarch64 companions, and binary-only third-party
wheels. It will then run strict fresh wheel-only short and full validations
with `sagelite[all-needed-extras]==10.9.post54` and explicit
`--optional sage`.

This checkpoint is preflight, cleanup, exact-source transfer, and build-start
evidence only. No `post54` wheel, install, smoke, short, or full result is
claimed, and no publication was attempted.
