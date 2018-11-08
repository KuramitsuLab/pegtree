## Source

import pegpy.utils as u

class SourcePosition(object):
    def __init__(self, inputs, spos, epos):
        self.pos = (inputs, spos, epos)

    def getpos(self):
        return u.decode_source(self.pos[0], self.pos[1], self.pos[2])

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
        while(cur is not None):
            if label == cur.tag: return cur.child
            cur = cur.prev
        return None

    def __contains__(self, label):
        cur = self.child
        while(cur is not None):
            if label == cur.tag :return True
            cur = cur.prev
        return False

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
        for tag, child in self:
            sb.append(' ' if tag is '' else ' ' + tag + '=')
            child.strOut(sb)
        if c == len(sb):
            s = self.inputs[self.spos:self.epos]
            if isinstance(s, str):
                sb.append(" '")
                sb.append(s)
                sb.append("'")
            elif isinstance(s, bytes):
                sb.append(" '")
                sb.append(s.decode('utf-8'))
                sb.append("'")
            else:
                sb.append(" ")
                sb.append(str(s))
        sb.append("]")

    def get(self, label: str, default = None, conv = None):
        cur = self.child
        while(cur is not None):
            if label == cur.tag:
                return cur.child if conv is None else conv(cur.child)
            cur = cur.prev
        return default

    def isString(self):
        return self.child is None

    def asString(self):
        s = self.inputs[self.spos:self.epos]
        return s.decode('utf-8') if isinstance(s, bytes) else s

    def isArray(self):
        cur = self.child
        while cur is not None:
            if cur.tag is not None and len(cur.tag) > 0:
                return False
            cur = cur.prev
        return True

    def asArray(self):
        a = []
        cur = self.child
        while cur is not None:
            if cur.child is not None:
                a.append(cur.child)
            cur = cur.prev
        a.reverse()
        return a

    def __iter__(self):
        return TreeLinkIter(self.child)

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

    def getpos(self):
        return u.decode_source(self.inputs, self.spos, self.epos)

    def pos3(self):
        return (self.inputs, self.spos, self.epos)

class TreeLink(object):
    __slots__ = ['tag', 'child', 'prev']

    def __init__(self, tag, child, prev):
        self.tag = tag
        self.child = child
        self.prev = prev

    def strOut(self, sb):
        sb.append('@@@@ FIXME @@@@')

class TreeLinkIter(object):
    __slots__ = ['stack']
    def __init__(self, cur: TreeLink):
        self.stack = []
        while cur is not None:
            if cur.child is not None:
                self.stack.append(cur)
            cur = cur.prev

    def __next__(self):
        if len(self.stack) == 0:
            raise StopIteration()
        cur = self.stack.pop()
        return (cur.tag, cur.child)

## TreeConv

class ParseTreeConv(object):
    def __init__(self, *args):
        self.dict = {}
        for c in args: self.dict[c.__name__] = c

    def setpos(self, s, t):
        if isinstance(s, SourcePosition):
            s.pos = (t.inputs, t.spos, t.epos)
        return s

    def conv(self, t: ParseTree):
        tag = t.tag
        if hasattr(self, tag):
            f = getattr(self, tag)
            return self.setpos(f(t), t)
        if tag in self.dict:
            c = self.dict[tag]
            if t.isString():
                return self.setpos(c(t.asString()),t)
            elif t.isArray():
                return self.setpos(c(*t.asArray()), t)
            else :
                d = {}
                for name in c.__slots__:
                    sub = t[name]
                    if sub is None:
                        print ('TODO', name, c)
                        continue
                    d[name] = self.conv(sub)
                return self.setpos(c(**d), t)
        print('@TODO', tag)
        return t

