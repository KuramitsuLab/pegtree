from .peg import *

# # PRange Utilities


def bitsetRange(chars, ranges):
    cs = 0
    for c in chars:
        cs |= 1 << ord(c)
    r = ranges
    while len(r) > 1:
        for c in range(ord(r[0]), ord(r[1])+1):
            cs |= 1 << c
        r = r[2:]
    return cs


def stringfyRange(bits):
    c = 0
    s = None
    p = None
    chars = []
    ranges = []
    while bits > 0:
        if bits & 1 == 1:
            if s is None:
                s = c
                p = c
            elif p + 1 == c:
                p = c
            else:
                _appendRange(s, p, chars, ranges)
                s = c
                p = c
        bits >>= 1
        c += 1
    if s is not None:
        _appendRange(s, p, chars, ranges)
    return ''.join(chars), ''.join(ranges)


def _appendRange(s, p, chars, ranges):
    if s == p:
        chars.append(chr(s))
    elif s+1 == p:
        chars.append(chr(s))
        chars.append(chr(p))
    else:
        ranges.append(chr(s))
        ranges.append(chr(p))


def uniqueRange(chars, ranges):
    bits = bitsetRange(chars, ranges)
    newchars, newranges = stringfyRange(bits)
    checkbits = bitsetRange(chars, ranges)
    assert bits == checkbits
    return newchars, newranges


#
# Inlining
#

def isCharOrRange(pe):
    return isinstance(pe, PChar) or isinstance(pe, PRange)


def inline(pe: PExpr, filter=isCharOrRange):
    start = pe
    while isinstance(pe, PRef) or isinstance(pe, PName):
        pe = pe.deref()
    if filter(pe):
        if(pe != start):
            logger.info('INLINE', start, '=>', pe)
        return pe
    return start

#
# make Minimum Rules
#


def makeMinimumRules(pe: PExpr, visited: dict, rules: list):
    if isinstance(pe, PName):
        pe.deref()
        pe = pe.e
    if isinstance(pe, PRef):
        uname = pe.uname()
        if uname not in visited:
            visited[uname] = pe
            makeMinimumRules(pe.deref(), visited, rules)
            rules.append(pe)
        return rules
    if isinstance(pe, PUnary) or isinstance(pe, PTuple):
        for e in pe:
            makeMinimumRules(e, visited, rules)
    return rules

#
# Sorting Rules
#


def sortRules(refs):
    newrefs = []
    unsolved = []
    for ref in refs:
        names = set([])
        _makeSortingRefs(ref.deref(), names)
        if len(names) == 0:
            newrefs.append(ref)
        else:
            unsolved.append((ref, set(names)))
    return _solveSortingRefs(newrefs, unsolved)


def _makeSortingRefs(e, names):
    if isinstance(e, PTuple):
        for e2 in e:
            _makeSortingRefs(e2, names)
    elif hasattr(e, 'e'):
        _makeSortingRefs(e.e, names)
    elif isinstance(e, PRef):
        names.add(e.uname())


def _removeSolvedName(unsolved, uname):
    removed = False
    for _, names in unsolved:
        if uname in names:
            removed = True
            names.remove(uname)
    return removed


def _solveSortingRefs(refs, unsolved):
    removed = False
    # print(refs)
    for ref in refs:
        removed |= _removeSolvedName(unsolved, ref.uname())
    max = 0
    while max < 10:
        removed = True
        while removed:
            removed = False
            newrefs = []
            stillUnsolved = []
            for ref, names in unsolved:
                if len(names) <= max:
                    refs.append(ref)
                    newrefs.append(ref)
                else:
                    stillUnsolved.append((ref, names))
            unsolved = stillUnsolved
            #print(max, newrefs)
            for ref in newrefs:
                removed |= _removeSolvedName(unsolved, ref.uname())
            if removed:
                max = 0
        max += 1
    for ref, _ in unsolved:
        refs.append(ref)
    return refs

###


