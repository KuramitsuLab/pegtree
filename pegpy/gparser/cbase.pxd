# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "string.h":
    cpdef int memcmp(char *a, char *b, int size)
