# core/benchmark.py

import time
from pymodule.logger import getAppLogger
from pymodule.c_ext.cmodulea.cmodulea import c_benchmark
from pymodule.cyth.worker import cython_benchmark

logger = getAppLogger(__name__)

def benchmark(n:int) -> None:
    logger.info(f"Benchmarks:")
    pdiff = python_benchmark(n)
    ydiff = cython_benchmark(n)
    cdiff = c_benchmark(n)

    print(f"Python = 100.0%")
    print(f"Cython = {((ydiff / pdiff) * 100.0)}%")
    print(f"C      = {(((cdiff) / pdiff)*100.0)}%")

def python_benchmark(n):
    start_time = time.time()
    for _ in range(n):
        python_fibonacci(300)
    end_time = time.time()
    diff = ((end_time - start_time) * 1000.0)
    print(f"Python function executed in {diff:03.6f} milliseconds")
    return diff

def python_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
