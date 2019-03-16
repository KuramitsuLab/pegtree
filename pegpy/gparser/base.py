#!/usr/local/bin/python

import pegpy.utils as u
from pegpy.expression import *
from pegpy.ast import *

# Empty

def gen_Empty(pe, **option):
    def empty(px): return True
    return empty

# Char

def gen_Char(pe, **option):
    chars = pe.a
    clen = len(pe.a)
    def match_char(px):
        if px.inputs.startswith(chars, px.pos):
            px.pos += clen
            return True
        return False
    return match_char

# Range

def gen_Range(pe, **option):
    offset = pe.min()
    bitset = first(pe) >> offset
    def bitmatch(px):
        if px.pos < px.length:
            shift = ord(px.inputs[px.pos]) - offset
            if shift >= 0 and (bitset & (1 << shift)) != 0:
                px.pos += 1
                return True
        return False

    return bitmatch

# Any

def gen_Any(pe, **option):
    def match_any(px):
        if px.pos < px.length:
            px.pos += 1
            return True
        return False

    return match_any

# And

def gen_And(pe, **option):
    pf = option['emit'](pe.inner, **option)
    def match_and(px):
        pos = px.pos
        if pf(px):
            # backtracking
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            return True
        return False

    return match_and

# Not

def gen_Not(pe, **option):
    pf = option['emit'](pe.inner, **option)
    def match_not(px):
        pos = px.pos
        ast = px.ast
        if not pf(px):
            # backtracking
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return True
        return False

    return match_not

# Many

def gen_Many(pe, **option):
    pf = option['emit'](pe.inner, **option)
    def match_many(px):
        pos = px.pos
        ast = px.ast
        while pf(px) and pos < px.pos:
            pos = px.pos
            ast = px.ast
        px.headpos = max(px.pos, px.headpos)
        px.pos = pos
        px.ast = ast
        return True

    return match_many

def gen_Many1(pe, **option):
    pf = option['emit'](pe.inner, **option)
    def match_many1(px):
        if pf(px):
            pos = px.pos
            ast = px.ast
            while pf(px) and pos < px.pos:
                pos = px.pos
                ast = px.ast
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return True
        return False

    return match_many1

#Seq

def gen_Seq(pe, **option):
    pf1 = option['emit'](pe.left, **option)
    pf2 = option['emit'](pe.right, **option)
    return lambda px: pf1(px) and pf2(px)

#Ore

def gen_Ore(pe, **option):
    pf1 = option['emit'](pe.left, **option)
    pf2 = option['emit'](pe.right, **option)
    def match_ore(px):
        pos = px.pos
        ast = px.ast
        if not pf1(px):
            px.headpos = max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return pf2(px)
        return True

    return match_ore

gen_Alt = gen_Ore

## Ref

class MemoEntry(object):
    __slots__ = ['key', 'matched', 'mpos', 'mtree', 'mstate']
    def __init__(self):
        self.key = -1
        self.matched = False
        self.mpos = -1
        self.mtree = None
        self.mstate = None

class MemoPoint(object):
    __slots__ = ['name', 'nid', 'nterms', 'isTree']
    def __init__(self, name, nid, nterms, isTree):
        self.name = name
        self.nid = nid
        self.nterms = nterms
        self.isTree = isTree

def memoize(mp, pf):
    msize = mp.size
    mid = mp.mp
    if mp.isTree:
        def tmemo(px):
            if mp is None:
                return pf(px)
            else:
                key = msize * px.pos + mid
                memo = px.memos[key % 127]
                if memo.key == key and px.state is memo.state:
                    px.pos = memo.pos
                    px.ast = memo.ast
                    return memo.result
                memo.result = pf(px)
                memo.key = key
                memo.pos = px.pos
                memo.ast = px.ast
                memo.state = px.state
                return memo.result
        return tmemo
    else:
        def pmemo(px):
            if mp is None:
                return pf(px)
            else:
                key = msize * px.pos + mid
                memo = px.memos[key % 127]
                if memo.key == key and px.state is memo.state:
                    px.pos = memo.pos
                    return memo.result
                memo.result = pf(px)
                memo.key = key
                memo.pos = px.pos
                memo.state = px.state
                return memo.result
        return pmemo

