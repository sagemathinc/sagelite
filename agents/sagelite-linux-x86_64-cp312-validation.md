# Sagelite Linux x86_64 CPython 3.12 Validation

## 2026-07-26 Assigned Mount Still Too Small At 10:02 UTC

Read-only reconciliation at `2026-07-26T10:02:01Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,445,134,336 bytes free, and the
separate `/mnt/cocalc` volume had 63,635,415,040 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,333,159,424 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`b7bf89ac8dd25a2274a7d7264c10f1fa83672b36`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 09:32 UTC

Read-only reconciliation at `2026-07-26T09:32:06Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,455,095,808 bytes free, and the
separate `/mnt/cocalc` volume had 63,646,507,008 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,334,609,408 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`1f1fbdba1027e98311add99346da6ed385c8130c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 09:02 UTC

Read-only reconciliation at `2026-07-26T09:02:51Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,456,410,624 bytes free, and the
separate `/mnt/cocalc` volume had 63,658,934,272 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,337,177,600 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`cf0b03fe8f96971e9447446d0a6abe49a2f2d3bc`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 08:31 UTC

Read-only reconciliation at `2026-07-26T08:31:33Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,457,807,360 bytes free, and the
separate `/mnt/cocalc` volume had 63,665,954,816 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,348,417,024 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`da5c67c276a50306f74961726cb9836949008ffd`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 08:01 UTC

Read-only reconciliation at `2026-07-26T08:01:58Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,450,049,536 bytes free, and the
separate `/mnt/cocalc` volume had 63,664,336,896 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,352,267,264 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`c35e91b97e0e4b74eb7fafb76ac607959f13eab4`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 07:31 UTC

Read-only reconciliation at `2026-07-26T07:31:54Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,451,393,024 bytes free, and the
separate `/mnt/cocalc` volume had 63,672,348,672 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,366,517,248 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`0515c2951d1035b84456fb9c6ec217b7723e3793`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 07:01 UTC

Read-only reconciliation at `2026-07-26T07:01:53Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,461,047,296 bytes free, and the
separate `/mnt/cocalc` volume had 63,679,967,232 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,383,527,936 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`d4e622667bacd6c438f09af2d8f3aa29af006612`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 06:32 UTC

Read-only reconciliation at `2026-07-26T06:32:01Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,462,341,632 bytes free, and the
separate `/mnt/cocalc` volume had 63,691,124,736 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,403,123,200 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`d5b641cc00614a2df441163a696ac81c0076e4a6`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 06:01 UTC

Read-only reconciliation at `2026-07-26T06:01:53Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,463,693,312 bytes free, and the
separate `/mnt/cocalc` volume had 63,697,575,936 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,494,623,744 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`e90e3c02252d3a0ce3c44877e58633ecf03f6814`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 05:32 UTC

Read-only reconciliation at `2026-07-26T05:32:17Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a literal-stdin `/proc` scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,454,645,248 bytes free, and the
separate `/mnt/cocalc` volume had 63,706,587,136 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,502,471,680 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`e7008f7c315f110183274a1375de22f5d34ffdf9`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 05:02 UTC

Read-only reconciliation at `2026-07-26T05:02:07Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding `/proc` scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,456,005,120 bytes free, and the
separate `/mnt/cocalc` volume had 63,715,909,632 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,498,379,776 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`828e8cec078d6bc92ab0d0ca7bb59721e0634bb2`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 04:31 UTC

Read-only reconciliation at `2026-07-26T04:31:57Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,467,375,616 bytes free, and the
separate `/mnt/cocalc` volume had 63,724,851,200 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,508,537,856 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`7d2bf5eece38848136b062d34187e411ee728291`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 04:02 UTC

Read-only reconciliation at `2026-07-26T04:02:05Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,468,710,912 bytes free, and the
separate `/mnt/cocalc` volume had 63,732,969,472 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,534,375,424 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`3d414d51eee8477fa8ac71747fe53c0162566056`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 03:31 UTC

Read-only reconciliation at `2026-07-26T03:31:43Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding encoded-pattern
process scan found zero Sagelite, cibuildwheel, or authoritative-run matches.
No result was inferred, no remote state was changed, and no duplicate build
was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,461,772,288 bytes free, and the
separate `/mnt/cocalc` volume had 63,737,008,128 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,548,994,048 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`4b9a7195ab1dac844e8bae0cb570b0f9e51e37f0`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 03:01 UTC

Read-only reconciliation at `2026-07-26T03:01:58Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an encoded-pattern process scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,463,128,064 bytes free, and the
separate `/mnt/cocalc` volume had 63,745,536,000 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,564,820,992 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`4e2f37d2597adb49c6f128164adb915f0dfd0215`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 02:31 UTC

Read-only reconciliation at `2026-07-26T02:31:57Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,472,868,352 bytes free, and the
separate `/mnt/cocalc` volume had 63,753,957,376 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,567,495,680 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`ad607e0e9aab0e1e1f16e680e372920731cd0ab4`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 02:01 UTC

Read-only reconciliation at `2026-07-26T02:01:13Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a wrapper-excluding process scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,474,359,296 bytes free, and the
separate `/mnt/cocalc` volume had 63,762,268,160 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,508,222,464 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`21b587823213dac1125b16d273ca9252d55c94de`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 01:31 UTC

Read-only reconciliation at `2026-07-26T01:31:51Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,475,858,432 bytes free, and the
separate `/mnt/cocalc` volume had 63,772,278,784 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,518,368,256 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`77b699cd96dfac00f5061838c1b08bee6cb0dcda`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 01:01 UTC

Read-only reconciliation at `2026-07-26T01:01:38Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a bracketed process scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,469,399,040 bytes free, and the
separate `/mnt/cocalc` volume had 63,778,693,120 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,528,624,640 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`7ca0f16229eee3d780085abdb0b930d27d25450b`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 00:31 UTC

Read-only reconciliation at `2026-07-26T00:31:22Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a bracketed process scan found zero
Sagelite, cibuildwheel, or authoritative-run matches. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,470,877,696 bytes free, and the
separate `/mnt/cocalc` volume had 63,785,476,096 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,522,484,736 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`b367dd3b8d06fbbf113ae335ad91e0b99644252c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-26 Assigned Mount Still Too Small At 00:01 UTC

Read-only reconciliation at `2026-07-26T00:01:53Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and separate bracketed process scans found
zero Sagelite, cibuildwheel, or authoritative-run matches. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,480,990,720 bytes free, and the
separate `/mnt/cocalc` volume had 63,797,792,768 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,521,407,488 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`92010750656f0f8677968b3994d7b82ee33c6811`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 23:31 UTC

Read-only reconciliation at `2026-07-25T23:31:40Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and a bracketed process scan found zero
matches. No result was inferred, no remote state was changed, and no duplicate
build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,421,426,688 bytes free, and the
separate `/mnt/cocalc` volume had 63,801,430,016 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,533,576,704 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`f5023cd2965c9f8ae896d902e80f9ca04cc6e506`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 23:02 UTC

Read-only reconciliation at `2026-07-25T23:02:06Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,422,716,928 bytes free, and the
separate `/mnt/cocalc` volume had 63,808,847,872 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,541,760,512 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`99c606d949725094276f691988ea44642e46fa59`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 22:31 UTC

Read-only reconciliation at `2026-07-25T22:31:29Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,424,084,992 bytes free, and the
separate `/mnt/cocalc` volume had 63,815,987,200 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,560,495,616 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`e7cbe1dc5ac58d1abf87dc8a63ccb529a5b276eb`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 22:01 UTC

Read-only reconciliation at `2026-07-25T22:01:34Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,417,506,816 bytes free, and the
separate `/mnt/cocalc` volume had 63,824,789,504 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,570,862,592 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`601fe5e1217fedc38672285515430bc8179a02f4`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 21:31 UTC

Read-only reconciliation at `2026-07-25T21:31:36Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,418,870,784 bytes free, and the
separate `/mnt/cocalc` volume had 63,830,409,216 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,577,895,424 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`ab624438fa8256e4b6973cbade00172d8edd959a`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 21:01 UTC

Read-only reconciliation at `2026-07-25T21:01:36Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,428,692,992 bytes free, and the
separate `/mnt/cocalc` volume had 63,844,556,800 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,590,113,792 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`218dc2ce529d9f42488d353a7d6d36720c536999`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 20:31 UTC

Read-only reconciliation at `2026-07-25T20:31:21Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,430,097,920 bytes free, and the
separate `/mnt/cocalc` volume had 63,853,899,776 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,585,034,752 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`c0b0212327dc9848115860716b6aeb6ad6db1c7c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 20:01 UTC

Read-only reconciliation at `2026-07-25T20:01:25Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,431,420,928 bytes free, and the
separate `/mnt/cocalc` volume had 63,861,555,200 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,592,219,136 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`6c1378a44960c2a8b010e0d22a038420fb48f33a`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 19:31 UTC

Read-only reconciliation at `2026-07-25T19:31:27Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,423,290,368 bytes free, and the
separate `/mnt/cocalc` volume had 63,865,454,592 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,623,057,920 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`6db0c6a6c5b0b64d547a5829c9ae34145686fa39`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 19:01 UTC

Read-only reconciliation at `2026-07-25T19:01:23Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,424,699,392 bytes free, and the
separate `/mnt/cocalc` volume had 63,872,249,856 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,646,536,192 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`f00c22647e19973321e80647abc5ea4d4d7f459f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 18:32 UTC

Read-only reconciliation at `2026-07-25T18:32:17Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,434,431,488 bytes free, and the
separate `/mnt/cocalc` volume had 63,878,180,864 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,645,655,552 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`576fa9ae0a0fc2d161e7af5163cb35219612adcc`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 18:01 UTC

Read-only reconciliation at `2026-07-25T18:01:57Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,435,758,592 bytes free, and the
separate `/mnt/cocalc` volume had 63,889,604,608 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,652,946,432 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`c05976d10a8922271088ba6d8f80c9c0ca075fd7`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 17:31 UTC

Read-only reconciliation at `2026-07-25T17:31:51Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,437,085,696 bytes free, and the
separate `/mnt/cocalc` volume had 63,900,061,696 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,621,730,816 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`2fade86fcda7cc7346b4a03a0f74964eb6ebeb8f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 17:01 UTC

Read-only reconciliation at `2026-07-25T17:01:56Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,429,422,080 bytes free, and the
separate `/mnt/cocalc` volume had 63,910,801,408 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,551,238,656 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`3341d96df7ef8c35e93eb2fdb42d00d6422ebb0b`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 16:32 UTC

Read-only reconciliation at `2026-07-25T16:32:05Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free. Its only entry was
`lost+found`, the authoritative exact-source run root remained absent, and
both durable service names were not found and inactive. Docker was absent,
Podman had no active container, and an ancestor-excluding process scan found
zero external matches. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,430,720,512 bytes free, and the
separate `/mnt/cocalc` volume had 63,917,584,384 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,619,752,448 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`712450d3d28350c7c3312978adf545807f7cc76e`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 16:02 UTC

Read-only reconciliation at `2026-07-25T16:02:05Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
excluding `/proc` scan found zero external processes matching the service or
run names. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,440,411,648 bytes free, and the
separate `/mnt/cocalc` volume had 63,925,886,976 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,624,004,096 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`ef923705e496b762b1bdeb01a4ccac6e6a78f976`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 15:31 UTC

Read-only reconciliation at `2026-07-25T15:31:51Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
excluding `/proc` scan found zero external processes matching the service or
run names. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,441,755,136 bytes free, and the
separate `/mnt/cocalc` volume had 63,936,225,280 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,630,422,528 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`fa9872b679ae09a75119c5ed479e5c8163ee19bc`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 15:01 UTC

Read-only reconciliation at `2026-07-25T15:01:58Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
excluding `/proc` scan found zero external processes matching the service or
run names. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,443,020,800 bytes free, and the
separate `/mnt/cocalc` volume had 63,941,312,512 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,622,816,256 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`7846b736e3a1bb745a72280e8184e5a324415434`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 14:31 UTC

Read-only reconciliation at `2026-07-25T14:31:46Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
excluding `/proc` scan found zero external processes matching the service or
run names. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,436,086,272 bytes free, and the
separate `/mnt/cocalc` volume had 63,947,890,688 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,651,152,384 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`fa980a73864505112a46ae57a0807a616e569f54`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 14:01 UTC

Read-only reconciliation at `2026-07-25T14:01:42Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,437,437,952 bytes free, and the
separate `/mnt/cocalc` volume had 63,954,837,504 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,648,301,568 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`2bd2ce654da269af3d7aa3664030fc205edc52e4`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 13:31 UTC

