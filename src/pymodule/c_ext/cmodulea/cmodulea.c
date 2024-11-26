#include <Python.h>

#include <pymodule.h>
#include <time.h>
#include <stdint.h>
#include "cmodulea.h"

typedef uint32_t DWORD;
typedef int32_t LONG;
typedef int64_t LONGLONG;

typedef union _LARGE_INTEGER {
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } DUMMYSTRUCTNAME;
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } u;
  LONGLONG QuadPart;
} LARGE_INTEGER;

// Function to print a message
static PyObject* print_hello_cmodulea(PyObject* self, PyObject* args) {

    printf("Hello to Python world from C world! I am CModule A!\n");
    hello_from_utils("cmodulea");
    Py_RETURN_NONE;
}

// The C function for benchmarking that accepts an integer and returns void
static PyObject* c_benchmark(PyObject* self, PyObject* args) {
    int n;
    long long result = 0;
    
    // Parse the input argument to get the integer n
    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }

    // Query the frequency of the performance counter
    LARGE_INTEGER frequency;
    QueryPerformanceFrequency(&frequency);  // Get the frequency of the performance counter
    
    // Get the start time using QueryPerformanceCounter()
    LARGE_INTEGER start_time;
    QueryPerformanceCounter(&start_time);
    
    // Perform the sum of squares calculation in a loop
    for (int i = 0; i < n; i++) {
        result += (i * i);
    }
    
    // Get the end time using QueryPerformanceCounter()
    LARGE_INTEGER end_time;
    QueryPerformanceCounter(&end_time);
    
    // Calculate the time taken in microseconds
    double time_taken = (end_time.QuadPart - start_time.QuadPart) * 1000000.0 / frequency.QuadPart;

    // Print the time it took (in microseconds)
    printf("C function executed in %.6f microseconds\n", time_taken);
    
    // Return the result as a Python long object
    return PyLong_FromLongLong(result);
}

// Method table for the module
static PyMethodDef CModuleMethods[] = {
    {"print_hello_cmodulea", print_hello_cmodulea, METH_NOARGS, "Prints a hello message from C"},
    {"c_benchmark", c_benchmark, METH_VARARGS, "Run a benchmark with an integer input"},
    {NULL, NULL, 0, NULL}  // Sentinel value
};

// Module definition
static struct PyModuleDef cmodulemodulea = {
    PyModuleDef_HEAD_INIT,
    "cmodulea",   // Module name
    "A simple example module",  // Module docstring
    -1,          // Size of per-interpreter state of the module
    CModuleMethods  // Method table
};

// Module initialization function
PyMODINIT_FUNC PyInit_cmodulea(void) {
    return PyModule_Create(&cmodulemodulea);
}