def gen_Ref(ref, **option):
    key = ref.uname()
    memo = option['memo']
    if not key in memo:
        memo[key] = lambda px: memo[key](px)
        memo[key] = option['emit'](ref.deref(), **option)
        #memo[key] = emit_trace(ref, emit(ref.deref()))
    return memo[key]

## Tree Construction

def gen_TreeAs(pe, **option):
    tag = pe.name
    pf = option['emit'](pe.inner, **option)
    mtree = option['tree'] if 'tree' in option else ParseTree
    def tree(px):
        pos = px.pos
        px.ast = None
        if pf(px):
            px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
            return True
        return False

    return tree

def gen_LinkAs(pe, **option):
    tag = pe.name
    pf = option['emit'](pe.inner, **option)
    mlink = option['link'] if 'link' in option else TreeLink
    def link(px):
        ast = px.ast
        if pf(px):
            px.ast = mlink(tag, px.ast, ast)
            return True
        return False

    return link

def gen_FoldAs(pe, **option):
    ltag = pe.left
    tag = pe.name
    pf = option['emit'](pe.inner, **option)
    mtree = option['tree'] if 'tree' in option else ParseTree
    mlink = option['link'] if 'link' in option else TreeLink
    def fold(px):
        pos = px.pos
        px.ast = mlink(ltag, px.ast, None)
        if pf(px):
            px.ast = mtree(tag, px.inputs, pos, px.pos, px.ast)
            return True
        return False

    return fold

def gen_Detree(pe, **option):
    pf = option['emit'](pe.inner, **option)
    def unit(px):
        ast = px.ast
        if pf(px):
            px.ast = ast
            return True
        return False

    return unit

# SymbolTable

class StateTable(object):
    __slots__ = ['nameid', 'val', 'sprev']

    def __init__(self, nameid, val, sprev):
        self.nameid = nameid
        self.val = val
        self.sprev = sprev

    def __str__(self):
        return str(self.sprev) + ' ' + str((self.nameid, self.val))

STATEIDs = {}

def state_id(name):
    if not name in STATEIDs:
        STATEIDs[name] = len(STATEIDs)
    return STATEIDs[name]

def getstate(state, nameid):
    while state is not None:
        if state.nameid == nameid: return state
        state = state.sprev
    return None

def adddict(px, s):
    if len(s) == 0: return
    key = s[0]
    if key in px.dict:
        l = px.dict[key]
        slen = len(s)
        for i in range(len(l)):
            if slen > len(l[i]):
                l.insert(i, s)
                return
        l.append(s)
    else:
        px.dict[key] = [s]

def gen_State(pe, **option):
    pf = option['emit'](pe.inner, **option)
    if pe.func == '@ref':
        if 'peg' in option and pe.name in option['peg']:
            return option['emit'](option['peg'][pe.name], **option)
        else :
            return pf

    elif pe.func == '@scope':
        def scope(px):
            state = px.state
            if pf(px):
                px.state = state
                return True
            return False
        return scope

    elif pe.func == '@newscope':
        def newscope(px):
            state = None
            if pf(px):
                px.state = state
                return True
            return False
        return newscope

    elif pe.func == '@symbol':
        nid = state_id(pe.name)
        def symbol(px):
            pos = px.pos
            if pf(px):
                px.state = StateTable(nid, px.inputs[pos:px.pos], px.state)
                return True
            return False
        return symbol

    elif pe.func == '@exists':
        nid = state_id(pe.name)
        return lambda px: getstate(px.state, nid) != None

    elif pe.func == '@match':
        nid = state_id(pe.name)
        def match(px):
            state = getstate(px.state, nid)
            if state is not None and px.inputs.startswith(state.val, px.pos):
                px.pos += len(state.val)
                return True
            return False
        return match

    elif pe.func == '@some':
        nid = state_id(pe.name)
        def match(px):
            mlen = 0
            state = getstate(px.state, nid)
            while state is not None:
                if len(state.val) > mlen and px.inputs.startswith(state.val, px.pos):
                    mlen += len(state.val)
                state = getstate(px.state, nid)
            if mlen > 0:
                px.pos += mlen
                return True
            return False
        return match

    elif pe.func == '@equals':
        nid = state_id(pe.name)
        def equals(px):
            pos = px.pos
            state = getstate(px.state, nid)
            return state is not None and pf(px) and px.inputs[pos:px:pos] == state.val
        return equals

    elif pe.func == '@contains':
        nid = state_id(pe.name)
        def contains(px):
            pos = px.pos
            state = getstate(px.state, nid)
            if state is not None and pf(px):
                val = px.inputs[pos:px:pos]
                while state is not None:
                    if state.val == val : return True
                    state = getstate(state)
            return False
        return contains

    elif pe.func == '@defdict':
        def defdict(px):
            pos = px.pos
            if pf(px):
                adddict(px, px.inputs[pos:px.pos])
                return True
            return False
        return defdict

    elif pe.func == '@dict':
        def refdict(px):
            if px.pos < px.length:
                key = px.inputs[px.pos]
                if key in px.dict:
                    for s in px.dict[key]:
                        if px.inputs.startswith(s, px.pos):
                            px.pos += len(s)
                            return True
            return False
        return refdict

    else:
        def unknown(px):
            print('unknown', pe)
            return False
        return unknown

