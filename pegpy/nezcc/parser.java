import java.util.ArrayList;
import java.util.HashMap;

class ParseTree {
  public String tag;
  public int spos;
  public int epos;
  public Object urn;
  public String inputs;
  public Edge[] nodes; // [string, ParseTree][];

  public ParseTree(String tag, int spos, int epos, Object child) {
    this.tag = tag;
    this.urn = child;
    this.inputs = "";
    this.spos = spos;
    this.epos = epos;
    this.nodes = new Edge[1];
  }

  // static empties: [string, ParseTree][] = []

  protected setup(String urn, String inputs) {
    if (this.urn != null) {
      ArrayList<Edge> nodes = new ArrayList<>();
      Edge entry = this.nodes[0];
      while (entry != null) {
        nodes.append(entry);
        entry = entry.prev;
      }
      this.nodes = nodes.toArray(this.nodes);
    }
    this.urn = urn;
    this.inputs = inputs;
    return this;
  }

  public boolean is(String tag) {
    return this.tag.equals(tag);
  }

  public boolean isError() {
    return this.is("err");
  }

  public int size() {
    return this.nodes.length;
  }

  public ParseTree[] subs() {
    ParseTree[] ts = new ParseTree[this.nodes.length];
    for (int i = 0; i < this.nodes.length; i++) {
      ts[i] = this.nodes[i].child;
    }
    return ts;
  }

  // public contains(edge: string) {
  // for (var i = 0; i < this.nodes.length; i += 1) {
  // if (this.nodes[i][0] === edge) return true;
  // }
  // return false;
  // }

  // public get(index: any) {
  // return (this as any)[index];
  // }

  // public tokenize(index?: any, defstr?: string) {
  // if (index === undefined) {
  // return this.inputs.substring(this.spos, this.epos);
  // }
  // const child = (this as any)[index];
  // if (child === undefined) {
  // return (defstr || '');
  // }
  // return child.tokenize();
  // }

  // private pos(pos: number) {
  // const s = this.inputs;
  // pos = Math.min(pos, s.length);
  // var row = 0;
  // var col = 0;
  // for (var i = 0; i <= pos; i += 1) {
  // if (s.charCodeAt(i) == 10) {
  // row += 1;
  // col = 0;
  // }
  // else {
  // col += 1;
  // }
  // }
  // return [pos, row, col]
  // }

  // public begin() {
  // return this.pos(this.spos);
  // }

  // public end() {
  // return this.pos(this.spos);
  // }

  // public length() {
  // return this.epos - this.spos;
  // }

  // public toString() {
  // const sb: string[] = [];
  // this.strOut(sb);
  // return sb.join('');
  // }

  // protected strOut(sb: string[]) {
  // sb.push("[#")
  // sb.push(this.tag)
  // for (const node of this.nodes) {
  // sb.push(node[0] === '' ? ' ' : ` ${node[0]}=`)
  // node[1].strOut(sb);
  // }
  // if (this.nodes.length == 0) {
  // const s = this.inputs.substring(this.spos, this.epos);
  // sb.push(" '");
  // sb.push(s);
  // sb.push("'");
  // }
  // sb.push("]")
  // }

}

class Edge {
  public Object prev;
  public String edge;
  public ParseTree child;

  public Edge(Object prev, String edge, ParseTree child) {
    this.prev = prev;
    this.edge = edge;
    this.child = child;
  }
}

class Memo {
  public long key;

  public Memo() {
    this.key = -1;
  }
}

class ParserContext {
  public String urn;
  public String inputs;
  public int pos;
  public int epos;
  public int head_pos;
  public Object ast;
  public State state;
  public Memo[] memos;

  public ParserContext(String urn, String inputs, int pos, int epos) {
    this.urn = urn;
    this.inputs = inputs;
    this.pos = pos;
    this.epos = epos;
    this.head_pos = pos;
    this.ast = null;
    this.state = null;
    this.memos = new Memo[1789];
    for (int i = 0; i < 1789; i++) {
      this.memos[i] = new Memo();
    }
  }
}

interface ParseFunc {
  public boolean parse(ParserContext px);
}

class Parser {

  public static ParseFunc EMPTY = (ParserContext px) -> {
    return true;
  };

  public static ParseFunc pEmpty() {
    return EMPTY;
  }

