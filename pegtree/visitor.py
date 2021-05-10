from .tree import ParseTree

from logging import getLogger
logger = getLogger(__name__)

class Visitor(object):
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
            logger.warning(
                f'@TODO undefined {method} method for {repr(tree)}')
            return self.acceptUndefined(tree)

    def acceptUndefined(self, tree):
        return None

    def TODO(self, msg, tree):
        logger.warning(f'@TODO {msg} for {repr(tree)}')

    def perror(self, ptree, msg='syntax error'):
        logger.error(ptree.message(msg))

    def warning(self, ptree, msg):
        logger.warning(ptree.message(msg))
