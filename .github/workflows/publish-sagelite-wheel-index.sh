#!/usr/bin/env bash

set -euo pipefail

artifact_root="${1:?artifact root is required}"
pages_dir="${2:-pages}"

if [ -z "${GITHUB_TOKEN:-}" ] || [ -z "${GITHUB_REPOSITORY:-}" ]; then
  echo "GITHUB_TOKEN and GITHUB_REPOSITORY are required" >&2
  exit 1
fi

wheel_count="$(find "${artifact_root}" -type f -name '*.whl' | wc -l)"
if [ "${wheel_count}" -eq 0 ]; then
  echo "No wheel artifacts found under ${artifact_root}" >&2
  exit 1
fi

rm -rf "${pages_dir}"
remote="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

if git ls-remote --exit-code --heads origin gh-pages >/dev/null 2>&1; then
  git clone --depth 1 --branch gh-pages "${remote}" "${pages_dir}"
else
  mkdir -p "${pages_dir}"
  git -C "${pages_dir}" init
  git -C "${pages_dir}" checkout -b gh-pages
  git -C "${pages_dir}" remote add origin "${remote}"
fi

git -C "${pages_dir}" rm -r --ignore-unmatch . >/dev/null 2>&1 || true
find "${pages_dir}" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
mkdir -p "${pages_dir}/wheels"
max_github_blob_size=$((100 * 1024 * 1024))
skipped_large_wheels=0
while IFS= read -r -d '' wheel; do
  wheel_size="$(stat -c '%s' "${wheel}")"
  if [ "${wheel_size}" -gt "${max_github_blob_size}" ]; then
    echo "Skipping $(basename "${wheel}") (${wheel_size} bytes): exceeds GitHub's 100 MiB file limit" >&2
    skipped_large_wheels=$((skipped_large_wheels + 1))
    continue
  fi
  cp -f "${wheel}" "${pages_dir}/wheels/"
done < <(find "${artifact_root}" -type f -name '*.whl' -print0)

published_wheel_count="$(find "${pages_dir}/wheels" -type f -name '*.whl' | wc -l)"
if [ "${published_wheel_count}" -eq 0 ]; then
  echo "No publishable wheel artifacts found under ${artifact_root}" >&2
  exit 1
fi
if [ "${skipped_large_wheels}" -gt 0 ]; then
  echo "Skipped ${skipped_large_wheels} oversized wheel artifact(s)" >&2
fi
rm -rf "${pages_dir}/simple"
python3 tools/build-sagelite-wheel-index.py "${pages_dir}/wheels" --output "${pages_dir}/simple"
touch "${pages_dir}/.nojekyll"
repo_owner="${GITHUB_REPOSITORY%%/*}"
repo_name="${GITHUB_REPOSITORY#*/}"
index_url="https://${repo_owner}.github.io/${repo_name}/simple"
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
    <pre>python -m pip install --extra-index-url ${index_url} 'sagelite[full]'</pre>
  </body>
</html>
EOF

git -C "${pages_dir}" config user.name "github-actions[bot]"
git -C "${pages_dir}" config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git -C "${pages_dir}" add .nojekyll index.html simple wheels

if git -C "${pages_dir}" diff --cached --quiet; then
  echo "Sagelite wheel index is already up to date"
  exit 0
fi

git -C "${pages_dir}" commit -m "sagelite: update staged wheel index"
git -C "${pages_dir}" push origin gh-pages
