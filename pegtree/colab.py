import pegtree as pg
import pegtree.graph as graph
from IPython.core.magic import register_cell_magic


@register_cell_magic
def match(line, src):
  peg = pg.grammar(src)
  if '@@example' not in peg:
    return
  parsers = {}
  res = None
  for testcase in peg['@@example']:
    name, doc = testcase
    if not name in peg:
      continue
    if not name in parsers:
      parsers[name] = pg.generate(peg, start=name)
    res = parsers[name](doc.inputs_, doc.urn_, doc.spos_, doc.epos_)
    # print()
    print(f'matching {name}', repr(
        doc.inputs_[doc.spos_:doc.epos_]), '=>', repr(str(res)))
  return None


@register_cell_magic
def pegtree(line, src):
  peg = pg.grammar(src)
  if '@@example' not in peg:
    return
  parsers = {}
  res = None
  for testcase in peg['@@example']:
    name, doc = testcase
    if not name in peg:
      continue
    if not name in parsers:
      parsers[name] = pg.generate(peg, start=name)
    res = parsers[name](doc.inputs_, doc.urn_, doc.spos_, doc.epos_)
    # print()
    print(f'parsing {name}', repr(
        doc.inputs_[doc.spos_:doc.epos_]), '=>', repr(res))
  return graph.Viz(res) if res is not None else None
