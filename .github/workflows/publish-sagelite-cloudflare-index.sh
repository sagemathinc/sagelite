#!/usr/bin/env bash

set -euo pipefail

artifact_root="${1:?artifact root is required}"
pages_dir="${2:-cloudflare-pages}"

require_env() {
  local name="$1"
  if [ -z "${!name:-}" ]; then
    echo "${name} is required" >&2
    exit 1
  fi
}

require_env CLOUDFLARE_API_TOKEN
require_env CLOUDFLARE_ACCOUNT_ID
require_env CLOUDFLARE_R2_BUCKET
require_env CLOUDFLARE_PAGES_PROJECT
require_env SAGELITE_WHEEL_BASE_URL

wheel_count="$(find "${artifact_root}" -type f -name '*.whl' | wc -l)"
if [ "${wheel_count}" -eq 0 ]; then
  echo "No wheel artifacts found under ${artifact_root}" >&2
  exit 1
fi

wheelhouse="${RUNNER_TEMP:-/tmp}/sagelite-cloudflare-wheelhouse"
rm -rf "${wheelhouse}" "${pages_dir}"
mkdir -p "${wheelhouse}" "${pages_dir}"

while IFS= read -r -d '' wheel; do
  target="${wheelhouse}/$(basename "${wheel}")"
  if [ -e "${target}" ] && ! cmp -s "${wheel}" "${target}"; then
    echo "Conflicting wheel artifact basename: $(basename "${wheel}")" >&2
    exit 1
  fi
  cp -f "${wheel}" "${target}"
done < <(find "${artifact_root}" -type f -name '*.whl' -print0)

published_wheel_count="$(find "${wheelhouse}" -type f -name '*.whl' | wc -l)"
if [ "${published_wheel_count}" -eq 0 ]; then
  echo "No publishable wheel artifacts found under ${artifact_root}" >&2
  exit 1
fi

r2_prefix="${SAGELITE_R2_WHEEL_PREFIX:-wheels}"
r2_prefix="${r2_prefix#/}"
r2_prefix="${r2_prefix%/}"
wheel_base_url="${SAGELITE_WHEEL_BASE_URL%/}"

while IFS= read -r -d '' wheel; do
  filename="$(basename "${wheel}")"
  object_path="${CLOUDFLARE_R2_BUCKET}/${r2_prefix}/${filename}"
  echo "Uploading ${filename} to R2 object ${object_path}"
  npx --yes wrangler@latest r2 object put "${object_path}" \
    --file "${wheel}" \
    --content-type application/octet-stream \
    --cache-control "public, max-age=31536000, immutable" \
    --remote
done < <(find "${wheelhouse}" -type f -name '*.whl' -print0 | sort -z)

python3 tools/build-sagelite-wheel-index.py \
  "${wheelhouse}" \
  --output "${pages_dir}/simple" \
  --wheel-base-url "${wheel_base_url}"

simple_index_url="${SAGELITE_SIMPLE_INDEX_URL:-https://${CLOUDFLARE_PAGES_PROJECT}.pages.dev/simple}"
cat > "${pages_dir}/index.html" <<EOF
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sagelite wheel index</title>
  </head>
  <body>
    <h1>Sagelite wheel index</h1>
    <p><a href="simple/">Simple package index</a></p>
    <pre>python -m pip install --extra-index-url ${simple_index_url} 'sagelite[full]'</pre>
  </body>
</html>
EOF

touch "${pages_dir}/.nojekyll"

deploy_args=(pages deploy "${pages_dir}" --project-name "${CLOUDFLARE_PAGES_PROJECT}")
if [ -n "${GITHUB_REF_NAME:-}" ]; then
  deploy_args+=(--branch "${GITHUB_REF_NAME}")
fi
if [ -n "${GITHUB_SHA:-}" ]; then
  deploy_args+=(--commit-hash "${GITHUB_SHA}")
fi
if [ -n "${GITHUB_SERVER_URL:-}" ] && [ -n "${GITHUB_REPOSITORY:-}" ] && [ -n "${GITHUB_RUN_ID:-}" ]; then
  deploy_args+=(--commit-message "Update Sagelite staged wheel index from ${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}")
fi

npx --yes wrangler@latest "${deploy_args[@]}"
