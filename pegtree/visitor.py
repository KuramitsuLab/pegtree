from .tree import ParseTree

from logging import getLogger
logger = getLogger(__name__)


class ParseTreeVisitor(object):
    def __init__(self, methods=None):
        self.methods = methods if methods is not None else {}

    def visit(self, tree: ParseTree):
        tag = tree.getTag()
        methods = self.methods
        if tag not in methods:
            methods[tag] = f'accept{tag}'
        method = methods[tag]
        if hasattr(self, method):
            method = getattr(self, method)
            return method(tree)
        else:
            return self.acceptUndefined(tree)

    def acceptUndefined(self, tree):
        logger.warning(
            f'(@TODO) undefined accept{tree.getTag()} method for {repr(tree)}')
        return None

    def TODO(self, msg, tree):
        logger.warning(f'(@TODO) {msg} for {repr(tree)}')

    def perror(self, ptree, msg='syntax error'):
        logger.error(ptree.message(msg))

    def warning(self, ptree, msg):
        logger.warning(ptree.message(msg))


class JSONfy(ParseTreeVisitor):
    def __init__(self, parser):
        ParseTreeVisitor.__init__(self, None)
        self.parser = parser

    def convert(self, source):
        tree = self.parser(source)
        value = self.visit(tree)
        return value

    def acceptDict(self, tree):
        adict = {}
        keys = tree.keys()
        for key in keys:
            adict[key] = self.visit(tree[key])
        return adict

    def acceptList(self, tree):
        alist = []
        for subtree in tree:
            alist.append(self.visit(subtree))
        return alist

    def acceptPair(self, tree):
        return [self.visit(tree[0]), self.visit(tree[1])]

    def acceptInt(self, tree):
        token = tree.getToken()
        return int(token)

    def acceptFloat(self, tree):
        token = tree.getToken()
        return float(token)

    def acceptString(self, tree):
        token = tree.getToken()
        if (token.startswith('"') or token.startswith("'")) and len(token) > 2 and token.endswith(token[0]):
            token = token[1:-1].encode().decode("unicode-escape")
        return str(token)

    def acceptBoolean(self, tree):
        token = tree.getToken()
        if token.lower() == 'true':
            return True
        return False

    def acceptUndefined(self, tree):
        if len(tree) == 0:
            token = tree.getToken()
            if token.count('.') == 1 and token.replace('.', '').isdigit():
                return self.acceptFloat(tree)
            if token.isdigit():
                return self.acceptInt(tree)
            return self.acceptString(tree)
        keys = tree.keys()
        adict = self.acceptDict(tree)
        alist = self.acceptDict(tree)
        if len(adict) == 0:
            return [f'#{tree.getTag}'] + alist
        if len(alist) > 0:
            adict['list'] = alist
        adict['tag'] = f'#{tree.getTag}'
        return adict


class JSONTree(ParseTreeVisitor):
    def __init__(self, parser):
        ParseTreeVisitor.__init__(self, None)
        self.parser = parser

    def convert(self, source):
        tree = self.parser(source)
        value = self.visit(tree)
        return value

    def acceptUndefined(self, tree):
        if len(tree) == 0:
            token = tree.getToken()
            return (token, f'#{tree.getTag()}', tree.spos_, tree.epos_)
        alist = []
        for subtree in tree:
            alist.append(self.acceptUndefined(subtree))
        keys = tree.keys()
        if len(keys) > 0:
            adict = {}
            adict['@tag'] = f'#{tree.getTag()}'
            if len(alist) > 0:
                adict['@list'] = alist
            for key in keys:
                adict[key] = self.acceptUndefined(tree[key])
            return adict
        return alist + [f'#{tree.getTag()}']
