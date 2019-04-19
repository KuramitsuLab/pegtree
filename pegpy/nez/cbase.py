#cython: langauge_level=3
import cython
from libc.string cimport memcmp

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")


@cython.cclass
class ParserContext:
    #__slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'state', 'dict', 'memo']
    inputs: cython.p_char
    length: cython.int
    pos: cython.int
    headpos: cython.int
    ast: object

    def __init__(self, inputs: cython.p_char, pos: cython.int, slen: cython.int):
        self.inputs = inputs
        self.pos = pos
        self.length = slen
        self.headpos = self.pos
        self.ast = None
        #self.ast = None
        # #self.state = None
        # #self.dict = {}
        # #self.memo = {}


@cython.cclass
class Tree:
    #__slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'state', 'dict', 'memo']
    tag = cython.declare(object, visibility='public')
    spos = cython.declare(cython.int, visibility='public')
    epos = cython.declare(cython.int, visibility='public')
    child = cython.declare(object, visibility='public')

    def __init__(self, tag: object, spos: cython.int, epos: cython.int, child: object):
        self.tag = tag
        self.spos = spos
        self.epos = epos
        self.child = child


@cython.cclass
class Link:
    label = cython.declare(object, visibility='public')
    child = cython.declare(object, visibility='public')
    prev = cython.declare(object, visibility='public')

    def __init__(self, label: object, child: object, prev: object):
        self.label = label
        self.child = child
        self.prev = prev

# Empty


@cython.cclass
class ParseFunc:
    def __init__(self):
        pass

    @cython.cfunc
    def p(self, px: ParserContext) -> cython.bint:
        return 1

# Char
@cython.cclass
class Char(ParseFunc):
    bs: cython.p_char
    blen: cython.int

    def __init__(self, chars: bytes, blen: int):
        self.bs = chars
        self.len = blen

    @cython.cfunc
    def p(self, px: ParserContext) -> cython.bint:
        if memcmp(px.inputs + px.pos, self.bs, self.blen) == 0:
            px.pos += self.blen
            return 1
        return 0


def gen_Char(pe, **option):
    return Char(pe.a, len(pe.a))

# Any


@cython.cclass
class Any(ParseFunc):

    def __init__(self):
        pass

    @cython.cfunc
    def p(self, px: ParserContext) -> cython.bint:
        if px.pos < px.length:
            px.pos += 1
            return 1
        return 0


def gen_Any(pe, **option):
    return Any(pe.a, len(pe.a))


@cython.cfunc
def max2(a: cython.int, b: cython.int) -> cython.bint:
    return a if a > b else b

# And


