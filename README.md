# README.md

## Introduction

This project is a simple skeleton of Python importable module plus CLI interface. It uses modern **pyproject.toml** and does not use **setup.py**.

## Virtual environment, installation, running

### Virtual environment

On a console terminal execute

`python -m venv venv`

This creates a virtual environment in a subdirectory **venv** of the current directory (usually the root directory of the project's repository). It is not obligatory. Virtual enevornment can be created in a parent irectory that contains several repositories and the projects in these repositiories to share common virtual envirnoment:

`python -m venv ..\venv`

or even

`python -m venv ..\..\venv`

Before use virtual enviromments must be activated:

`./venv/Scripts/activate`

or

`./venv/Scripts/Activate.ps1`

Note that the execution of powershell scripts must be enabled on Windows platforms. To enable this **globaly** execute:

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

This commands installs the project in so called editable mode. It is usefull mode when several projects are developed in the same time, par example an application that uses another library project which is under development. Any changes in the library project will be visible instantly from the other project(s) in the same virtual environment.

This procedure will install all needed external modules which are described in `dependencies` section of **pyproject.toml** file.

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