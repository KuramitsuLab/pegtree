import os

# Option
DebugFlag = 'DEBUG' in os.environ
VerboseFlag = 'VERBOSE' in os.environ
istty = True


def DEBUG(*x):
    if DebugFlag:
        print('DEBUG', *x)


def VERBOSE(*x):
    if DebugFlag:
        print(*x)


COLOR = {
    "Black": '0;30', "DarkGray": '1;30',
    "Red": '0;31', "LightRed": '1;31',
    "Green": '0;32', "LightGreen": '1;32',
    "Orange": '0;33', "Yellow": '1;33',
    "Blue": '0;34', "LightBlue": '1;34',
    "Purple": '0;35', "LightPurple": '1;35',
    "Cyan": '0;36', "LightCyan": '1;36',
    "LightGray": '0;37', "White": '1;37',
}

class Terminal(object):
    istty: bool
    def __init__(self):
        self.istty = True

    def bold(self, s):
        return '\033[1m' + str(s) + '\033[0m' if self.istty else str(s)

    def color(self, c, s):
        return '\033[{}m{}\033[0m'.format(COLOR[c], str(s)) + '' if self.istty else str(s)

    def log(type, pos, msg):
        print(pos.message(msg))


DefaultConsole = Terminal()

