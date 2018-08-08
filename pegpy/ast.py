class ParseTree(object):
    __slots__ = ['tag', 'inputs', 'spos', 'epos', 'child']

    def __init__(self, tag, inputs, spos, epos, child):
        self.tag = tag
        self.inputs = inputs
        self.spos = spos
        self.epos = epos
        self.child = child

    def __len__(self):
        c = 0
        cur = self.child
        while(cur is not None):
            c += 1
            cur = cur.prev
        return c

    def __eq__(self, other):
        return self.tag == other

    def __getitem__(self, label):
        cur = self.child
        if isinstance(label, int):
            c = 0
            while (cur is not None):
                if c == label: return cur.child
                c += 1
                cur = cur.prev
        else :
            while(cur is not None):
                if label is cur.tag :return cur.child
                cur = cur.prev
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def strOut(self, sb):
        sb.append("[#")
        sb.append(self.tag)
        c = len(sb)
        for tag, child in self.fields():
            sb.append(' ' if tag is '' else ' ' + tag + '=')
            child.strOut(sb)
        if c == len(sb):
            s = self.inputs[self.spos:self.epos]
            if isinstance(s, str):
                sb.append(" '")
                sb.append(s)
                sb.append("'")
            else:
                sb.append(" ")
                sb.append(str(s))
        sb.append("]")

    def asString(self):
        s = self.inputs[self.spos:self.epos]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def asArray(self):
        a = []
        cur = self.child
        while cur is not None:
            if cur.child is not None:
                a.append(cur.child)
            cur = cur.prev
        a.reverse()
        return a

    def fields(self):
        a = []
        cur = self.child
        while cur is not None:
            if cur.child is not None:
                a.append((cur.tag, cur.child))
            cur = cur.prev
        a.reverse()
        return a

    def asJSON(self, tag = '__class__', hook = None):
        listCount = 0
        cur = self.child
        while cur is not None:
            if cur.tag is not None and len(cur.tag) > 0:
                listCount = -1
                break
            listCount += 1
            cur = cur.prev
        if listCount == 0:
            return self.asString() if hook is None else hook(self)
        if listCount == -1:
            d = {}
            if self.tag is not None and len(self.tag) > 0:
                d[tag] = self.tag
            cur = self.child
            while cur is not None:
                if not cur.tag in d:
                    d[cur.tag] = cur.child.asJSON(tag, hook)
                cur = cur.prev
            return d
        else:
            return self.asArray()

class TreeLink(object):
    __slots__ = ['tag', 'child', 'prev']

    def __init__(self, tag, child, prev):
        self.tag = tag
        self.child = child
        self.prev = prev

    def strOut(self, sb):
        sb.append('@@@@ FIXME @@@@')

## Source

def encode_source(inputs, urn = '(unknown)', pos = 0):
    if isinstance(inputs, bytes):
        return bytes(urn, 'utf-8').ljust(256, b' ') + inputs, pos + 256
    return urn.ljust(256, ' ') + inputs, pos + 256

def bytestr(b):
    return b.decode('utf-8') if isinstance(b, bytes) else b

def decode_source(inputs, spos, epos):
    urn = inputs[0:256].strip()
    inputs = inputs[256:]
    spos -= 256
    epos -= 256
    ls = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
    pos = spos
    c = 1
    for l in ls:
        length = len(l) + 1
        if pos < length:
            line = l
            linenum = c
            break
        pos =- length
        c += 1
    epos = pos + (epos - spos)
    length = len(line) - pos if len(line) < epos else epos - pos
    if length <= 0: length = 1
    mark = (' ' * pos) + ('^' * length)
    return (bytestr(urn), spos, linenum, pos, bytestr(line), mark)

class SourcePosition(object):
    def __init__(self, inputs, spos, epos):
        self.pos = (inputs, spos, epos)

    def pos(self):
        return decode_source(self.pos[0], self.pos[1], self.pos[2])

class TreeConv(object):
    def __init__(self, *args):
        self.dict = {}
        for c in args: self.dict[c.__name__] = c

    def conv(self, t):
        tag = t.tag
        if hasattr(self, tag):
            f = getattr(self, tag)
            return self.pos(f(t), t)
        if tag in self.dict:
            c = self.dict[tag]
            if len(t) == 0:
                return self.pos(c(t.asString()),t)
            else :
                d = {}
                for name in c.__slots__:
                    sub = t[name]
                    if sub is None:
                        raise NameError(name)
                    d[name] = self.conv(sub)
                return self.pos(c(**d), t)
        return t.asJSON()

    def pos(self, s, t):
        if isinstance(s, SourcePosition):
            s.pos = (t.inputs, t.spos, t.epos)
        return s
