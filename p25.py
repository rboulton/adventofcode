import sys
from collections import defaultdict

def read(filename):
    result = {}
    for row in open(filename).readlines():
        depth, r = row.split(': ')
        r = int(r)
        assert r > 1
        result[int(depth)] = [r, r * 2 - 2]
    return result

def calccost(fw, delay):
    positions = dict(
        (k, 0)
        for k in fw.keys()
    )
    maxdepth = max(fw.keys())
    pos = 0
    cost = 0
    for _ in range(delay):
        for k in positions.keys():
            positions[k] = (positions[k] + 1) % fw[k][1]

    while pos <= maxdepth:
        if pos in fw and positions.get(pos) == 0:
            cost += pos * fw[pos][0]
        pos += 1
        for k in positions.keys():
            positions[k] = (positions[k] + 1) % fw[k][1]
    return cost

fw = read(sys.argv[1])
delay = 0
while True:
    cost = calccost(fw, delay)
    if cost == 0:
        break
    delay += 1
print delay
