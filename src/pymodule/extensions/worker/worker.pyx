# src/pymodule/cyth/worker.pyx

import time
from pymodule.logger import get_app_logger

logger = get_app_logger(__name__)

def worker_func():
    logger.info("Worker")
    for i in range(5):
        logger.info(f"i = {i}")
    logger.info("Worker finished")

def cython_benchmark(int n):
    cdef int i
    start_time = time.time()

    # Perform the sum of squares calculation in a Cythonized loop
    result = 0
    for i in range(n):
        cython_fibonacci(300)

    end_time = time.time()
    diff = ((end_time - start_time) * 1000.0)
    logger.info(f"Cython function executed in {diff:03.6f} milliseconds")
    return diff

def cython_fibonacci(int n):
    cdef int a = 0, b = 1, temp, i
    for i in range(n):
        temp = a
        a = b
        b = temp + b
    return a
