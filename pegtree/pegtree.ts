// Utilities from Python3 Porting
import { quote, generate as generate_pasm } from './pasm';
import { TPEG } from './tpeg';

const len = (s: string | any[]) => s.length

const translate = (s: string, dic: { [key: string]: string }) => {
    var foundESC = false;
    for (const c of Object.keys(dic)) {
        if (s.indexOf(c) !== -1) {
            foundESC = true;
            break;
        }
    }
    if (foundESC) {
        const sb = []
        for (const c of s) {
            if (c in dic) {
                sb.push(dic[c]);
            }
            else {
                sb.push(c);
            }
        }
        return sb.join('')
    }
    return s;
}

// const ESCTBL = { '\n': '\\n', '\t': '\\t', '\r': '\\r', '\v': '\\v', '\f': '\\f', '\\': '\\\\', "'": "\\'" }

// function quote(s: string) {
//     return "'" + translate(s, ESCTBL) + "'"
// }

// const range_min = (chars: string, ranges: string) => {
//     const s = chars + ranges;
//     var min = 0xffff;
//     for (var i = 0; i < s.length; i++) {
//         const c = s.charCodeAt(i)
//         min = Math.min(min, c);
//     }
//     return min;
// }

const range_max = (chars: string, ranges: string) => {
    const s = chars + ranges;
    var min = 0;
    for (var i = 0; i < s.length; i++) {
        const c = s.charCodeAt(i)
        min = Math.max(min, c);
    }
    return min;
}

const range_bitmap = (chars: string, ranges: string) => {
    const codemax = range_max(chars, ranges) + 1;
    const bitmap = new Uint8Array(((codemax / 8) | 0) + 1);
    bitmap[0] = 2;
    for (var i = 0; i < chars.length; i += 1) {
        const c = chars.charCodeAt(i);
        const n = (c / 8) | 0;
        const mask = 1 << ((c % 8) | 0);
        bitmap[n] |= mask;
    }
    for (var i = 0; i < ranges.length; i += 2) {
        for (var c = ranges.charCodeAt(i); c <= ranges.charCodeAt(i + 1); c += 1) {
            const n = (c / 8) | 0;
            const mask = 1 << ((c % 8) | 0);
            bitmap[n] |= mask;
        }
    }
    return bitmap;
}

// PExpr

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
        return len(this.text)
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
        const sb = []
        sb.push('[')
        sb.push(translate(this.chars, PRange.ESCTBL))
        const r = this.ranges
        for (var i = 0; i < r.length; i += 2) {
            sb.push(translate(r[i], PRange.ESCTBL))
            sb.push('-')
            sb.push(translate(r[i + 1], PRange.ESCTBL))
        }
        sb.push(']')
        return sb.join('')
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

const tail = (xs: PExpr[]) => {
    return xs[xs.length - 1];
}

