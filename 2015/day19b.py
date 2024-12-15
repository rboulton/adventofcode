import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations
from grid import Grid

data = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''

data = open(os.path.join(os.path.dirname(__file__), "input19.txt")).read()

data = data.strip()
data = data.split('\n')

target = data[-1]
start = 'e'

subs = []
max_repl_len = 0
for row in data[:-2]:
    row = row.split(' ')
    subs.append((row[0], row[2]))
    assert (len(row[0]) <= len(row[2])), row
    max_repl_len = max(max_repl_len, len(row[2]) + 1)
max_repl_len = len(target)

def split_elems(a):
    return tuple(re.findall('[A-Z][a-z]*', a))

def reverse(state):
    for pos in range(len(state) - 1, len(state) - max_repl_len, -1):
        if pos < 0:
            break
        for a, b in subs:
            if state[pos:pos+len(b)] == b:
                # print(pos, a, b)
                yield state[:pos] + a + state[pos+len(b):]

def find_path(state):
    print(f"find_path({state})")
    if state == 'e':
        return 0
    for seq in reverse(state):
        num = find_path(seq)
        if num is not None:
            return num + 1

print(find_path(target))
