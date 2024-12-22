import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
1
10
100
2024
'''

data = open(os.path.join(os.path.dirname(__file__), "input22.txt")).read()
data = data.strip()
data = data.split('\n')

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def nextsecret(num):
    num = prune(mix(num * 64, num))
    num = prune(mix(num // 32, num))
    num = prune(mix(num * 2048, num))
    return num

def evolve(num, repetitions):
    for _ in range(repetitions):
        num = nextsecret(num)
    return num

total = 0
for num in data:
    r = evolve(int(num), 2000)
    print(num, r)
    total += r
print(total)