Read-only reconciliation at `2026-07-25T13:31:40Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,447,116,800 bytes free, and the
separate `/mnt/cocalc` volume had 63,969,906,688 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,643,709,952 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`2e8e4641bae22cb5889f42b31490392978b4f8b6`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 13:01 UTC

Read-only reconciliation at `2026-07-25T13:01:53Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,448,415,232 bytes free, and the
separate `/mnt/cocalc` volume had 63,977,037,824 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,664,919,040 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`154958a5178bc644ccc5b2844ab78548185d1ce2`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 12:32 UTC

Read-only reconciliation at `2026-07-25T12:32:14Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,449,693,184 bytes free, and the
separate `/mnt/cocalc` volume had 63,988,117,504 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,680,127,488 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`09d0e866c719cab96aa2ad0128aa090b3ae7f65b`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 12:01 UTC

Read-only reconciliation at `2026-07-25T12:01:34Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,446,477,824 bytes free, and the
separate `/mnt/cocalc` volume had 63,993,585,664 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,674,888,704 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`beca88681744d3529e610d3ce964472f3adc911b`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 11:31 UTC

Read-only reconciliation at `2026-07-25T11:31:56Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,447,817,216 bytes free, and the
separate `/mnt/cocalc` volume had 63,986,831,360 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,689,499,136 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`de45c2dd65dd964a03c65c5c959cc3ba70c87e9c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 11:02 UTC

Read-only reconciliation at `2026-07-25T11:02:29Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,457,475,584 bytes free, and the
separate `/mnt/cocalc` volume had 63,994,318,848 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,690,920,448 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`c1492567f477f2a852200581ce1c19e05b5ebdc9`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 10:32 UTC

Read-only reconciliation at `2026-07-25T10:32:26Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,458,802,688 bytes free, and the
separate `/mnt/cocalc` volume had 63,994,310,656 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,707,177,472 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`8c97160cafec2585109027da5604e96e1bc5d1f2`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 10:01 UTC

Read-only reconciliation at `2026-07-25T10:01:43Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,460,174,848 bytes free, and the
separate `/mnt/cocalc` volume had 63,997,808,640 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,724,818,944 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`d405b0c8fdff5d7bf6eb97676248ed92ad62e464`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 09:02 UTC

Read-only reconciliation at `2026-07-25T09:02:30Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,454,673,920 bytes free, and the
separate `/mnt/cocalc` volume had 63,989,542,912 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,692,145,152 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`7a1df35ed169d4123a9c15689028e04a45c5599e`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 08:32 UTC

Read-only reconciliation at `2026-07-25T08:32:16Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,464,537,088 bytes free, and the
separate `/mnt/cocalc` volume had 64,001,122,304 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,733,318,144 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`b8557524a1fc4a27f71b62236323457dd09345bb`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 08:02 UTC

Read-only reconciliation at `2026-07-25T08:02:13Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,466,015,744 bytes free, and the
separate `/mnt/cocalc` volume had 64,008,052,736 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,745,757,696 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`98c5be4a42345a3e3f344972b449966d3567aa97`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 07:32 UTC

Read-only reconciliation at `2026-07-25T07:32:09Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,467,539,456 bytes free, and the
separate `/mnt/cocalc` volume had 64,017,661,952 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,757,476,352 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`0004ae3d3f55f5edc0801afa006e0525c5730cff`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 07:01 UTC

Read-only reconciliation at `2026-07-25T07:01:57Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,467,035,648 bytes free, and the
separate `/mnt/cocalc` volume had 64,025,788,416 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,721,312,768 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`b0745ae166a47417a6ae1db59f4a444198e836c8`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 06:32 UTC

Read-only reconciliation at `2026-07-25T06:32:14Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,468,416,000 bytes free, and the
separate `/mnt/cocalc` volume had 64,035,901,440 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,619,334,656 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`86e22be697b8447ff97e6efd5f0cca7ccc1e2b85`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 06:02 UTC

Read-only reconciliation at `2026-07-25T06:02:07Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,438,953,472 bytes free, and the
separate `/mnt/cocalc` volume had 63,595,024,384 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 58,516,398,080 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`9df1861d01edf16fd1a7cfe14a2d574463fb3f2c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 05:32 UTC

Read-only reconciliation at `2026-07-25T05:32:06Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an ancestor-
and self-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,440,407,552 bytes free, and the
separate `/mnt/cocalc` volume had 63,604,035,584 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,233,902,592 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`6309c4dfd622a1d02cb3ca19a2f4a9a39217a364`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 05:02 UTC

Read-only reconciliation at `2026-07-25T05:02:59Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor- and self-excluding `/proc` check found zero external processes
matching the service or run names. No result was inferred, no remote state
was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,441,824,768 bytes free, and the
separate `/mnt/cocalc` volume had 63,613,247,488 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,235,307,520 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`79f1f8b9b14d5286ba7cca77641e1c82660a1c05`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 04:31 UTC

Read-only reconciliation at `2026-07-25T04:31:57Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and a corrected
ancestor- and self-excluding `/proc` check found zero external processes
matching the service or run names. No result was inferred, no remote state
was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,436,545,024 bytes free, and the
separate `/mnt/cocalc` volume had 63,619,162,112 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,249,442,816 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`a8a96baff650c847333c68fd196b318b45cddd2e`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 04:02 UTC

Read-only reconciliation at `2026-07-25T04:02:30Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. The authoritative
exact-source run root remained absent. Both durable service names were not
found and inactive with retained successful result and exit-status
properties on the currently reached machine. Docker was absent, Podman had
no active container, and an ancestor-safe process check found zero external
processes matching the service or run names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,438,007,296 bytes free, and the
separate `/mnt/cocalc` volume had 63,629,824,000 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,270,201,344 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`3bb8056cf5d1eb035844350572a203da9faf180a`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 03:31 UTC

Read-only reconciliation at `2026-07-25T03:31:24Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,447,972,864 bytes free, and the
separate `/mnt/cocalc` volume had 63,639,552,000 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,279,851,520 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`b044ab73344303aade3608201d415b9be65c3d14`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 03:01 UTC

Read-only reconciliation at `2026-07-25T03:01:45Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,449,443,328 bytes free, and the
separate `/mnt/cocalc` volume had 63,652,503,552 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,285,729,280 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`971e3a462bf8fc51b3d02e5c092fae2808c22be8`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 02:31 UTC

Read-only reconciliation at `2026-07-25T02:31:28Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,450,950,656 bytes free, and the
separate `/mnt/cocalc` volume had 63,653,998,592 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,279,765,504 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`586c32fe25b2c51a174aea4407df48f1f1d22212`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 02:01 UTC

Read-only reconciliation at `2026-07-25T02:01:40Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,445,564,416 bytes free, and the
separate `/mnt/cocalc` volume had 63,664,222,208 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,298,754,560 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`7fe22958a691b340b1328c4e14b97fea7845dd56`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 01:31 UTC

Read-only reconciliation at `2026-07-25T01:31:47Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,447,055,360 bytes free, and the
separate `/mnt/cocalc` volume had 63,673,008,128 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,329,249,280 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`8a5db535870fc45ba566b7da6f45d21503bfae0f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 01:01 UTC

Read-only reconciliation at `2026-07-25T01:01:52Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,457,008,640 bytes free, and the
separate `/mnt/cocalc` volume had 63,677,001,728 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,337,850,880 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`a81f1923ea1da0e0117d6a57e4b6efcd07e565a9`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 00:31 UTC

Read-only reconciliation at `2026-07-25T00:31:50Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,458,577,408 bytes free, and the
separate `/mnt/cocalc` volume had 63,689,441,280 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,349,311,488 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`788bdc975bf96bc36f0a91f27346152e47a13c18`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-25 Assigned Mount Still Too Small At 00:01 UTC

Read-only reconciliation at `2026-07-25T00:01:39Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,459,277,824 bytes free, and the
separate `/mnt/cocalc` volume had 63,706,439,680 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,363,471,360 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`ccc818edd2ebd47b276f86f991cdfda61eedb40c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 23:31 UTC

Read-only reconciliation at `2026-07-24T23:31:47Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,387,114,496 bytes free, and the
separate `/mnt/cocalc` volume had 63,712,358,400 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,365,359,616 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`a00933534c137add8d247abffd6d12ea1545b672`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 23:01 UTC

Read-only reconciliation at `2026-07-24T23:01:27Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and a separate
ancestor-safe process check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,388,412,928 bytes free, and the
separate `/mnt/cocalc` volume had 63,720,103,936 bytes free, also below the
threshold and outside the assigned automation root. The controller
filesystems used by this iteration had 59,392,729,088 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`a85a9a2defb22c1d49562e3f4cae063ecbbb163c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 22:31 UTC

Read-only reconciliation at `2026-07-24T22:31:17Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,398,071,296 bytes free, and the
separate `/mnt/cocalc` volume had 63,729,205,248 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,399,929,856 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`1a2428aa73521101dc66203df0964a9528a9d784`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 22:01 UTC

Read-only reconciliation at `2026-07-24T22:01:15Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and an
ancestor-excluding `/proc` check found zero external processes matching the
service or run names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,399,357,440 bytes free, and the
separate `/mnt/cocalc` volume had 63,734,976,512 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,372,154,880 bytes free under
`/home/user` and 161,024,094,208 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`003718df970ab064baa1ac9bd60d0d44372b7bc1`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 21:31 UTC

Read-only reconciliation at `2026-07-24T21:31:52Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and a separate
process check found no external process matching the service or run names. No
result was inferred, no remote state was changed, and no duplicate build was
launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,400,623,104 bytes free, and the
separate `/mnt/cocalc` volume had 63,740,182,528 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,377,696,768 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`fdeebacfb2913bda2e658103d2c43b755fad1d6f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 21:01 UTC

Read-only reconciliation at `2026-07-24T21:01:20Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and a separate
process check found no external process matching the service or run names. No
result was inferred, no remote state was changed, and no duplicate build was
launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,391,583,232 bytes free, and the
separate `/mnt/cocalc` volume had 63,748,722,688 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,397,722,112 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`197dd00c2b308b9b7776945d8aac536be516e614`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Still Too Small At 20:31 UTC

Read-only reconciliation at `2026-07-24T20:31:37Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remained backed by the 52,521,566,208-byte
`/dev/sdc` ext4 filesystem with 49,820,409,856 bytes free, rather than the
previously observed 527,297,863,680-byte build filesystem. Its only entry was
`lost+found`, and the authoritative exact-source run root remained absent.
Both durable service names were not found and inactive with retained
successful result and exit-status properties on the currently reached
machine. Docker was absent, Podman had no active container, and a
`/proc`-based check excluding the probe's own ancestor processes found no
external process matching the service or run names. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The assigned filesystem cannot satisfy the binary 100 GiB heavy-build
threshold even when empty, so no cleanup can make it suitable for the
`post64` rebuild. The root filesystem had 17,392,869,376 bytes free, and the
separate `/mnt/cocalc` volume had 63,757,352,960 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,450,490,880 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`82aa9818da689f49dce6bacaa7ccd4735c6312c2`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Mount Returned Too Small At 20:01 UTC

Read-only reconciliation at `2026-07-24T20:01:38Z` reached `host` on the
first bounded attempt as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path was mounted again, but it was backed by a
52,521,566,208-byte ext4 filesystem with only 49,820,409,856 bytes free,
instead of the previously observed 527,297,863,680-byte build filesystem.
The authoritative run root remained absent. Both durable service names were
not found and inactive with retained successful result and exit-status
properties on the currently reached machine. Docker was absent, Podman had no
active container, and a separate process check found no external process
matching the automation names. No result was inferred, no remote state was
changed, and no duplicate build was launched.

The assigned filesystem is less than half the binary 100 GiB heavy-build
threshold even when empty, so cleanup cannot make it suitable for the
`post64` rebuild. The root filesystem had 17,402,638,336 bytes free, and the
separate `/mnt/cocalc` volume had 63,742,218,240 bytes free, also below the
threshold and outside the runbook-assigned automation root. The controller
filesystems used by this iteration had 59,436,814,336 bytes free under
`/home/user` and 161,024,131,072 bytes free under `/scratch`.

A direct public manifest fetch confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its tracking
ref, and the directly queried `origin/develop` ref were synchronized at
`5fc11c60c3102054df40f78e77b4ad97299561ad`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 19:31 UTC

