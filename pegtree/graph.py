from pegtree.pasm import ParseTree

try:
  from graphviz import Digraph
  is_graphviz_avaiable = True
except ModuleNotFoundError:
  is_graphviz_avaiable = False

class GenId(object):
  def __init__(self):
    self.c = 0

  def gen(self):
    self.c += 1
    return self.c

def draw_node(g, t, c, fontsize):
  nid = c.gen()
  nodeid = f'n{nid}'
  g.node(nodeid, label=f'#{t.getTag()}', fontsize=fontsize, fontname='Meiryo UI')
  es = []
  for i, child in enumerate(t):
    es.append((child.spos_, child, i))
  for key in t.keys():
    child = t.get(key)
    es.append((child.spos_, child, key))
  es.sort()
  if len(es) == 0:
    childid = f'c{nid}'
    g.node(childid, label=repr(t.getToken()), shape='rectangle', fontsize=fontsize, fontcolor='blue', fontname='monospace')
    g.edge(nodeid, childid, len='0.5')
  else:
    for i, e in enumerate(es):
      _, child, edge = e
      childid = draw_node(g, child, c, fontsize)
      g.edge(nodeid, childid, label=f'{edge}', len='1.0', fontsize=fontsize)
  return nodeid


def draw_graph(ptree: ParseTree, name='G', fontsize='12'):
  if is_graphviz_avaiable == False:
    print('Install graphviz FIRST')
    return
  name = 'tree'
  g = Digraph(name, format='png')
  g.attr('node', fontname='Meiryo UI')
  g.attr('edge')
  draw_node(g, ptree, GenId(), fontsize)
  return g

def repr_svg(tree):
  g = draw_graph(tree)
  g.format='svg'
  return g._repr_svg_()

if is_graphviz_avaiable:
  ParseTree._repr_svg_ = repr_svg
