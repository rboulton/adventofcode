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
        print(f"combinations {sizes} {size} = 0")
        return 0
    if size == 0:
        print(f"combinations {sizes} {size} = 1")
        return 1
    if len(sizes) == 1:
        if sizes[0] == size:
            print(f"combinations {sizes} {size} = 1")
            return 1
        else:
            print(f"combinations {sizes} {size} = 0")
            return 0
    r = combinations(sizes[1:], size) + combinations(sizes[1:], size - sizes[0])
    print(f"combinations {sizes} {size} = {r}")
    return r

print(combinations(sizes, size))
