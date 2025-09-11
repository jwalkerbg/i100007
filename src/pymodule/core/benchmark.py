# core/benchmark.py

import time
from pymodule.logger import get_app_logger

logger = get_app_logger(__name__)

def benchmark(n:int) -> None:
    logger.info("Benchmarks:")
    pdiff = python_benchmark(n)
    ydiff = 0
    cdiff = 0

    logger.info("Python = 100.0%")
    logger.info(f"Cython = {((ydiff / pdiff) * 100.0)}%")
    logger.info(f"C      = {((cdiff / pdiff)*100.0)}%")

def python_benchmark(n):
    start_time = time.time()
    for _ in range(n):
        python_fibonacci(300)
    end_time = time.time()
    diff = (end_time - start_time) * 1000.0
    logger.info(f"Python function executed in {diff:03.6f} milliseconds")
    return diff

def python_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