def flattenSeq(pe: PExpr, ps: list, conv=lambda x: x):
    if isinstance(pe, PSeq):
        for e in pe:
            ps.append(conv(e))
    else:
        ps.append(conv(pe))
    return ps


def appendSeq(ps: list, pe: PExpr):
    if pe == EMPTY or (isinstance(pe, PChar) and len(pe.text) == 0):
        return
    if isinstance(pe, PSeq):
        for e in pe:
            appendSeq(ps, e)
        return
    if len(ps) == 0:
        ps.append(pe)
        return
    e0 = ps[-1]
    if isinstance(pe, PChar) and isinstance(e0, PChar):
        ps[-1] = PChar(e0.text+pe.text)
        return
    ps.append(pe)


def newSeq(ps: list):
    optimized = []
    for e in ps:
        appendSeq(optimized, e)
    if len(optimized) == 0:
        return EMPTY
    if len(optimized) == 1:
        return optimized[0]
    return PSeq(*optimized)

#
# Ore
#


def flattenOre(pe: PExpr, ps: list, conv=lambda x: x):
    if isinstance(pe, POre):
        for e in pe:
            ps.append(conv(e))
    else:
        ps.append(conv(pe))
    return ps


def mergeRange(e, e2):
    if isAny(e) or isAny(e2):
        return ANY
    chars = ''
    ranges = ''
    if isinstance(e, PChar):
        chars += e.text
    if isinstance(e2, PChar):
        chars += e2.text
    if isinstance(e, PRange):
        chars += e.chars
        ranges += e.ranges
    if isinstance(e2, PRange):
        chars += e2.chars
        ranges += e2.ranges
    chars, ranges = uniqueRange(chars, ranges)
    return PRange.new(chars, ranges)


def prefixChar(pe):
    if isinstance(pe, PChar) and len(pe.text) > 0:
        return pe.text[0]
    if isinstance(pe, PSeq) and isinstance(pe.es[0], PChar) and len(pe.es[0].text) > 0:
        return pe.es[0].text[0]
    return None


def dc(pe):
    if isinstance(pe, PChar) and len(pe.text) > 0:
        return PChar.new(pe.text[1:])
    if isinstance(pe, PSeq) and isinstance(pe.es[0], PChar) and len(pe.es[0].text) > 0:
        first = PChar.new(pe.es[0].text[1:])
        return PSeq(first, *pe.es[1:])
    return FAIL


def appendOre(ps: list, pe, cmap=None, deref=False):
    start = pe
    while deref and (isinstance(pe, PRef) or isinstance(pe, PName)):
        pe = pe.deref()
    if isinstance(pe, POre):
        for e in pe:
            appendOre(ps, e, cmap, deref)
        return
    if len(ps) > 0:
        e0 = ps[-1]
        if isEmpty(e0):
            return
        if isSingleCharacter(e0) and isSingleCharacter(pe):
            ps[-1] = mergeRange(e0, pe)
            return
    c = prefixChar(pe)
    if c is not None and cmap != None:
        if c not in cmap:
            cmap[c] = len(ps)
            ps.append([pe])
        else:
            nested_choice = ps[cmap[c]]
            nested_choice.append(pe)
        return
    ps.append(start)


def newOre(ps: list, cmap=None, deref=False):
    optimized = []
    for e in ps:
        appendOre(optimized, e, cmap, deref)
    for i in range(len(optimized)):
        if not isinstance(optimized[i], list):
            continue
        nested_choice = optimized[i]
        if len(nested_choice) == 1:
            optimized[i] = nested_choice[0]
        else:
            first = PChar(prefixChar(nested_choice[0]))
            nested = []
            for ne in nested_choice:
                ne = dc(ne)
                appendOre(nested, ne)
            optimized[i] = PSeq.new(first, newOre(nested, {}))
    ps = optimized
    optimized = []
    for e in ps:
        appendOre(optimized, e, None, False)
    if len(optimized) == 0:
        return FAIL
    if len(optimized) == 1:
        return optimized[0]
    if len(optimized) == 2 and isEmpty(optimized[1]):
        return POption(optimized[0])
    return POre(*optimized)