Read-only reconciliation at `2026-07-24T19:31:20Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and a
separate process check found no external process matching the automation
names. No result was inferred, no remote state was changed, and no duplicate
build was launched.

The root filesystem had 17,336,508,416 bytes free. The separate
`/mnt/cocalc` volume had 63,697,711,104 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. The
controller filesystems used by this iteration had 59,445,522,432 bytes free
under `/home/user` and 161,024,131,072 bytes free under `/scratch`. A direct
public manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`a14576fac717de787cc7e8730982271725ac6c5b`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 19:01 UTC

Read-only reconciliation at `2026-07-24T19:01:41Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and a
separate process check found no external process matching the automation
names. No result was inferred, no remote state was changed, and no duplicate
build was launched.

The root filesystem had 17,329,762,304 bytes free. The separate
`/mnt/cocalc` volume had 63,708,721,152 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. The
controller filesystems used by this iteration had 59,459,805,184 bytes free
under `/home/user` and 161,024,131,072 bytes free under `/scratch`. A direct
public manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`df5f955acc83d098731cbc2f8000eb07ba946d49`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 18:31 UTC

Read-only reconciliation at `2026-07-24T18:31:20Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,340,592,128 bytes free. The separate
`/mnt/cocalc` volume had 63,717,679,104 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. The
controller filesystems used by this iteration had 59,441,647,616 bytes free
under `/home/user` and 161,024,131,072 bytes free under `/scratch`. A direct
public manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`23ee3493bada59e966600a188e1e90639969dbc6`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 18:01 UTC

Read-only reconciliation at `2026-07-24T18:01:32Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,409,421,312 bytes free. The separate
`/mnt/cocalc` volume had 63,689,334,784 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. The
controller filesystems used by this iteration had 59,463,962,624 bytes free
under `/home/user` and 161,024,131,072 bytes free under `/scratch`. A direct
public manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`4ab2d52c45803c89d0840932bdc7adbd33c3fe24`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 17:31 UTC

Read-only reconciliation at `2026-07-24T17:31:26Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,410,711,552 bytes free. The separate
`/mnt/cocalc` volume had 63,695,933,440 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`811115f121350bbe8f000fd200b131843f619428`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 17:01 UTC

Read-only reconciliation at `2026-07-24T17:01:41Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,416,069,120 bytes free. The separate
`/mnt/cocalc` volume had 63,696,879,616 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`4bad18b8b5855d882edbe37492bf9d75bd80f0c9`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 16:31 UTC

Read-only reconciliation at `2026-07-24T16:31:48Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,417,396,224 bytes free. The separate
`/mnt/cocalc` volume had 63,703,281,664 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`869ac0ad8fbe21d9b7efe74b4461d0fbec0ed696`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 16:01 UTC

Read-only reconciliation at `2026-07-24T16:01:23Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,428,680,704 bytes free. The separate
`/mnt/cocalc` volume had 63,707,721,728 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`b503faf13fbff553d9b9ac70bc0cca3ece145d41`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 15:31 UTC

Read-only reconciliation at `2026-07-24T15:31:17Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,430,003,712 bytes free. The separate
`/mnt/cocalc` volume had 63,717,580,800 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`e6eacac4b5d6c7cc1ac4abdf8e7aeac939f71ff2`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 15:01 UTC

Read-only reconciliation at `2026-07-24T15:01:05Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,431,392,256 bytes free. The separate
`/mnt/cocalc` volume had 63,723,462,656 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`2e8ebd6b266f3a323b787cae4d5e46cd2ffe6ec9`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 14:31 UTC

Read-only reconciliation at `2026-07-24T14:31:25Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,423,192,064 bytes free. The separate
`/mnt/cocalc` volume had 63,732,420,608 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`ca38dd1d300bb0d37bcb70db96957089cf278362`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 14:01 UTC

Read-only reconciliation at `2026-07-24T14:01:32Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,424,474,112 bytes free. The separate
`/mnt/cocalc` volume had 63,735,201,792 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`93035eeef6681f3ffd692640d049f32daf68e5f7`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 13:31 UTC

Read-only reconciliation at `2026-07-24T13:31:28Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,434,189,824 bytes free. The separate
`/mnt/cocalc` volume had 63,739,469,824 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`541dac45c79028c3b1f1c8b5b98ccbd35e3cff8a`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 13:01 UTC

Read-only reconciliation at `2026-07-24T13:01:44Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,435,492,352 bytes free. The separate
`/mnt/cocalc` volume had 63,744,933,888 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`10164294a0731af22a8aeccc662f488f567fb960`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 12:31 UTC

Read-only reconciliation at `2026-07-24T12:31:05Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,436,807,168 bytes free. The separate
`/mnt/cocalc` volume had 63,759,712,256 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`35532176f6111f43feead87c579bc47eb4293a07`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 12:02 UTC

Read-only reconciliation at `2026-07-24T12:02:00Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,411,375,104 bytes free. The separate
`/mnt/cocalc` volume had 63,765,651,456 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`acd819c889775774a80c901e19b8fd4dad3bdf26`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 11:31 UTC

Read-only reconciliation at `2026-07-24T11:31:33Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,412,681,728 bytes free. The separate
`/mnt/cocalc` volume had 63,776,894,976 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`36365febdb36e6e5742211e81b6bff3b3b63b8a9`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 11:01 UTC

Read-only reconciliation at `2026-07-24T11:01:19Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,422,372,864 bytes free. The separate
`/mnt/cocalc` volume had 63,782,297,600 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`e633927d9f3b48461daff641b813a8ed45f309fd`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 10:31 UTC

Read-only reconciliation at `2026-07-24T10:31:45Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative run root was
therefore invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the automation names. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 17,423,654,912 bytes free. The separate
`/mnt/cocalc` volume had 63,783,878,656 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`7289030de16f7a7a1cd1b9a26cb3c547ffcdfa0f`.

## 2026-07-24 Assigned Bulk Run Inaccessible At 10:01 UTC

Read-only reconciliation at `2026-07-24T10:01:48Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the machine had rebooted
at `09:46:26Z` and the assigned `/mnt/cocalc-scratch` path was absent. The
authoritative run root was therefore invisible. Both durable service names
were not found and inactive with retained successful result and exit-status
properties on the currently reached machine. Docker was absent, Podman had no
active container, and no external process matched the exact run root or
service names. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The root filesystem had 17,424,990,208 bytes free. The separate
`/mnt/cocalc` volume had 63,791,058,944 bytes free, below the binary 100 GiB
heavy-build threshold and outside the runbook-assigned automation root. A
direct public manifest fetch confirmed the unchanged 177-wheel set generated
at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`013ff1b59f94eb1d26dd0349f0f992b9e962015f`.

## 2026-07-24 Assigned Host Unreachable At 09:32 UTC

Three bounded read-only SSH attempts to `host` timed out during connection, so
the authoritative run root, durable service state, log growth, exit-code
artifacts, wheel outputs, and assigned bulk-filesystem capacity could not be
reconciled. The possibly surviving exact-source build and guarded watcher were
left untouched. No duplicate build was launched, no remote state was changed,
and no wheel, old-CPU result, validation pass, cell acceptance, or publication
is inferred.

The public `dev/manifest.json` was fetched independently with a pip user agent
and remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its tracking ref, and the directly
queried `origin/develop` ref were synchronized at
`f4cbc927a10158cfc5a369f918019f61b2ea6e18`.

## 2026-07-24 Resumed Post64 Build Healthy At 09:01 UTC

Read-only reconciliation at `2026-07-24T09:01:41Z` found the controlled
same-tree resume healthy. Both
`sagelite-post64-x86-cp312-build-r1.service` and
`sagelite-post64-x86-cp312-watch-r1.service` had remained continuously active
since `08:41:52Z`; their main PIDs were 1866048 and 1866076. The build service
still executed the recorded `build.sh` from the authoritative run root, and
the source checkout remained clean at exact pushed SHA
`014ae4bf44318b6f5032053957a92291d4363b7a`.

The native manylinux container had been up for 19 minutes and was using about
1,497% CPU with 80 processes. Its live process tree showed Maxima compiling
through the retained fat ECL together with Sage C and C++ extension modules.
Compiler invocations recorded `-march=x86-64 -mtune=generic`, while the build
continued against `/host/sage-fat-v1-manylinux_2_28_x86_64`. The resumed
command log had grown to 311,099 bytes, and direct container inspection showed
new compiler processes and output files after its last buffered write. The
watcher remained asleep behind the build-success gate. The assigned
527,297,863,680-byte filesystem had 165,481,246,720 bytes free.

No wheel, nonempty exit-code artifact, old-CPU result, validation pass, cell
acceptance, or publication is claimed yet. The directly fetched public
manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with no `post64` artifact. Before this
evidence edit, the canonical checkout, local tracking ref, and directly
queried `origin/develop` ref were synchronized at
`ab26fc179c1105a921bc5d3d81ca1f9cdc6f918e`.

## 2026-07-24 Exact Post64 Fat-Binary Build Resumed At 08:41 UTC

Read-only reconciliation at `2026-07-24T08:39:53Z` reached `host` on the
first bounded attempt as native Linux `x86_64` and found the assigned
527,297,863,680-byte `/mnt/cocalc-scratch` ext4 filesystem restored, with
174,154,424,320 bytes free. The authoritative run root
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260722-175911-014ae4bf443`
was visible again. It contained no wheel. Its original command log ended
during primary compilation, while `exit-code` and
`orchestration-exit-code` were zero-byte files and therefore not valid
results. The builder had rebooted at `2026-07-23T20:44:32Z`; both transient
units were absent and inactive, and no Docker container or matching external
process was active. No result was inferred from the retained successful unit
properties.

Exact pushed source `014ae4bf44318b6f5032053957a92291d4363b7a`, committed tree
`08c39ac15ef341f68af0676dfb4f9b61de0010db`, the clean checkout, and the
146,483,200-byte source archive with SHA256
`a7ce677432f01cff16fd93d88f6c12f3d988464d76a2c79aa215165d5df047ed`
all passed. All four launcher scripts matched their recorded hashes. The
persistent profile retained the exact build's cached prerequisites, its
`config.status` recorded `--enable-fat-binary` and `SAGE_FAT_BINARY=yes`, and
the host prefix symlink resolved to that profile. The interrupted zero-byte
control files were preserved separately as
`exit-code.interrupted-20260722` and
`orchestration-exit-code.interrupted-20260722`.

A controlled same-tree resume launched at `2026-07-24T08:41:52Z` under the
original `sagelite-post64-x86-cp312-build-r1.service` and
`sagelite-post64-x86-cp312-watch-r1.service` names. Its new durable logs are
`resume1-20260724-0844-command.log` and
`resume1-20260724-0844-orchestration.log` in the authoritative run root. At
`2026-07-24T08:42:25Z`, both services were active. The actual manylinux
container reported native `x86_64` and CPython 3.12.13, and Docker inspection
proved that the exact isolated fat prefix was mounted read/write at
`/host/sage-fat-v1-manylinux_2_28_x86_64`.

The watcher remains gated on build exit zero. It will then assemble the exact
closure, run the QEMU Nehalem probe after asserting that BMI2 and ADX are
absent, and run independent fresh short and full gates. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. No wheel,
validation pass, cell acceptance, or publication is claimed yet.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 08:31 UTC

Read-only reconciliation at `2026-07-24T08:31:21Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,566,752,768 bytes free. The separate `/mnt/cocalc`
volume had 94,375,497,728 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`185e03b35d2d794cc98f626a8d819faa01d159c3`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 08:01 UTC

Read-only reconciliation at `2026-07-24T08:01:34Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,595,613,184 bytes free. The separate `/mnt/cocalc`
volume had 95,385,055,232 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`8a84c4d4ee72faee859833a0bd6a21fafaaee4fd`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 07:31 UTC

Read-only reconciliation at `2026-07-24T07:31:28Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,256,763,392 bytes free. The separate `/mnt/cocalc`
volume had 94,559,940,608 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`e166ebf78d3970baf69c73111dd5812c555b0db7`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 07:01 UTC

Read-only reconciliation at `2026-07-24T07:01:26Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,274,257,408 bytes free. The separate `/mnt/cocalc`
volume had 94,778,765,312 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`fc106415421483204f91ce54076eaeeac7dea74a`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 06:31 UTC

Read-only reconciliation at `2026-07-24T06:31:29Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,269,526,528 bytes free. The separate `/mnt/cocalc`
volume had 94,795,616,256 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`ca7cacdd810a8c61020b26ce8cf4f04f02080937`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 06:01 UTC

