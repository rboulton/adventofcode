import sys
import copy

def read(filename):
    result = {}
    for row in open(filename).readlines():
        depth, r = row.split(': ')
        r = int(r)
        assert r > 1
        result[int(depth)] = [r, r * 2 - 2]
    return result

def caught(fw, positions):
    maxdepth = max(fw.keys())
    pos = 0
    while pos <= maxdepth:
        if pos in fw and positions.get(pos) == 0:
            return True
        pos += 1
        for k in positions.keys():
            positions[k] = (positions[k] + 1) % fw[k][1]
    return False

fw = read(sys.argv[1])
delay = 0
positions = dict(
    (k, 0)
    for k in fw.keys()
)
while True:
    if not caught(fw, copy.copy(positions)):
        break
    delay += 1
    for k in positions.keys():
        positions[k] = (positions[k] + 1) % fw[k][1]
print(delay)
