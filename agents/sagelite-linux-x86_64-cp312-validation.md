# Sagelite Linux x86_64 CPython 3.12 Validation

## 2026-07-18 Assigned Bulk Mount Absent

The required `host` alias was reachable again as Linux `x86_64`, and the two
recorded `post60` CPython 3.12 services were inactive with zero service
status. However, the expected `/mnt/cocalc-scratch` bulk filesystem was not
mounted: that path resolved to the 24 GB root filesystem with about 14 GB
free, and the recorded run root was absent there. The possibly surviving bulk
artifacts therefore could not be inspected. No wheel, validation result, or
failure is inferred, and no heavy x86_64 job was started on this staging host.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post60` or `post61` artifact.

## 2026-07-18 Post60 Build Still Unreconciled

The next scheduled matrix iteration made three new bounded SSH connection
attempts through the required `host` alias. All three timed out before a
session was established. The possibly surviving build and guarded watcher at

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260717-220219-22a2cb56739
```

were therefore left untouched. No wheel, service exit status, install, short
gate, full gate, or failure is inferred from the unavailable host.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `10.9.post60` artifact. Independent work continued on
the correctly assigned macOS arm64 builder; its checkpoint is recorded in
`agents/sagelite-macos-arm64-cp312-validation.md`.

## 2026-07-17 Post60 Release-Candidate Build Start

The scheduled matrix iteration selected Linux `x86_64` with CPython 3.12,
the highest-priority remaining cell in the authoritative work order. The
canonical repository was clean on `develop` at
`965a65b0a23a060642b6827286ac87aea1f2043b`, synchronized with
`origin/develop`. Selected release-candidate source
`22a2cb56739940d7a9eb313e997fd0a004a9ea36` (`10.9.post60`) is an ancestor of
that pushed tip and has already passed the independent full gates for Linux
`x86_64` CPython 3.13 and 3.14.

The directly fetched public `dev/manifest.json` remained the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels. No local `post60` artifact was assumed public.

Read-only preflight through the required `host` SSH alias found Linux
`x86_64`, an idle Docker engine, no active Sagelite automation service, and
the expected `/mnt/cocalc-scratch` bulk filesystem. It initially had
107,929,792,512 bytes free. Deliberate cleanup removed the regenerated strict
closure directories from three rejected CPython 3.14 runs and superseded
automation-owned source bundles and their disposable source-creation trees.
Their pushed source revisions, primary build outputs, focused evidence, and
concise validation reports remain. Final pre-launch capacity after staging
and verifying the exact checkout, then removing the transferred bundle copy,
was 110,680,420,352 bytes.

The source was transferred in a complete verified bundle:

```text
name:   sagelite-develop-965a65b0a23.bundle
size:   595244386
sha256: 309c081e8c8b23110d9fc6ec763c825483292b6fc3579b3a5e35e957dbf6fd21
```

The new run is:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260717-220219-22a2cb56739
```

Its source checkout is clean at exact SHA `22a2cb56739`. The build uses
cibuildwheel 3.4.1, `CIBW_BUILD=cp312-manylinux_x86_64`,
`CIBW_ARCHS=x86_64`, the repository Linux build and repair helpers, the
retained bulk-backed manylinux prefix, and append-only logs below the run
root. Unlike the CPython 3.13 and 3.14 legs, this CPython 3.12 contract emits
the complete synchronized platform companion set. The guarded validation
launcher will use those new exact-build companions, the new primary and
`pplpy` wheels, and the previously verified portable 4D polytope database. It
will resolve a fresh binary-only closure and run independent strict short and
full gates.

The durable services are:

```text
sagelite-post60-x86-cp312-build.service
sagelite-post60-x86-cp312-watch.service
```

At the launch checkpoint both services were active. The build main PID was
`2542148` and the watcher main PID was `2542191`. The actual manylinux
container reported `x86_64` and CPython 3.12.13, then entered native system
prerequisite installation. Script hashes are:

```text
db5b0dd729e58557aad128c0c05cac3f0d30363e01a2cf41d91c15e58cb785cf  build.sh
9fcfbef320d41b3d488e6760dd046da25debaf8b19b172fc892f0554b99850f1  follow-post60.sh
48841558d145232ec7f736ce1553dea9613adcbb50121aff84d864c71426351a  validate-post60.sh
```

No `post60` CPython 3.12 wheel, install, short gate, full gate, or publication
result is claimed yet. A resumed iteration must reconcile both services, the
container, `command.log`, log growth, build `exit-code`, wheel inventory, and
validation artifacts before launching any other x86_64 job.
