# Sagelite Linux x86_64 CPython 3.13 Validation

## 2026-08-01 Builder Alias Timed Out; Full Gate Unreconciled

At `2026-08-01T20:14:24Z`, `20:14:34Z`, and `20:14:44Z`, three bounded
SSH attempts through the required `host` alias timed out before establishing
a session. The durable full-gate service, container, logs, summaries, and
artifacts therefore could not be reconciled. No pass or failure is inferred,
and no duplicate build or validation run was started.

The last authoritative evidence remains the corrected fresh Nehalem pass and
independent short-gate pass, followed by the full gate starting at
`2026-07-30T03:16:16Z`. The directly fetched public manifest remains the
177-wheel set generated on 2026-07-09, with no post64 artifact. Continue only
after the alias points at the running x86 builder again, then reconcile the
existing durable service before deciding whether any retry is required.

## 2026-07-30 Exact Post64 Portable Rebuild Started

After Linux x86_64 CPython 3.12 became the seventh synchronized full-pass
cell, deliberate cleanup removed only its completed 21 GB full-install venv.
Its validated wheelhouse, strict closure, summaries, logs, and reducer evidence
remain. This restored 144 GiB free on the assigned `/mnt/cocalc-scratch`
filesystem.

The staged CPython 3.13 run is:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260730-012400-014ae4bf443
```

Its checkout is clean at exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` (`10.9.post64`). The
146,483,200-byte source archive again passed SHA256
`a7ce677432f01cff16fd93d88f6c12f3d988464d76a2c79aa215165d5df047ed`.
The isolated prefix still resolves to the fat-binary profile built from this
source, Docker was idle, and every launcher passed its recorded hash:

```text
2ed9e8f80c95a4b86897335aa0248f9e926a4ddc5c8232360b242efd3b13e457  build.sh
495622237b68e1cc72e22df1db2c0cc50c698ae262f623155289b56667f0b6f3  follow-post64.sh
f76eacb80d008f475445ccb01545631c9f0914ae65cf0b28b9e639c67fb4b711  oldcpu-post64.sh
d73fa19e720f733ee5fc86ea3f501545fbdeeab0053da08ef39e938cbcb1adf6  validate-post64.sh
```

The guarded watcher pins the previously accepted CPython 3.13 x86_64
`pycosat==0.6.6` wheel by SHA256, reuses only the synchronized post64
ABI-independent companions, and requires the corrected fresh QEMU Nehalem
probe plus independent short and full gates. The durable build and watcher
started at `2026-07-30T02:14:22Z` with main PIDs 1129004 and 1129011:

```text
sagelite-post64-x86-cp313-build-r1.service
sagelite-post64-x86-cp313-watch-r1.service
```

The build passed its exact-source guards and entered bootstrap. No post64
CPython 3.13 wheel or validation pass is claimed yet. The directly fetched
public manifest remains the 177-wheel set generated on 2026-07-09, with no
post64 artifact.

The build exited zero after about 31 minutes and produced four repaired wheels.
The primary is:

```text
filename: sagelite-10.9.post64-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:     261575877
sha256:   ae5624131009064ca0ed34378f5b19c9a2eea677219b5693e6315ef763f82589
```

The guarded watcher verified the accepted portable database and CPython 3.13
`pycosat` input, assembled the exact new primary and 9,744,065-byte `pplpy`
wheel, and resolved a strict 192-wheel closure totaling 14,364,637,365 bytes.
The corrected fresh QEMU Nehalem probe began at
`2026-07-30T02:46:53Z`. Independent short and full gates remain required, so
no validation pass or cell acceptance is claimed yet.

The Nehalem probe passed at `2026-07-30T02:49:45Z`. The independent fresh
short gate then passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation,
all selftest probes, and the bounded installed `--optional=sage` suite,
exiting zero at `03:16:12Z`. The separate fresh full gate started at
`2026-07-30T03:16:16Z`; full acceptance remains pending.

## 2026-07-17 Post60 Release-Candidate Build Start

The scheduled matrix iteration selected Linux `x86_64` with CPython 3.13,
the highest-priority remaining cell in the authoritative work order. The
canonical repository was clean on `develop` at
`11469917d9ea704afa24f77a54a2e44a9d685236`, synchronized with
`origin/develop`. Selected release-candidate source
`22a2cb56739940d7a9eb313e997fd0a004a9ea36` (`10.9.post60`) is an ancestor of
that pushed tip and was already accepted for Linux `x86_64` CPython 3.14.

The directly fetched public `dev/manifest.json` remained the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels. No local `post60` artifact was assumed public.

Read-only preflight through the required `host` SSH alias found Linux
`x86_64`, an idle Docker engine, no active Sagelite automation service, and
the expected `/mnt/cocalc-scratch` bulk filesystem. It initially had
106,631,876,608 bytes free, slightly below the runbook's binary 100 GiB
heavy-build threshold. Precise cleanup removed only these disposable source
checkouts from completed or superseded runs while retaining their wheelhouses
and validation evidence:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39/source
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/source
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-companions-20260717-105534-6361dc1935c/source
```

Those source checkouts are not recoverable from the builder, but their exact
pushed commits and durable evidence remain recorded. After staging the new
exact checkout, final pre-launch capacity was 107,631,353,856 bytes.

The new run is:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739
```

Its source checkout is clean at exact SHA `22a2cb56739`. The build uses
cibuildwheel 3.4.1, `CIBW_BUILD=cp313-manylinux_x86_64`, `CIBW_ARCHS=x86_64`,
the repository Linux build and repair helpers, the retained bulk-backed
manylinux prefix, and append-only logs below the run root. The guarded
validation launcher will reuse the synchronized 82-wheel platform companion
set and the verified portable 4D polytope database, but will accept only the
new exact `post60` CPython 3.13 primary and `pplpy` wheels. It will resolve a
fresh binary-only closure and run independent strict short and full gates.

