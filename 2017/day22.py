import sys
from collections import defaultdict, Counter

infected = set()
for y, line in enumerate(open(sys.argv[1]).readlines()):
    for x, ch in enumerate(line.strip()):
        if ch == '#':
            infected.add((x, y))

y = y / 2
x = x / 2
d = [0, -1]

count = 0
for _ in range(10000):
    if (x, y) in infected:
        d = [-d[1], d[0]]
        infected.remove((x, y))
    else:
        d = [d[1], -d[0]]
        infected.add((x, y))
        count += 1
    x = x + d[0]
    y = y + d[1]
    print count, len(infected), x, y, d
print count
print len(infected)

print len(infected)
