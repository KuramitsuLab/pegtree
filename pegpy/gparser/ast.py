from collections import namedtuple
import cython

@cython.cclass
class Tree:
    tag = cython.declare(cython.p_char, visibility='public')
    inputs = cython.declare(cython.p_char, visibility='public')
    urn = cython.declare(cython.p_char, visibility='public')
    spos = cython.declare(cython.int, visibility='public')
    epos = cython.declare(cython.int, visibility='public')
    child = cython.declare(object, visibility='public')

    def __init__(self, tag: cython.p_char, inputs: cython.p_char, urn: cython.p_char, spos: cython.int, epos: cython.int, child: object):
        self.tag = tag
        self.inputs = inputs
        self.urn = urn
        self.spos = spos
        self.epos = epos
        self.child = child

    def fields(self):
        a = []
        cur = self.child
        while cur is not None:
            if cur.child is not None:
                a.append((cur.tag, cur.child))
            cur = cur.prev
        a.reverse()
        return a
    
    def __str__(self):
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def strOut(self, sb):
        sb.append("[#")
        sb.append(self.tag)
        c = len(sb)
        for tag, child in self.fields():
            sb.append(' ' if tag is '' else ' ' + tag + '=')
            child.strOut(sb)
        if c == len(sb):
            s = self.inputs[self.spos:self.epos]
            if isinstance(s, str):
                sb.append(" '")
                sb.append(s)
                sb.append("'")
            else:
                sb.append(" ")
                sb.append(str(s))
        sb.append("]")


@cython.cclass
class Link:
    label = cython.declare(cython.p_char, visibility='public')
    child = cython.declare(object, visibility='public')
    prev = cython.declare(object, visibility='public')

    def __init__(self, label: cython.p_char, child: object, prev: object):
        self.label = label
        self.child = child
        self.prev = prev

