from pegpy.peg import *
from pegpy.ast import *
import pegpy.gpeg.gparsefunc as gparsefunc

# ParserFunction

def gdasm_setup():
    def emit(pe): return pe.gdasm()

    Empty.gdasm = lambda self: gparsefunc.true
    Any.gdasm = lambda self: gparsefunc.mresult(gparsefunc.any)
    Char.gdasm = gparsefunc.emit_GByte
    Range.gdasm = gparsefunc.emit_GByteRange

    Seq.gdasm = lambda pe: gparsefunc.emit_GSeq(pe,emit, TreeLink)
    Ore.gdasm = lambda pe: gparsefunc.emit_GOr(pe,emit)
    Alt.gdasm = lambda pe: gparsefunc.emit_GAlt(pe,emit, TreeLink)
    Not.gdasm = lambda pe: gparsefunc.emit_GNot(pe, emit)
    And.gdasm = lambda pe: gparsefunc.emit_GAnd(pe, emit)
    Many.gdasm = lambda pe: gparsefunc.emit_GMany(pe, emit, TreeLink)
    Many1.gdasm = lambda pe: gparsefunc.emit_GMany1(pe, emit, TreeLink)

    TreeAs.gdasm = lambda pe: gparsefunc.emit_GTreeAs(pe,emit, ParseTree)
    LinkAs.gdasm = lambda pe: gparsefunc.emit_GLinkAs(pe,emit, TreeLink)
    FoldAs.gdasm = lambda pe: gparsefunc.emit_GFoldAs(pe,emit, ParseTree, TreeLink)
    Detree.gdasm = lambda pe: gparsefunc.emit_GUnit(pe,emit)

    # Ref
    Ref.gdasm = lambda pe: gparsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
    Rule.gdasm = lambda pe: gparsefunc.emit_Rule(pe, emit)

gdasm_setup()

class GDAsmContext:
    __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'result']
    def __init__(self, inputs, pos = 0):
        self.inputs = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
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

def gdasm(peg: PEG, name = None):
    if isinstance(peg, ParsingExpression):
        f = peg.gdasm()
    else:
        if name == None: name = "start"
        f = gparsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.gdasm())
    def parse(s, pos = 0):
        px = GDAsmContext(s, pos)
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