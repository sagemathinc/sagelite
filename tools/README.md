# Tools Directory

This folder contains various command-line tools that are used to facilitate different development tasks. Below is a brief description of each command available in this directory.

## Update Conda Environment Files

This command is used to update the Conda environment files in the project. It automatically adds new dependencies to the Conda files, removes deleted dependencies, and updates the version of existing dependencies. The source of the dependencies is the `pyproject.toml` file, which specifies the following dependencies:

- `build-system.requires`: Python dependencies required for building
- `project.dependencies`: Python dependencies required for running
- `external.build-requires`: External dependencies required for building
- `external.host-requires`: External dependencies required for running


Within an active virtual environment where `grayskull` and `conda-lock` are installed, run the following command:

```bash
tools/update-conda.py
```

## Update Meson Build Files

This command is used to updates the Meson build files in the project. It automatically adds new source files (py, pyx) to the Meson files and removes deleted source files. This command is useful when adding or removing source files from the project.

Within an active virtual environment where Meson is installed, run the following command:

```bash
tools/update-meson.py
```

## Find Outdated Deprecations

Code that is deprecated can be safely removed one year after the first stable release containing the deprecation. This command searches for deprecated code in the source folder and prints all old deprecations.

Within an active virtual environment where `pygithub` and `tqdm` is installed, run the following command:

```bash
tools/check_deprecations.py <optional path to source folder>
```

It is recommended to pass a subfolder of the source folder to the script to avoid checking the entire source folder, which most likely triggers a rate limit on the GitHub API.
Alternatively, you can pass a [GitHub token](https://github.com/settings/tokens) via the `--token` argument to avoid the rate limit.

## Analyze Doctest Logs

This command reduces a large Sage doctest run into a smaller set of
categories and fingerprints. It is useful when triaging a broad wheel or
distribution validation run, where the raw log is too large to inspect
manually.

It combines the plain-text doctest log with the per-module stats JSON and can
write both machine-readable JSON and a Markdown summary.

Example:

```bash
python3 tools/analyze-doctest-log.py \
  --log /path/to/doctest.log \
  --stats /path/to/doctest.json \
  --json-out /tmp/doctest-analysis.json \
  --md-out /tmp/doctest-analysis.md
```

## Run Installed-Wheel Doctests

This command runs `python -m sage.doctest --installed` in the active
installed-wheel environment, captures the raw doctest log and stats JSON, and
then immediately reduces them with `tools/analyze-doctest-log.py`.
The runner prepends the selected interpreter's `bin` directory to `PATH`, sets
`PYTHONNOUSERSITE=1`, and removes inherited `PYTHONPATH` and `LD_LIBRARY_PATH`
so installed-wheel validation does not depend on source-tree imports or manual
library-path adjustments.

Example:

```bash
test-venv/bin/python tools/run-installed-wheel-doctests.py \
  --output-dir .local-build-logs \
  --label staged-index
```

This writes four artifacts per run:

- the raw doctest log
- the doctest stats JSON
- the reduced analysis JSON
- the reduced Markdown summary

Pass `--runtime-summary` to also write a runtime manifest and a JSON runtime
summary. After analysis completes, the runtime summary includes the analyzer's
category counts, fingerprint counts, and top actionable buckets so validation
runs can be triaged without opening the full log first.

## Validate a Sagelite Wheelhouse

This command creates a fresh virtual environment, installs sagelite from one or
more local wheelhouses with `--no-index`, runs `pip check`, then invokes
`tools/run-installed-wheel-doctests.py` with runtime manifest and selftest
capture enabled. It is intended for repaired-wheel validation artifacts from
the manylinux/CIBW build, where local raw-wheel repair is not authoritative.
The validation directory includes `install-metadata.json`, which records the
fresh install path, wheelhouse inputs, package requirement, commands, and
sanitized environment used for the run. It also records the controller Python
and requested base Python so CIBW artifacts show which interpreter created the
fresh venv. The metadata is updated after each step with command result
phase, status, exit code, and elapsed time so interrupted or failed scheduled
runs still identify the failing phase. Use
`--require-repaired-sagelite-wheel` for authoritative manylinux/CIBW proof
runs so raw Linux wheels fail during metadata-recorded preflight instead of
being mistaken for repaired-wheel evidence.

Example:

```bash
python3 tools/validate-sagelite-wheelhouse.py \
  --wheelhouse /scratch/sagelite-r2-work/wheelhouse-20260621 \
  --work-dir /scratch/sagelite-r2-work \
  --require-repaired-sagelite-wheel \
  --full
```

## Update Version Number

Increments the version number in the project. This command is useful when releasing a new version of the project.

Set `SAGE_ROOT` to the root directory of the Sage project and run the following command:

```bash
tools/update_version
```

## Generate cython header files for flint

The flint-autogen directory contains a script (`flint_autogen.py`)
that will automatically generate the pxd files in
`SAGE_ROOT/src/sage/libs/flint`. It requires gitpython to be
installed, and for `FLINT_GIT_DIR` to be set to a clone of the flint
git repository.

Example:

```bash
# don't forget to install gitpython first
cd flint-autogen
FLINT_GIT_DIR=/path/to/flint.git python flint_autogen.py
```
