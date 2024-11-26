#include <Python.h>

#include <pymodule.h>
#include "cmodulea.h"

// Function to print a message
static PyObject* print_hello_cmodulea(PyObject* self, PyObject* args) {

    printf("Hello to Python world from C world! I am CModule A!\n");
    hello_from_utils("cmodulea");
    Py_RETURN_NONE;
}

// The C function for benchmarking that accepts an integer and returns void
static PyObject* c_benchmark(PyObject* self, PyObject* args) {
    int input_number;

    // Parse the input argument as an integer
    if (!PyArg_ParseTuple(args, "i", &input_number)) {
        return NULL;  // Error if parsing fails
    }

    // Start the benchmark (you can use time functions to measure performance)
    clock_t start_time = clock();

    // Perform some operation with the input (for example, a simple loop)
    for (int i = 0; i < input_number; ++i) {
        // Dummy operation: just incrementing i
        int temp = i * 2;  // This is just to simulate a computation
    }

    // Stop the benchmark
    clock_t end_time = clock();
    double time_taken = (double)(end_time - start_time) / CLOCKS_PER_SEC;  // seconds

    // Print the result to the Python console (this is optional)
    printf("Benchmark with %d iterations took %f seconds\n", input_number, time_taken);

    // Return None to indicate a void return type
    Py_RETURN_NONE;
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
