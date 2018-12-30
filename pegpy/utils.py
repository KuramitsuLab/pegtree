#!/usr/local/bin/python
import sys, os, errno
from pathlib import Path

#bytes

UTF8LEN = [1] * 0xc0 + [2] * (0xe0 - 0xc0) + [3] * (0xf0 - 0xe0) + [4] * (0xff - 0xf0 + 1)

def decode_utf8(inputs: bytes, pos: int):
    return inputs[pos: pos+UTF8LEN[inputs[pos]]].decode('utf-8')

# Source, Pos3

def bytestr(b):
    return b.decode('utf-8') if isinstance(b, bytes) else b

def issrc(s):
    if isinstance(s, bytes):
        return s.startswith(b'\a\b\b\a')
    return s.startswith('\a\b\b\a')

def decsrc(s):
    assert issrc(s)
    head = bytestr(s[4:256].strip())
    inputs = s[256:]
    urn,pos,epos=head.split(',')
    return urn, inputs, int(pos)-256, int(epos)-256

def encsrc(urn, inputs, pos, epos):
    head = '\a\b\b\a{},{},{}'.format(urn, pos, epos)
    if isinstance(inputs, bytes):
        return bytes(head, 'utf-8').ljust(256, b' ') + inputs, pos + 256, epos+256
    return head.ljust(256, ' ') + inputs, pos + 256, epos+256

def encpos3(s, spos, epos):
    assert issrc(s)
    urn, inputs, _, _ = decsrc(s)
    return encsrc(urn, inputs, spos, epos)

def decpos3(s, spos, epos):
    urn, inputs, pos, length  = decsrc(s)
    spos -= 256
    epos -= 256
    lines = inputs.split(b'\n' if isinstance(inputs[:epos], bytes) else '\n')
    linenum = 0
    cols = spos
    for line in lines:
        len0 = len(line) + 1
        linenum += 1
        if cols < len0: break
        cols -= len0
    epos = cols + (epos - spos)
    length = len(line) - cols if len(line) < epos else epos - cols
    if length <= 0: length = 1
    mark = (' ' * cols) + ('^' * length)
    return (urn, spos, linenum, cols, bytestr(line), mark)

'''
def encode_source(inputs, urn = '(unknown)', pos = 0):
    if isinstance(inputs, bytes):
        return bytes(str(urn), 'utf-8').ljust(256, b' ') + inputs, pos + 256
    return urn.ljust(256, ' ') + inputs, pos + 256

def decode_source(inputs, spos, epos):
    token = inputs[spos:epos]
    urn = inputs[0:256].strip()
    inputs = inputs[256:]
    spos -= 256
    epos -= 256
    ls = inputs.split(b'\n' if isinstance(inputs, bytes) else '\n')
    #print('@', spos, ls)
    linenum = 0
    remain = spos
    for line in ls:
        len0 = len(line) + 1
        linenum += 1
        #print('@', linenum, len0, remain, line)
        if remain < len0: break
        remain -= len0
    epos = remain + (epos - spos)
    length = len(line) - remain if len(line) < epos else epos - remain
    if length <= 0: length = 1
    mark = (' ' * remain) + ('^' * length)
    return (bytestr(urn), spos, linenum, remain, bytestr(line), mark)
'''

def serror(pos3, msg='SyntaxError'):
    if pos3 is not None:
        urn, pos, linenum, cols, line, mark = decpos3(pos3[0], pos3[1], pos3[2])
        return '{} ({}:{}:{}+{})\n{}\n{}'.format(msg,urn,linenum,cols,pos, line, mark)
    return '{} (unknown source)'.format(msg)

def perror(pos3, msg='SyntaxError', file = sys.stdout):
    file.write(serror(pos3, msg))
    file.write(os.linesep)


def string_intern():
    d = {}
    def f(s):
        nonlocal d
        if not s in d:
            d[s] = s
        return d[s]
    return f

# quote