Read-only reconciliation at `2026-07-24T06:01:39Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,335,566,336 bytes free. The separate `/mnt/cocalc`
volume had 97,520,742,400 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`ffe5ead5f7d8d6760ba4e3784b247bb0b6a1da7b`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 05:31 UTC

Read-only reconciliation at `2026-07-24T05:31:26Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,334,345,728 bytes free. The separate `/mnt/cocalc`
volume had 97,869,570,048 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`aea37c4ceac7cdca18965f6df28932afaf81bd2c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 05:01 UTC

Read-only reconciliation at `2026-07-24T05:01:24Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,372,381,184 bytes free. The separate `/mnt/cocalc`
volume had 97,916,678,144 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch confirmed the unchanged 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`103a9ae0b495f414790b9cc3044b57aff9d856c8`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 04:31 UTC

Read-only reconciliation at `2026-07-24T04:31:16Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,389,137,920 bytes free. The separate `/mnt/cocalc`
volume had 98,062,688,256 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. A direct public
manifest fetch at `2026-07-24T04:31Z` confirmed the unchanged 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels, versions `10.9.post8` and `10.9.post9`, and no `post64`
artifact. Before this evidence edit, the canonical checkout, its local
tracking ref, and the directly queried `origin/develop` ref were synchronized
at `b9e84445545a79c889eb7750c652dc67008e4752`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 04:01 UTC

Read-only reconciliation at `2026-07-24T04:01:33Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,407,123,456 bytes free. The separate `/mnt/cocalc`
volume had 98,164,604,928 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`ad3b86651655a466d31be554f79f07c24f59c0eb`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 03:31 UTC

Read-only reconciliation at `2026-07-24T03:31:20Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,418,153,984 bytes free. The separate `/mnt/cocalc`
volume had 98,205,163,520 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`9c70323b739d121b42a53b7dff2b87fd56563af5`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 03:01 UTC

Read-only reconciliation at `2026-07-24T03:01:23Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,435,959,296 bytes free. The separate `/mnt/cocalc`
volume had 98,257,141,760 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`a2a91c7dad8ec71dc55e277d1eeffa074977274e`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 02:31 UTC

Read-only reconciliation at `2026-07-24T02:31:33Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,449,385,984 bytes free. The separate `/mnt/cocalc`
volume had 98,403,921,920 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`a863df4551f0102a525296ad37d8eafcb79e5056`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 02:01 UTC

Read-only reconciliation at `2026-07-24T02:01:35Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,477,918,720 bytes free. The separate `/mnt/cocalc`
volume had 98,477,010,944 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`358ed2ce561d7e4f9b7ecc5b3c75feca9fffdb5c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 01:31 UTC

Read-only reconciliation at `2026-07-24T01:31:56Z` reached `host` as native
Linux `x86_64`, but the assigned `/mnt/cocalc-scratch` path was absent and
the authoritative `post64` run root remained invisible. Both durable service
names were not found and inactive with retained successful result and
exit-status properties on the currently reached machine. Docker was absent,
Podman had no active container, and no external process matched the exact run
root or service names. No result was inferred, no remote state was changed,
and no duplicate build was launched.

The root filesystem had 9,484,365,824 bytes free. The separate `/mnt/cocalc`
volume had 98,463,223,808 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`55b483aa77db7b6e05eae70a3ee362bd091ed248`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 01:01 UTC

Read-only reconciliation at `2026-07-24T01:01:15Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,507,446,784 bytes free. The separate `/mnt/cocalc`
volume had 98,840,264,704 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`d0c9871be7393448b1ee08adfcf528c227b24137`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 00:31 UTC

Read-only reconciliation at `2026-07-24T00:31:14Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,523,089,408 bytes free. The separate `/mnt/cocalc`
volume had 98,967,437,312 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`ef1e047bbb691f25cddd3a30c57c662b6758d6af`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-24 Assigned Bulk Run Still Inaccessible At 00:01 UTC

Read-only reconciliation at `2026-07-24T00:01:30Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,550,041,088 bytes free. The separate `/mnt/cocalc`
volume had 99,190,304,768 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`3bc4678816a51aad67904419acc642c9ff8d0c68`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 23:31 UTC

Read-only reconciliation at `2026-07-23T23:31:32Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 8,986,378,240 bytes free. The separate `/mnt/cocalc`
volume had 98,989,232,128 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`507ea4f48b651c2220308a93fe46ee9b153ce426`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 23:01 UTC

Read-only reconciliation at `2026-07-23T23:01:37Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,005,613,056 bytes free. The separate `/mnt/cocalc`
volume had 98,112,806,912 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`55ead2d852f3453e71891ffea8308ab7540329f3`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 22:31 UTC

Read-only reconciliation at `2026-07-23T22:31:25Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,024,942,080 bytes free. The separate `/mnt/cocalc`
volume had 99,685,990,400 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`0cb56bc4dc90bc9131eba524525e91c6c5455d0c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 22:01 UTC

Read-only reconciliation at `2026-07-23T22:01:28Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,042,653,184 bytes free. The separate `/mnt/cocalc`
volume had 99,940,540,416 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`63358d9a18994366f0d2e92e607487ca79141f2c`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 21:31 UTC

Read-only reconciliation at `2026-07-23T21:31:14Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,050,841,088 bytes free. The separate `/mnt/cocalc`
volume had 100,038,082,560 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`20592987553f5741afab5ee2b1683acf579bed7f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 21:01 UTC

Read-only reconciliation at `2026-07-23T21:01:38Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,071,902,720 bytes free. The separate `/mnt/cocalc`
volume had 99,971,448,832 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`27cfc0f7962d5f42755f91c6099f530472de4ffd`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 20:31 UTC

Read-only reconciliation at `2026-07-23T20:31:51Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,087,004,672 bytes free. The separate `/mnt/cocalc`
volume had 100,207,951,872 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`aac0184be7ea7484fce8861c270aff27a647ead0`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 20:01 UTC

Read-only reconciliation at `2026-07-23T20:01:30Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,096,617,984 bytes free. The separate `/mnt/cocalc`
volume had 101,312,950,272 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`ae6e744df21668d781a7f17e65181b2673bc4ae2`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 19:31 UTC

Read-only reconciliation at `2026-07-23T19:31:39Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching processes were unrelated CoWasm work. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,121,071,104 bytes free. The separate `/mnt/cocalc`
volume had 101,534,134,272 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`98a7e3dcc68a1db2e2929bc28da06a9dfb77d6e4`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 19:01 UTC

Read-only reconciliation at `2026-07-23T19:01:25Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,137,164,288 bytes free. The separate `/mnt/cocalc`
volume had 101,640,740,864 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`2488b84468a5c4c25fd9a3659cc9a346499500a5`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 18:31 UTC

Read-only reconciliation at `2026-07-23T18:31:26Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,154,523,136 bytes free. The separate `/mnt/cocalc`
volume had 101,602,942,976 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels,
versions `10.9.post8` and `10.9.post9`, and no `post64` artifact. Before this
evidence edit, the canonical checkout, its local tracking ref, and the
directly queried `origin/develop` ref were synchronized at
`554cd384739c8d1179aef5ea9f58e1f4ecf9755f`. Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` remains an ancestor of that
branch.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 18:01 UTC

Read-only reconciliation at `2026-07-23T18:01:39Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,172,733,952 bytes free. The separate `/mnt/cocalc`
volume had 101,876,006,912 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `557dd17cbce51d83560385607b8d9bbd0844318f`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 17:31 UTC

Read-only reconciliation at `2026-07-23T17:31:15Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,183,240,192 bytes free. The separate `/mnt/cocalc`
volume had 103,785,172,992 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `641b17a2bb1317b096d0fd0e2214bd5c270aee0f`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 17:01 UTC

Read-only reconciliation at `2026-07-23T17:01:25Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
external process matched the exact run root or service names. No result was
inferred, no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,200,836,608 bytes free. The separate `/mnt/cocalc`
volume had 104,411,779,072 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `09e2f9096801cc9b939deada958e4cea29d83bbf`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 16:31 UTC

Read-only reconciliation at `2026-07-23T16:31:06Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
process matched the exact run root or service names. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,237,938,176 bytes free. The separate `/mnt/cocalc`
volume had 104,917,463,040 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `9365dfba44d39a761e23dbfa451a7e0501d30681`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 16:01 UTC

Read-only reconciliation at `2026-07-23T16:01:29Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
automation process was visible beyond the reconciliation command itself. No
result was inferred, no remote state was changed, and no duplicate build was
launched.

The root filesystem had 9,258,999,808 bytes free. The separate `/mnt/cocalc`
volume had 105,111,674,880 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `353dc7ef0572fe5a8d52be0442b158364195310c`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 15:31 UTC

Read-only reconciliation at `2026-07-23T15:31:37Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and no
process matched the exact run root or service names. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,268,875,264 bytes free. The separate `/mnt/cocalc`
volume had 105,593,630,720 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `69a6928b2510952bbaf7ce8cda629f8d25f03994`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 15:02 UTC

Read-only reconciliation at `2026-07-23T15:02:16Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching processes were unrelated CoWasm work. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,270,779,904 bytes free. The separate `/mnt/cocalc`
volume had 105,212,375,040 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `93466c9153d631e6fe7e12fed7b2c0dbda408155`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 14:31 UTC

Read-only reconciliation at `2026-07-23T14:31:22Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching processes were unrelated CoWasm work. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,280,249,856 bytes free. The separate `/mnt/cocalc`
volume had 104,838,905,856 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `fc10d552c6fc7a5a93e08d01fd82a603c6778091`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 14:01 UTC

Read-only reconciliation at `2026-07-23T14:01:03Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching processes were unrelated CoWasm work. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,289,379,840 bytes free. The separate `/mnt/cocalc`
volume had 104,863,166,464 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `ec53850363dc8a89b68cb34f30953f13f6c1a0b7`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 13:31 UTC

Read-only reconciliation at `2026-07-23T13:31:46Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching process was unrelated CoWasm work. No result was inferred, no
remote state was changed, and no duplicate build was launched.

The root filesystem had 9,309,495,296 bytes free. The separate `/mnt/cocalc`
volume had 105,125,359,616 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `9ff3738fe4f96424192ed273cef29601c2f276ff`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 13:01 UTC

Read-only reconciliation at `2026-07-23T13:01:40Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but the assigned
`/mnt/cocalc-scratch` path was absent and the authoritative `post64` run root
remained invisible. Both durable service names were not found and inactive
with retained successful result and exit-status properties on the currently
reached machine. Docker was absent, Podman had no active container, and the
only matching processes were unrelated CoWasm work. No result was inferred,
no remote state was changed, and no duplicate build was launched.

The root filesystem had 9,318,387,712 bytes free. The separate `/mnt/cocalc`
volume had 105,215,868,928 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `b3ac51c082d6757ba80c08f0a221d56762f33dd3`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 12:31 UTC

Read-only reconciliation at `2026-07-23T12:31:34Z` reached `host` as native
Linux `x86_64`, but the assigned `/mnt/cocalc-scratch` path was absent and
the authoritative `post64` run root remained invisible. Both durable service
names were not found and inactive with retained successful result and exit
status properties on the currently reached machine. Docker was absent,
Podman had no active container, and the only matching processes were unrelated
CoWasm work. No result was inferred, no remote state was changed, and no
duplicate build was launched.

The root filesystem had 9,318,989,824 bytes free. The separate `/mnt/cocalc`
volume had 105,099,616,256 bytes free, below the binary 100 GiB heavy-build
threshold and outside the runbook-assigned automation root. The directly
fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `254e57948e1f14a05260cd1ed6cae7d74b427b9d`.

## 2026-07-23 Assigned Bulk Run Still Inaccessible At 00:01 UTC

Read-only reconciliation at `2026-07-23T00:01:16Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but `/mnt/cocalc-scratch`
resolved to the 24,883,167,232-byte root filesystem, with 14,686,687,232
bytes free. The authoritative `post64` run root remained invisible. Both
durable services appeared inactive with retained successful result and exit
status properties on the currently reached machine, but no result is inferred
without the assigned bulk artifacts. Docker was absent, Podman had no
containers, and no matching Sagelite process was visible. The run was left
untouched and no duplicate build was launched.

The separate `/mnt/cocalc` volume had 78,444,380,160 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `7ceed9ddccbd72a8b2cb250fe37cac368ec6b927`.

## 2026-07-22 Assigned Bulk Run Still Inaccessible At 23:30 UTC

Read-only reconciliation at `2026-07-22T23:30:46Z` reached `host` on the
first bounded attempt as native Linux `x86_64`, but `/mnt/cocalc-scratch`
again resolved to the 24,883,167,232-byte root filesystem, with
14,649,933,824 bytes free. The authoritative `post64` run root remained
invisible. Both durable service names were not found and appeared inactive
with retained successful result and exit-status properties on the currently
reached machine, but no result is inferred without the assigned bulk
artifacts. Docker was absent, Podman had no active container, and no matching
Sagelite process was visible. The run was left untouched and no duplicate
build was launched.

