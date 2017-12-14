import sys

prog = open(sys.argv[1]).read().strip()
visited = set()

pos1 = [0, 0]
pos2 = [0, 0]
visited.add(tuple(pos1))

def move(pos, d):
    if d == '^':
        pos[1] -= 1
    if d == 'v':
        pos[1] += 1
    if d == '<':
        pos[0] -= 1
    if d == '>':
        pos[0] += 1

m = 0
for d in prog.strip():
    if m == 0:
        move(pos1, d)
        visited.add(tuple(pos1))
        m = 1
    else:
        move(pos2, d)
        visited.add(tuple(pos2))
        m = 0

print(len(visited))