#
# Out of order execution
#


def fixedSize(e: PExpr):
    if isinstance(e, PRange) or isinstance(e, PAny):
        return 1
    if isinstance(e, PChar):
        return len(e.text)
    if isinstance(e, PAnd) or isinstance(e, PNot):
        return 0
    return -1


def splitFixed(e, conv=lambda x: x):
    ps = flattenSeq(e, [], conv)
    if fixedSize(ps[0]) == -1:
        return None, -1, e
    shift = 0
    fixed = []
    for e in ps:
        size = fixedSize(e)
        if size == -1:
            break
        shift += size
        fixed.append(e)
    #print('@', fixed, shift, ps[len(fixed):])
    return fixed, shift, ps[len(fixed):]

###


class Optimizer(object):

    def visit(self, pe: PExpr):
        pe = inline(pe)
        cname = pe.cname()
        if not hasattr(self, cname):
            return pe
        f = getattr(self, cname)
        optimized = f(pe)
        return optimized

    def PRef(self, pe):
        return pe

    def PName(self, pe):
        return PName(self.visit(pe.e), pe.name, pe.tree, pe.isLeftRec)

    def PAnd(self, pe):
        return PAnd(self.visit(pe.e))

    def PNot(self, pe):
        return PNot(self.visit(pe.e))

    def PMany(self, pe):
        return PMany(self.visit(pe.e))

    def POneMany(self, pe):
        return POneMany(self.visit(pe.e))

    def POption(self, pe):
        return POption(self.visit(pe.e))

    def PSeq(self, pe):
        ps = flattenSeq(pe, [], lambda e: self.visit(e))
        return newSeq(ps)

    # Ore
    def POre(self, pe: POre):
        if pe.isDict() and len(pe.es) > 8:
            return pe
        ps = flattenOre(pe, [], lambda e: self.visit(e))
        return newOre(ps, {})

    # Tree Construction

    def PNode(self, pe: PNode):
        e = self.visit(pe.e)
        fixed, shift, ves = splitFixed(e)
        if fixed is None:  # or not self.Ooox:
            return PNode(e, pe.tag, pe.shift)
        fixed.append(PNode(newSeq(ves), pe.tag, pe.shift - shift))
        return newSeq(fixed)

    def PEdge(self, pe):
        e = self.visit(pe.e)
        fixed, shift, ves = splitFixed(e)
        if fixed is None:
            return PEdge(pe.edge, e, pe.shift)
        fixed.append(PEdge(pe.edge, newSeq(ves), pe.shift - shift))
        return newSeq(fixed)

    def PFold(self, pe):
        e = self.visit(pe.e)
        fixed, shift, ves = splitFixed(e)
        if fixed is None:  # or not self.Ooox:
            return PFold(pe.edge, e, pe.tag, pe.shift)
        fixed.append(PFold(pe.edge, newSeq(ves), pe.tag, pe.shift - shift))
        return newSeq(fixed)

    def PAbs(self, pe):
        return PAbs(self.visit(pe.e))

    def PAction(self, pe):
        return PAction(self.visit(pe.e), pe.func, pe.params, pe.ptree)


optimizer = Optimizer()


def default_optimizer(e):
    return optimizer.visit(e)


# def default_optimizer(e):
#   return e

def optimize(e):
    return optimizer.visit(e)


def prepare(peg: Grammar, start_name=None, optimize_function=default_optimizer):
    #peg = peg
    if start_name is None:
        start_name = peg.start()
    start_ref = peg.newRef(start_name)
    refs = makeMinimumRules(start_ref, {}, [])
    refs = sortRules(refs)
    rules = {}
    memos = []
    for ref in refs:
        uname = ref.uname(peg)
        rules[uname] = optimize_function(ref.deref())
        memos.append(uname)
        # if str(rules[uname]) != str(ref.deref()):
        #   print('OPTIMIZE', ref.deref(), '\n\t=>', rules[uname])
    if 'packrat' not in peg:
        memos.clear()
    return start_ref, refs, rules, memos