The separate `/mnt/cocalc` volume had 78,456,291,328 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `b4b821a192945e15bb659874db1f349c89917d77`.

## 2026-07-22 Assigned Bulk Run Still Inaccessible At 23:00 UTC

Read-only reconciliation at `2026-07-22T23:00:52Z` reached `host` as native
Linux `x86_64`, but `/mnt/cocalc-scratch` again resolved to the
24,883,167,232-byte root filesystem, with 14,640,721,920 bytes free. The
authoritative `post64` run root remained invisible. Both durable service names
were not found and appeared inactive with retained successful result and exit
status properties on the currently reached machine, but no result is inferred
without the assigned bulk artifacts. Docker was absent, Podman had no active
container, and no matching Sagelite process was visible. The run was left
untouched and no duplicate build was launched.

The separate `/mnt/cocalc` volume had 78,526,242,816 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `4e8e99cc45ccbeacf784756896effdc8259106bd`.

## 2026-07-22 Assigned Bulk Run Still Inaccessible At 22:30 UTC

Read-only reconciliation at `2026-07-22T22:30:55Z` reached `host` as native
Linux `x86_64`, but `/mnt/cocalc-scratch` resolved to the
24,883,167,232-byte root filesystem, with 14,641,491,968 bytes free. The
authoritative `post64` run root remained invisible. Both durable service names
were not found and appeared inactive with retained successful result and exit
status properties on the currently reached machine, but no result is inferred
without the assigned bulk artifacts. No active container or matching Sagelite
process was visible. The run was left untouched and no duplicate build was
launched.

The separate `/mnt/cocalc` volume had 78,554,972,160 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact. Before this evidence edit, the canonical checkout, its
local tracking ref, and the directly queried `origin/develop` ref were
synchronized at `4024ba1d60c50fc23690dd450e6bc4eedb743b9f`.

## 2026-07-22 Assigned Bulk Run Still Inaccessible At 21:30 UTC

Read-only reconciliation at `2026-07-22T21:30:59Z` reached `host` as native
Linux `x86_64`, but `/mnt/cocalc-scratch` again resolved to the
24,883,167,232-byte root filesystem, with 14,651,482,112 bytes free. The
authoritative `post64` run root remained invisible. Both durable service names
were not found and appeared inactive with retained successful result and exit
status properties on the currently reached machine, but no result is inferred
without the assigned bulk artifacts. No active container or matching Sagelite
process was visible. The run was left untouched and no duplicate build was
launched.

The separate `/mnt/cocalc` volume had 78,549,213,184 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact.

## 2026-07-22 Assigned Bulk Run Still Inaccessible At 20:39 UTC

Read-only reconciliation at `2026-07-22T20:39:33Z` again reached `host` as
native Linux `x86_64`, but `/mnt/cocalc-scratch` still resolved to the
24,883,167,232-byte root filesystem, with 14,652,686,336 bytes free. The
authoritative `post64` run root remained invisible. Both durable service names
were not found and appeared inactive with retained successful result and exit
status properties on the currently reached machine, but no result is inferred
without the assigned bulk artifacts. No active Docker container or matching
Sagelite process was visible. The run was left untouched and no duplicate
x86_64 job was launched.

The separate `/mnt/cocalc` volume had 78,561,914,880 bytes free, below the
binary 100 GiB heavy-build threshold and outside the runbook-assigned root.
The directly fetched public manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `post64` artifact.

## 2026-07-22 Assigned Bulk Run Became Inaccessible At 20:00 UTC

Read-only reconciliation at `2026-07-22T20:00:59Z` again reached `host` as
native Linux `x86_64`, but the assigned `/mnt/cocalc-scratch` filesystem was
no longer mounted. The path resolved to the 24,883,167,232-byte root
filesystem with 14,657,941,504 bytes free, and the authoritative `post64` run
root was not visible. The build and watcher service names were inactive with
retained `Result=success` and `ExecMainStatus=0`, but those properties are not
accepted as evidence from the currently reached machine without the bulk run
artifacts. No exit-code, wheel, validation file, active container, or
Sagelite automation process was visible. No remote state was changed and no
result was inferred from the inaccessible run.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with no `post64` artifact.
The x86_64 run remains untouched pending restoration of its assigned mount.
Independent work moved to an idle native macOS arm64 cell from the same exact
pushed `post64` source; it does not duplicate the inaccessible x86_64 target.

## 2026-07-22 Exact Post64 Fat-Binary Build Started At 17:59 UTC

Read-only reconciliation at `2026-07-22T17:50:15Z` reached `host` as native
Linux `x86_64` and found the assigned `/mnt/cocalc-scratch` mount restored.
It is a 527,297,863,680-byte ext4 filesystem and initially had
191,941,595,136 bytes free. The historical `post60` run root was visible
again but contained no exit-code and no wheel; its log ended during primary
compilation. Its service names were not found, Docker was idle through
non-interactive `sudo`, and no Sagelite or cibuildwheel process was active.
No result is inferred from that interrupted run.

The first exact `post64` launch is preserved at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260722-175330-014ae4bf443`.
It was deliberately stopped before native compilation after the live
cibuildwheel configuration showed that its explicit write-overlay destination
had been mechanically doubled to
`/host/sage-fat-v1-fat-v1-manylinux_2_28_x86_64`. It produced zero wheels.
The logs, source input, rejection metadata, and 309-byte partial prefix remain
preserved; its service exit-code artifacts are explicitly not success evidence
because its EXIT traps ran during the operator stop.

The authoritative fresh replacement is
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260722-175911-014ae4bf443`.
Its exact clean checkout is pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` (`10.9.post64`), with committed
tree `08c39ac15ef341f68af0676dfb4f9b61de0010db`. The 146,483,200-byte exact
shallow-repository archive has SHA256
`a7ce677432f01cff16fd93d88f6c12f3d988464d76a2c79aa215165d5df047ed`.
The new persistent prefix
`/mnt/cocalc-scratch/sagelite-manylinux-prefixes/sage-fat-v1-manylinux_2_28_x86_64`
was absent before this iteration and had zero entries at launch. Available
capacity was 188,728,115,200 bytes.

The durable build and watcher are active as
`sagelite-post64-x86-cp312-build-r1.service` and
`sagelite-post64-x86-cp312-watch-r1.service`. The actual manylinux container
reports Linux `x86_64` and CPython 3.12.13. Docker mount inspection proves
that the exact empty fat profile is mounted read/write at
`/host/sage-fat-v1-manylinux_2_28_x86_64`. The live log then ran `./configure`
with `--enable-fat-binary`, copied `config.status` into that persistent
profile, and entered GMP installation. Read-only reconciliation at
`2026-07-22T18:30:55Z` found both durable services still active, the same
manylinux container up for 30 minutes, and the command log growing through
`2026-07-22T18:30:16Z`. The isolated fat prefix had grown to 2.1 GiB. Native
prerequisites through GF2X, NTL, and LinBox completed successfully, the log
reported the Sage build/upgrade complete, and companion installation had
entered GAP. The assigned filesystem still had 183,216,492,544 bytes free.
No wheel or exit-code artifact existed. A further read-only reconciliation at
`2026-07-22T19:01:24Z` found the exact clean source checkout and both system
services still active with their original build and watcher PIDs. The command
log had grown through `2026-07-22T19:00:25Z`; GAP3 completed successfully and
Gfan installation began. The isolated fat prefix had grown to 2,876,896,785
bytes, while the assigned filesystem retained 177,204,658,176 bytes free. No
wheel, build exit-code, or validation summary existed. Read-only
reconciliation at `2026-07-22T19:31:09Z` again found exact source
`014ae4bf44318b6f5032053957a92291d4363b7a` clean and both durable services
active with their original PIDs. The same manylinux container remained up,
reported native Linux `x86_64` with CPython 3.12.13, and retained the intended
fat-profile mount read/write. The command log had grown through
`2026-07-22T19:30:48Z`; `msolve` completed successfully and `fplll`
installation began. The isolated prefix had grown to 4,050,336,312 bytes, and
the assigned filesystem retained 176,123,146,240 bytes free. No wheel,
build exit-code, or validation summary existed.

The watcher will assemble the strict
closure only after build success, then run a QEMU Nehalem probe whose CPUID
check asserts that BMI2 and ADX are absent before importing Sage and
exercising GMP, polynomial, and dense real-matrix paths. Independent fresh
short and full gates follow only if that portability probe passes. No
`post64` wheel, validation pass, cell acceptance, or publication is claimed
yet.

## 2026-07-22 Assigned Bulk Mount Still Absent At 17:31 UTC

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T17:31:09Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had only 9,308,643,328 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,557,911,552 bytes free, 2,183,729,152 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical CPython 3.12 `post60` run root was absent. Its build and
watcher service names were not found and were inactive with successful
retained result and exit-status properties. Docker was absent, Podman had no
active containers, and the process scan found no Sagelite or cibuildwheel
automation work other than the read-only preflight shell itself. No remote
state was changed and no Linux x86_64 build was started.

A direct public-manifest fetch during the same reconciliation confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` or `post64` artifact. Its generation timestamp
remains `2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the
canonical checkout was clean on `develop` at
`62ea9add75961366f9c007beb87c28e6913b2840`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post64` source `014ae4bf443` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or another automation root is explicitly approved.

## 2026-07-22 Assigned Bulk Mount Still Absent At 17:01 UTC

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T17:01:33Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had only 9,315,844,096 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,611,687,936 bytes free, 2,237,505,536 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical CPython 3.12 `post60` run root was absent. Its build and
watcher service names were not found and were inactive with successful
retained result and exit-status properties. Docker was absent, Podman had no
active containers, and the process scan found no Sagelite or cibuildwheel
automation work. No remote state was changed and no Linux x86_64 build was
started.

A direct public-manifest fetch at `2026-07-22T17:01Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` or `post64` artifact. Its generation timestamp
remains `2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the
canonical checkout was clean on `develop` at
`3494975fb9eb7a2a84bc8892dd5d56f64517a1b2`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post64` source `014ae4bf443` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or another automation root is explicitly approved.

## 2026-07-22 Assigned Bulk Mount Still Absent At 16:31 UTC

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T16:31:25Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had only 9,316,007,936 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,651,382,272 bytes free, 2,277,199,872 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical CPython 3.12 `post60` run root was absent. Its build and
watcher service names were not found and were inactive with successful
retained result and exit-status properties. Docker was absent, Podman had no
active containers, and independent service and process scans found no
Sagelite or cibuildwheel automation work. No remote state was changed and no
Linux x86_64 build was started.

A direct public-manifest fetch at `2026-07-22T16:31:43Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` or `post64` artifact. Its generation timestamp
remains `2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the
canonical checkout was clean on `develop` at
`dacd58d463f30fcbb6c4f004848b1868f6be408f`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post64` source `014ae4bf443` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or another automation root is explicitly approved.

## 2026-07-22 Assigned Bulk Mount Still Absent At 16:01 UTC

Read-only preflight reached `host` on its first bounded attempt at
`2026-07-22T16:01:20Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path was absent. The 24,883,167,232-byte root filesystem
had only 9,325,662,208 bytes free. The unassigned `/mnt/cocalc` btrfs
filesystem had 109,230,030,848 bytes free, 1,855,848,448 bytes above the
binary 100 GiB heavy-build threshold, but it remains outside the
runbook-assigned automation root.

The historical CPython 3.12 `post60` run root was absent. Its build and
watcher service names were not found and were inactive with successful
retained result and exit-status properties. Docker was absent, Podman had no
active containers, and the process scan found no Sagelite or cibuildwheel
automation work. No remote state was changed and no Linux x86_64 build was
started.

A direct public-manifest fetch during the same reconciliation confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` or `post64` artifact. Its generation timestamp
remains `2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the
canonical checkout was clean on `develop` at
`6141a202bda5cfaac6c18c0397f247a0ae2f0ef9`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post64` source `014ae4bf443` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or another automation root is explicitly approved.

