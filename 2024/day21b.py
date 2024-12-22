import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
029A
980A
179A
456A
379A
'''

data = open(os.path.join(os.path.dirname(__file__), "input21.txt")).read()
data = data.strip()
data = data.split('\n')

depth = 25

numkeypad = Grid(["789","456","123"," 0A"])
dirkeypad = Grid([" ^A","<v>"])

memo = {}
def paths(keypad, start, end):
    m = memo.setdefault(id(keypad), {})
    mv = m.get((start, end))
    if mv is not None: return mv
    mv = _paths(keypad, start, end)
    m[(start, end)] = mv
    return mv

def _paths(keypad, start, end):
    diff = end - start
    if diff.x > 0: xmoves = '>' * diff.x
    elif diff.x < 0: xmoves = '<' * (-diff.x)
    else: xmoves = ''
    if diff.y > 0: ymoves = 'v' * diff.y
    elif diff.y < 0: ymoves = '^' * (-diff.y)
    else: ymoves = ''

    if xmoves == '':
        return (ymoves + 'A', )
    if ymoves == '':
        return (xmoves + 'A', )

    if keypad.get(start + Coord(diff.x, 0)) == ' ':
        return (ymoves + xmoves + 'A', )
    if keypad.get(start + Coord(0, diff.y)) == ' ':
        return (xmoves + ymoves + 'A', )
    return (xmoves + ymoves + 'A', ymoves + xmoves + 'A', )

def dirkeypad_paths(segment):
    """Paths to take on a directional keypad to type a segment, starting at position A

    Returns an array of possible paths.

    """
    pos = dirkeypad.find('A')
    r = []
    for c in segment:
        n = dirkeypad.find(c)
        r.append(paths(dirkeypad, pos, n))
        pos = n
    return r

def kp_segment_options(segment):
    """Return the ways to type segment on dirkeypad1"""
    assert segment[-1] == 'A'
    assert 'A' not in segment[:-1], segment
    sequence = dirkeypad_paths(segment)
    result = ['']
    for options in sequence:
        newresult = []
        for p in options:
            for r in result:
                newresult.append(r + p)
        result = newresult
    return result

def segments(path):
    """Split a path ending in A into smallest segments, each ending in A"""
    assert path[-1] == 'A'
    return [s+'A' for s in path.split('A')[:-1]]

memo2 = {}
def cost_single(path, level):
    r = memo.get((path, level))
    if r is not None:
        return r
    if level == 0:
        r = len(path)
    else:
        r = 0
        for segment in segments(path):
            options = kp_segment_options(segment)
            c = cost(options, level - 1)
            r += c
    memo[(path, level)] = r
    print(f"cost_single({level}, {path}) == {r}")
    return r

def cost(paths, level):
    r = min(
        cost_single(path, level)
        for path in paths
    )
    print(f"cost({level}, {paths}) == {r}")
    return r


def shortpath_len(code):
    pos = numkeypad.find('A')
    r = 0
    for c in code:
        print(c)
        n = numkeypad.find(c)
        l0paths = paths(numkeypad, pos, n)
        print(l0paths)
        print(cost(l0paths, depth))
        r += cost(l0paths, depth)
        pos = n
    return r

def complexity(code, seqlen):
    return int(code[:-1]) * seqlen

result = 0
for code in data:
    print(code)
    pathlen = shortpath_len(code)
    print(pathlen)
    c = complexity(code, pathlen)
    result += c
    print(c)
    print()
print(result)