def gen_Move(pe, **option):
    if pe.func == '@skip':
        def skip(px):
            px.pos = px.headpos
            return px.pos < px.length
        return skip
    return gen_Empty(pe, **option)

def setting(**option):
    pg = option['pg']
    method = option['method']

    setattr(Empty, method, pg.gen_Empty)
    setattr(Any, method, pg.gen_Any)
    setattr(Char, method, pg.gen_Char)
    setattr(Range, method, pg.gen_Range)

    setattr(And, method, pg.gen_And)
    setattr(Not, method, pg.gen_Not)
    setattr(Many, method, pg.gen_Many)
    setattr(Many1, method, pg.gen_Many1)

    setattr(Seq, method, pg.gen_Seq)
    setattr(Ore, method, pg.gen_Ore)
    setattr(Alt, method, pg.gen_Alt)

    setattr(TreeAs, method, pg.gen_TreeAs)
    setattr(LinkAs, method, pg.gen_LinkAs)
    setattr(FoldAs, method, pg.gen_FoldAs)
    setattr(Detree, method, pg.gen_Detree)

    # State
    setattr(State, method, pg.gen_State)
    setattr(Move, method, pg.gen_Move)

    # Ref
    setattr(Ref, method, pg.gen_Ref)


class ParserContext:
  __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'state', 'dict', 'memo']

  def __init__(self, urn, inputs, pos, slen):
      self.inputs, self.pos, self.length = u.encsrc(urn, inputs, pos, slen)
      self.headpos = self.pos
      self.ast = None
      self.state = None
      self.dict = {}
      self.memo = {}

def findpeg(p):
    if isinstance(p, Ref):
        return p.peg if not '.' in p.name else None
    if hasattr(p, 'right'):
        peg = findpeg(p.right)
        return peg if peg is not None else findpeg(p.left)
    if hasattr(p, 'inner'):
        return findpeg(p.inner)
    return None

def generate(p, **option):
    if not hasattr(Char, option['method']):
        setting(**option)

    if not isinstance(p, ParsingExpression): # Grammar
        p = Ref(p.start().name, p)

    if not 'peg' in option: option['peg'] = findpeg(p)

    pf = getattr(p, option['method'])(**option)
    conv = option['conv'] if 'conv' in option else None

    def parse(inputs, urn = '(unknown)', pos = 0, epos = None):
        if u.issrc(inputs):
            urn, inputs, spos, epos = u.decsrc(inputs)
            pos = spos + pos
        else:
            #if isByte:
            #    inputs = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
            if epos is None: epos = len(inputs)
        px = ParserContext(urn, inputs, pos, epos)
        pos = px.pos
        result = None
        if not pf(px):
            result = ParseTree("err", px.inputs, px.headpos, epos, None)
        else:
            result = px.ast if px.ast is not None else ParseTree("", px.inputs, pos, px.pos, None)
        return conv(result) if conv is not None else result
    return parse


