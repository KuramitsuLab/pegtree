from pegpy.peg import *
from pegpy.ast import *
import pegpy.parsefunc as parsefunc

# ParserFunction

def dasm_setup():
    def emit(pe): return pe.dasm()

    Empty.dasm = lambda self: parsefunc.true
    Any.dasm = lambda self: parsefunc.any
    Char.dasm = parsefunc.emit_Byte
    Range.dasm = parsefunc.emit_ByteRange

    Seq.dasm = lambda pe: parsefunc.emit_Seq(pe,emit)
    Ore.dasm = lambda pe: parsefunc.emit_Or(pe,emit)
    Alt.dasm = lambda pe: parsefunc.emit_Or(pe, emit)
    Not.dasm = lambda pe: parsefunc.emit_Not(pe, emit)
    And.dasm = lambda pe: parsefunc.emit_And(pe, emit)
    Many.dasm = lambda pe: parsefunc.emit_Many(pe, emit)
    Many1.dasm = lambda pe: parsefunc.emit_Many1(pe, emit)

    TreeAs.dasm = lambda pe: parsefunc.emit_TreeAs(pe,emit, ParseTree)
    LinkAs.dasm = lambda pe: parsefunc.emit_LinkAs(pe,emit, TreeLink)
    FoldAs.dasm = lambda pe: parsefunc.emit_FoldAs(pe,emit, ParseTree, TreeLink)
    Detree.dasm = lambda pe: parsefunc.emit_Unit(pe,emit)

    # Ref
    Ref.dasm = lambda pe: parsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
    Rule.dasm = lambda pe: parsefunc.emit_Rule(pe, emit)

dasm_setup()

class DAsmContext:
    __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast']
    def __init__(self, inputs, pos = 0):
        self.inputs = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
        self.length = len(self.inputs)
        self.pos = pos
        self.headpos = pos
        self.ast = None

def dasm(peg: PEG, name = None):
    if isinstance(peg, ParsingExpression):
        f = peg.dasm()
    else:
        if name == None: name = "start"
        f = parsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.dasm())
    def parse(s, pos = 0):
        px = DAsmContext(s, pos)
        if not f(px):
            return ParseTree("err", s, px.pos, len(s), None)
        if px.ast == None:
            return ParseTree("", s, pos, px.pos, None)
        return px.ast
    return parse

