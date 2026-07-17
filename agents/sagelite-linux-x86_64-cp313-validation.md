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