class PSeq extends PTuple {
    static new(...es: PExpr[]) {
        const ls = []
        for (const e of es) {
            if (e === EMPTY) continue;
            if (ls.length === 0) {
                ls.push(e);
                continue;
            }
            const pe = tail(ls);
            if (e instanceof PChar && pe instanceof PChar) {
                ls[ls.length - 1] = pChar(pe.text + e.text)
                continue
            }
            ls.push(e)
        }
        return len(ls) === 1 ? ls[0] : pSeq(...ls)
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
    // @classmethod
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

    //     def optimize(self):
    //         choices =[]
    //     optimizedChoice(choices, self)
    // return choices[0] if len(choices) == 1 else Ore(* choices)

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
        if ('' in dic || len(dic) < 10) {
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

    static isCRange(e: PExpr) {
        return (e instanceof PChar && len(e.text) == 1) || (e instanceof PRange);
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
        else if (O2.isCRange(es[es.length - 1]) && O2.isCRange(pe)) {
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


class PMany1 extends PUnary {
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
    constructor(e: PExpr, tag = '') {
        super(e);
        this.tag = tag;
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
    constructor(edge: string, e: PExpr, tag = '') {
        super(e);
        this.tag = tag;
        this.edge = edge
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
const FAIL = new PNot(EMPTY)

const pEmpty = () => EMPTY
const pAny = () => ANY
const pChar = (c: string) => len(c) > 0 ? new PChar(c) : EMPTY
const pRange = (cs: string, rs = '') => new PRange(cs, rs)
const pAnd = (e: PExpr) => new PAnd(e)
const pNot = (e: PExpr) => new PNot(e)
const pMany = (e: PExpr) => new PMany(e)
const pMany1 = (e: PExpr) => new PMany1(e)
const pOption = (e: PExpr) => new POption(e)
const pSeq = (...es: PExpr[]) => new PSeq(...es)
const pSeq2 = (e: PExpr, e2: PExpr) => new PSeq(e, e2)
const pSeq3 = (e: PExpr, e2: PExpr, e3: PExpr) => new PSeq(e, e2, e3)
const pOre = (...es: PExpr[]) => POre.new(...es)
const pOre2 = (e: PExpr, e2: PExpr) => POre.new(e, e2)
const pOre3 = (e: PExpr, e2: PExpr, e3: PExpr) => POre.new(e, e2, e3)
const pRef = (peg: Grammar, name: string) => new PRef(peg, name)
const pNode = (e: PExpr, tag: string, shift = 0) => new PNode(e, tag)
const pEdge = (label: string, e: PExpr) => (label !== '') ? new PEdge(label, e) : e
const pFold = (label: string, e: PExpr, tag: string, shift = 0) => new PFold(label, e, tag)

// repr

const grouping = (e: PExpr, f: (e: PExpr) => boolean) => {
    return f(e) ? '(' + e.toString() + ')' : e.toString();
}

const inUnary = (e: PExpr) => {
    return e instanceof POre || e instanceof PSeq || e instanceof PAlt || e instanceof PEdge || e instanceof PFold;
}

// // Grammar

class Grammar {
    static ID = 0
    ns: string; // namespace
    names: string[]
    rules: { [key: string]: PExpr };
    examples: [string, ParseTree][]

    constructor() {
        this.ns = `${Grammar.ID++}`
        this.names = []
        this.rules = {}
        this.examples = []
    }

    public set(name: string, e: PExpr) {
        if (!(name in this.rules)) {
            this.names.push(name);
        }
        this.rules[name] = e;
    }

    public get(name: string) {
        return this.rules[name];
    }

    startName() {
        if (this.names.length === 0) {
            this.set('EMPTY', EMPTY);
        }
        return this.names[0];
    }

    newRef(name: string, t?: ParseTree) {
        return new PRef(this, name);
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

export const pRule = (peg: Grammar, name: string, e: PExpr) => {
    peg.set(name, e);
}

// const TPEG = (peg: Grammar) => {
//     pRule(peg, 'Start', pSeq3(pRef(peg, '__'), pRef(peg, 'Source'), pRef(peg, 'EOF')));
//     pRule(peg, '__', pMany(pOre2(pRange(' \t\r\n'), pRef(peg, 'COMMENT'))))
//     pRule(peg, '_', pMany(pOre2(pRange(' \t'), pRef(peg, 'COMMENT'))))
//     pRule(peg, 'COMMENT', pOre2(pSeq3(pChar('/*'), pMany(pSeq2(pNot(pChar('*/')), pAny())), pChar('*/')), pSeq2(pChar('//'), pMany(pSeq2(pNot(pRef(peg, 'EOL')), pAny())))))
//     pRule(peg, 'EOL', pOre(pChar('\n'), pChar('\r\n'), pRef(peg, 'EOF')))
//     pRule(peg, 'EOF', pNot(pAny()))
//     pRule(peg, 'S', pRange(' \t'))
//     pRule(peg, 'Source', pNode(pMany(pEdge('', pRef(peg, 'Statement'))), 'Source', 0))
//     pRule(peg, 'EOS', pOre2(pSeq2(pRef(peg, '_'), pMany1(pSeq2(pChar(';'), pRef(peg, '_')))), pMany1(pSeq2(pRef(peg, '_'), pRef(peg, 'EOL')))))
//     pRule(peg, 'Statement', pOre(pRef(peg, 'Import'), pRef(peg, 'Example'), pRef(peg, 'Rule')))
//     pRule(peg, 'Import', pSeq2(pNode(pSeq(pChar('from'), pRef(peg, 'S'), pRef(peg, '_'), pEdge('name', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'Char'))), pOption(pSeq(pRef(peg, '_'), pChar('import'), pRef(peg, 'S'), pRef(peg, '_'), pEdge('names', pRef(peg, 'Names'))))), 'Import', 0), pRef(peg, 'EOS')))
//     pRule(peg, 'Example', pSeq2(pNode(pSeq(pChar('example'), pRef(peg, 'S'), pRef(peg, '_'), pEdge('names', pRef(peg, 'Names')), pEdge('doc', pRef(peg, 'Doc'))), 'Example', 0), pRef(peg, 'EOS')))
//     pRule(peg, 'Names', pNode(pSeq3(pEdge('', pRef(peg, 'Identifier')), pRef(peg, '_'), pMany(pSeq(pChar(','), pRef(peg, '_'), pEdge('', pRef(peg, 'Identifier')), pRef(peg, '_')))), '', 0))
//     pRule(peg, 'Doc', pOre(pRef(peg, 'Doc1'), pRef(peg, 'Doc2'), pRef(peg, 'Doc0')))
//     pRule(peg, 'Doc0', pNode(pMany(pSeq2(pNot(pRef(peg, 'EOL')), pAny())), 'Doc', 0))
//     pRule(peg, 'Doc1', pSeq(pRef(peg, 'DELIM1'), pMany(pRef(peg, 'S')), pRef(peg, 'EOL'), pNode(pMany(pSeq2(pNot(pSeq2(pRef(peg, 'DELIM1'), pRef(peg, 'EOL'))), pAny())), 'Doc', 0), pRef(peg, 'DELIM1')))
//     pRule(peg, 'DELIM1', pChar("'''"))
//     pRule(peg, 'Doc2', pSeq(pRef(peg, 'DELIM2'), pMany(pRef(peg, 'S')), pRef(peg, 'EOL'), pNode(pMany(pSeq2(pNot(pSeq2(pRef(peg, 'DELIM2'), pRef(peg, 'EOL'))), pAny())), 'Doc', 0), pRef(peg, 'DELIM2')))
//     pRule(peg, 'DELIM2', pChar('```'))
//     pRule(peg, 'Rule', pSeq2(pNode(pSeq(pEdge('name', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'QName'))), pRef(peg, '__'), pOre2(pChar('='), pChar('<-')), pRef(peg, '__'), pOption(pSeq2(pRange('/|'), pRef(peg, '__'))), pEdge('e', pRef(peg, 'Expression'))), 'Rule', 0), pRef(peg, 'EOS')))
//     pRule(peg, 'Identifier', pNode(pRef(peg, 'NAME'), 'Name', 0))
//     pRule(peg, 'NAME', pSeq2(pRange('_', 'AZaz'), pMany(pRange('_.', 'AZaz09'))))
//     pRule(peg, 'Expression', pSeq2(pRef(peg, 'Choice'), pOption(pFold('', pMany1(pSeq(pRef(peg, '__'), pChar('|'), pNot(pChar('|')), pRef(peg, '_'), pEdge('', pRef(peg, 'Choice')))), 'Alt', 0))))
//     pRule(peg, 'Choice', pSeq2(pRef(peg, 'Sequence'), pOption(pFold('', pMany1(pSeq(pRef(peg, '__'), pOre2(pChar('/'), pChar('||')), pRef(peg, '_'), pEdge('', pRef(peg, 'Sequence')))), 'Ore', 0))))
//     pRule(peg, 'Sequence', pSeq2(pRef(peg, 'Predicate'), pOption(pFold('', pMany1(pSeq2(pRef(peg, 'SS'), pEdge('', pRef(peg, 'Predicate')))), 'Seq', 0))))
//     pRule(peg, 'SS', pOre2(pSeq3(pRef(peg, 'S'), pRef(peg, '_'), pNot(pRef(peg, 'EOL'))), pSeq3(pMany1(pSeq2(pRef(peg, '_'), pRef(peg, 'EOL'))), pRef(peg, 'S'), pRef(peg, '_'))))
//     pRule(peg, 'Predicate', pOre(pRef(peg, 'Not'), pRef(peg, 'And'), pRef(peg, 'Suffix')))
//     pRule(peg, 'Not', pSeq2(pChar('!'), pNode(pEdge('e', pRef(peg, 'Predicate')), 'Not', 0)))
//     pRule(peg, 'And', pSeq2(pChar('&'), pNode(pEdge('e', pRef(peg, 'Predicate')), 'And', 0)))
//     pRule(peg, 'Suffix', pSeq2(pRef(peg, 'Term'), pOption(pOre(pFold('e', pChar('*'), 'Many', 0), pFold('e', pChar('+'), 'Many1', 0), pFold('e', pChar('?'), 'Option', 0)))))
//     pRule(peg, 'Term', pOre(pRef(peg, 'Group'), pRef(peg, 'Char'), pRef(peg, 'Class'), pRef(peg, 'Any'), pRef(peg, 'Node'), pRef(peg, 'Fold'), pRef(peg, 'EdgeFold'), pRef(peg, 'Edge'), pRef(peg, 'Func'), pRef(peg, 'Ref')))
//     pRule(peg, 'Empty', pNode(pEmpty(), 'Empty', 0))
//     pRule(peg, 'Group', pSeq(pChar('('), pRef(peg, '__'), pOre2(pRef(peg, 'Expression'), pRef(peg, 'Empty')), pRef(peg, '__'), pChar(')')))
//     pRule(peg, 'Any', pNode(pChar('.'), 'Any', 0))
//     pRule(peg, 'Char', pSeq3(pChar("'"), pNode(pMany(pOre2(pSeq2(pChar('\\'), pAny()), pSeq2(pNot(pChar("'")), pAny()))), 'Char', 0), pChar("'")))
//     pRule(peg, 'Class', pSeq3(pChar('['), pNode(pMany(pOre2(pSeq2(pChar('\\'), pAny()), pSeq2(pNot(pChar(']')), pAny()))), 'Class', 0), pChar(']')))
//     pRule(peg, 'Node', pNode(pSeq(pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pEdge('e', pOre2(pSeq2(pRef(peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Node', 0))
//     pRule(peg, 'Tag', pSeq2(pChar('#'), pNode(pMany1(pSeq2(pNot(pRange(' \t\r\n}')), pAny())), 'Tag', 0)))
//     pRule(peg, 'Fold', pNode(pSeq(pChar('^'), pRef(peg, '_'), pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pEdge('e', pOre2(pSeq2(pRef(peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Fold', 0))
//     pRule(peg, 'Edge', pNode(pSeq(pEdge('edge', pRef(peg, 'Identifier')), pChar(':'), pRef(peg, '_'), pNot(pChar('^')), pEdge('e', pRef(peg, 'Term'))), 'Edge', 0))
//     pRule(peg, 'EdgeFold', pNode(pSeq(pEdge('edge', pRef(peg, 'Identifier')), pChar(':'), pRef(peg, '_'), pChar('^'), pRef(peg, '_'), pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pEdge('e', pOre2(pSeq2(pRef(peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Fold', 0))
//     pRule(peg, 'Func', pNode(pSeq(pChar('@'), pEdge('', pRef(peg, 'Identifier')), pChar('('), pRef(peg, '__'), pOre2(pEdge('', pRef(peg, 'Expression')), pEdge('', pRef(peg, 'Empty'))), pMany(pSeq(pRef(peg, '_'), pChar(','), pRef(peg, '__'), pEdge('', pRef(peg, 'Expression')))), pRef(peg, '__'), pChar(')')), 'Func', 0))
//     pRule(peg, 'Ref', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'QName')))
//     pRule(peg, 'QName', pNode(pSeq3(pChar('"'), pMany(pOre2(pSeq2(pChar('\\'), pAny()), pSeq2(pNot(pChar('"')), pAny()))), pChar('"')), 'Name', 0))
//     return peg
// }

// const TPEGGrammar = TPEG(new Grammar())
// console.log(TPEGGrammar)
// console.log(`${TPEGGrammar}`)

// // ast.env

// def bytestr(b):
// return b.decode('utf-8') if isinstance(b, bytes) else b

class PTree {
    prev: PTree | null;
    tag: string;
    spos: number;
    epos: number;
    child: PTree | null;
    constructor(prev: PTree | null, tag: string, spos: number, epos: number, child: PTree | null) {
        this.prev = prev
        this.tag = tag
        this.spos = spos
        this.epos = epos
        this.child = child
    }

    isEdge() {
        return (this.epos < 0);
    }

    dump(inputs: string) {
        const sb: string[] = []
        if (this.prev !== null) {
            sb.push(this.prev.dump(inputs))
            sb.push(',')
        }
        sb.push(`{#${this.tag} `)
        if (this.child === null) {
            sb.push("'")
            sb.push(inputs.substring(this.spos, this.epos))
            sb.push("'")
        }
        else {
            sb.push(this.child.dump(inputs))
        }
        sb.push('}')
        return sb.join('')
    }
}

class ParseTree {
    static readonly EMPTY: ParseTree[] = [];
    tag_: string;
    inputs_: string;
    spos_: number;
    epos_: number;
    urn_: string;
    subs_: ParseTree[];

    public constructor(tag: string, inputs: string, spos = 0, epos = -1, urn = UNKNOWN_URN) {
        this.tag_ = tag
        this.inputs_ = inputs
        this.spos_ = spos
        this.epos_ = (epos === -1) ? (len(inputs) - spos) : epos
        this.urn_ = urn
        this.subs_ = ParseTree.EMPTY;
    }

    public is(tag: string) {
        return this.tag_ === tag;
    }

    public gettag() {
        return this.tag_;
    }

    public add(t: ParseTree, edge: string = '') {
        if (edge === '') {
            if (this.subs_ === ParseTree.EMPTY) {
                this.subs_ = [];
            }
            this.subs_.push(t)
        }
        else {
            (this as any)[edge] = t;
        }
    }

    public get(key: string) {
        return (this as any)[key];
    }

    public subNodes() {
        return this.subs_;
    }

    public isSyntaxError() {
        return this.tag_ === 'err'
    }

    private pos_(pos: number) {
        const s = this.inputs_;
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

    public beginPosition() {
        return this.pos_(this.spos_);
    }

    public endPosition() {
        return this.pos_(this.spos_);
    }

    public length() {
        return this.epos_ - this.spos_;
    }

    public keys() {
        return Object.keys(this).filter(x => !x.endsWith('_'));
    }

    public toString() {
        return this.inputs_.substring(this.spos_, this.epos_);
    }

    public dump() {
        const sb: string[] = [];
        this.strOut(sb);
        return sb.join('');
    }

    protected strOut(sb: string[]) {
        var c = 0;
        sb.push("[#")
        sb.push(this.tag_)
        for (const node of this.subNodes()) {
            c += 1;
            sb.push(` `);
            node.strOut(sb);
        }
        for (const key of this.keys()) {
            sb.push(` ${key} = `);
            (this as any)[key].strOut(sb);
        }
        if (c == 0) {
            sb.push(' ');
            sb.push(quote(this.inputs_.substring(this.spos_, this.epos_)))
        }
        sb.push("]")
    }

    public showing(msg = 'Syntax Error') {
        const p = this.beginPosition();
        const pos = p[0];
        const row = p[1];
        const col = p[2];
        return `(${this.urn_}:${row}+${col}) ${msg}`
    }
}

const PTree2ParseTree = (pt: PTree, urn: string, inputs: string) => {
    if (pt.prev !== null) {
        return PTree2ParseTreeImpl('', urn, inputs, pt.spos, pt.epos, pt)
    }
    else {
        return PTree2ParseTreeImpl(pt.tag, urn, inputs, pt.spos, pt.epos, pt.child)
    }
}

const PTree2ParseTreeImpl = (tag: string, urn: string, inputs: string, spos: number, epos: number, subnode: PTree | null) => {
    const t = new ParseTree(tag, inputs, spos, epos, urn);
    while (subnode !== null) {
        if (subnode.isEdge()) {
            if (subnode.child === null) {
                var tt = PTree2ParseTreeImpl('', urn, inputs, subnode.spos, Math.abs(subnode.epos), null)
            }
            else {
                tt = PTree2ParseTree(subnode.child, urn, inputs);
            }
            t.add(tt, subnode.tag);
        }
        else {
            t.add(PTree2ParseTreeImpl(subnode.tag, urn, inputs,
                subnode.spos, Math.abs(subnode.epos), subnode.child))
        }
        subnode = subnode.prev;
    }
    const tail = t.subs_.length - 1
    for (var i = 0; i < (tail + 1) / 2; i += 1) {
        const t0 = t.subs_[i];
        t.subs_[i] = t.subs_[tail - i]
        t.subs_[tail - i] = t0;
    }
    return t;
}

// PContext

class PContext {
    x: string;
    pos: number;
    epos: number;
    headpos: number;
    ast: PTree | null;
    state: State | null;
    memos: Memo[];
    constructor(inputs: string, pos: number, epos: number) {
        this.x = inputs;
        this.pos = pos;
        this.epos = epos;
        this.headpos = pos
        this.ast = null
        this.state = null
        this.memos = [];
        for (var i = 0; i < 1789; i += 1) {
            this.memos.push(new Memo());
        }
    }
}

class Memo {
    key: number;
    pos: number;
    ast: PTree | null;
    result: boolean;
    constructor() {
        this.key = -1
        this.pos = 0
        this.ast = null
        this.result = false
    }
}

class State {
    sid: number;
    val: any;
    prev: State | null;
    constructor(sid: number, val: any, prev: State | null) {
        this.sid = sid;
        this.val = val;
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
    return state;
}

// Generator

const match_empty = (px: PContext) => true

const match_any = (px: PContext) => {
    if (px.pos < px.epos) {
        px.pos += 1
        return true
    }
    return false;
}

const match_trie = (px: PContext, d: any): boolean => {
    if (px.pos >= px.epos) {
        return false
    }
    if (!Array.isArray(d)) {
        const c = px.x[px.pos];
        if (c in d) {
            px.pos += 1;
            const s = d[c];
            if (typeof s === 'string') {
                if (px.x.startsWith(s, px.pos)) {
                    px.pos += len(s)
                    return true
                }
                return false;
            }
            return match_trie(px, s);
        }
        return false;
    }
    else {
        const inputs = px.x;
        const pos = px.pos;
        for (const s of d) {
            if (inputs.startsWith(s, pos)) {
                px.pos += len(s)
                return true
            }
        }
        return false;
    }
}


class Generator {
    peg: Grammar | null;
    generated: { [key: string]: (px: PContext) => boolean }
    generating_nonterminal: string;
    cache: { [key: string]: (px: PContext) => boolean }
    sids: { [key: string]: number }
    bitmaps: { [key: string]: Uint8Array };

    constructor() {
        this.peg = null
        this.generated = {}
        this.generating_nonterminal = ''
        this.cache = { '': match_empty }
        this.sids = {}
        this.bitmaps = {}
    }

    getsid(name: any) {
        name = name.toString();
        if (!(name in this.sids)) {
            this.sids[name] = len(Object.keys(this.sids))
        }
        return this.sids[name];
    }

    generate(peg: Grammar, options: any = {}) {
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
        const pf = this.generated[start.uname()]

        const parse = (inputs: string, options: any = {}) => {
            const pos: number = options.pos || options.spos || 0;
            const epos: number = options.epos || (len(inputs) - pos);
            const px = new PContext(inputs, pos, epos);
            if (pf(px)) {
                if (!px.ast) {
                    px.ast = new PTree(null, "", pos, px.pos, null);
                }
            }
            else {
                px.ast = new PTree(null, "err", px.headpos, px.headpos, null);
            }
            const conv: ((t: PTree, urn: string, inputs: string) => any) = options.conv || PTree2ParseTree;
            const urn = options.urn || UNKNOWN_URN;
            return conv(px.ast!, urn, inputs);
        }
        return parse
    }

    emit(pe: PExpr, step: number): ((px: PContext) => boolean) {
        //var pe = inline(pe) FIXME
        const cname = pe.cname()
        const f = (this as any)[cname];
        if (cname in (this as any)) {
            return (this as any)[cname](pe, step);
        }
        console.log('@TODO(Generator)', cname, pe)
        return match_empty
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
        return match_any
    }

    PChar(pe: PChar, step: number) {
        if (pe.text in this.cache) {
            return this.cache[pe.text]
        }
        const chars = pe.text
        const clen = len(pe.text)
        //
        this.cache[pe.text] = (px: PContext) => {
            if (px.x.startsWith(chars, px.pos)) {
                px.pos += clen
                return true
            }
            return false
        }
        return this.cache[pe.text];
    }

    //     def ManyChar(self, pe, step):
    //         chars = pe.text
    //     clen = len(pe.text)
    //     #
    //     def match_manychar(px):
    //         while px.x.startswith(chars, px.pos):
    //         px.pos += clen
    // return true
    // return match_manychar

    // def AndChar(self, pe, step):
    // chars = pe.text
    // def match_andchar(px):
    // return px.x.startswith(chars, px.pos)
    // return match_andchar

    // def NotChar(self, pe, step):
    // chars = pe.text
    // def match_notchar(px):
    // return not px.x.startswith(chars, px.pos)
    // return match_notchar

    PRange(pe: PRange, step: number) {
        const key = pe.toString();
        if (!(key in this.bitmaps)) {
            this.bitmaps[key] = range_bitmap(pe.chars, pe.ranges);
        }
        const bitmap = this.bitmaps[key];
        return (px: PContext) => {
            if (px.pos < px.epos) {
                const c = px.x.charCodeAt(px.pos);
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


    // def ManyRange(self, pe, step):
    // bitset = unique_range(pe.chars, pe.ranges) // >> offset

    // def match_manybitset(px):
    // while px.pos < px.epos:
    //     shift = ord(px.x[px.pos]) // - offset
    // if shift >= 0 and(bitset & (1 << shift)) != 0:
    // px.pos += 1
    // continue

    // return false
    // return match_bitset

    // def AndRange(self, pe, step):
    // bitset = unique_range(pe.chars, pe.ranges) // >> offset

    // def match_andbitset(px):
    // if px.pos < px.epos:
    //     shift = ord(px.x[px.pos]) // - offset
    // if shift >= 0 and(bitset & (1 << shift)) != 0:
    // return true
    // return false
    // return match_bitset

    // def NotRange(self, pe, step):
    // bitset = unique_range(pe.chars, pe.ranges) // >> offset

    // def match_notbitset(px):
    // if px.pos < px.epos:
    //     shift = ord(px.x[px.pos]) // - offset
    // if shift >= 0 and(bitset & (1 << shift)) != 0:
    // return false
    // return true
    // return match_notbitset

    PAnd(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            const pos = px.pos
            if (pf(px)) {
                px.headpos = Math.max(px.pos, px.headpos)
                px.pos = pos
                return true
            }
            return false
        }
    }

    PNot(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            const pos = px.pos
            const ast = px.ast
            if (!pf(px)) {
                px.headpos = Math.max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
                return true
            }
            return false
        }
    }

    PMany(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            var pos = px.pos
            var ast = px.ast
            while (pf(px) && pos < px.pos) {
                pos = px.pos
                ast = px.ast
            }
            px.headpos = Math.max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return true
        }
    }

    PMany1(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            if (!pf(px)) {
                return false;
            }
            var pos = px.pos
            var ast = px.ast
            while (pf(px) && pos < px.pos) {
                pos = px.pos
                ast = px.ast
            }
            px.headpos = Math.max(px.pos, px.headpos)
            px.pos = pos
            px.ast = ast
            return true
        }
    }

    POption(pe: PUnary, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            const pos = px.pos
            const ast = px.ast
            if (!pf(px)) {
                px.headpos = Math.max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
            }
            return true
        }
    }

    PSeq(pe: PTuple, step: number) {
        const pfs = pe.es.map(e => this.emit(e, step))
        return (px: PContext) => {
            for (const pf of pfs) {
                if (!pf(px)) {
                    return false;
                }
            }
            return true;
        }
    }

    POre(pe: PTuple, step: number) {
        const pfs = pe.es.map(e => this.emit(e, step))

        return (px: PContext) => {
            const pos = px.pos
            const ast = px.ast
            for (const pf of pfs) {
                if (pf(px)) {
                    return true;
                }
                px.headpos = Math.max(px.pos, px.headpos)
                px.pos = pos
                px.ast = ast
            }
            return false;
        }
    }

    // // Ore
    // def Ore(self, pe: Ore, step):
    // // pe2 = Ore.expand(pe)
    // // if not isinstance(pe2, Ore):
    // //     return this.emit(pe2)
    // // pe = pe2
    // if pe.isDict():
    //     dic = pe.trieDict()
    // DEBUG('DIC', dic)
    // return lambda px: match_trie(px, dic)

    // pfs = tuple(map(lambda e: this.emit(e, step), pe))

    // def match_ore(px):
    // pos = px.pos
    // ast = px.ast
    // f || pf in pfs:
    // if pf(px):
    //     return true
    // px.headpos = max(px.pos, px.headpos)
    // px.pos = pos
    // px.ast = ast
    // return false

    PAlt(pe: PTuple, step: number) {
        return this.POre(pe, step);
    }

    PRef(pe: PRef, step: number) {
        const uname = pe.uname();
        const generated = this.generated;
        if (!(uname in generated)) {
            this.generated[uname] = (px) => generated[uname](px);
        }
        return generated[uname];
    }

    PNode(pe: PNode, step: number) {
        const pf = this.emit(pe.e, step);
        const tag = pe.tag;

        return (px: PContext) => {
            const pos = px.pos
            const prev = px.ast
            px.ast = null;
            if (pf(px)) {
                px.ast = new PTree(prev, tag, pos, px.pos, px.ast);
                return true;
            }
            return false;
        }
    }

    PEdge(pe: PEdge, step: number) {
        const pf = this.emit(pe.e, step);
        const edge = pe.edge;
        if (edge === '') {
            return pf;
        }
        return (px: PContext) => {
            const pos = px.pos
            const prev = px.ast
            px.ast = null;
            if (pf(px)) {
                px.ast = new PTree(prev, edge, pos, -px.pos, px.ast);
                return true;
            }
            return false;
        }
    }

    PFold(pe: PFold, step: number) {
        const pf = this.emit(pe.e, step);
        const tag = pe.tag;
        const edge = pe.edge;
        return (px: PContext) => {
            const pos = px.pos
            var pt = px.ast;
            const prev = pt ? pt.prev : null;
            pt = pt ? (prev ? new PTree(null, pt.tag, pt.epos, pt.epos, pt.child) : pt) : null;
            px.ast = edge !== '' ? new PTree(null, edge, pos, -pos, pt) : pt;
            if (pf(px)) {
                px.ast = new PTree(prev, tag, pos, px.pos, px.ast);
                return true;
            }
            return false;
        }
    }

    PAbs(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            const ast = px.ast
            if (pf(px)) {
                px.ast = ast;
                return true;
            }
            return false;
        }
    }

    // StateTable

    // def adddict(px, s):
    //     if len(s) == 0:
    //         return
    //     key = s[0]
    //     if key in px.memo:
    //         l = px.memo[key]
    //         slen = len(s)
    //         f || i in range(len(l)):
    //             if slen > len(l[i]):
    //                 l.insert(i, s)
    //                 return
    //         l.push(s)
    //     else:
    //         px.memo[key] = [s]

    // def Lazy(self, pe, step): // @lazy(A)
    // name = pe.e.name
    // peg = this.peg
    // return peg.newRef(name).gen(** option) if name in peg else pe.e.gen(** option)

    Skip(pe: PAction, step: number) { // @skip()
        return (px: PContext) => {
            px.pos = Math.min(px.headpos, px.epos)
            return true
        }
    }

    Symbol(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        const sid = this.getsid(pe.params[0]);
        return (px: PContext) => {
            const pos = px.pos;
            if (pf(px)) {
                px.state = new State(sid, px.x.substring(pos, px.pos), px.state);
                return true;
            }
            return false;
        }
    }

    Scope(pe: PAction, step: number) {
        const pf = this.emit(pe.e, step);
        return (px: PContext) => {
            const pos = px.pos;
            const state = px.state;
            if (pf(px)) {
                px.state = state;
                return true;
            }
            return false;
        }
    }

    Exists(pe: PAction, step: number) {
        const sid = this.getsid(pe.params[0]);
        return (px: PContext) => {
            return getstate(px.state, sid) !== null;
        }
    }

    Match(pe: PAction, step: number) {
        const sid = this.getsid(pe.params[0]);
        return (px: PContext) => {
            const state = getstate(px.state, sid);
            if (state !== null && px.x.startsWith(state.val, px.pos)) {
                px.pos += len(state.val);
                return true;
            }
            return false;
        }
    }

    // def Def(self, pe, step):
    // params = pe.params
    // name = str(params[0])
    // pf = this.emit(pe.e, step)

    // def define_dict(px):
    // pos = px.pos
    // if pf(px):
    //     s = px.x[pos: px.pos]
    // if len(s) == 0:
    //     return true
    // if name in px.memo:
    //     d = px.memo[name]
    // else:
    // d = {}
    // px.memo[name] = d
    // key = s[0]
    // if not key in d:
    // d[key] = [s]
    // return true
    // l = d[key]
    // slen = len(s)
    // f || i in range(len(l)):
    // if slen > len(l[i]):
    //     l.insert(i, s)
    // break
    // return true
    // return false
    // return define_dict

    // def In(self, pe, step): // @in (NAME)
    // name = str(params[0])

    // def refdict(px):
    // if name in px.memo && px.pos < px.epos:
    //     d = px.memo[name]
    // key = px.x[px.pos]
    // if key in d:
    //     f || s in d[key]:
    // if px.x.startswith(s, px.pos):
    //     px.pos += len(s)
    // return true
    // return false
    // return refdict

    // '''
    // if fname == 'on': // @on(!A, e)
    //     name = str(params[0])
    // pf = pe.e.gen(** option)
    // if name.startswith('!'):
    //     sid = getsid(name[1:])

    // def off(px):
    // state = px.state
    // px.state = State(sid, false, px.state)
    // res = pf(px)
    // px.state = state
    // return res
    // return off

    //             else:
    // sid = getsid(name[1:])

    // def on(px):
    // state = px.state
    // px.state = State(sid, false, px.state)
    // res = pf(px)
    // px.state = state
    // return res
    // return on

    // if fname == 'if': // @if (A)
    //     sid = getsid(str(params[0]))

    // def cond(px):
    // state = getstate(px.state, sid)
    // return state != null && state.val
    // return cond
    // '''

    // generat || = Generator()

}
const gen = new Generator();

const generate = (peg: Grammar, options: any = {}) => {
    return gen.generate(peg, options);
}

// ParseTree

const UNKNOWN_URN = '(unknown source)'

// def rowcol(urn, inputs, spos):
// inputs = inputs[: spos + (1 if len(inputs) > spos else 0)]
// rows = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
// return urn, spos, len(rows), len(rows[-1]) - 1


// def nop(s): return s


type TPEGExpr = {
    e: ParseTree
    name: ParseTree
    names: ParseTree
}

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
                for (const name of stmt.get('names')) {
                    this.peg.examples.push([name, doc]);
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
        const tag = t.gettag()
        return (this as any)[tag](t);
    }

    static unquote(s: string, pos: number, sb: string[]) {
        if (!s.startsWith('\\', pos)) {
            sb.push(s[pos]);
            return pos + 1;
        }
        if ((s.startsWith('\\x') || s.startsWith('\\X')) && len(s) - pos >= 4) {
            const c = Number.parseInt(s.substring(pos + 2, pos + 4), 16);
            sb.push(String.fromCharCode(c));
            return pos + 4;
        }
        if ((s.startsWith('\\u') || s.startsWith('\\U')) && len(s) - pos >= 6) {
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

    Char(t: ParseTree | TPEGExpr) {
        const s = str(t);
        const sb: string[] = []
        var pos = 0;
        while (pos < len(s)) {
            pos = TPEGLoader.unquote(s, pos, sb)
        }
        return pChar(sb.join(''));
    }

    Class(t: ParseTree) {
        const s = str(t);
        const chars: string[] = []
        const ranges: string[] = []
        var pos = 0;
        while (pos < len(s)) {
            pos = TPEGLoader.unquote(s, pos, chars);
            if (s.startsWith("-", pos)) {
                ranges.push(chars.pop()!);
                pos = TPEGLoader.unquote(s, pos, ranges);
            }
        }
        if (len(chars) == 1 && len(ranges) == 0) {
            return pChar(chars.join(''));
        }
        return pRange(chars.join(''), ranges.join(''))
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

    Many(t: TPEGExpr) {
        return pMany(this.conv(t.e))
    }

    Many1(t: TPEGExpr) {
        return pMany1(this.conv(t.e))
    }

    Option(t: TPEGExpr) {
        return pOption(this.conv(t.e))
    }

    And(t: TPEGExpr) {
        return pAnd(this.conv(t.e))
    }

    Not(t: TPEGExpr) {
        return pNot(this.conv(t.e))
    }

    Seq(t: ParseTree) {
        return pSeq(...t.subNodes().map(p => this.conv(p)))
    }

    Ore(t: ParseTree) {
        return pOre(...t.subNodes().map(p => this.conv(p)))
    }

    Alt(t: ParseTree) {
        return pOre(...t.subNodes().map(p => this.conv(p)))
    }

    Node(t: ParseTree | any) {
        const tag = str(t.tag)
        const e = this.conv(t.e)
        return pNode(e, tag, 0)
    }

    Edge(t: ParseTree | any) {
        const edge = str(t.edge)
        const e = this.conv(t.e)
        return pEdge(edge, e)
    }

    Fold(t: ParseTree | any) {
        const edge = str(t.edge)
        const tag = str(t.tag)
        const e = this.conv(t.e)
        return pFold(edge, e, tag, 0)
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

    // static fileName(e) {
    //     s = str(e)
    //     return s[1: -1]// if s.startswith('"') else s
    // }

    //     @classmethod
    //     def choice(cls, urn, es):
    //         ds = set()
    //     f || e in es:
    // file = TPEGLoader.fileName(e)
    // file = Path(urn).parent / file
    // with file.open(encoding = 'utf-8_sig') as f:
    // ss = [x.strip('\r\n') f || x in f.readlines()]
    // ds |= { x f|| x in ss if len(x) > 0 && not x.startswith('#') }
    // choice = [Char(x) f || x in sorted(ds, key = lambda x: len(x))[:: -1]]
    // return Ore(* choice)

    // @classmethod
    // def choiceN(cls, urn, n, es):
    // ds = set()
    // f || e in es:
    // file = TPEGLoader.fileName(e)
    // file = Path(urn).parent / file
    // with file.open(encoding = 'utf-8_sig') as f:
    // ss = [x.strip('\r\n') f || x in f.readlines()]
    // if n == 0:
    //     ds |= { x f|| x in ss if len(x) > 9 && not x.startswith('#') }
    // else:
    // ds |= { x f|| x in ss if len(x) == n && not x.startswith('#') }
    // choice = [Char(x) f || x in ds]
    // return Ore(* choice)
}


//def grammar_factory():

const logger = (type: string, pos: ParseTree, msg: string) => {
    console.log(pos.showing(msg));
}

const TPEGGrammar = TPEG();
const pegparser = generate_pasm(TPEGGrammar, 'Start');

const load_grammar = (peg: Grammar, source: string, options: any = {}) => {
    const t = pegparser(source);
    const pconv = new TPEGLoader(peg);
    pconv.load(t);
    return peg;
}

const example = (start: string, input: string) => {
    const p = generate_pasm(TPEGGrammar, start);
    const t = p(input)
    console.log(t.dump())
    //console.log(`${t}`)
}

example('S', '  ')
example('NAME', 'Aa')
example('Identifier', 'Aa')
example('Expression', 'Aa')
example('Expression', 'a a a')

const peg = load_grammar(new Grammar(), `
A = 'a'
`)
console.log(peg);
