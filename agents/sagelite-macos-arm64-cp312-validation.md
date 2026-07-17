# Sagelite macOS arm64 CPython 3.12 Validation

## 2026-07-17 Post54 Exact Rebuild Start

The scheduled iteration first retried the higher-priority Linux x86_64
CPython 3.14 cell. All three bounded SSH attempts to `host` timed out. No
x86_64 build or validation was started. The directly fetched public
`dev/manifest.json` remained the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, including fourteen Sagelite primary
wheels.

Independent preflight found `m1` idle and native Darwin arm64 with Homebrew
CPython 3.12, 3.13, and 3.14 available. `/Volumes/sage` had 105 GiB free,
above the 100 GiB heavy-build threshold. The Lima backend also reported Linux
aarch64 with 103,443,718,144 bytes free, but no Linux work was selected because
the next independent matrix cell is native macOS arm64 CPython 3.12.

The selected release-candidate source is exact pushed commit
`4071f482bcc3865116d57391b00227ae0a9f28d4` (`10.9.post54`). It is an
ancestor of the verified `origin/develop` head. The controller-created source
archive is 151,219,896 bytes with SHA256
`7e457b3827627b290e2b58a426f618227de12269dc19aae3689d8a7072691ba2`.
Its independently materialized tree is
`513286131f987e2cb30e3fd12956c800cfca2328`, matching the committed tree.
The full archive size and digest were verified on `m1` before launch.

The native CPython 3.12 build is running durably under tmux session
`sagelite_cp312_post54_build`, with recorded PID 26677, at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260717-050335-4071f482bcc/
```

The build reuses the retained automation-owned native dependency prefix from
the proven macOS build chain at
`macos-arm64-cp313-20260716-021120-d75dd63d011`, creates a fresh CPython 3.12
build venv, and applies the committed cypari, Singular, PARI, and general
macOS repair stages. Its durable evidence includes `build-command.sh`,
`command.log`, `pid`, `disk-before.txt`, and, after source verification,
`run-metadata.txt`. Completion will be recorded in `exit-code`.

This is exact-source build-start evidence only. No CPython 3.12 `post54`
wheel, compatible closure, fresh installation, `pip check`, selftest, short
gate, full-suite pass, or publication result is claimed yet.
