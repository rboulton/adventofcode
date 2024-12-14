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

data = open(os.path.join(os.path.dirname(__file__), "input13.txt")).read()
data = data.strip()

Machine = namedtuple('Machine', 'ax ay bx by px py'.split())

def solve(m):
    print(m)
    # m.ax * A + m.bx * B == m.px
    # m.ay * A + m.by * B == m.py
    A_denom = m.ax * m.by - m.ay * m.bx
    A_numerator = m.px * m.by - m.py * m.bx
    if A_numerator % A_denom != 0:
        return 0
    B_denom = m.bx * m.ay - m.by * m.ax
    B_numerator = m.px * m.ay - m.py * m.ax
    if B_numerator % B_denom != 0:
        return 0
    A = A_numerator // A_denom
    B = B_numerator // B_denom
    assert m.ay * A + m.by * B == m.py, m.ay * A + m.by * B - m.py
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
