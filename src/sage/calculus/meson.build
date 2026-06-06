py.install_sources(
  '__init__.py',
  'all.py',
  'calculus.py',
  'desolvers.py',
  'expr.py',
  'functional.py',
  'functions.py',
  'integration.pyx',
  'interpolation.pxd',
  'interpolation.pyx',
  'interpolators.pyx',
  'notes.txt',
  'ode.pxd',
  'ode.pyx',
  'predefined.py',
  'riemann.pyx',
  'test_sympy.py',
  'tests.py',
  'todo.txt',
  'var.pyx',
  'wester.py',
  subdir: 'sage/calculus',
)

extension_data = {
  'integration': files('integration.pyx'),
  'interpolation': files('interpolation.pyx'),
  'interpolators': files('interpolators.pyx'),
  'ode': files('ode.pyx'),
  'riemann': files('riemann.pyx'),
  'var': files('var.pyx'),
}

foreach name, pyx : extension_data
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'sage/calculus',
    install: true,
    dependencies: [py_dep, cysignals, gmp, gsl, interpreters_dep, numpy],
  )
endforeach

subdir('transforms')
