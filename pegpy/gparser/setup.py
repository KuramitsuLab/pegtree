from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("cython_gpeg", sources=["cython_gpeg.py"])

setup(
  name='cython_gpeg',
  ext_modules=cythonize([ext])
)
