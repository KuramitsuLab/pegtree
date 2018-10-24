#!/usr/local/bin/python

# Source

def bytestr(b):
    return b.decode('utf-8') if isinstance(b, bytes) else b

def encode_source(inputs, urn = '(unknown)', pos = 0):
    if isinstance(inputs, bytes):
        return bytes(urn, 'utf-8').ljust(256, b' ') + inputs, pos + 256
    return urn.ljust(256, ' ') + inputs, pos + 256

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
            if s.startswith(b'\\r'):
                return '\r', s[2:]
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
