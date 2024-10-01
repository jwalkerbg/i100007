# setup.py

from setuptools import setup, find_packages

setup(
    name='tbench',
    version='0.1.0',
    author='Ivan Cenov',
    author_email='ivan.cenov@rnd.bg',
    description='Testbench package (tbench), skeleton (please rename)',
    url='https://repo.pts.rnd.bg:4444/ivan.cenov/tbench.git',  # Project's GitHub or website
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'jsonschema',  # Add your dependencies here
        'paho-mqtt',
        'rfc3986',
        'PyQt5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Specify the minimum Python version
)
