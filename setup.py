from setuptools import setup
from Cython.Build import cythonize

setup(
    name="pymodule",
    ext_modules=cythonize("src/pymodule/hellocyth.pyx"),
    package_dir={"": "src"},
    packages=["pymodule"],
)