The durable services are:

```text
sagelite-post60-x86-cp313-build.service
sagelite-post60-x86-cp313-watch.service
```

At the latest checkpoint both services were active. The build main PID was
`2100933` and the watcher main PID was `2100961`. The actual manylinux
container reported `x86_64` and CPython 3.13.12. Its selected-ABI cache guard
detected the retained CPython 3.14 interpreter, reset it, created the CPython
3.13 venv, and entered native prerequisite installation. Script hashes are:

```text
6549b91b3d8547bae831615b51f1ec4d2bc752087dabe4ef61e66b2f81c0c757  build.sh
01b9d8f4b842a2791550f14de75607174bf8438923eac8e89037cbf317a14013  follow-post60.sh
aab9f040e16e5e1e108ceaadd9ebb73f0c2d297339edc81d85db4fdec40c6f73  validate-post60.sh
```

No `post60` CPython 3.13 wheel, install, short gate, full gate, or publication
result is claimed yet. A resumed iteration must reconcile both services, the
container, `command.log`, log growth, build `exit-code`, wheel inventory, and
validation artifacts before launching any other x86_64 job.

## 2026-07-17 Post60 Build Completion And Validation Resume

The resumed scheduled iteration reconciled the existing run rather than
launching a duplicate. The correct system-level transient units, recorded
PIDs, process tree, manylinux container, and growing build log all agreed that
the build and watcher were healthy. The public `dev/manifest.json` remained
the 177-wheel set generated at `2026-07-09T17:17:42.743310+00:00`, with
fourteen Sagelite primary wheels and no `post60` publication.

The exact `post60` build completed with exit code zero. Its repaired primary
is:

```text
sagelite-10.9.post60-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244669165
sha256: f65a0903fa98471a38e5f6e145901258d6ef4503369d7febd46a078533f90885
```

The same run also emitted these new companion wheels:

```text
pplpy-0.9.0.post1-cp313-cp313-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl
size:   9569626
sha256: 1a09b70357c375f2faa4699bda9774533be0ec46062c7437cf8c3b26963abf37

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_x86_64.whl
size:   67999222
sha256: 1bb666e7f113407da73ce9be7efbca8b66365f4f8cacc34415a27fdd45754f1a

sagelite_qepcad_runtime-10.9.post4-py3-none-manylinux_2_28_x86_64.whl
size:   5287584
sha256: 15f184dc8f24fcc763f63202fa7e5c8668e2b4b6eae82133c642156258d4dabd
```

The guarded watcher correctly waited for build success and assembled the new
primary and `pplpy` wheel with the accepted portable 4D polytope database. Its
first binary-only closure resolution then stopped before installation because
PyPI supplied no CPython 3.13 wheel for `pycosat>=0.6.3`. The exact failure is
preserved at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/orchestration/closure-resolution-post60-initial-missing-pycosat.log
```

The public preview manifest already contained a compatible accepted wheel:

```text
pycosat-0.6.6-cp313-cp313-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl
size:   206987
sha256: bbde2e7c9c887e8e6f63015ac53145d96493dda4976f8ec69626b965641c5773
```

The wheel was fetched from the public preview, checked against that manifest
hash, and added as a fourth ABI-specific input. No Sage rebuild was needed.
One fresh durable retry then resolved a strict closure of 192 wheels totaling
14,292,168,533 bytes and started the independent short gate under:

```text
sagelite-post60-x86-cp313-validation-r1.service
```

At this checkpoint the service is active and the fresh wheel-only environment
is installing from the strict closure. No install, `pip check`, selftest,
short-gate, full-gate, or publication result is claimed yet. The next resumed
iteration must reconcile this validation unit and its short/full artifacts
before launching another x86_64 job.

## 2026-07-17 Post60 Full Acceptance

The durable retry completed with exit code zero. Its strict 192-wheel closure
totals 14,292,168,533 bytes and has wheelhouse SHA256
`076e61d239b295f985d1e17bf9b9658b3be7a0830f22011470beb1820db49a06`.
It contains one repaired primary, 81 Sagelite companion wheels, and 110
third-party wheels. The exact primary remains:

```text
sagelite-10.9.post60-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244669165
sha256: f65a0903fa98471a38e5f6e145901258d6ef4503369d7febd46a078533f90885
```

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post60` installation, `pip check`,
runtime isolation, every selftest, all 3,953 installed
`--optional=sage` modules with zero failures in 545.0 seconds, and packaged
pytest with 229 passes and 2 skips.

The separate fresh full gate passed the same preflight, installation,
isolation, and selftest contract. Its unrestricted installed standard doctest
sweep passed all 3,953 modules with zero failures in 930.2 seconds. Packaged
pytest then passed with 229 passes and 2 skips. The reducer recorded no failed
modules, examples, framework errors, timeouts, fingerprints, or actionable
buckets, and both the full validator and guarded orchestration service exited
zero. Durable evidence is below:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/validation/short-post60
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/validation/full-post60
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/validation-short-command.log
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/validation-full-command.log
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739/validation-follow.log
```

After preserving the exact wheelhouse and validation evidence, deliberate
cleanup removed only completed short/full install environments and disposable
exact-source/helper-venv copies from this run and the accepted CPython 3.14
run. One old extracted macOS transfer source was also removed while its source
archive and validation directory were retained. The builder then had
107,929,792,512 bytes free on `/mnt/cocalc-scratch`, above the binary 100 GiB
heavy-build threshold. The public R2 manifest remained the 177-wheel set
generated on 2026-07-09; no artifact was published.
