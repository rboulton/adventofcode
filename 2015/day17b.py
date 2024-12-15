import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

data = '''
20
15
10
5
5
'''
size = 25

data = open(os.path.join(os.path.dirname(__file__), "input17.txt")).read()
size = 150

data = data.strip()
data = data.split('\n')

sizes = list(map(int, data))
sizes.sort()

def combinations(sizes, size):
    if size < 0:
        return ((0, 0), )
    if size == 0:
        return ((0, 1), )
    if len(sizes) == 1:
        if sizes[0] == size:
            return ((1, 1), )
        else:
            return ((0, 0), )
    used = combinations(sizes[1:], size - sizes[0])
    not_used = combinations(sizes[1:], size)
    print(f"combinations {sizes} {size} used = {used}")
    print(f"combinations {sizes} {size} not used = {not_used}")
    r = Counter()
    for containers, ways in used:
        if ways > 0:
            r[containers + 1] += ways
    for containers, ways in not_used:
        if ways > 0:
            r[containers] += ways
    print(f"result {r}")

    return r.items()

r = list(combinations(sizes, size))
r.sort()
print(r)
print(r[0][1])
