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

def kp_options(segment):
    """Return the ways to type segment on dirkeypad1"""
    sequence = dirkeypad_paths(segment)
    result = ['']
    for options in sequence:
        newresult = []
        for p in options:
            for r in result:
                newresult.append(r + p)
        result = newresult
    return result

def shortest_paths(start, end):
    """Shortest paths on the numeric keypad"""
    results = []
    l0paths = paths(numkeypad, start, end)
    print("L0", l0paths)
    for path in l0paths:
        l1paths = kp_options(path)
        print("L1", l1paths)
        for option in l1paths:
            l2paths = kp_options(option)
            print("L2", l2paths)
            for path in l2paths:
                results.append(path)
        print()

    print("Results", len(results))
    print(results)
    minlen = min(len(r) for r in results)
    results = [r for r in results if len(r) == minlen]
    for r in results:
        assert len(r) == minlen, (r, minlen, results, [len(i) for i in results])
    print([len(r) for r in results])
    return results

def shortpath(code):
    pos = numkeypad.find('A')
    r = ''
    for c in code:
        print(c)
        n = numkeypad.find(c)
        paths = shortest_paths(pos, n)
        r = r + paths[0]
        pos = n
    return r

def complexity(code, seqlen):
    return int(code[:-1]) * seqlen

result = 0
for code in data:
    print(code)
    path = shortpath(code)
    print(path, len(path))
    c = complexity(code, len(path))
    result += c
    print(c)
    print()
print(result)
