// Utilities from Python3 Porting
import {
    PAsm, ParseTree, PFunc, Parser,
    quote, keyRange
} from './pasm';
import { TPEG } from './tpeg';

class PExpr {
    cname() {
        return this.constructor.name;
    }
    minLen() {
        return 0;
    }
}

class PAny extends PExpr {
    public toString() {
        return '.';
    }
    minLen() {
        return 1;
    }
}

class PChar extends PExpr {
    text: string;
    constructor(text: string) {
        super();
        this.text = text
    }

    public toString() {
        return quote(this.text);
    }

    minLen() {
        return this.text.length;
    }
}

class PRange extends PExpr {
    static readonly ESCTBL: { [key: string]: string } = {
        '\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f',
        '\\': '\\\\', ']': '\\]', '-': '\\-'
    }
    chars: string;
    ranges: string;
    constructor(chars: string, ranges: string) {
        super();
        this.chars = chars;
        this.ranges = ranges;
    }

    public toString() {
        return keyRange(this.chars, this.ranges);
    }

    minLen() {
        return 1;
    }
}

class PRef extends PExpr {
    peg: Grammar
    name: string
    minlen: number | null = null;
    constructor(peg: Grammar, name: string) {
        super();
        this.peg = peg
        this.name = name
    }

    public toString() {
        return this.name
    }

    uname(peg?: Grammar) {
        if (this.peg === peg) {
            return this.name;
        }
        return `${this.peg.ns}${this.name}`
    }

    deref() {
        return this.peg.get(this.name)
    }

    minLen() {
        if (!this.minlen) {
            this.minlen = 0
            this.minlen = this.deref().minLen()
        }
        return this.minlen!
    }
}


class PTuple extends PExpr {
    es: PExpr[]
    minlen: number | null = null;
    constructor(...es: PExpr[]) {
        super();
        this.es = es
    }
}

class PSeq extends PTuple {
    static new(...es: PExpr[]) {
        const ls: PExpr[] = []
        for (const e of es) {
            if (e === EMPTY) continue;
            if (ls.length === 0) {
                ls.push(e);
                continue;
            }
            const pe = ls[ls.length - 1];
            if (e instanceof PChar && pe instanceof PChar) {
                ls[ls.length - 1] = new PChar(pe.text + e.text)
                continue
            }
            ls.push(e)
        }
        return ls.length === 1 ? ls[0] : new PSeq(...ls)
    }

    public toString() {
        return this.es.map((e) => grouping(e, (x) => x instanceof POre)).join(' ');
    }

    minLen() {
        if (!this.minlen) {
            var mlen = 0
            for (const e of this.es) {
                mlen += e.minLen();
            }
            this.minlen = mlen;
        }
        return this.minlen;
    }
}
// def splitFixed(remains):
// fixed = []
// size = 0
// f || e in remains:
// if e instanceof Char):
//     size += len(e.text)
// fixed.push(e)
// elif e instanceof Range) || e instanceof Any):
// size += 1
// fixed.push(e)
// elif e instanceof And) || e instanceof Not):
// size += 0
// fixed.push(e)
//         else:
// break
// remains = remains[len(fixed):]

class PAlt extends PTuple {
    public toString() {
        return this.es.map((e) => e.toString()).join(' | ')
    }
}

class POre extends PTuple {
    static new(...es: PExpr[]) {
        const choices: PExpr[] = []
        for (const e of es) {
            O2.appendChoice(choices, e)
        }
        return choices.length === 1 ? choices[0] : new POre(...choices)
    }

    public toString() {
        return this.es.map((e) => e.toString()).join(' / ')
    }

    minLen() {
        if (!this.minlen) {
            var mlen = 0
            for (const e of this.es) {
                mlen = Math.min(e.minLen(), mlen);
            }
            this.minlen = mlen;
        }
        return this.minlen;
    }

    isDict() {
        for (const e of this.es) {
            if (!(e instanceof PChar)) {
                return false;
            }
        }
        return true;
    }

    listDict() {
        const dic = this.es.map(e => (e instanceof PChar) ? e.text : '')
        const dic2 = [];
        for (const s of dic) {
            if (s === '') break;
            dic2.push(s);
        }
        return dic2
    }

    trieDict(dic?: string[]) {
        if (dic === undefined) {
            dic = this.listDict();
        }
        if ('' in dic || dic.length < 10) {
            return dic;
        }
        const d: { [key: string]: string | string[] } = {};
        for (const s of dic) {
            const c = s[0];
            const s1 = s.slice(1);
            if (c in d) {
                const entry = d[c];
                if (typeof entry === 'string') {
                    d[c] = [entry, s1]
                }
                else {
                    entry.push(s1);
                }
            }
            else {
                d[c] = s1
            }
        }
        return d;
    }
}

