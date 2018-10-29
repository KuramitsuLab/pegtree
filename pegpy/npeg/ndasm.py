from pegpy.peg import *
from pegpy.ast import *
import pegpy.gpeg.gparsefunc as gparsefunc
import pegpy.npeg.nparsefunc as nparsefunc
import pegpy.parsefunc as parsefunc

# ParserFunction


def ndasm_setup():
    def emit(pe): return pe.ndasm()

    Empty.ndasm = lambda self: gparsefunc.true
    Any.ndasm = lambda self: gparsefunc.mresult(parsefunc.any)
    Char.ndasm = gparsefunc.emit_GChar
    Range.ndasm = nparsefunc.emit_NCharRange
    NRange.ndasm = nparsefunc.emit_NCharRange

    Seq.ndasm = lambda pe: gparsefunc.emit_GSeq(pe, emit, TreeLink)
    Ore.ndasm = lambda pe: gparsefunc.emit_GOr(pe, emit)
    Alt.ndasm = lambda pe: gparsefunc.emit_GAlt(pe, emit, TreeLink)
    Not.ndasm = lambda pe: gparsefunc.emit_GNot(pe, emit)
    And.ndasm = lambda pe: gparsefunc.emit_GAnd(pe, emit)
    Many.ndasm = lambda pe: gparsefunc.emit_GMany(pe, emit, TreeLink)
    Many1.ndasm = lambda pe: gparsefunc.emit_GMany1(pe, emit, TreeLink)

    TreeAs.ndasm = lambda pe: gparsefunc.emit_GTreeAs(pe, emit, ParseTree)
    LinkAs.ndasm = lambda pe: gparsefunc.emit_GLinkAs(pe, emit, TreeLink)
    FoldAs.ndasm = lambda pe: gparsefunc.emit_GFoldAs(
        pe, emit, ParseTree, TreeLink)
    Detree.ndasm = lambda pe: gparsefunc.emit_GUnit(pe, emit)

    # Ref
    Ref.ndasm = lambda pe: gparsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
    Rule.ndasm = lambda pe: gparsefunc.emit_Rule(pe, emit)


ndasm_setup()


class NDAsmContext:
    __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'result']

    def __init__(self, inputs, pos=0):
        self.inputs = inputs
        self.length = len(self.inputs)
        self.pos = pos
        self.headpos = pos
        self.ast = None
        self.result = {}


def collect_amb(s, pos, result):
    is_first = True
    for result_pos, r in result.items():
        if r == None:
            r = ParseTree("", s, pos, result_pos, None)
        if is_first:
            prev = TreeLink("", r, None)
            is_first = False
        else:
            prev = TreeLink("", r, prev)
    return prev


def ndasm(peg: PEG, name=None):
    if isinstance(peg, ParsingExpression):
        f = peg.ndasm()
    else:
        if name == None:
            name = "start"
        f = gparsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.ndasm())

    def parse(s, pos=0):
        px = NDAsmContext(s, pos)
        if not f(px):
            return ParseTree("err", s, px.pos, len(s), None)
        if len(px.result) == 0:
            return ParseTree("", s, pos, px.pos, None)
        if len(px.result) == 1:
            (result_pos, result_ast) = list(px.result.items())[0]
            if result_ast == None:
                return ParseTree("", s, pos, result_pos, None)
            else:
                return result_ast
        return ParseTree("Ambiguity", s, pos, px.pos, collect_amb(s, pos, px.result))
    return parse
