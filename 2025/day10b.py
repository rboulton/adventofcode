import re
from scipy.optimize import linprog

input = '''
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''

input = open('input10.txt', 'r').read()

targets = []
toggles = []

def quickest(target, toggles):
    print(target, toggles)
    toggle_transpose = tuple(zip(*toggles))

    r = linprog(
        [1] * len(toggles), # All toggles cost the same
        A_eq=toggle_transpose, b_eq=target,
        integrality=[1] * len(toggles), # All constraints must be linear
    )
    assert r.success, r

    # Check the output
    v = [0] * len(target)
    for m, toggle in zip(r.x, toggles):
        m = round(m)
        for i, t in enumerate(toggle):
            v[i] += t * m
    assert target == v, r
    return sum(map(round, r.x))

total = 0
for row in input.strip('\n').split('\n'):
    mo = re.match(r'''\[(.*)\] (.*) (\{.*\})''', row)
    target, toggles, joltage = mo.groups()
    joltage = [int(j) for j in joltage[1:-1].split(',')]
    def make_toggle(t, num):
        r = [0] * num
        for i in t:
            r[i] = 1
        return r
    toggles = [make_toggle(map(int, t[1:-1].split(',')), len(joltage)) for t in toggles.split()]
    q = quickest(joltage, toggles)
    print(q)
    total += q

print(total)
