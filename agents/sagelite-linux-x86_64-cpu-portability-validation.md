# Sagelite Linux x86_64 CPU Portability Validation

## 2026-07-21 22:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-21T22:31:49Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,297,276,928 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 80,549,621,760 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite automation work. No remote state was
changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-21T22:32:15Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` remote ref were
synchronized at `6274d67da670fed4ae05e2f4bcb2c91a3d9fce0e`. Exact pushed
source `014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first
clean fat-binary CPython 3.12 build once the assigned filesystem returns with
at least 100 GiB free.

## 2026-07-21 22:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-21T22:01:15Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,306,849,280 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 83,309,445,120 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` service names were not found and were inactive with
successful retained result and exit-status properties. Docker was absent,
Podman had no active containers, and independent service and process scans
found no Sagelite automation work. An unrelated CoWasm build remained active
outside the assigned automation scope. No remote state was changed and no
`post64` build was started.

The public manifest fetched at `2026-07-21T22:01:16Z` remains the 177-wheel
set generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post64` artifact. Exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first clean
fat-binary CPython 3.12 build once the assigned filesystem returns with at
least 100 GiB free.

## 2026-07-21 21:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-21T21:31:32Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,313,693,696 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 83,756,257,280 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` service names were not found and were inactive with
successful retained result and exit-status properties. Docker was absent,
Podman had no active containers, and independent service and process scans
found no Sagelite automation work. No remote state was changed and no
`post64` build was started.

The public manifest fetched at the same checkpoint remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post64` artifact. Exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first clean
fat-binary CPython 3.12 build once the assigned filesystem returns with at
least 100 GiB free.

## 2026-07-21 Exact Post64 Source Pushed; Assigned Mount Absent

The repair was committed, pushed, and verified on `origin/develop` as exact
`10.9.post64` source `014ae4bf44318b6f5032053957a92291d4363b7a`.

Read-only preflight at `2026-07-21T21:01:27Z` reached `host` as native Linux
`x86_64`, but `/mnt/cocalc-scratch` was absent. The 24,883,167,232-byte root
filesystem had only 9,335,996,416 bytes free. The only visible bulk
filesystem, `/mnt/cocalc`, had 83,778,723,840 bytes free, below the binary
100 GiB heavy-build threshold, and it is not the runbook-assigned automation
root. The historical `post60` run was absent, and both old service names were
not found and inactive. Docker was absent, Podman had no active containers,
and an unrelated CoWasm Sagelite build was active outside the assigned
automation scope. No remote state was changed and no `post64` build was
started.

The public manifest fetched during the same `2026-07-21T21:01Z`
reconciliation remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with no `post64`
artifact. The first fat-binary build remains blocked until the assigned bulk
filesystem returns with at least 100 GiB free, or another qualifying
automation root is explicitly approved.

## 2026-07-21 Public Post9 SIGILL Diagnosis And Post64 Repair

A Sage developer reported that the documented CPython 3.14 install command on
Debian testing terminated during `from sage.all import *` with `SIGILL`.  The
reported crash trace is preserved at `/home/user/scratch/sagelite`:

```text
size:   7,777 bytes
sha256: acf7c40979f997a07d4dea37e058ea0dacb0c6df9c110d819c4176f03445a482
```

The first failing native frame is `__gmpn_sqr_basecase`, reached while
`sage.misc.randstate` initializes GMP's random state.  The later cysignals
frames and its missing-Cython diagnostic are crash-reporting behavior, not the
source of the illegal instruction.

The exact public CPython 3.14 wheel was downloaded to
`/scratch/sagelite-cpu-diagnosis/sagelite-post9-cp314.whl`:

```text
filename: sagelite-10.9.post9-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:     244,864,035 bytes
sha256:   0fe0a862dd0ec00b860d97d18df55995f5f54de6d2757e45a1d1047ed25c3e7c
```

Its bundled `libgmp-cf1565e2.so.10.5.0` has SHA256
`2aa2677d980a53710bed8127b6f884f2982fd7c37e2c45994c140c810f8ad8a5`.
`objdump -d -M intel --disassemble=__gmpn_sqr_basecase` shows unconditional
BMI2 and ADX instructions including `mulx`, `shrx`, `sarx`, `adcx`, and
`adox`.  The library has no `__gmpn_cpuvec_init` dynamic-dispatch symbol.  The
same wheel bundles a 40,595,993-byte library named
`libopenblas_zenp-r0-40fa294e.3.28.so`, confirming that OpenBLAS also selected
the AMD Zen build host rather than a portable runtime-dispatch build.

The Linux wheel hook previously configured Sage without
`--enable-fat-binary`.  Sage's existing package recipes use that setting to
enable GMP `--enable-fat`, OpenBLAS `DYNAMIC_ARCH=1`, and non-native modes for
NTL, FFLAS-FFPACK, and other CPU-sensitive dependencies.  The public Linux
x86_64 wheels and the retained local Linux x86_64 baselines are therefore
rejected as portability evidence even where they passed on the build host.

The `10.9.post64` working repair:

- configures all Linux wheel prefixes with `--enable-fat-binary`;
- moves the persistent native build into the new isolated profile
  `/host/sage-fat-v1-${AUDITWHEEL_PLAT}` so no old tuned library or install
  marker can be reused;
- passes that exact profile through compile, link, repair, and companion-wheel
  staging paths;
- checks cached `config.status` for `SAGE_FAT_BINARY=yes` and fails closed if
  an incompatible configuration is ever found in the fat profile.

Focused validation passed shell syntax checks, `git diff --check`, and five
Linux wheel-hook metadata tests. The complete companion-metadata file reported
261 passes plus three unrelated pre-existing failures involving stale generated
Flatter metadata and the already-absent Regina dependency. No repaired
`post64` wheel, old-CPU smoke, fresh install, or doctest pass is claimed yet.
The first authoritative Linux x86_64 build must start from the new empty fat
profile, and acceptance must add an x86_64 baseline probe without BMI2 or ADX
in addition to the standard fresh short and full gates.
