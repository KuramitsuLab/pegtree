export class ParseTree {
  public tag: string;
  public urn: any;
  public inputs: string;
  public spos: number;
  public epos: number;
  public nodes: [string, ParseTree][];

  public constructor(tag: string, spos: number, epos: number, child: any) {
    this.tag = tag;
    this.urn = child;
    this.inputs = '';
    this.spos = spos;
    this.epos = epos;
    this.nodes = ParseTree.empties;
  }

  static empties: [string, ParseTree][] = []

  protected setup(urn: string, inputs: string) {
    if (this.urn !== null) {
      const nodes: [string, ParseTree][] = [];
      var entry: Merge = this.urn;
      while (entry !== null) {
        nodes.push([entry.edge, entry.child.setup(urn, inputs)])
        entry = entry.prev;
      }
      this.nodes = nodes.reverse();
    }
    this.urn = urn;
    this.inputs = inputs;
    var t: any = this;
    for (var i = 0; i < this.nodes.length; i += 1) {
      t[i] = this.nodes[i][1];
      if (this.nodes[i][0] !== '') {
        t[this.nodes[i][0]] = this.nodes[i][1];
      }
    }
    return this;
  }

  public is(tag: string) {
    return this.tag === tag;
  }

  public isError() {
    return this.tag === 'err';
  }

  public subs() {
    const subs: ParseTree[] = [];
    for (var i = 0; i < this.nodes.length; i += 1) {
      subs.push(this.nodes[i][1]);
    }
    return subs;
  }

  public size() {
    return this.nodes.length;
  }

  public contains(edge: string) {
    for (var i = 0; i < this.nodes.length; i += 1) {
      if (this.nodes[i][0] === edge) return true;
    }
    return false;
  }

  public get(index: any) {
    return (this as any)[index];
  }

  public tokenize(index?: any, defstr?: string) {
    if (index === undefined) {
      return this.inputs.substring(this.spos, this.epos);
    }
    const child = (this as any)[index];
    if (child === undefined) {
      return (defstr || '');
    }
    return child.tokenize();
  }

  private pos(pos: number) {
    const s = this.inputs;
    pos = Math.min(pos, s.length);
    var row = 0;
    var col = 0;
    for (var i = 0; i <= pos; i += 1) {
      if (s.charCodeAt(i) == 10) {
        row += 1;
        col = 0;
      }
      else {
        col += 1;
      }
    }
    return [pos, row, col]
  }

  public begin() {
    return this.pos(this.spos);
  }

  public end() {
    return this.pos(this.spos);
  }

  public length() {
    return this.epos - this.spos;
  }

  public toString() {
    const sb: string[] = [];
    this.strOut(sb);
    return sb.join('');
  }

  protected strOut(sb: string[]) {
    sb.push("[#")
    sb.push(this.tag)
    for (const node of this.nodes) {
      sb.push(node[0] === '' ? ' ' : ` ${node[0]}=`)
      node[1].strOut(sb);
    }
    if (this.nodes.length == 0) {
      const s = this.inputs.substring(this.spos, this.epos);
      sb.push(" '");
      sb.push(s);
      sb.push("'");
    }
    sb.push("]")
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

const find_codemax = (chars: string, ranges: string[]) => {
  var code = 0;
  for (var i = 0; i < chars.length; i += 1) {
    code = Math.max(chars.charCodeAt(i), code);
  }
  for (const range of ranges) {
    code = Math.max(range.charCodeAt(0), code);
    code = Math.max(range.charCodeAt(1), code);
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

const pRange = (chars: string, ranges: string[]) => {
  const codemax = find_codemax(chars, ranges) + 1;
  const bitmap = new Uint8Array(((codemax / 8) | 0) + 1);
  bitmap[0] = 2;
  for (var i = 0; i < chars.length; i += 1) {
    set_bitmap(bitmap, chars.charCodeAt(i));
  }
  for (const range of ranges) {
    for (var c = range.charCodeAt(0); c <= range.charCodeAt(1); c += 1) {
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

const pEdge = (edge: string, match: (px: ParserContext) => boolean) => {
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
      if (px.inputs.startsWith(state.value, px.pos)) {
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
  if (match === undefined) {
    console.log(`undefined ${start}`)
    console.log(peg)
  }
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
    return px.ast.setup(px.urn, inputs);
  }
}

let peg: any = null;

const grammar = (start: string) => {
  if (peg === null) {
    peg = {};
    //TPEG
  }
  return peg[start];
}

const example = (start: string, sample?: string) => {
  const parser = generate(start);
  const t = parser(sample || 'abc');
  console.log(`${start} ${sample}`)
  console.log(t.toString());
}

//EXAMPLE

// pegpy nezcc -g math.tpeg parser.ts > math.ts
// npx ts-node math.ts 
