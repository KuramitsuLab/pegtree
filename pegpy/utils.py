#!/usr/local/bin/python

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

