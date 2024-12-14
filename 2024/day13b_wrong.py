import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple

data = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

# data = open(os.path.join(os.path.dirname(__file__), "input13.txt")).read()
data = data.strip()

Machine = namedtuple('Machine', 'ax ay bx by px py'.split())

def find_offset_and_gap(p, da, db):
    a_offset = None
    a_gap = None
    # Will finish much faster than 10000, but can't be bothered to work out what the maximum is
    for a in range(10000):
        v = p - da * a
        if v % db == 0:
            b = v // db
            if a_offset is None:
                a_offset = a
            else:
                a_gap = a - a_offset
                break
    return a_offset, a_gap
 

def find_solutions(ax_offset, ax_gap, ay_offset, ay_gap):
    # Grid search for possible solutions for M and N
    min_M = None
    for M in range(ay_gap):
        for N in range(ax_gap):
            if ax_offset + M * ax_gap == ay_offset + N * ay_gap:
                print(f"M, N = {M} + k * {ay_gap}, {N} + k * {ax_gap}")
                if min_M is None:
                    min_M = M
    if min_M == 0: return 1
    return min_M


def solve(m):
    print()
    print(f"Finding cost for {m}")
    ax_offset, ax_gap = find_offset_and_gap(m.px, m.ax, m.bx)
    ay_offset, ay_gap = find_offset_and_gap(m.py, m.ay, m.by)
    # print(f"A needs to be pressed {ax_offset} + M * {ax_gap} times")
    # print(f"A needs to be pressed {ay_offset} + N * {ay_gap} times")
    if ax_offset is None or ay_offset is None:
        return 0

    M = find_solutions(ax_offset, ax_gap, ay_offset, ay_gap)
    # print(f"Possible A = {ax_offset} + ({M} + k * {ay_gap}) * {ax_gap}")
    A1 = ax_offset + M * ax_gap
    Ad = ax_gap * ay_gap

    bx_offset, bx_gap = find_offset_and_gap(m.px, m.bx, m.ax)
    by_offset, by_gap = find_offset_and_gap(m.py, m.by, m.ay)
    print(f"B needs to be pressed {bx_offset} + M * {bx_gap} times")
    print(f"B needs to be pressed {by_offset} + N * {by_gap} times")
    if bx_offset is None or by_offset is None:
        return 0

    M = find_solutions(bx_offset, bx_gap, by_offset, by_gap)
    print(f"Possible B = {bx_offset} + ({M} + k * {by_gap}) * {bx_gap}")
    B1 = bx_offset + M * bx_gap
    Bd = bx_gap * by_gap

    print(f"Possible A = {A1} + k * {Ad}")
    print(f"Possible B = {B1} + j * {Bd}")
    # ax * A1 + ax * Ad * k + bx * B1 + bx * Bd * j == px
    # ay * A1 + ay * Ad * k + by * B1 + by * Bd * j == py
    # therefore
    # ax * Ad * k + bx * Bd * j == px - (ax * A1 + bx * B1)
    # ay * Ad * k + by * Bd * j == py - (ay * A1 + by * B1)
    Kxmult = m.ax * Ad
    Kymult = m.ay * Ad
    Jxmult = m.bx * Bd
    Jymult = m.by * Bd
    Zx = m.px - (m.ax * A1 + m.bx * B1)
    Zy = m.py - (m.ay * A1 + m.by * B1)
    print(f"{Kxmult} * k + {Jxmult} * j == {Zx}")
    print(f"{Kymult} * k + {Jymult} * j == {Zy}")
    if  (Zx * Jymult - Zy * Jxmult) % (Kxmult * Jymult - Kymult * Jxmult) != 0:
        print("Solution not an integer")
        return 0
    k = (Zx * Jymult - Zy * Jxmult) // (Kxmult * Jymult - Kymult * Jxmult)
    j = (Zy - (Kymult * k)) // Jymult
    print(f"k={k} j={j}")
    assert (Zy - (Kymult * k)) % Jymult == 0

    A = A1 + k * Ad
    B = B1 + j * Bd
    print(f"A = {A1} + {k} * {Ad} = {A}")
    print(f"B = {B1} + {j} * {Bd} = {B}")
    print(f"{m.px - m.ax * A - m.bx * B}")
    print(f"{m.py - m.ay * A - m.by * B}")

    return A * 3 + B

total_cost = 0
for b in data.split("\n\n"):
    r = re.compile('''
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
'''.strip())
    m = r.search(b).groups()
    m = list(map(int, m))
    #m[4] += 10000000000000
    #m[5] += 10000000000000
    m[4] += 10000000000000
    m[5] += 10000000000000
    machine = Machine(*m)
    cost = solve(machine)
    print(f"cost: {cost}")
    if cost is not None:
        total_cost += cost

print(total_cost)
