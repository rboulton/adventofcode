import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
1
2
3
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

def sequence(num, repetitions):
    r = []
    for _ in range(repetitions):
        last = num % 10
        num = nextsecret(num)
        digit = num % 10
        r.append((digit - last, digit))
    return r

def values(num):
    result = {}
    seq = sequence(num, 2000)
    for i in range(len(seq) - 3):
        subseq = (seq[i][0], seq[i+1][0], seq[i+2][0], seq[i+3][0])
        val = seq[i+3][1]
        #print(subseq, val)
        if subseq not in result:
            result[subseq] = val
    return result.items()

scores = Counter()
for num in data:
    for k, v in values(int(num)):
        scores[k] += v
print(max(scores.values()))
