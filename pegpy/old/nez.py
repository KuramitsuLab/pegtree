#!/usr/local/bin/python

import pegpy.parser as p

def dasm(peg, name = None, conv = None):
    if not hasattr(p.Char, 'dasm'):
        def emit(pe): return pe.dasm()

        p.Empty.dasm = lambda self: p.true
        p.Any.dasm = lambda self: p.any
        p.Char.dasm = p.emit_Byte
        p.Range.dasm = p.emit_ByteRange

        p.Seq.dasm = lambda pe: p.emit_Seq(pe, emit)
        p.Ore.dasm = lambda pe: p.emit_Or(pe, emit)
        p.Not.dasm = lambda pe: p.emit_Not(pe, emit)
        p.And.dasm = lambda pe: p.emit_And(pe, emit)
        p.Many.dasm = lambda pe: p.emit_Many(pe, emit)
        p.Many1.dasm = lambda pe: p.emit_Many1(pe, emit)

        p.TreeAs.dasm = lambda pe: p.emit_TreeAs(pe, emit, p.ParseTree)
        p.LinkAs.dasm = lambda pe: p.emit_LinkAs(pe, emit, p.TreeLink)
        p.FoldAs.dasm = lambda pe: p.emit_FoldAs(pe, emit, p.ParseTree, p.TreeLink)
        p.Detree.dasm = lambda pe: p.emit_Unit(pe, emit)

        # Ref
        p.Ref.dasm = lambda pe: p.emit_Ref(pe.peg, pe.name, "_DAsm_", emit)
        p.Rule.dasm = lambda pe: p.emit_Rule(pe, emit)
    # end of dasm

    if isinstance(peg, p.ParsingExpression):
        f = peg.dasm()
    else:
        if name == None: name = "start"
        f = p.emit_Ref(peg, name, "_DAsm_", lambda pe: pe.dasm())

    def parse(s, urn = '(unknown)', pos = 0):
        px = p.ParserContext(s, urn, pos)
        pos = px.pos
        ast0 = None
        if not f(px):
            ast0 = p.ParseTree("err", px.inputs, px.headpos, len(s), None)
        else:
            ast0 = px.ast if px.ast is not None else p.ParseTree("", px.inputs, pos, px.pos, None)
        return conv(ast0) if conv is not None else ast0

    return parse
