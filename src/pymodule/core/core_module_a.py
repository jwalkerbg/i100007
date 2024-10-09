# core/core_module_a.py

from pymodule.logger import getAppLogger, getAreaLogger

logger = getAreaLogger("module_a")

def hello_from_core_module_a() -> int:
    logger.info(f"Hello from core_module_a")
    return 1

def goodbye_from_core_module_a() -> int:
    logger.info(f"Goodbye from core_module_a")
    return -1
