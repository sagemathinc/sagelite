# Sagelite Linux x86_64 CPU Portability Validation

## 2026-07-22 Exact Post64 Fat-Binary Build Started

The assigned `/mnt/cocalc-scratch` mount returned as a
527,297,863,680-byte ext4 filesystem with 191,941,595,136 bytes free during
the `2026-07-22T17:50:15Z` reconciliation. The old `post60` run was visible
but interrupted during primary compilation with no exit-code and no wheel, so
it supplies no evidence.

An initial exact-`post64` launch was stopped and rejected before native
compilation when live configuration exposed a doubled explicit overlay
destination. It produced zero wheels, and its artifacts are preserved at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260722-175330-014ae4bf443`.
The fresh authoritative replacement is active at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260722-175911-014ae4bf443`
under `sagelite-post64-x86-cp312-build-r1.service` and its guarded watcher.

The replacement uses exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` from a verified
146,483,200-byte archive with SHA256
`a7ce677432f01cff16fd93d88f6c12f3d988464d76a2c79aa215165d5df047ed`.
The persistent `sage-fat-v1-manylinux_2_28_x86_64` profile was absent before
the iteration and empty at launch. The actual manylinux environment reports
Linux `x86_64` and CPython 3.12.13, and Docker inspection proves that the
profile is over-mounted read/write at the exact path selected by the `post64`
hooks. The live build then ran `./configure` with `--enable-fat-binary`, copied
the resulting configuration into the persistent profile, and entered GMP
installation. The guarded validation adds a QEMU Nehalem probe that executes
CPUID leaf 7, asserts both BMI2 and ADX bits are absent, then imports Sage and
exercises representative GMP, polynomial, and dense real-matrix operations.
The normal strict short and full gates remain required after that probe. No
wheel or pass is claimed yet.

## 2026-07-22 15:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T15:31:16Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,341,075,456 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,259,780,096 bytes free, 1,885,597,696 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite or cibuildwheel automation work. No remote state was changed and
no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T15:31:43Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `c69bd1d35bb48afb92262189d39878d9cc4a0b98`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 15:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T15:01:25Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,356,136,448 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,308,235,776 bytes free, 1,934,053,376 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T15:01:49Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `69d8c527617c84694f12e2b54e4281a127a2145c`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 14:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T14:31:13Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,365,684,224 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,655,982,080 bytes free, 2,281,799,680 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch during the same reconciliation confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `8f0bf35b41fa33f1865c22044dd60d43f85b3104`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 14:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T14:01:13Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,380,560,896 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,732,081,664 bytes free, 2,357,899,264 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T14:01:25Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `5376737f75291333805ef6ccd9b02dd2ffa6bc46`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 13:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T13:31:22Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,388,347,392 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,715,836,928 bytes free, 2,341,654,528 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T13:31:35Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `19944363bba13eb3d349fff49b35047080b805ca`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 13:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T13:01:21Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,380,302,848 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,749,846,016 bytes free, 2,375,663,616 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T13:01:51Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `b381836b025eefa6a168909c974fc4b60565e7d5`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 12:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T12:31:21Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,388,179,456 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,770,158,080 bytes free, 2,395,975,680 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T12:31:53Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `5c0d0fee58eed8fe72c56be13e45e2bae815bbd9`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 12:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T12:01:40Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,399,816,192 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,752,369,152 bytes free, 2,378,186,752 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite or cibuildwheel automation work. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T12:02:08Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `487235771a4869d67d7863e941432631be30db7b`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 11:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T11:31:37Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,406,664,704 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,815,279,616 bytes free, 2,441,097,216 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite or cibuildwheel automation work. No remote state was changed and
no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T11:31:36Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `4a5ed6fb119db2dd6fbb990ec5e244ce43935be7`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 11:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T11:01:55Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,413,074,944 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,723,496,448 bytes free, 2,349,314,048 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite automation work. No remote state was
changed and no `post64` build was started.

A direct public-manifest fetch during the same reconciliation confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `574ae49c5f3d1b0117a51b6882bdd6321005ee9e`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 10:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T10:31:30Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,430,765,568 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,901,639,680 bytes free, 2,527,457,280 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite or cibuildwheel automation work. No remote state was changed and
no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T10:32Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `78a800b32bdb853eb087514d93015c453ec7154f`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 10:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T10:01:01Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path remained absent. The 24,883,167,232-byte root
filesystem had 9,446,100,992 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,967,499,264 bytes free, 2,593,316,864 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and independent service
and process scans found no Sagelite automation work. No remote state was
changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T10:01:33Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `3787a28db8ddc28fb319ead77ac4e55e47fa047f`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free or another qualifying
automation root is explicitly approved.

## 2026-07-22 09:31 UTC Host Unreachable

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-22T09:31:40Z`, `2026-07-22T09:32:04Z`, and
`2026-07-22T09:32:24Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` artifacts, service
state, container state, and process state therefore could not be rechecked.
The last successful read-only preflight remains the
`2026-07-22T08:31:54Z` evidence: `/mnt/cocalc-scratch` was absent, while the
unassigned `/mnt/cocalc` filesystem had 102,412,967,936 bytes free,
4,961,214,464 bytes below the binary 100 GiB heavy-build threshold. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T09:31:20Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `bbffe12a763c853d2091311c56b56f123e1ca146`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free.

