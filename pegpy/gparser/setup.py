from distutils.core import setup, Extension
from Cython.Build import cythonize

cython_gpeg = Extension("cython_gpeg", sources=["cython_gpeg.py"])
# gchar = Extension("gchar", sources=["GChar.pyx"])
# ast = Extension("ast", sources=["ast.py"])

setup(
  name='cython_gpeg',
  # ext_modules=cythonize([cython_gpeg, gchar, ast])
  ext_modules=cythonize([cython_gpeg])
)
