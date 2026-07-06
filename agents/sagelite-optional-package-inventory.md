# Sagelite Optional Package Inventory

This generated report is a first-pass triage of Sage packages whose
`build/pkgs/*/type` is `optional` or `experimental`. It is not a legal
review and it is not proof that a package builds as a wheel.

Regenerate with:

```bash
python tools/sagelite_optional_package_inventory.py > agents/sagelite-optional-package-inventory.md
```

## Summary

- Optional/experimental package directories: 165
- By Sage type: experimental=8, optional=157
- By triage tier: excluded=2, tier 0=65, tier 1=28, tier 2=27, tier 3=43
- By Sagelite status: base dependency=12, extra -> PyPI/system=11, extra -> companion=42, not packaged=100

Tier meanings:

- `tier 0`: already represented in Sagelite base dependencies, extras, or companion-wheel metadata.
- `tier 1`: likely first-batch candidate: pip-style metadata, no huge/nonfree signal, and limited native packaging risk.
- `tier 2`: plausible but needs native packaging or manual metadata review.
- `tier 3`: high-risk, huge, experimental, patched native source, or otherwise likely to need focused work.
- `excluded`: nonfree dependency or license signal in Sage metadata.

## First-Batch Candidates

| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |
|---|---:|---|---|---|---|---|
| `admcycles` | - | unknown | not packaged | pip | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip-style package metadata |
| `biopython` | - | unknown | not packaged | pip, distros | - | pip-style package metadata |
| `clarabel` | 0.11.1 | unknown | not packaged | pip | numpy scipy cffi \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip-style package metadata |
| `ecos_python` | 2.0.14 | unknown | not packaged | pip, native, distros | numpy scipy \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip package with Sage install wrapper |
| `gap_jupyter` | 0.9 | unknown | not packaged | pip, native, distros | \| $(PYTHON_TOOLCHAIN) ipython gap $(PYTHON) | pip package with Sage install wrapper |
| `gitpython` | - | unknown | not packaged | pip | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip-style package metadata |
| `jupymake` | 0.9 | unknown | not packaged | pip, native, distros | polymake \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip package with Sage install wrapper |
| `nibabel` | - | unknown | not packaged | pip, distros | - | pip-style package metadata |
| `ore_algebra` | - | unknown | not packaged | pip, distros | \| $(PYTHON_TOOLCHAIN) $(SAGERUNTIME) $(PYTHON) | pip-style package metadata |
| `osqp_python` | 1.1.1 | unknown | not packaged | pip, native, distros | qdldl_python numpy scipy jinja2 joblib \| $(PYTHON_TOOLCHAIN) cmake $(PYTHON) | pip package with Sage install wrapper |
| `pandoc_attributes` | 8bc82f6d | unknown | not packaged | pip, native, distros | \| pandocfilters $(PYTHON) $(PYTHON_TOOLCHAIN) | pip package with Sage install wrapper |
| `pari_jupyter` | 1.4.3 | unknown | not packaged | pip, native, distros | pari \| $(PYTHON_TOOLCHAIN) cython notebook jupyter_core ipykernel $(PYTHON) | pip package with Sage install wrapper |
| `pybtex` | - | unknown | not packaged | pip, distros | - | pip-style package metadata |
| `pygraphviz` | - | unknown | not packaged | pip, distros | libgraphviz \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip-style package metadata |
| `pyppeteer` | - | unknown | not packaged | pip, distros | appdirs urllib3 certifi \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip-style package metadata |
| `pysingular` | 0.9.7 | unknown | not packaged | pip, native, distros | singular \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip package with Sage install wrapper |
| `python_flint` | 0.8.0 | unknown | not packaged | pip, native | flint \| $(PYTHON_TOOLCHAIN) cython $(PYTHON) | pip package with Sage install wrapper |
| `pyx` | - | unknown | not packaged | pip, distros | - | pip-style package metadata |
| `qdldl_python` | 0.1.9.post1 | unknown | not packaged | pip, native, distros | pybind11 numpy scipy \| $(PYTHON_TOOLCHAIN) cmake $(PYTHON) | pip package with Sage install wrapper |
| `rst2ipynb` | 0.2.3 | unknown | not packaged | pip, native, distros | pandoc pandocfilters \| $(PYTHON_TOOLCHAIN) notedown $(PYTHON) | pip package with Sage install wrapper |
| `sage_flatsurf` | - | unknown | not packaged | pip | \| $(PYTHON_TOOLCHAIN) surface_dynamics $(SAGERUNTIME) $(PYTHON) | pip-style package metadata |
| `scs` | 3.2.11 | unknown | not packaged | pip, native, distros | numpy scipy \| $(PYTHON_TOOLCHAIN) cmake $(PYTHON) | pip package with Sage install wrapper |
| `singular_jupyter` | 0.9.7 | unknown | not packaged | pip, native, distros | jupyter_client \| $(PYTHON_TOOLCHAIN) pysingular ipython ipywidgets $(PYTHON) | pip package with Sage install wrapper |
| `slabbe` | - | unknown | not packaged | pip, distros | \| $(PYTHON_TOOLCHAIN) $(SAGERUNTIME) $(PYTHON) | pip-style package metadata |
| `snappy` | - | unknown | not packaged | pip | decorator ipython cypari \| $(PYTHON_TOOLCHAIN) sagelib $(PYTHON) | pip-style package metadata |
| `sqlalchemy` | - | unknown | not packaged | pip, distros | - | pip-style package metadata |
| `surface_dynamics` | - | unknown | not packaged | pip, distros | cysignals pplpy $(SAGE_SRC)/sage/rings/integer.pxd $(SAGE_SRC)/sage/ext/stdsage.pxd \| $(PYTHON_TOOLCHAIN) $(SAGERUNTIME) $(PYTHON) | pip-style package metadata |
| `texttable` | 1.7.0 | unknown | not packaged | pip, native, distros | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | pip package with Sage install wrapper |

