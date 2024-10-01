# setup.py

from setuptools import setup, find_packages

setup(
    name='tbench',
    version='0.0.1',
    description='Testbench package (tbench), skeleton',
    author='Ivan Cenov',
    author_email='ivan.cenov@rnd.bg',
    url='https://repo.pts.rnd.bg:4444/ivan.cenov/tbench.git',  # Project's GitHub or website
    packages=find_packages(),
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
    python_requires='>=3.6',  # Specify the minimum Python version
)
