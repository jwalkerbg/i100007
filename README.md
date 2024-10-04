# README.md

## Introduction

This project is a simple skeleton of Python importable module which has in addition CLI interface. It uses modern **pyproject.toml** and does not use **setup.py**.

## Directory structure

The directory structure is as follows (this is an example, if in a given project `utils` or `drivers` are not needed, they can be deleted):

```
src
    # projects sources, distributed in modules
    cli
        # command line entry points
        app.py
    core
        # modules that expose API interface to applications
        __init__.py
        config.py
        core_module_a.py
        core_module_b.py
    drivers
        # driver files, can be in subdirectories
        __init__.py
        ina236.py
    utils
        __init__.py
        utilities.py
tests
    # test files for modules in other :
    test_core_module_a.py
    test_core_module_b.py
# files at root level:
MANIFEST.in
pyproject.toml
# other files may present here depending on the project
```

### Why is used directory "src"? Is it possible to use real project root? What is the benefit to use "src"?

The use of a `src/` directory in Python projects is commonly adopted but not required. Both approaches—using the `src/` directory or the project root as the source code directory—are considered valid. However, the use of a `src/` directory offers several advantages that make it appealing, particularly for larger or more complex projects.

Why Is the `src/` Directory Used?

1. Prevention of **Accidental Import of Unbuilt Code**: When the project root is used as the source directory (i.e., when the packages and modules are placed at the root of the project), it can result in direct access to the source code during development by being in the current working directory. This may cause potential issues:
  * If scripts or tests are executed from the project root, Python may locate and import the code from the project directory itself instead of from the installed package. This can hide packaging issues (such as missing files in the final distribution) because the local code is being used unknowingly.
  * Confusion during testing may arise, as tests could be inadvertently run against local files rather than the installed package version.

 By placing the code within a src/ directory, Python is forced to look for installed packages rather than directly accessing the project files unless explicitly instructed. This ensures that the code is properly installed and tested in an environment that more closely resembles production.

2. Mitigation of Namespace Clashes: If common names are chosen for the project or modules, such as test.py or setup.py, conflicts may occur if everything is located in the root directory. For instance:

  * The presence of both a `tests/` directory and a `tests.py` file in the root directory could lead to confusion for both Python and external tools.
  * Project-related scripts (like `setup.py` or `manage.py`) could be accidentally imported instead of the actual source code modules.

  The `src/` directory helps to isolate the actual code from the rest of the project structure (such as tests, documentation, or build files), thereby reducing the risk of name collisions.

  3. `Improved Clarity`: A project structure that includes a dedicated `src/` directory makes the location of the actual source code more apparent. This is particularly helpful in larger projects where other directories, such as `docs/`, `tests/`, or `ci/`, may exist at the root level. The source code is better organized when separated by the `src/` directory.

## Imports

Depending on the project, one can organize exposition of packages' internals differently. In this template project, each directory under `src/` has `__init__.py` file which brings objects from python module files to a package level. This makes the usage of the packages easier - there is no need for an application programmer to know internal structure. See `src/cli/app.py` for how they are used.

## Virtual environment, installation, running

### Virtual environment

On a console terminal execute

`python -m venv venv`

This creates a virtual environment in a subdirectory `venv` of the current directory (usually the root directory of the project's repository). It is not obligatory. Virtual environment can be created in a parent directory that contains several repositories and the projects in these repositiories can share common virtual envirnoment:

`python -m venv ..\venv`

or even

`python -m venv ..\..\venv`

Before use virtual enviromments must be activated:

Windows:

`./venv/Scripts/activate`

or

`./venv/Scripts/Activate.ps1`

Linux:

`source ./venv/bin/activate`

Note that the path to `activate` in Linux is different that the path in Windows.

Note that the execution of powershell scripts must be enabled on Windows platforms. To enable this globaly execute:

1. Open powershell console as Administrator
2. To view curent execution policy execute
`Get-ExecutionPolicy`
3. To enable execution of local scripts (not coming from the Internet) execute
`Set-ExecutionPolicy RemoteSigned`
or
`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. To revert to restricted policy execute `Set-ExecutionPolicy Restricted`

### Editable installation

To install the project in editable mode run

`pip install -e .`

This command installs the project in so called editable mode. It is usefull mode when several projects are developed in the same time, par example an application that uses another library project which is under development. Any changes in the library project will be visible instantly from the other project(s) in the same virtual environment.

The procedure will install all needed external modules which are described in `dependencies` section of **pyproject.toml** file.

### Editable installation plus unit tests

`pytest` is used for unit testing. It must be installed in the virtual environment before use. This can be made by hand by

`pip install pytest`

or automaticaly by

`pip install -e .[dev]`

This command expects following code to exist in `pyproject.toml`:

```toml
# Optional dependencies section for development tools
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0"
]
```

The command installs the current package in editable mode (`-e .`) along with any optional dependencies defined under `[project.optional-dependencies]` (in this case, `dev` dependencies).

### Building package

To produce distributable package execute following command

`python -m build`

This command will produce two files in **dist** folder. It will be created if does not exist.

```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----      2.10.2024 г.     12:23           3045 pymodule-0.1.0-py3-none-any.whl
-a----      2.10.2024 г.     12:23           3832 pymodule-0.1.0.tar.gz
```

At last, **pymodule-0.1.0-py3-none-any.whl** can be installed outside the virtual environment, in other console even in other machine:

`pip install pymodule-0.1.0-py3-none-any.whl`

These packages can be also uploaded at [PyPI](https://pypi.org/) for distribution in the Milky Way Galaxy.

## Unit tests

### Configuration

Units tests are exceuted by `pytest` module which have to be installed in the virtual enviroment of the project. How this is done is given in above sections.

`pytest` automatically finds the tests. To know where to search, following must be given in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Running tests

To run the unit tests, use the following command in the project root:

```
pytest
```

This will discover and run all the test files in the `tests/` directory automatically. `pytest` looks for files starting with `test_` or ending with `_test.py`, and for functions inside those files starting with `test_`.

### Writing Unit Tests

Unit tests are written in the `tests/` directory. For example, if you have a module `src/core/core_module_a.py` that contains a function like this:

```python
# core/core_module_a.py

def hello_from_core_module_a() -> int:
    print(f"Hello from core_module_a")
    return 1
```

The corresponding unit test in `tests/test_core_module_a.py` might look like this:

```python
class TestCore_a(unittest.TestCase):
    def test_hello_from_core_module_a(self):
        self.assertEqual(core_module_a.hello_from_core_module_a(),1)
```

It is allowed test files to be organized in subdirectories of `tests/` directory which is convenient for bigger projects. The directory structure under `tests/` can mirrors that of `src/`, which can help keep tests organized and easy to navigate as the project grows.

### `__init__.py` in Test Subdirectories (Optional)

Adding an `__init__.py` file in subdirectories is optional in modern versions of Python. If it is needed to treat subdirectories as packages and import code across test files, `__init__.py` files can be included, but `pytest` will discover tests even if they are not present. No additional configuration is needed unless you want to customize the discovery behavior (e.g., you can add `pytest` options in `pyproject.toml` or a `pytest.ini` file).

### Customizing Test Discovery

For more control over test discovery (for example, if there is non-standard naming conventions or have to exclude certain directories), pytest settings in `pyproject.toml` can be customized:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```
This configures `pytest` to:

* Look for test files in the tests directory (`testpaths`).
* Recognize test files with names starting with test_ (`python_files`).
* Discover test classes and functions starting with `Test` and `test_`.

`pytest` has a lot of command-line options. For more information see the online [pytest documentation](https://docs.pytest.org/en/stable/).