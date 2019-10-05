class ParseTree {
  public tag: string;
  public urn: any;
  public inputs: string;
  public spos: number;
  public epos: number;
  public child: [string, ParseTree][];

  public constructor(tag: string, spos: number, epos: number, child: any) {
    this.tag = tag;
    this.urn = child;
    this.inputs = '';
    this.spos = spos;
    this.epos = epos;
    this.child = ParseTree.empties;
  }

  // def __eq__(self, tag):
  // return self.tag == tag

  // def isError(self):
  // return self.tag == 'err'

  // def subs(self):
  // if not isinstance(self.child, list):
  // stack = []
  // cur = self.child
  // while cur is not None:
  // prev, edge, child = cur
  // if child is not None:
  // stack.append((edge, child))
  // cur = prev
  // self.child = list(stack[:: -1])
  // return self.child

  // def __len__(self):
  // return len(self.subs())

  // def __contains__(self, label):
  // for edge, _ in self.subs():
  //   if label == edge: return True
  // return False

  // def __getitem__(self, label):
  // if isinstance(label, int):
  //   return self.subs()[label][1]
  // for edge, child in self.subs():
  //   if label == edge:
  //     return child
  // return None

  // def get(self, label: str, default=None, conv = lambda x: x):
  // for edge, child in self.subs():
  //   if label == edge:
  //     return conv(child)
  // return default

  // def __getattr__(self, label: str):
  // for edge, child in self.subs():
  //   if label == edge: return child
  // raise AttributeError()

  // def getString(self, label: str, default=None):
  // return self.get(label, default, str)

  // def keys(self):
  // ks = []
  // for edge, _ in self.subs():
  //   if edge != '': ks.append(edge)
  // return ks

  // def __iter__(self):
  // return map(lambda x: x[1], self.subs())

  // def __str__(self):
  // s = self.inputs[self.spos: self.epos]
  // return s.decode('utf-8') if isinstance(s, bytes) else s

  // def __repr__(self):
  // if self.isError():
  //   return self.showing('Syntax Error')
  // sb = []
  // self.strOut(sb)
  // return "".join(sb)

  public toString() {
    const sb: string[] = [];
    this.strOut(sb);
    return sb.join('');
  }

  protected strOut(sb: string[]) {
    sb.push("[#")
    sb.push(this.tag)
    for (const node of this.child) {
      sb.push(node[0] === '' ? ' ' : ` ${node[0]}=`)
      node[1].strOut(sb);
    }
    if (this.child.length == 0) {
      const s = this.inputs.substring(this.spos, this.epos);
      sb.push(" '");
      sb.push(s);
      sb.push("'");
    }
    sb.push("]")
  }

  // def pos(self):
  // return self.start()

  // def getpos4(self):
  // return ParseRange(self.urn, self.inputs, self.spos, self.epos)

  // def dump(self, indent = '', edge = '', bold = lambda x: x, println = lambda * x: print(* x)):
  // if self.child is None:
  // s = self.inputs[self.spos : self.epos]
  // println(indent + edge + bold("[#" + self.tag), repr(s) + bold("]"))
  // return
  // println(indent + edge + bold("[#" + self.tag))
  // indent2 = '  ' + indent
  // for tag, child in self.subs():
  //   if tag != '': tag = tag + '='
  // child.dump(indent2, tag, bold, println)
  // println(indent + bold("]"))

  static empties: [string, ParseTree][] = []

  protected finalize(urn: string, inputs: string) {
    if (this.urn !== null) {
      const child: [string, ParseTree][] = [];
      var entry: Merge = this.urn;
      while (entry !== null) {
        child.push([entry.edge, this.finalize(urn, inputs)])
      }
      this.child = child.reverse();
    }
    this.urn = urn;
    this.inputs = inputs;
    return this;
  }

}

class Merge {
  public prev: any;
  public edge: string;
  public child: ParseTree;

  public constructor(prev: any, edge: string, child: ParseTree) {
    this.prev = prev;
    this.edge = edge;
    this.child = child;
  }
}

