# Sagelite Linux x86_64 CPython 3.14 Validation

## 2026-07-15 Preflight Blocker

The scheduled matrix iteration selected Linux `x86_64` with CPython 3.14, the
next cell in the authoritative work order. The canonical repository was clean
at source commit `cef925c228a6803f37c8ca68ed92d516bb8c94b5` on `develop`, with
`origin/develop` at the same commit.

The public `dev/manifest.json` still reported 177 wheels generated on
2026-07-09 and the public Sagelite project page still listed fourteen primary
wheels: seven each for `10.9.post8` and `10.9.post9`. No newer local aarch64
primary was assumed to be public.

Read-only preflight through the required `host` SSH alias found:

- the environment reported Linux `x86_64`;
- the expected `/mnt/cocalc-scratch` filesystem was not mounted;
- `/mnt/cocalc` had 64 GiB free and `/` had 17 GiB free;
- no automation-owned Sagelite build or validation process, PID, exit-code,
  validation summary, or run metadata was present;
- Podman 4.9.3 was available, but Docker and host `python3.14` were not.

The 64 GiB filesystem is above the 30 GiB test-only threshold but below the
runbook's non-negotiable 100 GiB threshold for a heavy build. It is also a
different mount from the assigned automation root. Safe cleanup cannot repair
the capacity shortfall: the filesystem was only 13% used and its total size
was 75 GiB.

No build, validation, or public publication was started. Re-running the public
`10.9.post9` CPython 3.14 wheel would not validate the current committed source
and would predate failure fixes already proved in the aarch64 work. The cell
therefore remains `smoke only`. Resume by restoring the expected bulk volume
on `host` (with at least 100 GiB free), then preflight again and build the exact
current committed revision using the repository CIBW contract.
