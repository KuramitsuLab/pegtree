# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "<string.h>" nogil:
  int  memcmp   (const void *a1, const void *a2, size_t size)

# cdef char_memcmp(char* inputs, int pos, char* bs, int blen)

# cdef check_empty(GParserContext px, dict new_pos2ast)
