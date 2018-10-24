from pegpy.ast import *
import pegpy.old.parsefunc as parsefunc

# ParserFunction

def dasm(peg: PEG, name = None, conv = None):
    if not hasattr(Char, 'dasm'):
        def emit(pe): return pe.dasm()

        Empty.dasm = lambda self: parsefunc.true
        Any.dasm = lambda self: parsefunc.any
        Char.dasm = parsefunc.emit_Byte
        Range.dasm = parsefunc.emit_ByteRange

        Seq.dasm = lambda pe: parsefunc.emit_Seq(pe, emit)
        Ore.dasm = lambda pe: parsefunc.emit_Or(pe, emit)
        Not.dasm = lambda pe: parsefunc.emit_Not(pe, emit)
        And.dasm = lambda pe: parsefunc.emit_And(pe, emit)
        Many.dasm = lambda pe: parsefunc.emit_Many(pe, emit)
        Many1.dasm = lambda pe: parsefunc.emit_Many1(pe, emit)

        TreeAs.dasm = lambda pe: parsefunc.emit_TreeAs(pe, emit, ParseTree)
        LinkAs.dasm = lambda pe: parsefunc.emit_LinkAs(pe, emit, TreeLink)
        FoldAs.dasm = lambda pe: parsefunc.emit_FoldAs(pe, emit, ParseTree, TreeLink)
        Detree.dasm = lambda pe: parsefunc.emit_Unit(pe, emit)

        # Ref
        Ref.dasm = lambda pe: parsefunc.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
        Rule.dasm = lambda pe: parsefunc.emit_Rule(pe, emit)
    # end of dasm

    if isinstance(peg, ParsingExpression):
        f = peg.dasm()
    else:
        if name == None: name = "start"
        f = parsefunc.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.dasm())

    class DAsmContext:
        __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast']

        def __init__(self, inputs, urn='(unknown)', pos=0):
            s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
            self.inputs, self.pos = encode_source(s, urn, pos)
            self.length = len(self.inputs)
            self.headpos = self.pos
            self.ast = None

    def parse(s, urn = '(unknown)', pos = 0):
        px = DAsmContext(s, urn, pos)
        pos = px.pos
        ast0 = None
        if not f(px):
            ast0 = ParseTree("err", px.inputs, px.headpos, len(s), None)
        else:
            ast0 = px.ast if px.ast is not None else ParseTree("", px.inputs, pos, px.pos, None)
        return conv(ast0) if conv is not None else ast0

    return parse