## Second-Batch Candidates

| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |
|---|---:|---|---|---|---|---|
| `cbc` | 2.9.4.p0 | Eclipse Public License, Version 1.0 (EPL-1.0) | not packaged | native, distros | readline $(BLAS) | native source package with distro package names |
| `e_antic` | 2.1.0 | unknown | not packaged | native, distros | $(MP_LIBRARY) flint | native source package with distro package names |
| `free_fonts` | - | unknown | not packaged | distros | - | metadata needs manual review |
| `gp2c` | 0.0.14 | unknown | not packaged | native, distros | pari | native source package with distro package names |
| `isl` | 0.20 | isl is released under the MIT license, but depends on the LGPL GMP | not packaged | native, distros | $(MP_LIBRARY) | native source package with distro package names |
| `joblib` | 1.5.3 | unknown | not packaged | - | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | metadata needs manual review |
| `libgraphviz` | - | unknown | not packaged | distros | - | metadata needs manual review |
| `libjpeg` | - | unknown | not packaged | distros | - | metadata needs manual review |
| `libnauty` | - | unknown | not packaged | native, distros | $(SAGE_LOCAL)/$(SPKG_INST_RELDIR)/nauty-$(vers_nauty) | native source package with distro package names |
| `libogg` | 1.3.1.p0 | unknown | not packaged | native, distros | # no dependencies | native source package with distro package names |
| `libsemigroups` | 3.5.1 | unknown | not packaged | native, distros | # no dependencies | native source package with distro package names |
| `libxml2` | - | unknown | not packaged | distros | iconv | metadata needs manual review |
| `lidia` | 2.3.0+latte-patches-2019-05-02 | lidia is released under the GPL, or so it is claimed. See https://groups.google.com/forum/#!msg/sage-devel/kTxgPSqrbUM/5Txj3_IKhlQJ | not packaged | native, distros | $(MP_LIBRARY) | native source package with distro package names |
| `mcqd` | 1.0.p0 | unknown | not packaged | native, distros | - | native source package with distro package names |
| `mpfrcx` | 0.6.3 | MPFRCX is distributed under the Gnu Lesser General Public License, either version 2.1 of the licence, or (at your option) any later version | not packaged | native, distros | $(MP_LIBRARY) mpfr mpc | native source package with distro package names |
| `normaliz` | 3.11.1 | unknown | not packaged | native, distros | $(MP_LIBRARY) flint e_antic libnauty | native source package with distro package names |
| `onetbb` | 2021.12.0 | unknown | not packaged | native, distros | \| cmake | native source package with distro package names |
| `perl_cpan_polymake_prereq` | - | Various free software licenses | not packaged | distros | - | metadata needs manual review |
| `perl_mongodb` | - | Various free software licenses | not packaged | distros | - | metadata needs manual review |
| `polymake` | 4.14 | unknown | not packaged | native, distros | $(MP_LIBRARY) bliss cddlib normaliz perl_term_readline_gnu ppl libxml2 perl_cpan_polymake_prereq lrslib \| ninja_build | native source package with distro package names |
| `rpy2_robjects` | 3.6.5 | unknown | not packaged | - | rpy2_rinterface jinja2 tzlocal \| $(PYTHON_TOOLCHAIN) $(PYTHON) | metadata needs manual review |
| `saclib` | 2.2.8 | unknown | not packaged | native, distros | # no dependencies | native source package with distro package names |
| `sbcl` | - | unknown | not packaged | distros | - | metadata needs manual review |
| `texlive` | - | Various FSF-approved free software licenses. See | not packaged | native, distros | - | native source package with distro package names |
| `texlive_luatex` | - | unknown | not packaged | distros | texlive | metadata needs manual review |
| `valgrind` | - | Valgrind is Open Source / Free Software, and is freely available under | not packaged | distros | - | metadata needs manual review |
| `xindy` | - | unknown | not packaged | distros | - | metadata needs manual review |