## 2026-07-22 09:01 UTC Host Unreachable

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-22T09:01:37Z`, `2026-07-22T09:01:56Z`, and
`2026-07-22T09:02:14Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` artifacts, service
state, container state, and process state therefore could not be rechecked.
The last successful read-only preflight remains the `2026-07-22T08:31:54Z`
evidence: `/mnt/cocalc-scratch` was absent, while the unassigned
`/mnt/cocalc` filesystem had 102,412,967,936 bytes free, 4,961,214,464 bytes
below the binary 100 GiB heavy-build threshold. No remote state was changed
and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T09:01:37Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `b4f04be7789d9f81b93b3453dccdb21e75079a6b`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free.

## 2026-07-22 08:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T08:31:54Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,527,115,776 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 102,412,967,936 bytes free, 4,961,214,464 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work beyond the read-only preflight shell itself. No
remote state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-22T08:31:53Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `c71a20a955689749bbaa2bc0e7952659d0c57c50`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free.

## 2026-07-22 08:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T08:01:26Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,544,318,976 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 102,721,482,752 bytes free, 4,652,699,648 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the only matching
processes belonged to an unrelated CoWasm test workload outside the assigned
automation scope. No remote state was changed and no `post64` build was
started.

A direct public-manifest fetch at `2026-07-22T08:01:59Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `c1cceece833687d16fd8c2a5328a4f995c5557cc`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free.

## 2026-07-22 07:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T07:31:17Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,613,053,952 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 102,900,084,736 bytes free, 4,474,097,664 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the only matching
processes belonged to an unrelated CoWasm build outside the assigned
automation scope. No remote state was changed and no `post64` build was
started.

A direct public-manifest fetch at `2026-07-22T07:31:40Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `e061e28eb150c0be452aed4ed25df0ef6466d261`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`
remains ready for the first clean fat-binary CPython 3.12 build once the
assigned filesystem returns with at least 100 GiB free.

## 2026-07-22 07:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T07:01:13Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,675,825,152 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 103,239,163,904 bytes free, 4,135,018,496 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work beyond the read-only preflight scan. No remote
state was changed and no `post64` build was started.

A direct public-manifest fetch during the same checkpoint confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `b31a4960332ac7cdca94ced42ef8382fe73101f1`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a` remains
ready for the first clean fat-binary CPython 3.12 build once the assigned
filesystem returns with at least 100 GiB free.

## 2026-07-22 06:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T06:31:15Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,696,182,272 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 103,275,933,696 bytes free, 4,098,248,704 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work. No remote state was changed and no `post64` build
was started.

A direct public-manifest fetch at `2026-07-22T06:31:39Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `dc25e7b4b3b569b73dbf8117fd4aa00be82d4972`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a` remains
ready for the first clean fat-binary CPython 3.12 build once the assigned
filesystem returns with at least 100 GiB free.

## 2026-07-22 05:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T05:31:33Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,755,795,456 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 106,714,570,752 bytes free, 659,611,648 bytes below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned
automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the only matching
processes belonged to an unrelated CoWasm test workload outside the assigned
automation scope. No remote state was changed and no `post64` build was
started.

A direct public-manifest fetch at `2026-07-22T05:31:46Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post63` or `post64` artifact. Before this evidence edit, the canonical
checkout, its local tracking ref, and the directly queried `origin/develop`
remote ref were synchronized at `fd11e617b0f6dfcb4841b6853af9b1ac878625ca`.
Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a` remains
ready for the first clean fat-binary CPython 3.12 build once the assigned
filesystem returns with at least 100 GiB free.

## 2026-07-22 00:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T00:31:35Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,907,695,616 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 79,989,059,584 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work. No remote state was changed and no `post64` build
was started.

A direct public-manifest fetch at `2026-07-22T00:31:47Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` remote ref were
synchronized at `ca923a2e4cffb4cc3455bae9c6a47d8e066dbeea`. Exact pushed
source `014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first
clean fat-binary CPython 3.12 build once the assigned filesystem returns with
at least 100 GiB free.

## 2026-07-22 00:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T00:01:19Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,932,599,296 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 80,164,249,600 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work. No remote state was changed and no `post64` build
was started.

A direct public-manifest fetch at `2026-07-22T00:01:33Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` remote ref were
synchronized at `1b7e1420afcf1a793d4ad4e9af1badd9a3ebbaca`. Exact pushed
source `014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first
clean fat-binary CPython 3.12 build once the assigned filesystem returns with
at least 100 GiB free.

## 2026-07-21 23:31 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-21T23:31:24Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,271,767,040 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 79,677,571,072 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and the process scan found
no Sagelite automation work beyond the read-only preflight shell itself. No
remote state was changed and no `post64` build was started.

A direct public-manifest fetch at `2026-07-21T23:31:36Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` remote ref were
synchronized at `47152ce5cc1517a93110898c0c099e328c0c8e75`. Exact pushed
source `014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first
clean fat-binary CPython 3.12 build once the assigned filesystem returns with
at least 100 GiB free.

## 2026-07-21 23:01 UTC Assigned Mount Still Absent

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-21T23:01:44Z` and confirmed native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had 9,275,002,880 bytes free. The only visible bulk filesystem,
`/mnt/cocalc`, had 80,324,231,168 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root.

The historical `post60` run root was absent. Its service names were not found
and were inactive with successful retained result and exit-status properties.
Docker was absent, Podman had no active containers, and an independent process
scan found no Sagelite automation work. No remote state was changed and no
`post64` build was started.

A direct public-manifest fetch at `2026-07-21T23:02:13Z` confirmed that
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` remote ref were
synchronized at `6dd7065ecc3a189ea7bda9f476a84b4f17ce9288`. Exact pushed
source `014ae4bf44318b6f5032053957a92291d4363b7a` remains ready for the first
clean fat-binary CPython 3.12 build once the assigned filesystem returns with
at least 100 GiB free.

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