  public static ParseFunc ANY = (ParserContext px) -> {
    if (px.pos < px.epos) {
      px.pos += 1;
      return true;
    }
    return false;
  };

  public static ParseFunc pAny() {
    return ANY;
  }

  public static ParseFunc pChar(String text) {
    final int text_length = text.length();
    return (px) -> {
      if (px.inputs.startsWith(text, px.pos)) {
        px.pos += text_length;
        return true;
      }
      return false;
    };
  }

  // const find_codemax=(chars:string,ranges:string[])=>
  // {
  // var code = 0;
  // for (var i = 0; i < chars.length; i += 1) {
  // code = Math.max(chars.charCodeAt(i), code);
  // }
  // for (const range of ranges) {
  // code = Math.max(range.charCodeAt(0), code);
  // code = Math.max(range.charCodeAt(1), code);
  // }
  // return code;
  // }

  // const set_bitmap=(bitmap:Uint8Array,c:number)=>
  // {
  // const n = (c / 8) | 0;
  // const mask = 1 << ((c % 8) | 0);
  // //console.log(n);
  // //console.log(bitmap[n])
  // bitmap[n] |= mask;
  // //console.log(bitmap);
  // }

  public static ParseFunc pRange(String chars, String[] ranges) {
    int codemax = find_codemax(chars, ranges) + 1;
    byte[] bitmap = new byte[((codemax / 8) | 0) + 1];
    bitmap[0] = 2;
    for (int i = 0; i < chars.length(); i += 1) {
      set_bitmap(bitmap, chars.charAt(i));
    }
    for (String range : ranges) {
      for (int c = range.charAt(0); c <= range.charAt(1); c += 1) {
        set_bitmap(bitmap, c);
      }
    }
    return (px) -> {
      if (px.pos < px.epos) {
        int c = px.inputs.charAt(px.pos);
        int n = (c / 8) | 0;
        int mask = 1 << ((c % 8) | 0);
        if (n < bitmap.length && (bitmap[n] & mask) == mask) {
          px.pos += 1;
          return true;
        }
      }
      return false;
    };
  }

  public static ParseFunc pMany(ParseFunc match) {
    return (px) -> {
      int pos = px.pos;
      Object ast = px.ast;
      while (match(px) && px.pos > pos) {
        pos = px.pos;
        ast = px.ast;
      }
      px.head_pos = Math.max(px.pos, px.head_pos);
      px.pos = pos;
      px.ast = ast;
      return true;
    };
  }