## Hard Cases

| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |
|---|---:|---|---|---|---|---|
| `_bootstrap` | - | unknown | not packaged | native, distros | - | internal Sage aggregate/tooling package |
| `_develop` | - | unknown | not packaged | native, distros | _bootstrap git pytest pytest_xdist github_cli | internal Sage aggregate/tooling package |
| `_gcc10` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `_gcc11` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `_gcc12` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `_gcc8` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `_gcc9` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `_recommended` | - | unknown | not packaged | native, distros | pandoc ffmpeg imagemagick git libjpeg texlive texlive_luatex free_fonts xindy | internal Sage aggregate/tooling package |
| `_sagemath` | - | unknown | not packaged | distros | - | internal Sage aggregate/tooling package |
| `auditwheel_or_delocate` | - | unknown | not packaged | pip | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | developer/build tooling, not user-facing Sage functionality |
| `awali` | 1.0.2-190218 | unknown | not packaged | native, distros | cmake cython nbconvert ncurses \| $(PYTHON) | Sage marks this package experimental |
| `barvinok` | 0.41.7 | unknown | not packaged | native, distros | ntl isl polylib | Sage marks this package experimental |
| `bliss` | 0.77 | unknown | not packaged | native, patches, distros | \| cmake | native source package needing build work |
| `ccache` | 4.10.2 | unknown | not packaged | native, distros | cmake | developer/build tooling, not user-facing Sage functionality |
| `cocoalib` | 0.99564 | unknown | not packaged | native, patches, distros | $(MP_LIBRARY) | Sage marks this package experimental |
| `coxeter3` | 8ac9c71723c8ca57a836d6381aed125261e44e9e.p0 | unknown | not packaged | native, patches, distros | # no dependencies | native source package needing build work |
| `deformation` | 20210503 | unknown | not packaged | native, distros | $(MP_LIBRARY) mpfr flint | Sage marks this package experimental |
| `dsdp` | 5.8 | Permissive open source license | not packaged | native, patches, distros | $(BLAS) \| cmake | native source package needing build work |
| `gdb` | - | unknown | not packaged | distros | - | developer/build tooling, not user-facing Sage functionality |
| `git` | - | unknown | not packaged | distros | - | developer/build tooling, not user-facing Sage functionality |
| `github_cli` | - | unknown | not packaged | distros | - | developer/build tooling, not user-facing Sage functionality |
| `highspy` | 1.13.1 | unknown | not packaged | native | numpy \| $(PYTHON_TOOLCHAIN) scikit_build_core pybind11 cmake $(PYTHON) | native source package needing build work |
| `llvm` | - | unknown | not packaged | distros | - | developer/build tooling, not user-facing Sage functionality |
| `modular_resolution` | 1.1 | Copyright (C) 2018 Simon A. King <simon.king@uni-jena.de> Copyright (C) 2011 Simon A. King <simon.king@uni-jena.de> Copyright (C) 2009 Simon A. | not packaged | native | singular meataxe | native source package needing build work |
| `notedown` | 1.5.1 | unknown | not packaged | pip, native, patches, distros | nbformat nbconvert six pandoc_attributes \| $(PYTHON) $(PYTHON_TOOLCHAIN) | native source package needing build work |
| `p_group_cohomology` | 3.3.3.p1 | Copyright (C) 2018 Simon A. King <simon.king@uni-jena.de> Copyright (C) 2011 Simon A. King <simon.king@uni-jena.de> Copyright (C) 2009 Simon A. | not packaged | pip, native, patches, distros | cython cysignals singular meataxe modular_resolution $(SAGE_SRC)/sage/matrix/matrix_gfpn_dense.pxd $(SAGE_SRC)/sage/structure/element.pxd $(SAGE_SRC)/sage/matrix/matrix_gfpn_dense.pxd $(SAGE_SRC)/sage/matrix/matrix0.pxd $(SAGE_SRC)/sage/libs/meataxe.pxd $(SAGE_SRC)/sage/rings/morphism.pxd \| $(PYTHON_TOOLCHAIN) matplotlib gap $(SAGERUNTIME) ipywidgets $(PYTHON) | native source package needing build work |
| `papilo` | 2.2.1 | unknown | not packaged | native | $(MP_LIBRARY) onetbb $(BLAS) gfortran \| cmake | native source package needing build work |
| `perl_term_readline_gnu` | 1.35 | unknown | not packaged | native, patches, distros | readline | native source package needing build work |
| `polylib` | 5.22.5 | unknown | not packaged | native, distros | $(MP_LIBRARY) mpfr ntl | Sage marks this package experimental |
| `r_jupyter` | - | unknown | not packaged | native, distros | notebook rpy2 | Sage marks this package experimental |
| `rpy2_rinterface` | 3.6.6 | unknown | not packaged | native | cffi \| $(PYTHON_TOOLCHAIN) pycparser $(PYTHON) | native source package needing build work |
| `sagemath_categories` | 10.9.post3 | unknown | not packaged | pip, native | sagemath_objects \| $(PYTHON_TOOLCHAIN) sagemath_environment sage_setup cython pkgconfig python_build $(PYTHON) | modular Sage split package, not a Sagelite optional target |
| `sagemath_doc_html` | - | unknown | not packaged | native | sagelib sphinx sphinx_copybutton sphinx_inline_tabs pplpy_doc \| $(SAGERUNTIME) maxima networkx scipy sympy matplotlib pillow mathjax mpmath ipykernel jupyter_client conway_polynomials tachyon ipywidgets sage_docbuild elliptic_curves furo fpylll graphs typing_extensions | modular Sage split package, not a Sagelite optional target |
| `sagemath_doc_pdf` | - | unknown | not packaged | native | sagemath_doc_html texlive texlive_luatex free_fonts xindy | modular Sage split package, not a Sagelite optional target |
| `sagemath_environment` | 10.9.post3 | unknown | not packaged | pip, native | \| $(PYTHON_TOOLCHAIN) python_build $(PYTHON) | modular Sage split package, not a Sagelite optional target |
| `sagemath_giac` | 0.1.3 | unknown | not packaged | native | cysignals cython giac gmpy2 sagelib \| $(PYTHON_TOOLCHAIN) $(PYTHON) | modular Sage split package, not a Sagelite optional target |
| `sagemath_objects` | 10.9.post3 | unknown | not packaged | pip, native | FORCE  cysignals gmpy2 \| $(PYTHON_TOOLCHAIN) sagemath_environment sage_setup cython pkgconfig python_build $(PYTHON) | modular Sage split package, not a Sagelite optional target |
| `sagemath_repl` | 10.9.post3 | unknown | not packaged | pip, native | sagemath_objects sagemath_environment ipython ipywidgets \| $(PYTHON_TOOLCHAIN) python_build $(PYTHON) | modular Sage split package, not a Sagelite optional target |
| `scip` | 9.0.1 | unknown | not packaged | native, patches, distros | $(MP_LIBRARY) readline soplex papilo bliss \| cmake | native source package needing build work |
| `scip_sdp` | 4.3.0 | unknown | not packaged | native | scip dsdp \| cmake | native source package needing build work |
| `semigroups` | 5.6.0 | unknown | not packaged | native, patches, distros | gap gap_packages libsemigroups \| $(SAGERUNTIME) | native source package needing build work |
| `soplex` | 7.0.1 | unknown | not packaged | native, patches, distros | $(MP_LIBRARY) mpfr papilo \| cmake | native source package needing build work |
| `tdlib` | 0.9.3.p0 | - GNU General Public License v2 | not packaged | native, patches, distros | - | native source package needing build work |

