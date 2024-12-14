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
    mincost = None
    for a in range(101):
        x = m.px - m.ax * a
        y = m.py - m.ay * a
        if x % m.bx == 0 and y % m.by == 0 and x // m.bx == y // m.by:
            cost = a * 3 + x // m.bx
            if mincost is None or cost < mincost:
                mincost = cost
    return mincost

total_cost = 0
for b in data.split("\n\n"):
    r = re.compile('''
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
'''.strip())
    m = r.search(b).groups()
    machine = Machine(*map(int, m))
    cost = solve(machine)
    print(cost)
    if cost is not None:
        total_cost += cost

print(total_cost)
