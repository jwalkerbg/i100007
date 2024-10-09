# core/core_module_b.py

from pymodule.logger.logger_module import logger, string_handler

def hello_from_core_module_b() -> int:
    logger.info(f"Hello from core_module_b")
    return 2

def goodbye_from_core_module_b() -> int:
    logger.info(f"Goodbye from core_module_b")
    return -2