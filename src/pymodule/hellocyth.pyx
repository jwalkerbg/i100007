def say_hello() -> int:
    print("Hello from Cython integrated with Python!")

def fibonacci(int n) -> int:
    """Compute the nth Fibonacci number."""
    cdef int a = 0
    cdef int b = 1
    cdef int i

    if n <= 0:
        return 0

    for i in range(n - 1):
        b, a = a + b, b

    return b