## 2026-07-21 Assigned Host Unreachable At 16:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T16:01:23Z`, `2026-07-21T16:01:47Z`, and
`2026-07-21T16:02:09Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T16:02:44Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`837b87534ba72b8837ee5f7dd444bfa17f62e416`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 15:01 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T15:01:00Z`, `2026-07-21T15:01:16Z`, and
`2026-07-21T15:01:39Z`. The third result was confirmed with an independent
bounded recheck after the original combined command yielded before recording
its result. All three timed out before a session was established. The assigned
filesystem, historical CPython 3.12 `post60` run root, systemd services,
container state, and process state therefore could not be rechecked. No remote
state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T15:01:00Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`d25e25f42755dec6157b422a9346e31499d6ad20`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 14:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T14:31:19Z`, `2026-07-21T14:31:42Z`, and
`2026-07-21T14:32:01Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T14:32:27Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`8e6675b5512bafcb1da5b81c2db0083713608c02`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 14:01 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T14:01:00Z`, `2026-07-21T14:01:10Z`, and
`2026-07-21T14:01:20Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T14:01:48Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`0ca49dc3971714d638a5f1064a77ec5b81ae9111`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 13:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T13:31:30Z`, `2026-07-21T13:31:45Z`, and
`2026-07-21T13:32:06Z`. The third attempt was repeated independently after
the original bounded command window ended before recording its result. All
three timed out before a session was established. The assigned filesystem,
historical CPython 3.12 `post60` run root, systemd services, container state,
and process state therefore could not be rechecked. No remote state was
changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T13:31:30Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`18624d1a51afc660a2d08fd63d0bc945e8d0febf`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 13:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T13:01:32Z`, `2026-07-21T13:01:47Z`, and
`2026-07-21T13:02:10Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T13:02:51Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`120d5f6f68c0d7803eb80479bca8e3f258123914`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 12:33 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
began at `2026-07-21T12:31:20Z`, `2026-07-21T12:32:04Z`, and
`2026-07-21T12:32:30Z`. All three timed out before a session was established.
The assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch confirmed at `2026-07-21T12:33:17Z` that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`da3f95b2b0aef7b72a404d7a5dbe3275c58ce6b8`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 12:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T12:01:31Z` and `2026-07-21T12:02:20Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T12:02:38Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`1172583540a709cdadf14eb041ed8fea094505c9`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 11:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T11:31:30Z` and `2026-07-21T11:32:19Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T11:32:34Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`1749137b083b5d340a765a305fa5d2133e8e2f95`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 11:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T11:01:15Z` and `2026-07-21T11:02:00Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T11:02:23Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`afdd6b42176879804e8bad8e8a6160454d78203b`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 10:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T10:31:09Z` and `2026-07-21T10:32:22Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T10:32:34Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`4084f0c9e0e8aff23b306143c13d47cad1af8544`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 10:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T10:01:36Z` and `2026-07-21T10:02:21Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T10:02:46Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`b6090532678bda349d14269a608fd7057d56c5fe`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 09:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T09:01:24Z` and `2026-07-21T09:02:08Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T09:01:24Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`beb0d6df9001052886a02ac120aa1fc5b91df4cc`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 08:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T08:31:21Z` and `2026-07-21T08:32:06Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

A direct public-manifest fetch at `2026-07-21T08:32:21Z` confirmed that
`dev/manifest.json` still contains 177 wheels, including fourteen Sagelite
primary wheels and no `post63` artifact. Its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`. Before this evidence edit, the canonical
checkout was clean on `develop` at
`94ca971ffac90c1ae3ebe864c6d92749fef66a66`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 08:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T08:01:31Z` and `2026-07-21T08:02:22Z` timed out before a
session was established. The assigned filesystem, historical CPython 3.12
`post60` run root, systemd services, container state, and process state
therefore could not be rechecked. No remote state was changed and no Linux
x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`ad436705f0f390e0958fc21dda4dcd4890ede7f9`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 07:32 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T07:31:41Z` and `2026-07-21T07:32:37Z` timed out before a
session was established. The third attempt was repeated independently after
the original bounded command window ended before recording its result. The
assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`bff76d205a3a7fa94fafd210d0754179cd00a9bb`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 07:02 UTC

Three confirmed bounded SSH connection attempts to the required `host` alias
between `2026-07-21T07:01:42Z` and `2026-07-21T07:02:35Z` timed out before a
session was established. The third attempt was repeated independently after
the original bounded command window ended before recording its result. The
assigned filesystem, historical CPython 3.12 `post60` run root, systemd
services, container state, and process state therefore could not be rechecked.
No remote state was changed and no Linux x86_64 build was started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`640630c47441dc5c8ed84e3d68adbf9afa2e7bd2`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 06:32 UTC

Three bounded SSH connection attempts to the required `host` alias between
`2026-07-21T06:31:15Z` and `2026-07-21T06:32:00Z` timed out before a session
was established. The assigned filesystem, historical CPython 3.12 `post60`
run root, systemd services, container state, and process state therefore could
not be rechecked. No remote state was changed and no Linux x86_64 build was
started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`0432f6555979c3334f1f3212826b0996bade615e`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Host Unreachable At 06:02 UTC

Three bounded SSH connection attempts to the required `host` alias between
`2026-07-21T06:01Z` and `2026-07-21T06:02Z` timed out before a session was
established. The assigned filesystem, historical CPython 3.12 `post60` run
root, systemd services, container state, and process state therefore could not
be rechecked. No remote state was changed and no Linux x86_64 build was
started.

The last successful read-only preflight remains the
`2026-07-21T05:31:32Z` evidence. At that time the assigned
`/mnt/cocalc-scratch` path was an essentially empty 20,957,446,144-byte ext4
filesystem with only 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical run root was absent. The separate
writable `/mnt/cocalc` btrfs filesystem had 212,582,658,048 bytes free, but it
is not the automation root assigned by the authoritative runbook.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`d062e69d6aa7db355bbaa44293034bb5745a170b`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem is restored, or another automation root is explicitly
approved.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 05:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T05:31:32Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,658,048
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`7cedccaba81276c9299234915ce4ff97f39189e8`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 05:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T05:01:23Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,690,816
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`dabecf865db0915fe9b6f78a52407b114191b47d`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 04:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T04:31:27Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,711,296
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`a6674b348163194b93b965c9d1c0ce1384ca6f29`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 04:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T04:01:23Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and an
independent process scan found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,711,296
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`7828c82212ca801db678fe3556ba3e2efd33d56e`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 03:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T03:31:18Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,727,680
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`f103d5e89785ef16a565e6783232adb55be9f7e1`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 03:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T03:01:47Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,727,680
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`89cde0700899a4811342149b4f4bc463becf081f`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 02:33 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T02:33:11Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,764,544
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`1f0deffcc254da790c857aa1c6f15995eb162dc7`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 02:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T02:01:31Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,785,024
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`2ddfe7c82d77056eaa8671db71face04f96b08c6`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 01:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T01:01:29Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,801,408
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`2c0060c14f0a657c7d17eedf62511ee0534f3e6e`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 00:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T00:31:18Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,801,408
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`26053bfc21df79b7136f6230972ea8a7e2c18e07`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-21 Assigned Bulk Filesystem Too Small At 00:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-21T00:01:44Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,838,272
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`11437b68ee37a16beaa3e433c630214b461af377`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 23:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T23:31:47Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,838,272
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`5a9c1ea8b01488ef4b374f6ca8ce14e136806a0e`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 22:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T22:31:30Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,875,136
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`bb7a186dec5f58f428d22da60274360b4d88dd16`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 22:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T22:01:28Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,875,136
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`76d139e2348aeccc393169c36ed94733af2c6929`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 21:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T21:31:31Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,916,096
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`23035e9659c534cb2a7c72ac23c5fe2579e5946b`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 21:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T21:01:31Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,916,096
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`4df9e19bd458388db55ed3f33dc89d791f8f584c`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 20:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T20:31:52Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,932,480
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`1e9d94961f52ac2d241cf44114a1f85843be7d00`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 20:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T20:01:21Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are not
found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,952,960
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`8ee3824116f7f408d7d18540fae45c6b4d42d160`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 19:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T19:31:43Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,952,960
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`c42bcba330066cb44ea5987f95483cbf94be856c`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 19:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T19:01:52Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,989,824
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`fbb7711232e92b05ec457ec19ff081a84b0e5140`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 18:33 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T18:33:26Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and independent
service and process scans found no Sagelite automation work. No result is
inferred from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,582,989,824
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`95f79edefb57fa0880dfdd34fee913cc2bdff06d`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 18:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T18:01:06Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and the process
scan found no independent Sagelite automation process. No result is inferred
from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,583,006,208
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`537cb54d77ad20719a7dea37966d8b255b8f5117`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 17:30 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T17:30:59Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and the process
scan found no independent Sagelite automation process. No result is inferred
from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,583,026,688
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`fb7eb238ebdf9c5071d7d443176f5b74e0dd493d`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 17:01 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T17:01:26Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains the essentially empty 20,957,446,144-byte
ext4 filesystem with only 19,866,902,528 bytes free, far below the binary
100 GiB heavy-build threshold. Its only entry is `lost+found`. The historical
CPython 3.12 `post60` run root is absent. Both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties, Docker is absent, Podman has no active container, and the process
scan found no independent Sagelite automation process. No result is inferred
from the missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,583,026,688
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`fa5b1286789f45e55383dbaab068be11f9d627e9`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 16:31 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T16:31:36Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path is again mounted, but it is the essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The historical CPython 3.12
`post60` run root is absent. Both historical systemd units are not found and
inactive while retaining successful result and exit-status properties,
Docker is absent, Podman has no active container, and an independent process
scan found no Sagelite automation process. No result is inferred from the
missing artifacts.

The separate writable `/mnt/cocalc` btrfs filesystem has 212,583,055,360
bytes free, but it is not the automation root assigned by the authoritative
runbook. No cleanup or Linux x86_64 build was started there without explicit
direction. The assigned 20 GiB filesystem contains insufficient total
capacity, so cleanup cannot make it satisfy the threshold.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`683c561302e75405fee38a1f0302120f0fb4ab3b`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 16:02 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The confirmed attempts began at `2026-07-20T16:01:39Z`,
`2026-07-20T16:01:54Z`, and `2026-07-20T16:02:19Z`; the final confirmed
attempt ended at `2026-07-20T16:02:34Z` after its 15-second connection timeout
with exit status 255. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-20T15:32:23Z` found the
assigned `/mnt/cocalc-scratch` path absent. The only writable bulk filesystem
then found was the separate `/mnt/cocalc` btrfs filesystem, with
157,214,433,280 bytes free, but it is not assigned by the authoritative
runbook. No later capacity, mount, service, container, process, or artifact
state is claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`66126ce23aaca83ac00f76aa5ac51d651108ad22`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Absent At 15:32 UTC

Read-only preflight reached the required `host` alias on the first bounded
attempt at `2026-07-20T15:32:23Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path does not exist. Its historical CPython 3.12
`post60` run root is therefore absent, and both historical systemd units are
not found and inactive while retaining successful result and exit-status
properties. Docker is absent, Podman has no active container, and an
independent process scan found no Sagelite automation process. No result is
inferred from the missing artifacts.

