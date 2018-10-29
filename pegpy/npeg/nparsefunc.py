import pegpy.gpeg.gparsefunc as gparsefunc

def isCharRange(inputs, pos, ranges, strs, maxlength):
    c = inputs[pos]
    for r in ranges:
        if r[0] <= c and c <= r[1]:
            return (True, 1)
    for s in strs:
        length = len(s)
        if pos + length - 1 < maxlength:
            if inputs[pos:(pos+length)] == s:
                return (True, length)
    return (False, 0)


def emit_NCharRange(pe):
    chars = pe.chars
    ranges = pe.ranges

    def curry(px):
        if px.pos < px.length:
          (res, move) = isCharRange(px.inputs, px.pos, ranges, chars, px.length)
          if res:
            px.pos += move
            px.headpos = max(px.pos, px.headpos)
            return True
        return False
    return gparsefunc.mresult(curry)
