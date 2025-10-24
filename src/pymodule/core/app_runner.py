# app_runner.py

import argparse

from importlib.metadata import version as pkg_version

import pymodule
from pymodule.core.config import Config
from pymodule.logger import get_app_logger
from pymodule.extensions.cmodulea.cmodulea import print_hello_cmodulea
from pymodule.extensions.cmoduleb.cmoduleb import print_hello_cmoduleb
from pymodule.extensions.hello_world import hello
from pymodule.extensions.worker import worker_func

logger = get_app_logger(__name__)

# CLI application main function with collected options & configuration
def run_app(cfg:Config) -> None:
    try:
        # Add real application code here.
        logger.info("Running run_app")
        logger.info("config = %s",str(cfg.config))
        pymodule.hello_from_core_module_a()
        pymodule.goodbye_from_core_module_a()
        pymodule.hello_from_core_module_b()
        pymodule.goodbye_from_core_module_b()
        pymodule.hello_from_utils()
        pymodule.hello_from_ina236()
        print_hello_cmodulea()
        print_hello_cmoduleb()
        print(f"{hello()}")
        worker_func()

        pymodule.core.benchmark.benchmark(500000)
    except ValueError as e:
        logger.error("Error in application run: %s",str(e))
    except Exception as e:
        logger.error("Unexpected error in application run: %s",str(e))
    finally:
        logger.info("Exiting run_app")

