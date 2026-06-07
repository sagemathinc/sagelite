# sagelite-mathjax-runtime

Optional MathJax companion runtime for `sagelite`.

This package bundles the MathJax JavaScript runtime used by Sage documentation
and rich output paths. When installed with `sagelite`, `sage.env` points
`MATHJAX_DIR` at the bundled runtime if the build-time Sage prefix is not
available.

To test installation directly from GitHub, use:

```bash
pip install "git+https://github.com/sagemathinc/sagelite.git@develop#subdirectory=companion-packages/sagelite-mathjax-runtime"
```
