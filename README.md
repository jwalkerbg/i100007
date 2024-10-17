# README.md

- [README.md](#readmemd)
  - [Introduction](#introduction)
  - [Directory structure](#directory-structure)
    - [Why is used directory "src"? Is it possible to use real project root? What is the benefit to use "src"?](#why-is-used-directory-src-is-it-possible-to-use-real-project-root-what-is-the-benefit-to-use-src)
  - [Imports](#imports)
  - [Virtual environment, installation, running](#virtual-environment-installation-running)
    - [Virtual environment](#virtual-environment)
    - [Editable installation](#editable-installation)
    - [Editable installation plus unit tests](#editable-installation-plus-unit-tests)
    - [Building package](#building-package)
  - [Configuration system.](#configuration-system)
  - [Version information](#version-information)
    - [Versions](#versions)
    - [Print version information](#print-version-information)
  - [Logger](#logger)
  - [Unit tests](#unit-tests)
    - [Configuration](#configuration)
    - [Running tests](#running-tests)
    - [Writing Unit Tests](#writing-unit-tests)
    - [`__init__.py` in Test Subdirectories (Optional)](#__init__py-in-test-subdirectories-optional)
    - [Customizing Test Discovery](#customizing-test-discovery)
    - [Running tests with test coverage](#running-tests-with-test-coverage)
  - [Start a new project from pymodule](#start-a-new-project-from-pymodule)


## Introduction

This project is a simple skeleton of Python importable module which has in addition CLI interface. It uses modern `pyproject.toml` and does not use `setup.py`.

## Directory structure

The directory structure is as follows (this is an example, if in a given project `utils` or `drivers` are not needed, they can be deleted):

```
src
    pymodule    # name of the module, will be used as a name of the directory where the module will be installed
        __init__.py
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
            ina236.py       # exaple driver module; can have separate diretories for drivers
        logger
            # application logger
            __init__.py
            logger_module.py
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

At last, `pymodule-0.1.0-py3-none-any.whl` can be installed outside the virtual environment, in other console even in other machine:

`pip install pymodule-0.1.0-py3-none-any.whl`

These packages can be also uploaded at [PyPI](https://pypi.org/) for distribution in the Milky Way Galaxy.

## Configuration system.

The coniguration system of the module is implemented in `core/config.py` and `cli/app.py`. It is organized at three levels:

* default settings, hard-coded in the source of the module
* configuration file, by default `config.toml` in current directory
* command line options

The line of priority is (lowest) `default settings` -> `configuration file` -> `command line options` (highest).

Default configuration is in `pymodule.core.config.py`. Configuration file is in `toml` format. There are lots of information about `toml` files in the Internet. Command line options are implemented in `pymodule.cli.app`.

Application configuration is implemented in `pymodule.core.config` in `class Config`.

The default configuration comes with information about `pymodule` template meta data: template name, version and description. This information can be used by application to know what template it lay on. This information should not be altered. Hoever, new configuration options can be added as needed. The configuration is presented as a `Dict` object `Config.DEFAULT_CONFIG`.

Logging configuration is in `logging`. It can be changed with other values in the configuration file or with CLI option. By now, one option is available - `--verbose`.

Application options consist of two example options - `param` and `param2` from type `int`. They are here to demonstrate the implementation. These options are in configuration options and at CLI.

For consistency, each option on command line should have a configuration option in the default confiuration and/or the conifuration file.

## Version information

### Versions

This template project offers two versions:

* version of the template
* version of the application developed based on this template

The version of the template is stored in `config.py` in `Config.DEFAULT_CONFIG'template']['template_version'] as a string. This string should be of type `major.minor.patch`.

The version of the application is in `pyproject.toml` in `[project.version]`:

```toml
[project]
name = "name_of_ the _project"
version = "major.minor.patch"
```

Usually, an appliction programmer should not change template version (and name). It may do this only when upgrades the template the appliation project lays on.

However, changing application version is up to the team that develop the project, followoing project's versioning policy.

### Print version information

The version information of the application can be seen when the option `-v` is given at the command line. This version overrides all other options except `--config`. When `-v` presents at the command line the version is printed and the application exits. There is no way the version information to be printed and then the normal program flow to begin. The format is

```application_name major.minor.patch```

There is no way to show / print template version.

## Logger

Logger module is a simple wrapper over the standard logger in `logging` module. It adds two classes

* `class CustomFormatter` that has implementation of `format` member function
* `class StringHandler` that writes log message into a string array.

`CustomFormatter.format` defines the format of the log messages. If needed it can be edited.

`StringHandler` overloads `emit` member function - it stores messages in internal array called `log_messages`. Two new member functions are added: `get_logs` to get the collected log messages and `clear_logs` to clear collected messages.

Each program module that wants to produce log messages must import logger module by

```
from pymodule.logger import getAppLogger
```

Then creating module logger is

```
logger = getAppLogger(__name__)       # Here __name__ may be changed with any hardcoded string.
```

If a module wants to store log messages to a string along to console printing it should import the functions that handle log messages in `StringHandler`:

```
from pymodule.logger import getAppLogger, enableStringHandler, disableStringHandler, getStringLogs, clearStringLogs
```

and to create logger this way

```
logger = getAppLogger(__name__,True)
```

`enableStringHandler`, `disableStringHandler` and `clearStringLogs` are obvious.

`getStringLogs` returns one big string with log messages separated by '\n'. To print them line by line following can be done

```
messages = getStringLogs().split('\n')
for msg in messages:
    print(msg)
```

## Unit tests

### Configuration

Units tests are executed by `pytest` module which have to be installed in the virtual enviroment of the project. How this is done is given in above sections.

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

The corresponding unit test in `tests/core/test_core_module_a.py` might look like this:

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

### Running tests with test coverage

To run unit tests with test coverage execute following command from the root of the project.

`pytest --cov=.`

Since MS Visual Studio Code 1.94 it is possible to run tests + coverage from left palette, from testing pane. You can run tests, debug tests and run tests with test coverage. Additional value from such running is that Test coverage pane is updated with percents of coverage of each python module + small graphics showing module state. Test explorer show all tests and makes easy to select which tests to execute. Project explorer alse have marks about percents for test coverage.

The project must be installed par example with `pip install -e .` to work with tests.

## Start a new project from pymodule

1. Rename `src/pymodule` to `src/my_application_module_name` by

    `git mv pymodule application_module_name`
1. Edit `pyproject.py`. Change `pymodule` to the real application name.
1. Edit other parts of `pyproject.py` as needed for the application.
1. Edit imports in `.py` files to use new `application_module_name`.
1. Everywhere change `pymodule` to the `application_module_name`.
1. Do not change following sections:

    * `[build-system]`
    * `[tool.setuptools]`
    * `[tool.setuptools.packages.find]`
    * `[tool.pytest.ini_options]`
