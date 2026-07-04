const INDEX_DOCUMENT = "index.html";

const TEXT_TYPES = new Map([
  [".html", "text/html; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".txt", "text/plain; charset=utf-8"],
  [".whl", "application/octet-stream"],
]);

function html(body, init = {}) {
  return new Response(`<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sagelite wheel index</title>
  </head>
  <body>
${body}
  </body>
</html>
`, {
    ...init,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "public, max-age=60",
      ...(init.headers || {}),
    },
  });
}

function rootIndex() {
  return html(`    <h1>Sagelite wheel index</h1>
    <ul>
      <li><a href="/dev/simple/">Developer preview simple index</a></li>
      <li><a href="/dev/linux-x86_64-cp312/simple/">Linux x86_64 CPython 3.12 simple index</a></li>
      <li><a href="/dev/linux-aarch64-cp312/simple/">Linux aarch64 CPython 3.12 simple index</a></li>
    </ul>
    <p>Example:</p>
    <pre>python3.12 -m venv sage-pip-test &amp;&amp; sage-pip-test/bin/python -m pip install --upgrade pip &amp;&amp; sage-pip-test/bin/python -m pip install --extra-index-url https://sagelite.sagemath.org/dev/simple/ 'sagelite==10.9.post3'</pre>
`);
}

function objectKey(pathname) {
  let key = pathname.replace(/^\/+/, "");
  if (key === "") {
    return "";
  }
  if (key.endsWith("/")) {
    key += INDEX_DOCUMENT;
  }
  return key;
}

function fallbackContentType(key) {
  const lower = key.toLowerCase();
  for (const [suffix, contentType] of TEXT_TYPES) {
    if (lower.endsWith(suffix)) {
      return contentType;
    }
  }
  return "application/octet-stream";
}

function responseHeaders(object, key) {
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);
  if (!headers.has("content-type")) {
    headers.set("content-type", fallbackContentType(key));
  }
  if (!headers.has("cache-control")) {
    if (key.endsWith(".whl")) {
      headers.set("cache-control", "public, max-age=31536000, immutable");
    } else {
      headers.set("cache-control", "public, max-age=60");
    }
  }
  return headers;
}

async function serveObject(request, env, key) {
  const object = await env.SAGELITE_BUCKET.get(key);
  if (object === null) {
    return null;
  }
  const headers = responseHeaders(object, key);
  if (request.method === "HEAD") {
    return new Response(null, { headers });
  }
  return new Response(object.body, { headers });
}

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("method not allowed\n", {
        status: 405,
        headers: { allow: "GET, HEAD" },
      });
    }

    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "") {
      if (request.method === "HEAD") {
        return new Response(null, {
          headers: {
            "content-type": "text/html; charset=utf-8",
            "cache-control": "public, max-age=60",
          },
        });
      }
      return rootIndex();
    }

    const key = objectKey(url.pathname);
    let response = await serveObject(request, env, key);
    if (response !== null) {
      return response;
    }

    if (!url.pathname.endsWith("/")) {
      const indexKey = `${key}/${INDEX_DOCUMENT}`;
      response = await serveObject(request, env, indexKey);
      if (response !== null) {
        url.pathname += "/";
        return Response.redirect(url.toString(), 301);
      }
    }

    return new Response("not found\n", {
      status: 404,
      headers: {
        "content-type": "text/plain; charset=utf-8",
        "cache-control": "public, max-age=60",
      },
    });
  },
};