class O2 {

    static inline(pe: PExpr) {
        const start = pe
        while (pe instanceof PRef) {
            pe = pe.deref();
            if (pe instanceof PChar || pe instanceof PRange) {
                return pe;
            }
        }
        return start
    }

    static isRange(e: PExpr) {
        return (e instanceof PChar && e.text.length == 1) || (e instanceof PRange);
    }

    static mergeRange(e: PExpr, e2: PExpr) {
        var chars = ''
        var ranges = ''
        if (e instanceof PChar) {
            chars += e.text;
        }
        if (e2 instanceof PChar) {
            chars += e2.text;
        }
        if (e instanceof PRange) {
            chars += e.chars
            ranges += e.ranges
        }
        if (e2 instanceof PRange) {
            chars += e2.chars
            ranges += e2.ranges
        }
        return new PRange(chars, ranges)
    }

    static appendChoice(es: PExpr[], pe: PExpr) {
        if (pe instanceof POre) {
            for (const e of pe.es) {
                O2.appendChoice(es, e);
            }
        }
        else if (es.length === 0) {
            es.push(pe);
        }
        else if (O2.isRange(es[es.length - 1]) && O2.isRange(pe)) {
            es[es.length - 1] = O2.mergeRange(es[es.length - 1], pe);
        }
        else if (es[es.length] !== EMPTY) {
            es.push(pe)
        }
    }

    static appendChoice2(es: PExpr[], pe: PExpr) {
        const start = pe;
        while (pe instanceof PRef) {
            pe = pe.deref()
        }
        if (pe instanceof POre) {
            for (const e of pe.es) {
                O2.appendChoice2(es, e);
            }
        }
        else if (pe instanceof PChar || pe instanceof PRange) {
            O2.appendChoice(es, pe);
        }
        else {
            O2.appendChoice(es, start);
        }
    }
}

// def inline(pe):

class PUnary extends PExpr {
    e: PExpr
    constructor(e: PExpr) {
        super()
        this.e = e;
    }
    minLen() {
        return this.e.minLen()
    }
}

class PAnd extends PUnary {
    public toString() {
        return '&' + grouping(this.e, inUnary)
    }
    minLen() {
        return 0
    }
}

class PNot extends PUnary {
    public toString() {
        return '!' + grouping(this.e, inUnary)
    }
    minLen() {
        return 0;
    }
}

class PMany extends PUnary {
    public toString() {
        return grouping(this.e, inUnary) + '*';
    }
    minLen() { return 0 }
}


class POneMany extends PUnary {
    public toString() {
        return grouping(this.e, inUnary) + '+';
    }
}

class POption extends PUnary {
    public toString() {
        return grouping(this.e, inUnary) + '?'
    }
    minLen() { return 0 }
}

class PNode extends PUnary {
    tag: string
    shift: number
    constructor(e: PExpr, tag = '', shift = 0) {
        super(e);
        this.tag = tag;
        this.shift = shift;
    }

    public toString() {
        return `{${this.e}  #${this.tag}}`;
    }
}

class PEdge extends PUnary {
    edge: string
    constructor(edge: string, e: PExpr) {
        super(e);
        this.edge = edge;
    }
    public toString() {
        return this.edge + ': ' + grouping(this.e, inUnary)
    }
}

class PFold extends PUnary {
    tag: string
    edge: string
    shift: number
    constructor(edge: string, e: PExpr, tag = '', shift = 0) {
        super(e)
        this.tag = tag
        this.edge = edge
        this.shift = shift
    }

    public toString() {
        var edge = (this.edge !== '') ? `${this.edge}: ` : ''
        return `${edge}: ^ {${this.e}  #${this.tag}}`
    }
}


class PAbs extends PUnary {
    constructor(e: PExpr) {
        super(e)
    }
    public toString() {
        return `@Abs(${this.e})`
    }
}

class PAction extends PUnary {
    func: string;
    params: PExpr[];
    constructor(e: PExpr, func: string, params: PExpr[], t?: ParseTree) {
        super(e);
        this.func = func
        this.params = params
    }

    public toString() {
        return `@${this.func}${this.params}`
    }

}

// CONSTANT
const EMPTY = new PChar('')
const ANY = new PAny()
//const FAIL = new PNot(EMPTY)

// repr

