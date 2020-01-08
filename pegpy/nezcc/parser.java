import java.util.ArrayList;
import java.util.HashMap;
import java.util.function.Function;

class ParTree {
  public ParTree prev;
  public String label;
  public int spos;
  public int epos;
  public ParTree child;

  public ParTree(ParTree prev, String tag, int spos, int epos, ParTree child) {
    this.prev = prev;
    this.label = tag;
    this.spos = spos;
    this.epos = epos;
    this.child = child;
  }
}

class Memo {
  public long key;

  public Memo() {
    this.key = -1;
  }
}

class State {
  public int sid;
  public String value;
  public State prev;

  public State(int sid, String value, State prev) {
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

class ParserContext {
  public String urn;
  public String inputs;
  public int pos;
  public int epos;
  public int head_pos;
  public ParTree ast;
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
  public boolean apply(ParserContext px);
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

  private static int find_codemax(String chars, String[] ranges) {
    int code = 0;
    for (int i = 0; i < chars.length(); i += 1) {
      code = Math.max(chars.charAt(i), code);
    }
    for (String range : ranges) {
      code = Math.max(range.charAt(0), code);
      code = Math.max(range.charAt(1), code);
    }
    return code;
  }

  private static void set_bitmap(byte[] bitmap, int c) {
    int n = (c / 8) | 0;
    int mask = 1 << ((c % 8) | 0);
    // console.log(n);
    // console.log(bitmap[n])
    bitmap[n] |= mask;
    // console.log(bitmap);
  }

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
      ParTree ast = px.ast;
      while (match.apply(px) && px.pos > pos) {
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
      if (match.apply(px)) {
        int pos = px.pos;
        ParTree ast = px.ast;
        while (match.apply(px) && px.pos > pos) {
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
      if (match.apply(px)) {
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
      ParTree ast = px.ast;
      if (match.apply(px)) {
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
      ParTree ast = px.ast;
      if (!match.apply(px)) {
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
        if (!match.apply(px)) {
          return false;
        }
      }
      return true;
    };
  }

  public static ParseFunc pSeq2(ParseFunc match, ParseFunc match2) {
    return (ParserContext px) -> {
      return match.apply(px) && match2.apply(px);
    };
  }

  public static ParseFunc pSeq3(ParseFunc match, ParseFunc match2, ParseFunc match3) {
    return (ParserContext px) -> {
      return match.apply(px) && match2.apply(px) && match3.apply(px);
    };
  }

  public static ParseFunc pOre(ParseFunc... matches) {
    return (ParserContext px) -> {
      int pos = px.pos;
      ParTree ast = px.ast;
      for (ParseFunc match : matches) {
        if (match.apply(px)) {
          return true;
        }
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        px.ast = ast;
      }
      return false;
    };
  }

  public static ParseFunc pOre2(ParseFunc match, ParseFunc match2) {
    return (ParserContext px) -> {
      int pos = px.pos;
      ParTree ast = px.ast;
      if (!match.apply(px)) {
        px.head_pos = Math.max(px.pos, px.head_pos);
        px.pos = pos;
        px.ast = ast;
        return match2.apply(px);
      }
      return true;
    };
  }

  public static ParseFunc pRef(HashMap<String, ParseFunc> peg, String name) {
    if (peg.containsKey(name)) {
      return peg.get(name);
    }
    return (ParserContext px) -> {
      return peg.get(name).apply(px);
    };
  }

  public static ParseFunc pNode(ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      int pos = px.pos;
      px.ast = null;
      if (match.apply(px)) {
        px.ast = new ParTree(null, tag, pos + shift, px.pos, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pEdge(String edge, ParseFunc match) {
    return (ParserContext px) -> {
      ParTree ast = px.ast;
      if (match.apply(px)) {
        px.ast = new ParTree(ast, edge, -1, -1, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pFold(String edge, ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      int pos = px.pos;
      px.ast = new ParTree(null, edge, -1, -1, px.ast);
      if (match.apply(px)) {
        px.ast = new ParTree(null, tag, pos + shift, px.pos, px.ast);
        return true;
      }
      return false;
    };
  }

  public static ParseFunc pAbs(String edge, ParseFunc match, String tag, int shift) {
    return (ParserContext px) -> {
      ParTree ast = px.ast;
      if (match.apply(px)) {
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
      if (match.apply(px)) {
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
      boolean res = match.apply(px);
      px.state = state;
      return res;
    };
  }

  static HashMap<String, ParseFunc> peg = null;

  static ParseFunc grammar(String start) {
    if (peg == null) {
      peg = new HashMap();
      // TPEG
    }
    return peg.get(start);
  }

  public static Function<String, ParTree> generate(String start) {
    ParseFunc match = grammar(start);
    if (match == null) {
      throw new RuntimeException("undefined " + start);
    }
    return (String inputs) -> {
      int pos = 0;
      ParserContext px = new ParserContext(null, inputs, 0, inputs.length());
      if (match.apply(px)) {
        if (px.ast == null) {
          px.ast = new ParTree(null, "", pos, px.pos, null);
        }
      } else {
        px.ast = new ParTree(null, "err", px.head_pos, px.head_pos + 1, null);
      }
      return px.ast;
    };
  }
}