## Excluded By Metadata Signal

| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |
|---|---:|---|---|---|---|---|
| `sage_numerical_backends_cplex` | 10.4 | unknown | not packaged | pip, native, nonfree-deps, distros | cysignals $(SAGE_SRC)/sage/numerical/backends/generic_backend.pxd $(SAGE_SRC)/sage/cpython/string.pxd $(SAGE_SRC)/sage/cpython/string_impl.h \| $(SAGERUNTIME) $(PYTHON_TOOLCHAIN) cython ipywidgets $(PYTHON) | nonfree dependency or license signal |
| `sage_numerical_backends_gurobi` | 10.4 | unknown | not packaged | pip, native, nonfree-deps, distros | cysignals $(SAGE_SRC)/sage/numerical/backends/generic_backend.pxd $(SAGE_SRC)/sage/cpython/string.pxd $(SAGE_SRC)/sage/cpython/string_impl.h \| $(SAGERUNTIME) $(PYTHON_TOOLCHAIN) cython ipywidgets $(PYTHON) | nonfree dependency or license signal |

## Already Represented

| Package | Version | License hint | Sagelite status | Signals | Sage dependencies | Notes |
|---|---:|---|---|---|---|---|
| `4ti2` | 1.6.10 | unknown | extra -> companion | native, distros | $(MP_LIBRARY) glpk | already represented in Sagelite metadata |
| `benzene` | 20130630 | Benzene is licensed under the GNU General Public License v2 or later | extra -> companion | native, distros | - | already represented in Sagelite metadata |
| `buckygen` | 1.1 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `csdp` | 6.2.p1 | unknown | extra -> companion | native, patches, distros | $(BLAS) | already represented in Sagelite metadata |
| `cunningham_tables` | 1.0 | unknown | extra -> companion | native, distros | - | already represented in Sagelite metadata |
| `cvxpy` | 1.8.2 | unknown | extra -> PyPI/system | pip, native, distros | numpy scipy glpk cvxopt osqp_python ecos_python scs clarabel highspy \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `cylp` | 0.94.0 | unknown | extra -> PyPI/system | pip, native | numpy scipy cbc \| $(PYTHON_TOOLCHAIN) cython $(PYTHON) | already represented in Sagelite metadata |
| `d3js` | 3.4.8 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_cremona_ellcurve` | 20190911 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_cubic_hecke` | 2022.4.4 | unknown | base dependency | pip, native | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `database_jones_numfield` | 4 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_knotinfo` | 2026.3.1 | unknown | base dependency | pip, native | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `database_kohel` | 20160724 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_mutation_class` | 1.0 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_odlyzko_zeta` | 20061209 | unknown | extra -> companion | native, distros | \| $(SAGERUNTIME) | already represented in Sagelite metadata |
| `database_stein_watkins` | 20110713 | Public Domain | extra -> companion | native, huge, distros | # no dependencies | already represented in Sagelite metadata |
| `database_stein_watkins_mini` | 20070827 | Public Domain | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `database_symbolic_data` | 20070206 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `dot2tex` | 2.11.3.p0 | unknown | base dependency | pip, native, patches, distros | \| $(PYTHON_TOOLCHAIN) pyparsing $(PYTHON) | already represented in Sagelite metadata |
| `ffmpeg` | - | "FFmpeg is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later. However, FFmpeg incorporates several optional parts and optimizations that are covered by the GNU General Public License (GPL) version | extra -> PyPI/system | distros | - | already represented in Sagelite metadata |
| `fricas` | 1.3.12 | unknown | extra -> companion | native, distros | ecl | already represented in Sagelite metadata |
| `frobby` | 0.9.0.p2 | unknown | extra -> companion | native, patches, distros | $(MP_LIBRARY) | already represented in Sagelite metadata |
| `gap3` | 04jul17 | Most parts of the GAP distribution, including the core part of the GAP system, are distributed under the terms of the GNU General Public License (see http://www.gnu.org/licenses/gpl.html or the file GPL in the | extra -> companion | native | # no dependencies | already represented in Sagelite metadata |
| `gap_packages` | 4.15.1 | unknown | extra -> companion | native, distros | gap planarity \| $(SAGERUNTIME) | already represented in Sagelite metadata |
| `giac` | 1.9.0.15p0 | unknown | extra -> companion | native, patches, distros | readline libpng $(MP_LIBRARY) mpfr mpfi ntl gsl pari glpk curl cliquer ecm | already represented in Sagelite metadata |
| `glucose` | 4.1 | unknown | extra -> companion | native, patches, distros | - | already represented in Sagelite metadata |
| `graphviz` | - | unknown | extra -> companion | distros | - | already represented in Sagelite metadata |
| `igraph` | 0.10.15 | unknown | base dependency | native, distros | $(MP_LIBRARY) glpk $(BLAS) \| cmake | already represented in Sagelite metadata |
| `imagemagick` | - | unknown | extra -> companion | distros | - | already represented in Sagelite metadata |
| `jmol` | 14.29.52 | unknown | extra -> companion | native, distros | - | already represented in Sagelite metadata |
| `jupyter_jsmol` | 2022.1.0 | unknown | base dependency | pip, distros | ipywidgets \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `kenzo` | 1.1.10 | unknown | extra -> companion | native, distros | ecl | already represented in Sagelite metadata |
| `khoca` | 1.4 | unknown | extra -> PyPI/system | pip, native | ipython cypari \| $(PYTHON_TOOLCHAIN) sagelib $(PYTHON) | already represented in Sagelite metadata |
| `kissat` | 3.1.0 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `latte_int` | 1.7.6 | unknown | extra -> companion | native, patches, distros | $(MP_LIBRARY) ntl 4ti2 cddlib lidia | already represented in Sagelite metadata |
| `lie` | 2.2.2 | unknown | extra -> companion | native, patches, distros | readline ncurses | already represented in Sagelite metadata |
| `lrslib` | 071b+autotools-2021-07-13 | unknown | extra -> companion | native, distros | $(MP_LIBRARY) | already represented in Sagelite metadata |
| `mathics` | - | unknown | extra -> PyPI/system | pip, distros | numpy pillow mpmath dateutil requests sympy pyyaml charset_normalizer typing_extensions \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `matroid_database` | 0.3 | unknown | base dependency | pip | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `meataxe` | 1.0.2 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `msolve` | 0.8.0 | unknown | extra -> companion | native | $(MP_LIBRARY) flint mpfr | already represented in Sagelite metadata |
| `pandoc` | - | unknown | extra -> PyPI/system | distros | - | already represented in Sagelite metadata |
| `pari_elldata` | 20161017 | unknown | extra -> companion | native, distros | pari_seadata_small | already represented in Sagelite metadata |
| `pari_galpol` | 20180625 | unknown | extra -> companion | native, distros | pari_seadata_small | already represented in Sagelite metadata |
| `pari_nftables` | 20080929 | unknown | extra -> companion | native, distros | pari_seadata_small | already represented in Sagelite metadata |
| `pari_seadata` | 20090618 | unknown | extra -> companion | native, distros | pari_seadata_small | already represented in Sagelite metadata |
| `pdf2svg` | - | unknown | extra -> companion | distros | - | already represented in Sagelite metadata |
| `phitigra` | - | unknown | base dependency | pip | ipywidgets pillow numpy \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `plantri` | 5.8 | unknown | extra -> companion | native, distros | # no dependencies | already represented in Sagelite metadata |
| `polytopes_db_4d` | 1.0 | unknown | extra -> companion | native, huge, distros | - | already represented in Sagelite metadata |
| `pycosat` | 0.6.3 | unknown | base dependency | pip, native, distros | \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `pycryptosat` | - | unknown | base dependency | pip, distros | m4ri libpng \| cmake $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `pynormaliz` | 2.24 | unknown | base dependency | pip, native, distros | normaliz \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `pyscipopt` | 6.1.0 | unknown | extra -> PyPI/system | pip, native, distros | scip numpy \| $(PYTHON_TOOLCHAIN) cython $(PYTHON) | already represented in Sagelite metadata |
| `python_igraph` | 1.0.0 | unknown | extra -> PyPI/system | pip, native, distros | igraph texttable  \| $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `qepcad` | 1.74 | unknown | extra -> companion | native, patches, distros | readline saclib | already represented in Sagelite metadata |
| `r` | - | unknown | extra -> PyPI/system | distros | - | already represented in Sagelite metadata |
| `regina` | - | unknown | base dependency | pip | $(PYTHON) \| $(PYTHON_TOOLCHAIN) numpy | already represented in Sagelite metadata |
| `rubiks` | 20070912.p21 | unknown | extra -> companion | native, patches, distros | # no dependencies | already represented in Sagelite metadata |
| `sage_numerical_backends_coin` | 10.4 | unknown | extra -> PyPI/system | pip, native, distros | cbc cysignals $(SAGE_SRC)/sage/numerical/backends/generic_backend.pxd $(SAGE_SRC)/sage/cpython/string.pxd $(SAGE_SRC)/sage/cpython/string_impl.h \| $(SAGERUNTIME) $(PYTHON_TOOLCHAIN) cython ipywidgets $(PYTHON) | already represented in Sagelite metadata |
| `sirocco` | 2.1.1 | unknown | extra -> companion | native, distros | mpfr | already represented in Sagelite metadata |
| `symengine` | 0.14.0 | unknown | base dependency | native, distros | $(MP_LIBRARY) ecm flint mpc mpfr \| cmake | already represented in Sagelite metadata |
| `symengine_py` | 0.14.1 | symengine.py is MIT licensed and uses several LGPL, BSD-3 and MIT | extra -> PyPI/system | pip, native, distros | symengine  \| cmake cython $(PYTHON_TOOLCHAIN) $(PYTHON) | already represented in Sagelite metadata |
| `tides` | 2.0.p0 | unknown | extra -> companion | native, patches, distros | $(MP_LIBRARY) mpfr | already represented in Sagelite metadata |
| `topcom` | 1.1.2 | unknown | extra -> companion | native, patches, distros | cddlib | already represented in Sagelite metadata |

