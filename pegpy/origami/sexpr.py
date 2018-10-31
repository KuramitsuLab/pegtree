import pegpy.utils as u

## SExpression

class SExpr(object):
    ORIGAMI = {
        'Unary': 'name expr',
        'Infix': 'name left right',
        'IntExpr': lambda t: int(t.asString())
    }
    @classmethod
    def of(cls, t, intern, conv = ORIGAMI):
        if t is None: return SExprList(())
        key = t.tag
        if len(t) == 0 :
            if key in conv:
                return SExprAtom(conv[key](t), t.pos3())
            else:
                return SExprAtom(intern(t.asString()), t.pos3())
        else:
            lconv = conv[key] if key in conv else None
            cons = []
            if isinstance(lconv, str):
                for name in lconv.split():
                    if name.startswith('#'):
                        cons.append(SExprAtom(intern(name[1:]), t.pos3()))
                    else:
                        cons.append(SExpr.of(t[name], intern, conv))
                return SExprList(cons)
            else:
                cons.append(SExprAtom(intern(key.lower()), t.pos3()))
                for n, v in t:
                    cons.append(SExpr.of(v, intern, conv))
                return SExprList(cons)

    @classmethod
    def new(cls, s):
        """
        >>> parse_sexp("(+ 5 (+ 3 5))")
        [['+', '5', ['+', '3', '5']]]
        """
        sexp = [[]]
        word = ''
        in_str = False
        for char in s:
            if char == '(' and not in_str:
                sexp.append([])
            elif char == ')' and not in_str:
                if word:
                    sexp[-1].append(word)
                    word = ''
                temp = sexp.pop()
                sexp[-1].append(temp)
            elif char in (' ', '\n', '\t') and not in_str:
                if word:
                    sexp[-1].append(word)
                    word = ''
            elif char == '\"':
                in_str = not in_str
            else:
                word += char
        return sexp[0]

class SExprAtom(SExpr):
    __slots__ = ['data', 'pos3', 'ty']
    def __init__(self, data, pos3 = None, ty = None):
        self.data = data
        self.pos3 = pos3
        self.ty = ty
    def __str__(self):
        return str(self.data)

class SExprList(SExpr):
    __slots__ = ['data', 'ty']
    def __init__(self, data, ty = None):
        self.data = tuple(data)
        self.ty = ty
    def __str__(self):
        return '(' + (' '.join(map(str, self.data))) + ')'


def sconv(t):
    intern = u.string_intern()
    return SExpr.of(t, intern)

