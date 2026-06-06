py.install_sources(
  '__init__.py',
  'all.py',
  'base.pyx',
  'data.h',
  'data.pxd',
  'element.py',
  'functions.h',
  'functions.pxd',
  'point_configuration.py',
  'triangulations.h',
  'triangulations.pxd',
  subdir: 'sage/geometry/triangulation',
)

extension_data_cpp = {
  'base': files('base.pyx', 'data.cc', 'functions.cc', 'triangulations.cc'),
}

foreach name, pyx : extension_data_cpp
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'sage/geometry/triangulation',
    install: true,
    override_options: ['cython_language=cpp'],
    include_directories: [],
    dependencies: [py_dep, gmp],
  )
endforeach
