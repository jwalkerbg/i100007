# core/core_module_a.py

from pymodule.logger.logger_module import logger, string_handler

def hello_from_core_module_a() -> int:
    logger.info(f"Hello from core_module_a")
    return 1

def goodbye_from_core_module_a() -> int:
    logger.info(f"Goodbye from from_core_module_a")
    return -1
