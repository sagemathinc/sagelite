# Sagelite Worker

This Cloudflare Worker serves staged Sagelite wheels from the private
`sagelite` R2 bucket at `https://sagelite.sagemath.org/`.

It is intentionally small:

- `GET` and `HEAD` only
- private R2 bucket binding named `SAGELITE_BUCKET`
- `/path/` maps to R2 key `/path/index.html`
- missing `/path` redirects to `/path/` when `/path/index.html` exists
- wheel, HTML, and JSON content types are set when R2 metadata is absent

Deploy with a Cloudflare token that can edit Workers for `sagemath.org`:

```bash
export CLOUDFLARE_API_TOKEN="$(cat /run/secrets/cocalc/sagemath.org-cloudflare-worker-token.txt)"
cd tools/sagelite-worker
npx wrangler deploy
```

The staged pip indexes currently published by `tools/publish-sagelite-r2-wheel-index.sh`
are:

```text
https://sagelite.sagemath.org/dev/simple/
https://sagelite.sagemath.org/dev/linux-x86_64-cp312/simple/
https://sagelite.sagemath.org/dev/linux-aarch64-cp312/simple/
```

The current Linux CPython 3.12 developer trial command is:

```bash
python3.12 -m venv sage-pip-test && sage-pip-test/bin/python -m pip install --upgrade pip && sage-pip-test/bin/python -m pip install --extra-index-url https://sagelite.sagemath.org/dev/simple/ 'sagelite==10.9.post1'
```
