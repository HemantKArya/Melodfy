from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [Extension("*", ["*.py"])]

setup(
    ext_modules = cythonize(extensions)
)