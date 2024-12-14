import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

data = '''
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''

data = open(os.path.join(os.path.dirname(__file__), "input13.txt")).read()
data = data.strip()

h = {}
for row in data.split('\n'):
    r = row.rstrip('.').split()
    a = r[0]
    b = r[-1]
    if r[2] == 'lose':
        c = -int(r[3])
    else:
        c = int(r[3])
    h.setdefault(a, {})[b] = c

def cost(order):
    t = 0
    for a, b in zip(order, list(order[1:]) + [order[0]]):
        t += h[a][b]
        t += h[b][a]
    return t

for order in permutations(h.keys()):
    print(order, cost(order))

print(max(cost(order) for order in permutations(h.keys())))