def quote_string(e: str, esc ="'"):
    sb = []
    for c in e:
        if c == '\n' : sb.append(r'\n')
        elif c == '\t' : sb.append(r'\t')
        elif c == '\\' : sb.append(r'\\')
        elif c == '\r' : sb.append(r'\r')
        elif c in esc : sb.append('\\' + str(c))
        else: sb.append(c)
    return "".join(sb)

# unquote

def unquote(s):
    if isinstance(s, str):
        if s.startswith('\\'):
            if s.startswith('\\n'):
                return '\n', s[2:]
            if s.startswith('\\t'):
                return '\t', s[2:]
            if s.startswith('\\r'):
                return '\r', s[2:]
            if s.startswith('\\v'):
                return '\v', s[2:]
            if s.startswith('\\f'):
                return '\f', s[2:]
            if s.startswith('\\b'):
                return '\b', s[2:]
            if (s.startswith('\\x') or s.startswith('\\X')) and len(s) > 4:
                c = int(s[2:4], 16)
                return chr(c), s[4:]
            if (s.startswith('\\u') or s.startswith('\\U')) and len(s) > 6:
                c = int(s[2:6], 16)
                return chr(c), s[6:]
            else:
                return s[1], s[2:]
        else:
            return s[0], s[1:]
    else:
        if s.startswith(b'\\'):
            if s.startswith(b'\\n'):
                return '\n', s[2:]
            if s.startswith(b'\\t'):
                return '\t', s[2:]
            if s.startswith(b'\\v'):
                return '\v', s[2:]
            if s.startswith(b'\\r'):
                return '\r', s[2:]
            if s.startswith(b'\\f'):
                return '\f', s[2:]
            if s.startswith(b'\\b'):
                return '\b', s[2:]
            if (s.startswith(b'\\x') or s.startswith(b'\\X')) and len(s) > 4:
                c = bytes.fromhex(s[2:4])
                return c, s[4:]
            if (s.startswith(b'\\u') or s.startswith(b'\\U')) and len(s) > 6:
                c = int(s[2:6], 16)
                return chr(c).encode('utf-8'), s[6:]
            else:
                return s[1], s[2:]
        else:
            return s[0], s[1:]

def unquote_string(s):
    l = []
    while(len(s)>0):
        c, s = unquote(s)
        l.append(c)
    return ''.join(l)

#Path

def find_path(file, subdir='grammar'):
    path = Path(file)
    if path.exists():
        return path
    else:
        path = Path(__file__).resolve().parent / subdir / file
        if path.exists():
            return path
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

def find_importPath(sourcePath, importPath):
    path = Path(importPath)
    if not path.exists():
        path = Path(sourcePath).resolve().parent / importPath
        if not path.exists(): return importPath
    return str(path.absolute())


COLOR = {
    "Black": '0;30', "DarkGray": '1;30',
    "Red": '0;31',     "LightRed": '1;31',
    "Green": '0;32',     "LightGreen": '1;32',
    "Orange": '0;33',     "Yellow": '1;33',
    "Blue": '0;34',     "LightBlue": '1;34',
    "Purple": '0;35',     "LightPurple": '1;35',
    "Cyan": '0;36',     "LightCyan": '1;36',
    "LightGray": '0;37',     "White": '1;37',
}

class Writer(object):
    __slots__ = ['file', 'istty']

    def __init__(self, file = None):
        if file is None:
            self.file = sys.stdout
            self.istty = True
        else:
            self.file = open(file, 'w')
            self.istty = False

    def print(self, *args):
        file = self.file
        if len(args) > 0:
            file.write(str(args[0]))
            for a in args[1:]:
                file.write(' ')
                file.write(str(a))

    def println(self, *args):
        self.print(*args)
        self.file.write(os.linesep)
        self.file.flush()

    def dump(self, o, indent=''):
        if hasattr(o, 'dump'):
            o.dump(self, indent)
        else:
            self.println(o)

    def bold(self, s):
        return '\033[1m' + str(s) + '\033[0m' if self.istty else str(s)

    def c(self, color, s):
        return '\033[{}m{}\033[0m'.format(COLOR[color],str(s)) + '' if self.istty else str(s)

    def perror(self, pos3, msg='SyntaxError'):
        self.println(self.c('Red', serror(pos3, msg)))
