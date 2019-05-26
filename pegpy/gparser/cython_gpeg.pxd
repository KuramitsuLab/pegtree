# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "<string.h>" nogil:
  int  memcmp   (const void *a1, const void *a2, size_t size)

# cdef char_memcmp(char* inputs, int pos, char* bs, int blen)

# cdef check_empty(GParserContext px, dict new_pos2ast)

cdef class GParserContext:
  cdef char* inputs
  cdef int length
  cdef int headpos
  cdef dict pos2ast
  cdef dict memo

cdef class Tree:
  cdef object tag
  cdef char* inputs
  cdef int spos
  cdef int epos
  cdef object child

cdef class Link:
  cdef object inner
  cdef object prev
