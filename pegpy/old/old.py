def setup_loader():
    class PEGConv(TreeConv):
        def __init__(self, *args):
            super(PEGConv, self).__init__(*args)

        def Empty(self, t):
            return EMPTY

        def Any(self, t):
            return ANY

        def Char(self, t):
            s = t.asString()
            if s.find(r'\x') >= 0:
                sb = []
                s = s.encode('utf-8')
                while len(s) > 0:
                    c, s = u.unquote(bytes(s, 'ascii'))
                    sb.append(c)
                return pe(b''.join(sb))
            else:
                sb = []
                while len(s) > 0:
                    c, s = u.unquote(s)
                    sb.append(c)
                return pe(''.join(sb))

        def Class(self, t):
            s = t.asString()
            sb = []
            while len(s) > 0:
                c, s = u.unquote(s)
                if s.startswith('-') and len(s) > 2:
                    c2, s = u.unquote(s[1:])
                    sb.append((c, c2))
                else:
                    sb.append(c)
            return Range(sb)

        def Fold(self, t):
            left = t['left'].asString() if t.has('left') else ''
            name = t['name'].asString() if t.has('name') else ''
            inner = self.conv(t['inner'])
            return FoldAs(left, name, inner)

    PEGconv = PEGConv(Ore, Alt, Seq, And, Not, Many, Many1, TreeAs, FoldAs, LinkAs, Ref)
    pegparser = pegp(tpeg())

    def load(self, path):
        f = open(path)
        data = f.read()
        f.close()
        # print('@@', data)
        t = pegparser(data, path)
        # print('@@', pegparser(data))
        # load
        for stmt in t.asArray():
            if stmt == 'Rule':
                name = stmt['name'].asString()
                pexr = stmt['inner']
                # print(name, '\n\t', pexr, '\n\t', pexr.asJSON())
                print(name, PEGconv.conv(pexr))
    PEG.load = load

#setup_loader()
