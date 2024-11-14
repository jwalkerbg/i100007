from setuptools import setup, Extension

# Define the C extension module
cmodule = Extension(
    'cmodule',  # Name of the module
    sources=['src/cmodules/cmodule.c'],  # Path to C source files
)

# Set up the package
setup(
    name='cmodule',
    version='1.0',
    description='A simple C extension module',
    ext_modules=[cmodule],  # Specify the C extension module here
)
