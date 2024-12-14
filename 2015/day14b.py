import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

data = '''
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''

data = open(os.path.join(os.path.dirname(__file__), "input14.txt")).read()
data = data.strip()

def distance(speed, fly, rest, time):
    complete_cycles = time // (fly + rest)
    left = time % (fly + rest)

    return (complete_cycles * fly + min(left, fly)) * speed

reindeers = []
for row in data.split('\n'):
    row = row.split()
    name, speed, fly, rest = row[0], int(row[3]), int(row[6]), int(row[-2])
    reindeers.append((name, speed, fly, rest))

score = Counter()
for T in range(2503):
    dists = []
    for name, speed, fly, rest in reindeers:
        d = distance(speed, fly, rest, T + 1)
        dists.append((d, name))
    dists.sort()
    winner = dists[-1][1]
    score[winner] +=1

print(max(score.values()))
