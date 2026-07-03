#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat >&2 <<'EOF'
usage: tools/publish-sagelite-r2-wheel-index.sh WHEELHOUSE [PREFIX]

Publish a wheelhouse to a Cloudflare R2 bucket using S3-compatible
credentials, then build and publish a PEP 503 simple index for the wheels.

Environment:
  SAGELITE_R2_SECRET_FILE   shell file containing R2 credentials
                            (default: /run/secrets/cocalc/sagelite-r2-bucket.sh)
  SAGELITE_R2_BUCKET        R2 bucket name (default: sagelite)
  SAGELITE_R2_ENDPOINT      R2 S3 endpoint URL; can also be `s3_endpoint`
                            in the secret file
  SAGELITE_R2_PREFIX        object prefix when PREFIX is omitted
                            (default: dev)
  SAGELITE_R2_WORK_DIR      scratch directory for generated index files
                            (default: /scratch/sagelite-r2-work)
  SAGELITE_SIMPLE_INDEX_URL public simple-index URL to show in output
  SAGELITE_PUBLISH_DRY_RUN  set to 1 to pass --dryrun to aws s3 sync/cp

The secret file may define lower-case access_key_id, secret_access_key, and
s3_endpoint variables; they are mapped to AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY, and SAGELITE_R2_ENDPOINT.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

wheelhouse="${1:-}"
prefix="${2:-${SAGELITE_R2_PREFIX:-dev}}"
if [ -z "${wheelhouse}" ]; then
  usage
  exit 2
fi

if [ ! -d "${wheelhouse}" ]; then
  echo "wheelhouse directory does not exist: ${wheelhouse}" >&2
  exit 1
fi

wheel_count="$(find "${wheelhouse}" -maxdepth 1 -type f -name '*.whl' | wc -l)"
if [ "${wheel_count}" -eq 0 ]; then
  echo "no wheels found in ${wheelhouse}" >&2
  exit 1
fi

secret_file="${SAGELITE_R2_SECRET_FILE:-/run/secrets/cocalc/sagelite-r2-bucket.sh}"
if [ -f "${secret_file}" ]; then
  # shellcheck source=/dev/null
  . "${secret_file}"
fi

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-${access_key_id:-}}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-${secret_access_key:-}}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-auto}"

bucket="${SAGELITE_R2_BUCKET:-sagelite}"
endpoint="${SAGELITE_R2_ENDPOINT:-${s3_endpoint:-}}"
work_dir="${SAGELITE_R2_WORK_DIR:-/scratch/sagelite-r2-work}"
aws_bin="${AWS_BIN:-aws}"

if [ -z "${AWS_ACCESS_KEY_ID}" ] || [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
  echo "R2 access credentials are required" >&2
  exit 1
fi
if [ -z "${endpoint}" ]; then
  echo "SAGELITE_R2_ENDPOINT or s3_endpoint is required" >&2
  exit 1
fi
if ! command -v "${aws_bin}" >/dev/null 2>&1; then
  echo "aws CLI not found; set AWS_BIN or install awscli" >&2
  exit 1
fi

prefix="${prefix#/}"
prefix="${prefix%/}"
if [ -z "${prefix}" ]; then
  echo "prefix must not be empty" >&2
  exit 1
fi

publish_dir="${work_dir%/}/publish-${prefix//\//-}"
simple_dir="${publish_dir}/simple"
root_dir="${publish_dir}/root"
manifest="${publish_dir}/manifest.json"
rm -rf "${publish_dir}"
mkdir -p "${simple_dir}" "${root_dir}"

python3 tools/build-sagelite-wheel-index.py "${wheelhouse}" --output "${simple_dir}"

python3 - "${wheelhouse}" "${manifest}" <<'PY'
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

wheelhouse = Path(sys.argv[1])
manifest = Path(sys.argv[2])
wheels = []
for wheel in sorted(wheelhouse.glob("*.whl")):
    digest = hashlib.sha256()
    with wheel.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    wheels.append(
        {
            "filename": wheel.name,
            "size": wheel.stat().st_size,
            "sha256": digest.hexdigest(),
        }
    )
manifest.write_text(
    json.dumps(
        {
            "schema": "sagelite-r2-wheel-index-v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "wheel_count": len(wheels),
            "wheels": wheels,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)
PY

simple_index_url="${SAGELITE_SIMPLE_INDEX_URL:-}"
cat > "${root_dir}/index.html" <<EOF
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sagelite wheel index</title>
  </head>
  <body>
    <h1>Sagelite wheel index</h1>
    <p><a href="simple/">Simple package index</a></p>
    <p><a href="manifest.json">Wheel manifest</a></p>
EOF
if [ -n "${simple_index_url}" ]; then
  cat >> "${root_dir}/index.html" <<EOF
    <pre>python -m pip install --extra-index-url ${simple_index_url} sagelite</pre>
EOF
fi
cat >> "${root_dir}/index.html" <<'EOF'
  </body>
</html>
EOF
cp "${manifest}" "${root_dir}/manifest.json"

dry_run_args=()
if [ "${SAGELITE_PUBLISH_DRY_RUN:-0}" = "1" ]; then
  dry_run_args=(--dryrun)
fi

wheel_dest="s3://${bucket}/${prefix}/wheels/"
simple_dest="s3://${bucket}/${prefix}/simple/"
root_dest="s3://${bucket}/${prefix}/"

echo "Publishing ${wheel_count} wheel(s) to ${wheel_dest}"
"${aws_bin}" s3 sync "${wheelhouse}/" "${wheel_dest}" \
  --endpoint-url "${endpoint}" \
  --exclude "*" \
  --include "*.whl" \
  --cache-control "public, max-age=31536000, immutable" \
  --content-type "application/octet-stream" \
  --size-only \
  "${dry_run_args[@]}"

echo "Publishing simple index to ${simple_dest}"
"${aws_bin}" s3 sync "${simple_dir}/" "${simple_dest}" \
  --endpoint-url "${endpoint}" \
  --delete \
  --cache-control "public, max-age=60" \
  --content-type "text/html; charset=utf-8" \
  "${dry_run_args[@]}"

echo "Publishing root index and manifest to ${root_dest}"
"${aws_bin}" s3 cp "${root_dir}/index.html" "${root_dest}index.html" \
  --endpoint-url "${endpoint}" \
  --cache-control "public, max-age=60" \
  --content-type "text/html; charset=utf-8" \
  "${dry_run_args[@]}"
"${aws_bin}" s3 cp "${root_dir}/manifest.json" "${root_dest}manifest.json" \
  --endpoint-url "${endpoint}" \
  --cache-control "public, max-age=60" \
  --content-type "application/json; charset=utf-8" \
  "${dry_run_args[@]}"

echo "Published R2 prefix: s3://${bucket}/${prefix}/"
echo "Generated index files: ${publish_dir}"
if [ -n "${simple_index_url}" ]; then
  echo "Simple index URL: ${simple_index_url}"
fi
