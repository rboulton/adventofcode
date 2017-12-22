import sys
from collections import defaultdict, Counter

infected = {}
for y, line in enumerate(open(sys.argv[1]).readlines()):
    for x, ch in enumerate(line.strip()):
        if ch == '#':
            infected[(x, y)] = '#'

y = y / 2
x = x / 2
d = [0, -1]

count = 0
for i in range(10000000):
    state = infected.get((x, y))
    if state == None:
        d = [d[1], -d[0]]
    if state == '#':
        # Right
        d = [-d[1], d[0]]
    if state == 'F':
        d = [-d[0], -d[1]]

    if state == None:
        infected[x, y] = 'W'
    elif state == 'W':
        infected[x, y] = '#'
        count += 1
    elif state == '#':
        infected[x, y] = 'F'
    elif state == 'F':
        del infected[x, y]
    x = x + d[0]
    y = y + d[1]
    if i % 1000 == 0:
        print count, len(infected), x, y, d
print count
print len(infected)

print len(infected)
