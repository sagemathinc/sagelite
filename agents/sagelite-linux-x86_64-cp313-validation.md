# Sagelite Linux x86_64 CPython 3.13 Validation

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
