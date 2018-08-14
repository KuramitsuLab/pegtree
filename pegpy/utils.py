#!/usr/local/bin/python

def unquote(s):
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

def unquoteb(s: bytes):
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

def unquote_string(s):
    sb = []
    while len(s) > 0:
        c, s = unquote(s)
        sb.append(c)
    return ''.join(sb)

def unquote_class(s):
    sb = []
    while len(s) > 0:
        c, s = unquote(s)
        if s.startswith('-'):
            c2, s = unquote(s[1:])
            sb.append((c, c2))
        else:
            sb.append(c)
    return sb
