# ParseTree


def rowcol(urn, inputs, spos):
    inputs = inputs[:spos + (1 if len(inputs) > spos else 0)]
    rows = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
    return urn, spos, len(rows), len(rows[-1])-1


def nop(s): return s


UNKNOWN_SOURCE = '(unknown source)'


class ParseTree(list):
    def __init__(self, tag, inputs, spos=0, epos=None, urn=UNKNOWN_SOURCE):
        self.tag_ = tag
        self.inputs_ = inputs
        self.spos_ = spos
        self.epos_ = epos if epos is not None else len(inputs)
        self.urn_ = urn

    def getTag(self):
        return self.tag_

    def __eq__(self, tag):
        return self.tag_ == tag

    def getPosition(self):
        return rowcol(self.urn_, self.inputs_, self.spos_)

    def getEndPosition(self):
        return rowcol(self.urn_, self.inputs_, self.epos_)

    def decode(self):
        inputs, spos, epos = self.inputs_, self.spos_, self.epos_
        LF = b'\n' if isinstance(inputs, bytes) else '\n'
        rows = inputs[:spos + (1 if len(inputs) > spos else 0)]
        rows = rows.split(LF)
        linenum, column = len(rows), len(rows[-1])-1
        begin = inputs.rfind(LF, 0, spos) + 1
        # print('@', spos, begin, inputs)
        end = inputs.find(LF, spos)
        # print('@', spos, begin, inputs)
        if end == -1:
            end = len(inputs)
        # print('@[', begin, spos, end, ']', epos)
        line = inputs[begin:end]  # .replace('\t', '   ')
        mark = []
        endcolumn = column + (epos - spos)
        for i, c in enumerate(line):
            if column <= i and i <= endcolumn:
                mark.append('^' if ord(c) < 256 else '^^')
            else:
                mark.append(' ' if ord(c) < 256 else '  ')
        mark = ''.join(mark)
        return (self.urn_, spos, linenum, column, line, mark)

    def message(self, msg='Syntax Error'):
        urn, pos, linenum, cols, line, mark = self.decode()
        return '{} ({}:{}:{}+{})\n{}\n{}'.format(msg, urn, linenum, cols, pos, line, mark)

    def __eq__(self, tag):
        return self.tag_ == tag

    def isSyntaxError(self):
        return self.tag_ == 'err'

    def keys(self):
        ks = []
        for key in self.__dict__:
            v = self.__dict__[key]
            if isinstance(v, ParseTree):
                ks.append(key)
        return ks

    def subs(self):
        es = []
        for i, child in enumerate(self):
            es.append((child.spos_, '', child))
        for key in self.__dict__:
            v = self.__dict__[key]
            if isinstance(v, ParseTree):
                es.append((v.spos_, key, v))
        es.sort()
        return [(x[1], x[2]) for x in es]

    def isEmpty(self):
        return self.tag_ == 'empty'

    def newEmpty(self):
        return ParseTree('empty', self.inputs_, self.epos_, self.epos_, self.urn_)

    def getNodeSize(self):
        return len(self)

    def getSubNodes(self):
        return list(self)

    def has(self, key):
        if isinstance(key, str):
            return hasattr(self, key) and isinstance(getattr(self, key), ParseTree)
        if isinstance(key, int):
            return key < self.getNodeSize()
        return False

    def get(self, key):
        if not self.has(key):
            return self.newEmpty()
        if isinstance(key, str):
            return getattr(self, key)
        return self[key]

    def set(self, key, tree):
        assert isinstance(tree, ParseTree)
        self.spos_ = min(self.spos_, tree.spos_)
        self.epos_ = min(self.epos_, tree.epos_)
        if key == '':
            self.append(tree)
        else:
            setattr(self, key, tree)

    def getToken(self, key=None, default_token=''):
        if key is None:
            s = self.inputs_[self.spos_:self.epos_]
            return s.decode('utf-8') if isinstance(s, bytes) else s
        return self.get(key).getToken() if self.has(key) else default_token

    def substring(self, start=None, end=None):
        if start is None:
            if end is None:
                return self.getToken()
            s = self.inputs_[end.epos_:self.epos_]
        else:
            if end is None:
                s = self.inputs_[self.spos_: start.spos_]
            else:
                s = self.inputs_[start.epos_:end.spos_]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def __str__(self):
        s = self.inputs_[self.spos_:self.epos_]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def __repr__(self):
        if self.isSyntaxError():
            return self.message('Syntax Error')
        sb = []
        self.strOut(sb, indent='', tab='')
        return "".join(sb)

    def dump(self, indent='\n', tab='  ', tag=nop, edge=nop, token=nop):
        if self.isSyntaxError():
            print(self.message('Syntax Error'))
        else:
            sb = []
            self.strOut(sb, indent, tab, '', tag, edge, token)
            print("".join(sb))

    def strOut(self, sb, indent='\n  ', tab='  ', prefix='', tag=nop, edge=nop, token=nop):
        sb.append(indent + prefix + "[" + tag(f'#{self.getTag()} '))
        subs = self.subs()
        if len(subs) > 0:
            next_indent = indent + tab
            for label, child in subs:
                prefix = edge(label) + ': ' if label != '' else ''
                child.strOut(sb, next_indent, tab, prefix, tag, edge, token)
            sb.append(indent + "]")
        else:
            sb.append(token(repr(str(self))))
            sb.append("]")
