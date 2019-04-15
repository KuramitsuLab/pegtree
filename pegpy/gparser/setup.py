from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("cgpeg", ["cython_gpeg.py"],  libraries=["m"])]

setup(
    name='Cython GPEG Parser',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)