class ParserContext {
  public urn: string;
  public inputs: String;
  public pos: number;
  public epos: number;
  public head_pos: number;
  public ast: any;
  public state: State | null;
  public memos: Memo[];
  public constructor(urn: string, inputs: string, pos: number, epos: number) {
    this.urn = urn;
    this.inputs = inputs;
    this.pos = pos;
    this.epos = epos;
    this.head_pos = pos;
    this.ast = null;
    this.state = null;
    this.memos = []
    for (var i = 0; i < 1789; i++) {
      this.memos.push(new Memo());
    }
  }
}

const EMPTY = (px: ParserContext) => {
  return true;
}

const pEmpty = () => {
  return EMPTY;
}

const ANY = (px: ParserContext) => {
  if (px.pos < px.epos) {
    px.pos += 1;
    return true;
  }
  return false;
}

const pAny = () => {
  return ANY;
}

const pChar = (text: string) => {
  const text_length = text.length;

  return (px: ParserContext) => {
    if (px.inputs.startsWith(text, px.pos)) {
      px.pos += text_length;
      return true;
    }
    return false;
  }
}

const find_codemax = (chars: string, ranges: [number, number][]) => {
  var code = 0;
  for (var i = 0; i < chars.length; i += 1) {
    code = Math.max(chars.charCodeAt(i), code);
  }
  for (const range of ranges) {
    code = Math.max(range[0], code);
    code = Math.max(range[1], code);
  }
  return code;
}

const set_bitmap = (bitmap: Uint8Array, c: number) => {
  const n = (c / 8) | 0;
  const mask = 1 << ((c % 8) | 0);
  //console.log(n);
  //console.log(bitmap[n])
  bitmap[n] |= mask;
  //console.log(bitmap);
}

const pRange = (chars: string, ranges: [number, number][]) => {
  const codemax = find_codemax(chars, ranges) + 1;
  const bitmap = new Uint8Array(((codemax / 8) | 0) + 1);
  bitmap[0] = 2;
  for (var i = 0; i < chars.length; i += 1) {
    set_bitmap(bitmap, chars.charCodeAt(i));
  }
  for (const range of ranges) {
    for (var c = range[0]; i <= range[1]; i += 1) {
      set_bitmap(bitmap, c);
    }
  }
  //console.log(`bitmap ${ bitmap.length } `)
  return (px: ParserContext) => {
    if (px.pos < px.epos) {
      const c = px.inputs.charCodeAt(px.pos);
      const n = (c / 8) | 0;
      const mask = 1 << ((c % 8) | 0);
      if (n < bitmap.length && (bitmap[n] & mask) === mask) {
        px.pos += 1;
        return true;
      }
    }
    return false;
  }
}

const pMany = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    var pos = px.pos;
    var ast = px.ast;
    while (match(px) && px.pos > pos) {
      pos = px.pos;
      ast = px.ast;
    }
    px.head_pos = Math.max(px.pos, px.head_pos);
    px.pos = pos;
    px.ast = ast;
    return true;
  }
}

const pMany1 = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    if (match(px)) {
      var pos = px.pos;
      var ast = px.ast;
      while (match(px) && px.pos > pos) {
        pos = px.pos;
        ast = px.ast;
      }
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      px.ast = ast;
      return true;
    }
    return false;
  }
}

const pAnd = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    if (match(px)) {
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      return true;
    }
    return false;
  }
}

const pNot = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    const ast = px.ast;
    if (match(px)) {
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      px.ast = ast;
      return false;
    }
    return true;
  }
}

const pOption = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    const ast = px.ast;
    if (!match(px)) {
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      px.ast = ast;
    }
    return true;
  }
}

const pSeq = (...matches: ((px: ParserContext) => boolean)[]) => {
  return (px: ParserContext) => {
    for (const match of matches) {
      if (!match(px)) {
        return false;
      }
    }
    return true;
  }
}

const pSeq2 = (match: (px: ParserContext) => boolean, match2: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    return match(px) && match2(px);
  }
}

const pSeq3 = (match: (px: ParserContext) => boolean, match2: (px: ParserContext) => boolean, match3: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    return match(px) && match2(px) && match3(px);
  }
}