The only writable bulk filesystem found was the separate `/mnt/cocalc` btrfs
filesystem, with 157,214,433,280 bytes free. Although that exceeds the binary
100 GiB heavy-build threshold, it is not the automation root assigned by the
authoritative runbook. No cleanup or Linux x86_64 build was started there
without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`f53942e274abda1b6cb20ca4acd0d5f9fbc68851`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until a qualifying assigned bulk filesystem is
restored or `/mnt/cocalc` is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 14:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The attempts began at `2026-07-20T14:31:37Z`,
`2026-07-20T14:31:52Z`, and `2026-07-20T14:32:07Z`; the final attempt ended
at `2026-07-20T14:32:22Z` after its 15-second connection timeout with exit
status 255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`035ffcf39eb45696fea1851f3c589ef6992df398`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 14:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The attempts began at `2026-07-20T14:01:30Z`,
`2026-07-20T14:01:45Z`, and `2026-07-20T14:02:00Z`; the final attempt ended
at `2026-07-20T14:02:15Z` after its 15-second connection timeout with exit
status 255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`bbb1e07909713562f235e2a3d1f1a03e4cdcca69`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 13:32 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The attempts began at `2026-07-20T13:31:27Z`,
`2026-07-20T13:31:42Z`, and `2026-07-20T13:32:24Z`; the final confirmed
attempt ended at `2026-07-20T13:32:39Z` after its 15-second connection timeout
with exit status 255. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`ac86090be18044b25e8dd349e0293e18bdf820f3`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 13:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The attempts began at `2026-07-20T13:01:41Z`,
`2026-07-20T13:01:56Z`, and `2026-07-20T13:02:11Z`; the final attempt ended
at `2026-07-20T13:02:26Z` after its 15-second connection timeout with exit
status 255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`f45133eebdf16a76cc21a364db8e26ef2effc7ef`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 12:33 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The attempts began at `2026-07-20T12:32:11Z`,
`2026-07-20T12:32:26Z`, and `2026-07-20T12:32:56Z`; the final attempt ended
at `2026-07-20T12:33:11Z` after its 15-second connection timeout with exit
status 255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`4aee1111b312a293b3459dae79bb084a1697c4e7`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 12:02 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The attempts began at `2026-07-20T12:01:50Z`,
`2026-07-20T12:02:05Z`, and `2026-07-20T12:02:30Z`; the final attempt ended
at `2026-07-20T12:02:45Z` after its 15-second connection timeout with exit
status 255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`cf9362bfa4f356a163de0ad8cb389c7fa632a543`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 11:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The attempts began at `2026-07-20T11:31:20Z`,
`2026-07-20T11:31:35Z`, and `2026-07-20T11:31:50Z`; the final attempt ended
at `2026-07-20T11:32:05Z` after its 15-second connection timeout, and the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`53ecc47aff7fec805ff749a156b39cffbea48850`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 11:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The attempts began at `2026-07-20T11:01:17Z`,
`2026-07-20T11:01:32Z`, and `2026-07-20T11:01:47Z`; the final attempt ended
at `2026-07-20T11:02:02Z` after its 15-second connection timeout, and the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`5b3b106dbda98242735e0b765f00ac7e67bd22ab`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 10:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T10:31:46Z` and
ended at `2026-07-20T10:32:01Z` after its 15-second connection timeout; the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`3c1b6f3fa235a0204e868a140eb59a2dfa2605d2`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 10:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T10:01:52Z` and
ended at `2026-07-20T10:02:08Z` after its 15-second connection timeout; the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Before this
evidence edit, the canonical checkout was clean on `develop` at
`d1b3f85078c6b8b1e9c759aa1bf511375325254b`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact
pushed `post63` source `16d6d78012a` remains the selected release candidate.
This cell remains blocked until `host` is reachable and a qualifying assigned
bulk filesystem can be verified, or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 09:01 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T09:01:38Z` and
ended at `2026-07-20T09:01:53Z` after its 15-second connection timeout; the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`fa27f0ba3307bdc7e0d9413be9774a3d3d72babe`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 08:31 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T08:31:42Z` and
ended at `2026-07-20T08:31:57Z` after its 15-second connection timeout; the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`7bffa99f7c9966a45e83972efd023978a06c37d7`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 08:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T08:02:27Z` and
ended at `2026-07-20T08:02:42Z` after its 15-second connection timeout; the
bounded loop exited with status 255. No remote state is inferred, the missing
historical CPython 3.12 `post60` artifacts remain untouched, and no Linux
x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`d900678e4f1335d1de0d2c7b0c4723cf04b99b06`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 07:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-20T07:31:55Z` and
ended at `2026-07-20T07:32:10Z` after its 15-second connection timeout. No
remote state is inferred, the missing historical CPython 3.12 `post60`
artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`d944c7bd1a9cf66749e757e0be701dd12b3b5fe6`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 07:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T07:01:50Z` and ended at
`2026-07-20T07:02:06Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`6b366f8578999b296ca509436aabf1f42aae7e6f`, synchronized with its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 06:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T06:31:56Z` and ended at
`2026-07-20T06:32:11Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`e2200b266f8210fb0ff71e5fccd1da230cd786ef`, synchronized with both its local
tracking ref and the directly queried `origin/develop` remote ref. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This cell
remains blocked until `host` is reachable and a qualifying assigned bulk
filesystem can be verified, or a different filesystem is explicitly approved
as the automation root.

## 2026-07-20 Assigned Host Unreachable At 06:03 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The final confirmed attempt began at
`2026-07-20T06:03:05Z` and ended at `2026-07-20T06:03:20Z` with exit status
255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`16fc5fa47b359beec184ec33911c854082ab6714`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 05:32 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The final confirmed attempt began at
`2026-07-20T05:32:11Z` and ended at `2026-07-20T05:32:26Z` with exit status
255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`277df44653104b7b89b29a23ba0b97aa013ccb24`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 05:03 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The final confirmed attempt began at
`2026-07-20T05:02:59Z` and ended at `2026-07-20T05:03:08Z` with exit status
255. No remote state is inferred, the missing historical CPython 3.12
`post60` artifacts remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`10166590dcdd2f29e5288816eb01cd65589f95ea`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 04:31 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T04:31:38Z` and ended at
`2026-07-20T04:31:53Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`5c72c5742613a29d03bf798a2f9bf111d68be107`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 04:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T04:02:03Z` and ended at
`2026-07-20T04:02:18Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-20T03:31:15Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,010,279,424 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`3ca6eed64f27861d6534e7188979e99c4b22d57e`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 03:31 UTC

Read-only preflight reached the required `host` alias at
`2026-07-20T03:31:15Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains an essentially empty 20,957,446,144-byte
ext4 filesystem with 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. Its only entry is `lost+found`. The historical CPython
3.12 `post60` build and watcher are inactive and not found, with retained
`Result=success` and `ExecMainStatus=0`, but their bulk run root is absent, so
no wheel or validation result is inferred. Podman has no active container,
Docker is absent, and an independent process scan found no Sagelite automation
process.

The separate writable `/mnt/cocalc` filesystem has 207,010,279,424 bytes
free, but it is not the build root assigned by the authoritative runbook. No
cleanup or Linux x86_64 build was started there without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`ac243632288ba792479fcc057207d27bfac73979`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until a qualifying
assigned bulk filesystem is restored or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 03:01 UTC

Read-only preflight reached the required `host` alias at
`2026-07-20T03:01:15Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains an essentially empty 20,957,446,144-byte
ext4 filesystem with 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. Its only entry is `lost+found`. The historical CPython
3.12 `post60` build and watcher are inactive with `Result=success` and
`ExecMainStatus=0`, but their bulk run root is absent, so no wheel or
validation result is inferred. Podman has no active container, Docker is
absent, and an independent process scan found no Sagelite automation process.

The separate writable `/mnt/cocalc` filesystem has 207,060,836,352 bytes
free, but it is not the build root assigned by the authoritative runbook. No
cleanup or Linux x86_64 build was started there without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`a0757dacca2af69bcafb707b1448b9447780273b`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until a qualifying
assigned bulk filesystem is restored or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 02:31 UTC

Read-only preflight reached the required `host` alias at
`2026-07-20T02:31:41Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains an essentially empty 20,957,446,144-byte
ext4 filesystem with 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical CPython 3.12 `post60` build and watcher
are inactive with `Result=success` and `ExecMainStatus=0`, but their bulk run
root is absent, so no wheel or validation result is inferred. Podman has no
active container, Docker is absent, and an independent process scan found no
Sagelite automation process.

The separate writable `/mnt/cocalc` filesystem has 207,050,526,720 bytes
free, but it is not the build root assigned by the authoritative runbook. No
cleanup or Linux x86_64 build was started there without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`0fe9c62598c79fc110aa38b0392f751aa540f81e`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until a qualifying
assigned bulk filesystem is restored or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 02:01 UTC

Read-only preflight reached the required `host` alias at
`2026-07-20T02:01:27Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains an essentially empty 20,957,446,144-byte
ext4 filesystem with 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical CPython 3.12 `post60` build and watcher
are inactive with `Result=success` and `ExecMainStatus=0`, but their bulk run
root is absent, so no wheel or validation result is inferred. Podman has no
active container, Docker is absent, and no Sagelite automation process is
running.

The separate writable `/mnt/cocalc` filesystem has 207,077,015,552 bytes
free, but it is not the build root assigned by the authoritative runbook. No
cleanup or Linux x86_64 build was started there without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`a483b15092d0a4fafbf0567d6c954f1d22139d7e`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until a qualifying
assigned bulk filesystem is restored or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Bulk Filesystem Too Small At 01:31 UTC

Read-only preflight reached the required `host` alias at
`2026-07-20T01:31:01Z` as native Linux `x86_64`. The assigned
`/mnt/cocalc-scratch` path remains an essentially empty 20,957,446,144-byte
ext4 filesystem with 19,866,902,528 bytes free, far below the binary 100 GiB
heavy-build threshold. The historical CPython 3.12 `post60` build and watcher
are inactive with `Result=success` and `ExecMainStatus=0`, but their bulk run
root is absent, so no wheel or validation result is inferred. Podman has no
active container, Docker is absent, and no Sagelite automation process is
running.

The separate writable `/mnt/cocalc` filesystem has 207,157,825,536 bytes
free, but it is not the build root assigned by the authoritative runbook. No
cleanup or Linux x86_64 build was started there without explicit direction.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`8bb7a739ca00226a37be60f9fe1e237ea7cbeebc`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until a qualifying
assigned bulk filesystem is restored or a different filesystem is explicitly
approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 01:01 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The final confirmed attempt began at
`2026-07-20T01:01:38Z` and ended at `2026-07-20T01:01:53Z` after its 15-second
connection timeout. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`b45809e29ef7688c5c45902d9cb4dccff0f39620`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 00:31 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T00:31:42Z` and ended at
`2026-07-20T00:31:57Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`d0128a06fa8f461cfc54d1de323e021abaa32919`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-20 Assigned Host Unreachable At 00:01 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-20T00:01:35Z` and ended at
`2026-07-20T00:01:50Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`5b5e3f1be04466bb05330eeb34975ce78da6f30c`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 23:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T23:32:09Z` and ended at
`2026-07-19T23:32:24Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`b8d240360fb72270535c1515f08566bf8a70a6a7`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 23:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T23:02:02Z` and ended at
`2026-07-19T23:02:17Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`b3ff97be2c873a4db7db983fd1ccf7140318a3fd`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 22:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T22:31:52Z` and ended at
`2026-07-19T22:32:07Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`d2f45736a5a095df54a41db9f9725fa214001ec9`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 22:02 UTC

Three confirmed bounded SSH connection attempts through the required `host`
alias timed out. The final confirmed attempt began at
`2026-07-19T22:01:53Z` and ended at `2026-07-19T22:02:08Z` after its 15-second
connection timeout. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`cdd29f0cad636ee1d2d576d7bc94582ecfa39ba2`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 21:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T21:31:51Z` and ended at
`2026-07-19T21:32:06Z` after its 15-second connection timeout. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`633327b58f7d89e7cf1d50aae5313a3f4f4e06e0`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 21:01 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T21:01:42Z`, and the bounded
SSH loop exited with status 255 at `2026-07-19T21:01:57Z`. No remote state is
inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`c79842cbace9a94af957b18530e33e6f2d09dc1f`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 20:31 UTC

Three bounded SSH connection attempts through the required `host` alias
timed out. The final confirmed attempt began at `2026-07-19T20:31:57Z` and
returned exit status 255 after its 15-second connection timeout. No remote
state is inferred, the missing historical CPython 3.12 `post60` artifacts
remain untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`f0246209a78efddd9098c4016cb1ac02675e1bd0`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 20:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt began at `2026-07-19T20:02:30Z` and returned
exit status 255 after its 15-second connection timeout. No remote state is
inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`914c02b61a425a5377fffa3a599258ad6b8108c3`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 19:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final controller checkpoint was recorded at
`2026-07-19T19:32:25Z`. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`0cbffd95651b40764d72b607a98c1a67fadd7a13`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 19:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final controller checkpoint was recorded at
`2026-07-19T19:02:26Z`. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`d53f1054a7f44646fad9ad2cd716ca711b1aaf4a`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 18:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final controller checkpoint was recorded at
`2026-07-19T18:32:33Z`. No remote state is inferred, the missing historical
CPython 3.12 `post60` artifacts remain untouched, and no Linux x86_64 build
was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, process, or artifact state is
claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`7eed745c8f44c130fb919f77ff852c6c93196d2f`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 18:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt ended at `2026-07-19T18:02:39Z`. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, or process state is claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`a1c5ad9d01a32d40707ae80dde6865d04aec1be2`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 17:33 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt ended at `2026-07-19T17:33:01Z`. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, or process state is claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`76474bda5918669e82453d089d7dd0900f315d6e`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 17:02 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt ended at `2026-07-19T17:02:34Z`. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, or process state is claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`b56c469203a7d473526e11186fc9f2217202a7a2`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Host Unreachable At 16:32 UTC

All three bounded SSH connection attempts through the required `host` alias
timed out. The final attempt ended at `2026-07-19T16:32:13Z`. No remote state
is inferred, the missing historical CPython 3.12 `post60` artifacts remain
untouched, and no Linux x86_64 build was started.

