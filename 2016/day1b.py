prog = 'R3, L2, L2, R4, L1, R2, R3, R4, L2, R4, L2, L5, L1, R5, R2, R2, L1, R4, R1, L5, L3, R4, R3, R1, L1, L5, L4, L2, R5, L3, L4, R3, R1, L3, R1, L3, R3, L4, R2, R5, L190, R2, L3, R47, R4, L3, R78, L1, R3, R190, R4, L3, R4, R2, R5, R3, R4, R3, L1, L4, R3, L4, R1, L4, L5, R3, L3, L4, R1, R2, L4, L3, R3, R3, L2, L5, R1, L4, L1, R5, L5, R1, R5, L4, R2, L2, R1, L5, L4, R4, R4, R3, R2, R3, L1, R4, R5, L2, L5, L4, L1, R4, L4, R4, L4, R1, R5, L1, R1, L5, R5, R1, R1, L3, L1, R4, L1, L4, L4, L3, R1, R4, R1, R1, R2, L5, L2, R4, L1, R3, L5, L2, R5, L4, R5, L5, R3, R4, L3, L3, L2, R2, L5, L5, R3, R4, R3, R4, R3, R1'

steps = prog.split(', ')

def move():
    pos = [0, 0]
    d = [0, 1]
    visited = set()
    visited.add(tuple(pos))

    for step in steps:
        t, dist = step[0], int(step[1:])
        if t == 'R':
            d = [d[1], -d[0]]
        else:
            assert t == 'L'
            d = [-d[1], d[0]]
        for _ in range(dist):
            pos[0] = pos[0] + d[0]
            pos[1] = pos[1] + d[1]

            if tuple(pos) in visited:
                return pos
            visited.add(tuple(pos))
    return pos

pos = move()
print(pos, abs(pos[0]) + abs(pos[1]))