  public static ParseFunc pMany1(ParseFunc match) {
    return (px) -> {
      if (match(px)) {
        int pos = px.pos;
        Object ast = px.ast;
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
    };
  }

  public static ParseFunc pAnd(ParseFunc match) {
    return (ParserContext px) -> {
      int pos = px.pos;
      if (match(px)) {
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pOr(ParseFunc match) {
    return (ParserContext px) -> {
      int pos = px.pos;
      Object ast = px.ast;
      if (match(px)) {
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        px.ast = ast;
        return false;
      }
      return true;
    };
  }

  public static ParseFunc pOption(ParseFunc match) {
    return (ParserContext px) -> {
      int pos = px.pos;
      Object ast = px.ast;
      if (!match(px)) {
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        px.ast = ast;
      }
      return true;
    };
  }

  public static ParseFunc pSeq(ParseFunc... matches) {
    return (ParserContext px) -> {
      for (ParseFunc match : matches) {
        if (!match(px)) {
          return false;
        }
      }
      return true;
    };
  }

  // const
  // pSeq2=(match:(px:ParserContext)=>boolean,match2:(px:ParserContext)=>boolean)=>
  // {
  // return (px: ParserContext) => {
  // return match(px) && match2(px);
  // }
  // }

  // const
  // pSeq3=(match:(px:ParserContext)=>boolean,match2:(px:ParserContext)=>boolean,match3:(px:ParserContext)=>boolean)=>
  // {
  // return (px: ParserContext) => {
  // return match(px) && match2(px) && match3(px);
  // }
  // }

  public static ParseFunc pOre(ParseFunc... matches) {
    return (ParserContext px) -> {
      int pos = px.pos;
      Object ast = px.ast;
      for (ParseFunc match : matches) {
        if (match(px)) {
          return true;
        }
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        px.ast = ast;
      }
      return false;
    };
  }

  // const
  // pOre2=(match:(px:ParserContext)=>boolean,match2:(px:ParserContext)=>boolean)=>
  // {
  // return(px:ParserContext)=>{const pos=px.pos;const
  // ast=px.ast;if(match(px)){return
  // true;}px.head_pos=Math.max(px.pos,px.head_pos);px.pos=pos;px.ast=ast;return
  // match2(px);}
  // }

  public static ParseFunc pRef(HashMap<String, ParseFunc> peg, String name) {
    if (peg.containsKey(name)) {
      return peg.get(name);
    }
    return (ParserContext px) -> {
      return peg.get(name);
    };
  }

  public static ParseFunc pNode(ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      int pos = px.pos;
      px.ast = null;
      if (match(px)) {
        px.ast = new ParseTree(tag, pos + shift, px.pos, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pEdge(String edge, ParseFunc match) {
    return (ParserContext px) -> {
      Object ast = px.ast;
      if (match(px)) {
        px.ast = new Merge(ast, edge, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pFold(String edge, ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      int pos = px.pos;
      px.ast = new Merge(null, edge, px.ast);
      if (match(px)) {
        px.ast = new ParseTree(tag, pos + shift, px.pos, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pAbs(String edge, ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      Object ast = px.ast;
      if (match(px)) {
        px.ast = ast;
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pSkipErr() {
    return (ParserContext px) -> {
      px.pos = Math.min(px.head_pos, px.epos);
      return true;
    };
  }

  public static ParseFunc pSymbol(int sid, ParseFunc match) {
    return (ParserContext px) -> {
      int pos = px.pos;
      if (match(px)) {
        px.state = new State(sid, px.inputs.substring(pos, px.pos), px.state);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pExists(int sid, ParseFunc match) {
    return (ParserContext px) -> {
      return State.get(px.state, sid) != null;
    };
  }

  public static ParseFunc pMatch(int sid, ParseFunc match) {
    return (ParserContext px) -> {
      State state = State.get(px.state, sid);
      if (state != null) {
        if (px.inputs.startsWith(state.value, px.pos)) {
          px.pos += state.value.length();
          return true;
        }
      }
      return false;
    };
  }

  public static ParseFunc pScope(ParseFunc match) {
    return (ParserContext px) -> {
      State state = px.state;
      boolean res = match(px);
      px.state = state;
      return res;
    };
  }

  static HashMap<String, ParseFunc> peg = null;

  static grammar(String start) {
    if(peg == null) {
      peg = new HashMap();
      //TPEG
    }
    return peg.get(start); 
  }

  public static Object generate(String start) {
    ParseFunc match = grammar(start);
    if (match == null) {
      throw new RuntimeException("undefined " + start);
    }
    return (String inputs) -> {
      int pos = 0;
      ParserContext px = new ParserContext(null, inputs, 0, inputs.length);
      if (match(px)) {
        if (px.ast == null) {
          px.ast = new ParseTree("", pos, px.pos, null);
        }
      } else {
        px.ast = new ParseTree("err", px.head_pos, px.head_pos + 1, null);
      }
      return px.ast.setup(px.urn, inputs);
    };
  }
}

class State {
  public int sid;
  public String value;
  public State prev;

  public State(int sid, _object value, State prev) {
    this.sid = sid;
    this.value = value;
    this.prev = prev;
  }

  public static State get(State state, int sid) {
    while (state != null) {
      if (state.sid == sid) {
        return state;
      }
      state = state.prev;
    }
    return null;
  }
}

// export const generate=(start:string)=>
// {
// const match=grammar(start);if(match===undefined){console.log(`undefined
// ${start}`)console.log(peg)}return(inputs:string,options?:any)=>{const
// op=(options===undefined)?{}:options;const pos=0;const px=new
// ParserContext(op['urn']||'(unknown
// source)',inputs,0,inputs.length);if(match(px)){if(px.ast===null){px.ast=new
// ParseTree('',pos,px.pos,null);}}else{px.ast=new
// ParseTree('err',px.head_pos,px.head_pos+1,null);}return
// px.ast.setup(px.urn,inputs);}
// }

// let peg:any=null;

// const grammar=(start:string)=>
// {
// if(peg===null){peg={};
// // TPEG
// }return peg[start];
// }

// const example=(start:string,sample?:string)=>
// {
// const parser=generate(start);const
// t=parser(sample||'abc');console.log(`${start}${sample}`)console.log(t.toString());
// }
