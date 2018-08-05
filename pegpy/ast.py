
class ParseTree(object):
    __slots__ = ['tag', 'inputs', 'spos', 'epos', 'child']

    def __init__(self, tag, inputs, spos, epos, child):
        self.tag = tag
        self.inputs = inputs
        self.spos = spos
        self.epos = epos
        self.child = child

    def __str__(self):
        sb = []
        self.strOut(sb)
        return "".join(sb)

    def strOut(self, sb):
        sb.append("[#")
        sb.append(self.tag)
        c = len(sb)
        cur = self.child
        while cur != None:
            cur.strOut(sb)
            cur = cur.prev
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

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        c = 0
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

    def asArray(self):
        a = []
        if self.child is not None:
            self.child.toArray(a)
        return a

class TreeLink(object):
    __slots__ = ['tag', 'child', 'prev']

    def __init__(self, tag, child, prev):
        self.tag = tag
        self.child = child
        self.prev = prev

    def strOut(self, sb):
        if self.child != None:
            if self.tag != None:
                ttag = '' if self.tag == '' else self.tag + "="
                sb.append(" " + ttag)
            self.child.strOut(sb)

    def toArray(self, a):
        if self.child != None:
            if self.prev != None:
                self.prev.toArray(a)
            if self.tag != None:
                a.append(self.child)

##

