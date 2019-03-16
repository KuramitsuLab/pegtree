from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "Cython Parser",
    ext_modules = cythonize('cbase.py'), # accepts a glob pattern
)