@cython.cclass
class And(ParseFunc):
    f0: ParseFunc

    def __init__(self, f0: ParseFunc):
        self.f0 = f0

    @cython.cfunc
    @cython.locals(pos=cython.int, ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        ast = px.ast
        if self.f0.p(px):
            px.headpos = max2(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return 1
        return 0


def gen_And(pe, **option):
    pf = option['emit'](pe.inner, **option)
    return And(pf)

# Not


@cython.cclass
class Not(ParseFunc):
    f0: ParseFunc

    def __init__(self, f0: ParseFunc):
        self.f0 = f0

    @cython.cfunc
    @cython.locals(pos=cython.int, ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        ast = px.ast
        if not self.f0.p(px):
            px.headpos = max2(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return 1
        return 0


def gen_Not(pe, **option):
    pf = option['emit'](pe.inner, **option)
    return Not(pf)

# Many


@cython.cclass
class Many(ParseFunc):
    f0: ParseFunc

    def __init__(self, f0: ParseFunc):
        self.f0 = f0

    @cython.cfunc
    @cython.locals(pos=cython.int, ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        ast = px.ast
        while self.f0.p(px):
            pos = px.pos
            ast = px.ast
        px.headpos = max2(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return 1


def gen_Many(pe, **option):
    pf = option['emit'](pe.inner, **option)
    return Many(pf)

# Many


@cython.cclass
class Many1(ParseFunc):
    f0: ParseFunc

    def __init__(self, f0: ParseFunc):
        self.f0 = f0

    @cython.cfunc
    @cython.locals(pos=cython.int, ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        if self.f0.p(px):
            pos = px.pos
            ast = px.ast
            while self.f0.p(px):
                pos = px.pos
                ast = px.ast
            px.headpos = max2(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return 1
        return 0


def gen_Many1(pe, **option):
    pf = option['emit'](pe.inner, **option)
    return Many1(pf)

# Seq


@cython.cclass
class Seq2(ParseFunc):
    f0: ParseFunc
    f1: ParseFunc

    def __init__(self, f0: ParseFunc, f1: ParseFunc):
        self.f0 = f0
        self.f1 = f1

    @cython.cfunc
    def p(self, px: ParserContext) -> cython.bint:
        return self.f0.p(px) and self.f1.p(px)


def gen_Seq(pe, **option):
    f0 = option['emit'](pe.left, **option)
    f1 = option['emit'](pe.right, **option)
    return Seq2(f0, f1)

# Ore


@cython.cclass
class Ore2(ParseFunc):
    f0: ParseFunc
    f1: ParseFunc

    def __init__(self, f0: ParseFunc, f1: ParseFunc):
        self.f0 = f0
        self.f1 = f1

    @cython.cfunc
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        ast = px.ast
        if self.f0.p(px):
            return 1
        px.headpos = max2(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return self.f1.p(px)


def gen_Ore(pe, **option):
    f0 = option['emit'](pe.left, **option)
    f1 = option['emit'](pe.right, **option)
    return Ore2(f0, f1)


def gen_Alt(pe, **option):
    f0 = option['emit'](pe.left, **option)
    f1 = option['emit'](pe.right, **option)
    return Ore2(f0, f1)

# Tree


@cython.cclass
class TreeAs(ParseFunc):
    f0: ParseFunc
    tag: object

    def __init__(self, f0: ParseFunc, tag: object):
        self.f0 = f0
        self.tag = tag

    @cython.cfunc
    @cython.locals(pos=cython.int)
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        px.ast = None
        if self.f0.p(px):
            px.ast = Tree(self.tag, px.source, pos, px.pos, px.ast)
            return 1
        return 0


def gen_TreeAs(pe, **option):
    tag = pe.name
    pf = option['emit'](pe.inner, **option)
    return TreeAs(pf, tag)


@cython.cclass
class LinkAs(ParseFunc):
    f0: ParseFunc
    label: object

    def __init__(self, label: object, f0: ParseFunc):
        self.f0 = f0
        self.label = label

    @cython.cfunc
    @cython.locals(ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        ast = px.ast
        if self.f0.p(px):
            px.ast = Link(self.label, px.ast, ast)
            return 1
        return 0


def gen_LinkAs(pe, **option):
    label = pe.name
    pf = option['emit'](pe.inner, **option)
    return LinkAs(label, pf)


@cython.cclass
class FoldAs(ParseFunc):
    label: object
    f0: ParseFunc
    tag: object

    def __init__(self, label: object, f0: ParseFunc, tag: object):
        self.label = label
        self.f0 = f0
        self.tag = tag

    @cython.cfunc
    @cython.locals(ast=object, pos=cython.int)
    def p(self, px: ParserContext) -> cython.bint:
        pos = px.pos
        ast = Link(self.label, px.ast, None)
        if self.f0.p(px):
            px.ast = Tree(self.tag, px.source, pos, px.pos, px.ast)
            return 1
        return 0


def gen_FoldAs(pe, **option):
    label = pe.left
    tag = pe.name
    pf = option['emit'](pe.inner, **option)
    return FoldAs(label, pf, tag)


@cython.cclass
class Detree(ParseFunc):
    f0: ParseFunc

    def __init__(self, f0: ParseFunc):
        self.f0 = f0

    @cython.cfunc
    @cython.locals(ast=object)
    def p(self, px: ParserContext) -> cython.bint:
        ast = px.ast
        if self.f0.p(px):
            px.ast = ast
            return 1
        return 0


def gen_Detree(pe, **option):
    pf = option['emit'](pe.inner, **option)
    return Detree(pf)