const pOre = (...matches: ((px: ParserContext) => boolean)[]) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    const ast = px.ast;
    for (const match of matches) {
      if (match(px)) {
        return true;
      }
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      px.ast = ast;
    }
    return false;
  }
}

const pOre2 = (match: (px: ParserContext) => boolean, match2: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    const ast = px.ast;
    if (match(px)) {
      return true;
    }
    px.head_pos = Math.max(px.pos, px.head_pos);
    px.pos = pos;
    px.ast = ast;
    return match2(px);
  }
}


const pRef = (peg: any, name: string) => {
  if (peg[name]) {
    return peg[name];
  }
  return (px: ParserContext) => {
    return peg[name](px)
  }
}

class Memo {
  public key: number;
  public constructor() {
    this.key = -1;
  }
}




const pNode = (match: (px: ParserContext) => boolean, tag: string, shift: number) => {
  return (px: ParserContext) => {
    const pos = px.pos
    px.ast = null;
    if (match(px)) {
      px.ast = new ParseTree(tag, pos + shift, px.pos, px.ast);
      return true;
    }
    return false;
  }
}

//def Merge(prev, edge, child):
//return (prev, edge, child)

const pEdge = (match: (px: ParserContext) => boolean, edge: string) => {
  return (px: ParserContext) => {
    const ast = px.ast;
    if (match(px)) {
      px.ast = new Merge(ast, edge, px.ast);
      return true;
    }
    return false;
  }
}

const pFold = (edge: string, match: (px: ParserContext) => boolean, tag: string, shift: number) => {
  return (px: ParserContext) => {
    const pos = px.pos;
    px.ast = new Merge(null, edge, px.ast);
    if (match(px)) {
      px.ast = new ParseTree(tag, pos + shift, px.pos, px.ast);
      return true;
    }
    return false;
  }
}

const pAbs = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const ast = px.ast;
    if (match(px)) {
      px.ast = ast;
      return true;
    }
    return false;
  }
}

const pSkipErr = () => {
  return (px: ParserContext) => {
    px.pos = Math.min(px.head_pos, px.epos);
    return true;
  }
}

class State {
  public sid: number;
  public value: any;
  public prev: State | null;
  public constructor(sid: number, value: any, prev: State | null) {
    this.sid = sid;
    this.value = value;
    this.prev = prev;
  }
}

const getstate = (state: State | null, sid: number) => {
  while (state !== null) {
    if (state.sid === sid) {
      return state;
    }
    state = state.prev;
  }
  return null;
}

const pSymbol = (sid: number, match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const pos = px.pos
    if (match(px)) {
      px.state = new State(sid, px.inputs.substring(pos, px.pos), px.state)
      return true;
    }
    return false;
  }
}

const pExists = (sid: number) => {
  return (px: ParserContext) => {
    return getstate(px.state, sid) !== null;
  }
}

const pMatch = (sid: number) => {
  return (px: ParserContext) => {
    const state = getstate(px.state, sid);
    if (state !== null) {
      if (px.inputs.startsWith(state.value)) {
        px.pos += (state.value as string).length;
        return true;
      }
    }
    return false;
  }
}

const pScope = (match: (px: ParserContext) => boolean) => {
  return (px: ParserContext) => {
    const state = px.state;
    const res = match(px);
    px.state = state;
    return res;
  }
}

export const generate = (start: string) => {
  const match = grammar(start);
  return (inputs: string, options?: any) => {
    const op = (options === undefined) ? {} : options;
    const pos = 0;
    const px = new ParserContext(op['urn'] || '(unknown source)', inputs, 0, inputs.length);
    if (match(px)) {
      if (px.ast === null) {
        px.ast = new ParseTree('', pos, px.pos, null);
      }
    }
    else {
      px.ast = new ParseTree('err', px.head_pos, px.head_pos + 1, null);
    }
    return px.ast.finalize(px.urn, inputs);
  }
}

const grammar = (start: string) => {
  const peg: any = {};
  //TPEG
  //peg['Name'] = pSeq(pChar('a'), pChar('b'), pRange('ABCDEFGHIJKLMNあ', []));
  return peg[start];
}

//const parser = generate('Name');
//const t = parser('abあc');
//console.log(t.toString());