The last reachable read-only preflight at `2026-07-19T16:01:34Z` found the
assigned `/mnt/cocalc-scratch` path backed by an essentially empty
20,957,446,144-byte ext4 filesystem with only 19,866,902,528 bytes free, far
below the binary 100 GiB heavy-build threshold. The separate `/mnt/cocalc`
filesystem had 207,304,851,456 bytes free but was not assigned by the runbook.
No later capacity, mount, service, container, or process state is claimed.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The canonical
checkout was clean on `develop` at
`b3c6bbdf801748e85e1a875e9045bfca8be4f3c4`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell remains blocked until `host` is
reachable and a qualifying assigned bulk filesystem can be verified, or a
different filesystem is explicitly approved as the automation root.

## 2026-07-19 Assigned Mount Remains Undersized At 16:01 UTC

Read-only preflight at `2026-07-19T16:01:34Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path remains the new
20,957,446,144-byte ext4 filesystem, with 19,866,902,528 bytes free. Its only
entry is `lost+found`, and only 24,576 bytes are used, so no
automation-owned cleanup can make this filesystem satisfy the binary 100 GiB
heavy-build threshold.

The recorded exact `post60` run root remains absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker remains absent, Podman has no active container, and no
Sagelite automation process is running.

The separate writable `/mnt/cocalc` btrfs filesystem has 207,304,851,456
bytes free, but it is not the build root assigned by the automation runbook.
This iteration therefore did not move the build there without explicit
direction. No cleanup or Linux x86_64 build was started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`06599f46ba0109f370a5f56452fbc8a5862faadd`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Assigned Mount Remains Undersized At 15:31 UTC

Read-only preflight at `2026-07-19T15:31:25Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path remains the new
20,957,446,144-byte ext4 filesystem, with 19,866,902,528 bytes free. Its only
entry is `lost+found`, and only 24,576 bytes are used, so no
automation-owned cleanup can make this filesystem satisfy the binary 100 GiB
heavy-build threshold.

The recorded exact `post60` run root remains absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker remains absent, Podman has no active container, and no
Sagelite automation process is running.

The separate writable `/mnt/cocalc` btrfs filesystem has 207,307,476,992
bytes free, but it is not the build root assigned by the automation runbook.
This iteration therefore did not move the build there without explicit
direction. No cleanup or Linux x86_64 build was started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`ef070b98595f5614f5a8b3e08482fd993fa2256c`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Assigned Mount Remains Undersized At 15:01 UTC

Read-only preflight at `2026-07-19T15:01:26Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path remains the new
20,957,446,144-byte ext4 filesystem, with 19,866,902,528 bytes free. Its only
entry is `lost+found`, and only 24,576 bytes are used, so no
automation-owned cleanup can make this filesystem satisfy the binary 100 GiB
heavy-build threshold.

The recorded exact `post60` run root remains absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker remains absent, Podman has no active container, and no
Sagelite automation process is running.

The separate writable `/mnt/cocalc` btrfs filesystem has 207,313,035,264
bytes free, but it is not the build root assigned by the automation runbook.
This iteration therefore did not move the build there without explicit
direction. No cleanup or Linux x86_64 build was started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`62b7c64e532d3f2fb69e0a2f8365187b4f57948d`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Assigned Mount Remains Undersized At 14:31 UTC

Read-only preflight at `2026-07-19T14:31:24Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path remains the new
20,957,446,144-byte ext4 filesystem, with 19,866,902,528 bytes free. Its only
entry is `lost+found`, and only 24,576 bytes are used, so no
automation-owned cleanup can make this filesystem satisfy the binary 100 GiB
heavy-build threshold.

The recorded exact `post60` run root remains absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker remains absent, Podman has no active container, and no
Sagelite automation process is running.

The separate writable `/mnt/cocalc` btrfs filesystem has 207,316,758,528
bytes free, but it is not the build root assigned by the automation runbook.
This iteration therefore did not move the build there without explicit
direction. No cleanup or Linux x86_64 build was started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`08f80f3fad9ca23ede8da891a5a6a66ea90b254c`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Assigned Mount Remains Undersized At 14:01 UTC

Read-only preflight at `2026-07-19T14:01:53Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path remains the new
20,957,446,144-byte ext4 filesystem, with 19,866,902,528 bytes free. A direct
inventory at `2026-07-19T14:02:05Z` found only `lost+found` and 20,480 bytes
used, so no automation-owned cleanup can make this filesystem satisfy the
binary 100 GiB heavy-build threshold.

The recorded exact `post60` run root remains absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker remains absent, Podman has no active container, and no
Sagelite automation process is running.

The separate writable `/mnt/cocalc` btrfs filesystem now has
207,321,169,920 bytes free, but it is not the build root assigned by the
automation runbook. This iteration therefore did not move the build there
without explicit direction. No cleanup or Linux x86_64 build was started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`db1055a9c203e8fed5c7b2903d20620f892e9ba8`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Assigned Mount Returned Undersized At 13:31 UTC

Read-only preflight at `2026-07-19T13:31:26Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path was mounted again, but it
was a new, empty 20,957,446,144-byte ext4 filesystem with only
19,866,902,528 bytes free. That is far below the binary 100 GiB heavy-build
threshold, and cleanup cannot make this filesystem large enough.

The recorded exact `post60` run root was absent. Systemd reported both
historical units as not found and inactive while retaining `Result=success`
and `ExecMainStatus=0`; no artifact result is inferred without the historical
bulk files. Docker was absent, Podman had no active container, and no Sagelite
automation process was running.

A separate writable `/mnt/cocalc` btrfs filesystem had
210,119,565,312 bytes free, above the threshold. It is not the build root
assigned by the automation runbook, so this iteration did not move the build
there without explicit direction. No cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. The
canonical checkout was clean on `develop` at
`ca0284c7023e6049318183c35c38032127431d5b`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. This cell is blocked until a qualifying assigned
bulk mount returns or the larger `/mnt/cocalc` filesystem is explicitly
approved as the automation root.

## 2026-07-19 Host Timed Out At 13:02 UTC

All three bounded SSH attempts through the required `host` alias timed out.
The final controller checkpoint was `2026-07-19T13:02:19Z`. No remote session
was established, so this iteration could not recheck the architecture, mount
inventory, historical services, containers, old `post60` run root, or current
free space. The possibly surviving bulk artifacts remain untouched, and no
wheel, validation result, or failure is inferred.

The last reachable preflight at `2026-07-19T12:01:17Z` found the assigned
`/mnt/cocalc-scratch` mount absent and only 85,317,668,864 bytes free on the
separate `/mnt/cocalc` volume, below the binary 100 GiB heavy-build threshold.
No Linux x86_64 build was launched. The other six release-candidate cells on
Linux aarch64 and macOS arm64 are already synchronized and accepted, so no
independent matrix work remained for this iteration.

The canonical checkout was clean on `develop` at
`225d8240849ba42b161c948eb13529725ddd87e7`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. The directly fetched public `dev/manifest.json`
still contains 177 wheels, including fourteen Sagelite primary wheels and no
`post63` artifact; its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`.

## 2026-07-19 Host Timed Out At 12:31 UTC

All three bounded SSH attempts through the required `host` alias timed out.
The final controller checkpoint was `2026-07-19T12:32:50Z`. No remote session
was established, so this iteration could not recheck the architecture, mount
inventory, historical services, containers, old `post60` run root, or current
free space. The possibly surviving bulk artifacts remain untouched, and no
wheel, validation result, or failure is inferred.

The last reachable preflight at `2026-07-19T12:01:17Z` found the assigned
`/mnt/cocalc-scratch` mount absent and only 85,317,668,864 bytes free on the
separate `/mnt/cocalc` volume, below the binary 100 GiB heavy-build threshold.
No Linux x86_64 build was launched. The other six release-candidate cells on
Linux aarch64 and macOS arm64 are already synchronized and accepted, so no
independent matrix work remained for this iteration.

The canonical checkout was clean on `develop` at
`7c9bcea2c07810893b31c8b1be846c6ae2220d7b`, synchronized with
`origin/develop`. Exact pushed `post63` source `16d6d78012a` remains the
selected release candidate. The directly fetched public `dev/manifest.json`
still contains 177 wheels, including fourteen Sagelite primary wheels and no
`post63` artifact; its generation timestamp remains
`2026-07-09T17:17:42.743310+00:00`.

## 2026-07-19 Assigned Bulk Mount Still Absent At 12:01 UTC

Read-only preflight at `2026-07-19T12:01:17Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,093,563,392 bytes free. The recorded exact
`post60` run root was not visible. Systemd reported both historical units as
not found and inactive, while retaining `Result=success` and
`ExecMainStatus=0`; no wheel or validation result is inferred without the
assigned bulk artifacts.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,317,668,864 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation process was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 11:31 UTC

Read-only preflight at `2026-07-19T11:31:14Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,102,517,248 bytes free. The recorded exact
`post60` run root was not visible. Systemd reported both historical units as
not found and inactive, while retaining `Result=success` and
`ExecMainStatus=0`; no wheel or validation result is inferred without the
assigned bulk artifacts.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,326,938,112 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation process was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 11:01 UTC

Read-only preflight at `2026-07-19T11:01:07Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,103,074,304 bytes free. The recorded exact
`post60` run root was not visible. Its historical build and watcher services
remained inactive with `Result=success` and `ExecMainStatus=0`, but the missing
bulk artifacts prevent any wheel or validation inference.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,346,979,840 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation service was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 10:31 UTC

Read-only preflight at `2026-07-19T10:31:26Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,103,631,360 bytes free. The recorded exact
`post60` run root was not visible. Its historical build and watcher services
remained inactive with `Result=success` and `ExecMainStatus=0`, but the missing
bulk artifacts prevent any wheel or validation inference.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,360,570,368 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation service was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 10:01 UTC

Read-only preflight at `2026-07-19T10:01:16Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,104,176,128 bytes free. The recorded exact
`post60` run root was not visible. Its historical build and watcher services
remained inactive with `Result=success` and `ExecMainStatus=0`, but the missing
bulk artifacts prevent any wheel or validation inference.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,370,339,328 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation service was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 09:31 UTC

Read-only preflight at `2026-07-19T09:31:27Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,104,724,992 bytes free. The recorded exact
`post60` run root was not visible. Its historical build and watcher services
remained inactive with `Result=success` and `ExecMainStatus=0`, but the missing
bulk artifacts prevent any wheel or validation inference.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,366,231,040 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation service was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent At 09:01 UTC

Read-only preflight at `2026-07-19T09:01:36Z` reached `host` as native Linux
`x86_64`. The required `/mnt/cocalc-scratch` path still resolved to the 24 GB
root filesystem, which had 15,105,253,376 bytes free. The recorded exact
`post60` run root was not visible. Its historical build and watcher services
remained inactive with `Result=success` and `ExecMainStatus=0`, but the missing
bulk artifacts prevent any wheel or validation inference.

The complete mount inventory again found only `/mnt/cocalc` as a separate
writable bulk filesystem. It had 85,377,052,672 bytes free, below the binary
100 GiB heavy-build threshold. Docker was absent; Podman was installed but had
no active container, and no Sagelite automation service was running. The
visible bulk volume is not assigned to this job, and no safe automation-owned
cleanup target was identified, so no cleanup or Linux x86_64 build was
started.

The directly fetched public `dev/manifest.json` still contains 177 wheels,
including fourteen Sagelite primary wheels and no `post63` artifact. Its
generation timestamp remains `2026-07-09T17:17:42.743310+00:00`. Exact pushed
`post63` source `16d6d78012a` remains the selected release candidate. This
cell is blocked until the assigned bulk mount returns or another explicitly
in-scope filesystem meets the threshold.

## 2026-07-19 Assigned Bulk Mount Still Absent

The latest read-only preflight at `2026-07-19T08:31:28Z` reached `host` as
native Linux `x86_64`, but
the required `/mnt/cocalc-scratch` bulk filesystem was still absent. That path
resolved to the 24 GB root filesystem with 15,105,802,240 bytes free. The
recorded exact `post60` run root remained invisible. Both historical services
were inactive with `Result=success` and `ExecMainStatus=0`, but no wheel or
validation result is inferred without the assigned bulk artifacts.

A complete mount inventory found no safe host-side replacement that met the
binary 100 GiB heavy-build threshold. The only separate writable bulk mount,
`/mnt/cocalc`, had 85,399,818,240 bytes free, and this staging host did not
provide Docker. No cleanup or build was started. Exact pushed `post63` source
`16d6d78012a` remains the selected release candidate, but this cell cannot be
rebuilt until the assigned bulk mount returns or another explicitly in-scope
filesystem exceeds the threshold.

The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post63` artifact.

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
