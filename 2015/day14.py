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

T = 2503
race = []
for row in data.split('\n'):
    print(row)
    row = row.split()
    name, speed, fly, rest = row[0], int(row[3]), int(row[6]), int(row[-2])
    d = distance(speed, fly, rest, T)
    print(name, T, d)
    race.append((d, name))
race.sort()
print(race)