const grouping = (e: PExpr, f: (e: PExpr) => boolean) => {
    return f(e) ? '(' + e.toString() + ')' : e.toString();
}

const inUnary = (e: PExpr) => {
    return e instanceof POre || e instanceof PSeq || e instanceof PAlt || e instanceof PEdge || e instanceof PFold;
}

// // Grammar

export class Grammar {
    static ID = 0
    ns: string; // namespace
    names: string[]
    rules: { [key: string]: PExpr };
    examples: [string, ParseTree][]

    public constructor(source?: string) {
        this.ns = `${Grammar.ID++}`
        this.names = []
        this.rules = {}
        this.examples = []
        if (source !== undefined) {
            load_grammar(this, source)
        }
    }

    set(name: string, e: PExpr) {
        if (!(name in this.rules)) {
            this.names.push(name);
        }
        this.rules[name] = e;
    }

    public get(name: string) {
        return this.rules[name];
    }

    public startName() {
        if (this.names.length === 0) {
            this.set('EMPTY', EMPTY);
        }
        return this.names[0];
    }

    newRef(name: string, t?: ParseTree) {
        return new PRef(this, name);
    }

    public generate(start?: string) {
        start = start || this.startName();
        return generate(this, { start: start });
    }

    public toString() {
        const sb = []
        for (const name of this.names) {
            sb.push(`${name} = ${this.rules[name]}`)
        }
        return sb.join('\n')
    }

}

const makelist = (pe: PExpr, cnt: { [key: string]: number }, es: PRef[]) => {
    if (pe instanceof PRef) {
        const u = pe.uname()
        const c = cnt[u] || 0;
        cnt[u] = c + 1;
        if (c == 0) {
            makelist(pe.deref(), cnt, es);
            es.push(pe)
        }
        return es;
    }
    if (pe instanceof PTuple) {
        for (const e of pe.es) {
            makelist(e, cnt, es);
        }
        return es;
    }
    if (pe instanceof PUnary) {
        makelist(pe.e, cnt, es);
    }
    return es;
}

// // ast.env

// def bytestr(b):
// return b.decode('utf-8') if isinstance(b, bytes) else b

class Generator {
    peg: Grammar | null;
    generated: { [key: string]: PFunc }
    generating_nonterminal: string;
    sids: { [key: string]: number }

    constructor() {
        this.peg = null
        this.generated = {}
        this.generating_nonterminal = ''
        this.sids = {}
    }

    getsid(name: any) {
        name = name.toString();
        if (!(name in this.sids)) {
            this.sids[name] = Object.keys(this.sids).length
        }
        return this.sids[name];
    }

    generate(peg: Grammar, options: any = {}): Parser {
        this.peg = peg
        const name: string = options.start || peg.startName()
        const start = peg.newRef(name)
        // if 'memos' in option && not isinstance(option['memos'], list):
        const memos: string[] = options.memos || peg.names;
        const es = makelist(start, {}, [])

        for (const ref of es) {
            //assert isinstance(ref, Ref)
            const uname = ref.uname()
            this.generating_nonterminal = uname
            //console.log(`generating ${uname}`);
            const A = this.emit(ref.deref(), 0);
            //console.log(`generated ${uname}`);
            this.generating_nonterminal = ''
            const idx = memos.indexOf(ref.name)
            // if idx != -1 && ref.peg == peg:
            //     A = this.memoize(idx, len(memos), A)
            this.generated[uname] = A
        }
        return PAsm.generate(this.generated, start.uname());
    }

    emit(pe: PExpr, step: number): PFunc {
        //var pe = inline(pe) FIXME
        const cname = pe.cname()
        if (cname in (this as any)) {
            return (this as any)[cname](pe, step);
        }
        console.log('@TODO(Generator)', cname, pe)
        return PAsm.pEmpty();
    }

    //     def memoize(self, mp, msize, A):
    //         def match_memo(px):
    //         key = (msize * px.pos) + mp
    // m = px.memo[key % 1789]
    // if m.key == key:
    //     px.pos = m.pos
    // if m.ast != false:
    //     px.ast = m.ast
    // return m.result
    // prev = px.ast
    // m.result = A(px)
    // m.pos = px.pos
    // m.ast = px.ast if prev != px.ast else false
    // m.key = key
    // return m.result
    // return match_memo

    PAny(pe: PAny, step: number) {
        return PAsm.pAny();
    }

    PChar(pe: PChar, step: number) {
        return PAsm.pChar(pe.text);
    }

    PRange(pe: PRange, step: number) {
        return PAsm.pRange(pe.chars, pe.ranges);
    }

