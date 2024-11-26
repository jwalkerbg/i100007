import os
import sys
import shutil
from pathlib import Path
import logging

# Check Python version at runtime
if sys.version_info >= (3, 11):
    import tomllib as toml  # Use the built-in tomllib for Python 3.11+
else:
    import tomli as toml    # Use the external tomli for Python 3.7 to 3.10

logging.basicConfig(level=logging.DEBUG)

# Uncomment if library can still function if extensions fail to compile (e.g. slower, python fallback).
# Don't allow failure if cibuildwheel is running.
# allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"
allowed_to_fail = False

def read_cython_path():
    try:
        with open("pyproject.toml", "rb") as f:
            pyproject_data = toml.load(f)
    except toml.TOMLDecodeError as e:
        return {}
    except Exception as e:
        return {}

    return pyproject_data.get("tool", {}).get("build", {}).get("config", {})

def build_cython_extensions():
    # when using setuptools, you should import setuptools before Cython,
    # otherwise, both might disagree about the class to use.
    from setuptools import Extension  # noqa: I001
    from setuptools.dist import Distribution  # noqa: I001
    import Cython.Compiler.Options  # pyright: ignore [reportMissingImports]
    from Cython.Build import build_ext, cythonize  # pyright: ignore [reportMissingImports]

    Cython.Compiler.Options.annotate = True

    config = read_cython_path()
    cython_path = config.get("cython_path", "cython")
    c_ext_path = config.get("c_ext_path", "c_ext")
    include_dirs = config.get("include_dirs", [])
    print(f"Using Cython path: {cython_path}, c_ext path: {c_ext_path}")

    if os.name == "nt":  # Windows
        extra_compile_args = [
            "/O2",
        ]
    else:  # UNIX-based systems
        extra_compile_args = [
            "-O3",
            "-Werror",
            "-Wno-unreachable-code-fallthrough",
            "-Wno-deprecated-declarations",
            "-Wno-parentheses-equality",
            "-Wno-unreachable-code",  # TODO: This should no longer be necessary with Cython>=3.0.3
        ]
    extra_compile_args.append("-UNDEBUG")  # Cython disables asserts by default.
    # Relative to project root director
    if isinstance(include_dirs, str):
        include_dirs = [dir.strip() for dir in include_dirs.split(",")]
    else:
        include_dirs = [str(Path(dir)) for dir in include_dirs]

    # Dynamically find all .pyx files in the cyth directory
    pyx_files = list(Path(cython_path).rglob("*.pyx"))
    extensions = [
        Extension(
            pyx_file.stem,  # The module name (e.g., "hello_world" from "hello_world.pyx")
            [str(pyx_file)],
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            language="c",
        )
        for pyx_file in pyx_files
    ]

    # Dynamically find all .c files in the cyth directory
    root_path = Path(c_ext_path)
    c_extensions = []
    for subdir in root_path.iterdir():
        c_files = []
        if subdir.is_dir():
            # Recursively get all .c files for the current module
            c_files = list(subdir.rglob("*.c"))
        if c_files:
            c_extensions.append(
                Extension(
                    str(subdir.name),
                    [str(c_file) for c_file in c_files],
                    include_dirs=include_dirs,
                    extra_compile_args=extra_compile_args,
                    language="c"
                )
            )

    logging.info(f"c_extensions: {c_extensions}")

    extensions.extend(c_extensions)

    # Log discovered extensions
    logging.info(f"Discovered .pyx files: {pyx_files}")
    logging.info(f"Creating Extensions: {[ext.name for ext in extensions]}")

    include_dirs = set()
    for extension in extensions:
        include_dirs.update(extension.include_dirs)
    include_dirs = list(include_dirs)

    logging.info("Cythonizing.....")
    ext_modules = cythonize(extensions, include_path=include_dirs, language_level=3, annotate=True)
    logging.info("End of Cythonizing")
    dist = Distribution({"ext_modules": ext_modules})
    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()

    for output, src_path in zip(cmd.get_outputs(),cmd.get_source_files()):
        output = Path(output)

        logging.info(f"src_path: {src_path}")
        src_path = Path(src_path).parent

        logging.info(f"Generated file: {output}")
        src_relative_path = Path(src_path) / output.name
        shutil.copyfile(output, src_relative_path)
        logging.info(f"Copied {output} to {src_relative_path}")

def build(setup_kwargs):
    try:
        build_cython_extensions()
    except Exception:
        if not allowed_to_fail:
            raise
