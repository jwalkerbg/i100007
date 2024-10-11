# utils/utilities.py

from pymodule.logger import getAppLogger

logger = getAppLogger(__name__)

def hello_from_utils() ->  None:
    logger.info(f"Hello from utils")