    PAnd(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pAnd(pf);
    }

    PNot(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pNot(pf);
    }

    PMany(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pMany(pf);
    }

    POneMany(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pOneMany(pf);
    }

    POption(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pOption(pf);
    }

    PSeq(pe: PTuple, step: number) {
        const pfs = pe.es.map(e => this.emit(e, step))
        return PAsm.pSeq(...pfs);
    }

    POre(pe: PTuple, step: number) {
        const pfs = pe.es.map(e => this.emit(e, step))
        return PAsm.pOre(...pfs);
    }

    PAlt(pe: PTuple, step: number) {
        return this.POre(pe, step);
    }

    PRef(pe: PRef, step: number) {
        const uname = pe.uname();
        const generated = this.generated;
        return PAsm.pRef(generated, uname);
    }

    PNode(pe: PNode, step: number) {
        const pf = this.emit(pe.e, step);
        const tag = pe.tag;
        return PAsm.pNode(pf, pe.tag, pe.shift);
    }

    PEdge(pe: PEdge, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pEdge(pe.edge, pf);
    }

    PFold(pe: PFold, step: number) {
        const pf = this.emit(pe.e, step);
        const tag = pe.tag;
        const edge = pe.edge;
        return PAsm.pFold(pe.edge, pf, pe.tag, pe.shift);
    }

    PAbs(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pAbs(pf);
    }

    Skip(pe: PAction, step: number) { // @skip()
        return PAsm.pSkip();
    }

    Symbol(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        const sid = this.getsid(pe.params[0]);
        return PAsm.pSymbol(pf, sid);
    }

    Scope(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        return PAsm.pScope(pf);
    }

    Exists(pe: PAction, step: number) {
        const sid = this.getsid(pe.params[0]);
        return PAsm.pExists(sid);
    }

    Match(pe: PAction, step: number) {
        const sid = this.getsid(pe.params[0]);
        return PAsm.pMatch(sid);
    }

}

const gen = new Generator();

const generate = (peg: Grammar, options: any = {}) => {
    return gen.generate(peg, options);
}

// ParseTree

const UNKNOWN_URN = '(unknown source)'

const str = (t: any) => t ? t.toString() : ''

class TPEGLoader {
    names: any;
    peg: Grammar;

    constructor(peg: Grammar) {
        this.names = {}
        this.peg = peg
    }

    load(t: ParseTree) {
        for (const stmt of t.subNodes()) {
            if (stmt.is('Rule')) {
                const name = stmt.get('name').toString();
                if (name in this.names) {
                    logger('error', stmt.get('name'), `redefined name {name}`)
                }
                this.names[name] = stmt.get('e');
            } else if (stmt.is('Example')) {
                const doc = stmt.get('doc')
                for (const name of stmt.get('names').subNodes()) {
                    this.peg.examples.push([name.getToken(), doc]);
                }
            }
            else if (stmt.is('Import')) {
                logger('warning', stmt.get('name'), `ignored import`)
            }
            else if (stmt.is('err')) {
                throw new Error('Syntax Error');
            }
        }
        //
        for (const name of Object.keys(this.names)) {
            const tt = this.names[name];
            this.peg.set(name, this.conv(tt));
        }
    }

    conv(t: ParseTree) {
        const tag = t.getTag()
        return (this as any)[tag](t);
    }

    static unquote(s: string, pos: number, sb: string[]) {
        if (!s.startsWith('\\', pos)) {
            sb.push(s[pos]);
            return pos + 1;
        }
        if ((s.startsWith('\\x') || s.startsWith('\\X')) && s.length - pos >= 4) {
            const c = Number.parseInt(s.substring(pos + 2, pos + 4), 16);
            sb.push(String.fromCharCode(c));
            return pos + 4;
        }
        if ((s.startsWith('\\u') || s.startsWith('\\U')) && s.length - pos >= 6) {
            const c = Number.parseInt(s.substring(pos + 2, pos + 6), 16);
            sb.push(String.fromCharCode(c));
            return pos + 6;
        }
        if (s.startsWith('\\n')) {
            sb.push('\n');
        }
        else if (s.startsWith('\\t')) {
            sb.push('\t');
        }
        else if (s.startsWith('\\r')) {
            sb.push('\r');
        }
        else if (s.startsWith('\\f')) {
            sb.push('\f');
        }
        else if (s.startsWith('\\v')) {
            sb.push('\v');
        }
        else {
            sb.push(s[pos + 1]);
        }
        return pos + 2;
    }

    Empty(t: ParseTree) {
        return EMPTY
    }

    Any(t: ParseTree) {
        return ANY
    }

    Char(t: ParseTree) {
        const s = str(t);
        const sb: string[] = []
        var pos = 0;
        while (pos < s.length) {
            pos = TPEGLoader.unquote(s, pos, sb)
        }
        const text = sb.join('');
        return text.length > 0 ? new PChar(text) : EMPTY;
    }

    Class(t: ParseTree) {
        const s = str(t);
        const chars: string[] = []
        const ranges: string[] = []
        var pos = 0;
        while (pos < s.length) {
            pos = TPEGLoader.unquote(s, pos, chars);
            if (s.startsWith("-", pos)) {
                ranges.push(chars.pop()!);
                pos = TPEGLoader.unquote(s, pos, ranges);
            }
        }
        if (chars.length == 1 && ranges.length == 0) {
            return new PChar(chars.join(''));
        }
        return new PRange(chars.join(''), ranges.join(''))
    }

    // def Ref(self, t):
    // name = str(t)
    // if name in this.peg:
    //     return Action(this.peg.newRef(name), 'NT', (name,), t.getpos4())
    // if name[0].isupper() || name[0].islower() || name.startswith('_'):
    //     logger('warning', t, f'undefined nonterminal {name}')
    // this.peg.add(name, EMPTY)
    // return this.peg.newRef(name)
    // return pChar(name[1: -1]) if name.startswith('"') else char1(name)

    Name(t: ParseTree) {
        const name = str(t);
        if (name in this.names) {
            return this.peg.newRef(name, t);
        }
        // if name[0].isupper() || name[0].islower() || name.startswith('_'):
        //     default_logger('warning', t, f'undefined nonterminal {name}')
        // this.peg.add(name, EMPTY)
        // return this.peg.newRef(name)
        // return pChar(name[1: -1]) if name.startswith('"') else char1(name)
    }

    Many(t: ParseTree | any) {
        return new PMany(this.conv(t.e))
    }

    OneMany(t: ParseTree | any) {
        return new POneMany(this.conv(t.e))
    }

    Option(t: ParseTree | any) {
        return new POption(this.conv(t.e))
    }

    And(t: ParseTree | any) {
        return new PAnd(this.conv(t.e))
    }

    Not(t: ParseTree | any) {
        return new PNot(this.conv(t.e))
    }

    Seq(t: ParseTree) {
        return new PSeq(...t.subNodes().map(p => this.conv(p)))
    }

    Ore(t: ParseTree) {
        return POre.new(...t.subNodes().map(p => this.conv(p)))
    }

    Alt(t: ParseTree) {
        return POre.new(...t.subNodes().map(p => this.conv(p)))
    }

    Node(t: ParseTree | any) {
        const tag = str(t.tag)
        const e = this.conv(t.e)
        return new PNode(e, tag)
    }

    Edge(t: ParseTree | any) {
        const edge = str(t.edge)
        const e = this.conv(t.e)
        return new PEdge(edge, e)
    }

    Fold(t: ParseTree | any) {
        const edge = str(t.edge)
        const tag = str(t.tag)
        const e = this.conv(t.e)
        return new PFold(edge, e, tag)
    }

    static readonly EPSILON: { [key: string]: string } = {
        'exists': 'exists', 'recover': 'recover',
    }

    Func(t: ParseTree) {
        const ts = t.subNodes();
        const funcname = str(ts[0])
        const es = ts.slice(1).map((t) => this.conv(t))
        // if funcname.startswith('choice'):
        //     n = funcname[6:]
        // if n.isdigit():
        //     return TPEGLoader.choiceN(t.urn_, int(n), ps)
        // return TPEGLoader.choice(t.urn_, ps)
        if (funcname === 'abs') {
            return new PAbs(es[0]);
        }
        if (funcname in TPEGLoader.EPSILON) {
            return new PAction(EMPTY, funcname, es, t);
        }
        return new PAction(es[0], funcname, es, t)
    }
}

//def grammar_factory():

const logger = (type: string, pos: ParseTree, msg: string) => {
    console.log(pos.message(msg));
}

const TPEGGrammar = TPEG();
const pegparser = PAsm.generate(TPEGGrammar, 'Start');

const load_grammar = (peg: Grammar, source: string, options: any = {}) => {
    const t = pegparser(source);
    const pconv = new TPEGLoader(peg);
    pconv.load(t);
    return peg;
}

// const peg = load_grammar(new Grammar(), `
// A = 'a'
// `)
// console.log(peg);
