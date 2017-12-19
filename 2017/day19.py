import sys

grid = [
    line
    for line in open(sys.argv[1]).readlines()
]

pos = [grid[0].find('|'), 0]
seen = []
d = [0, 1]

def at(pos, dp=(0, 0)):
    x = pos[0] + dp[0]
    y = pos[1] + dp[1]
    try:
        return grid[y][x]
    except IndexError:
        return ' '

step = 0
while True:
    ch = at(pos)
    assert ch != ' ', (pos, ''.join(seen), step)
    if ch not in '-+|':
        seen.append(ch)
    if ch == '+':
        turn1 = [d[1], d[0]]
        turn2 = [-d[1], -d[0]]
        if at(pos, turn1) != ' ':
            d = turn1
        elif at(pos, turn2) != ' ':
            d = turn2
        else:
            assert False, pos
    pos[0] = pos[0] + d[0]
    pos[1] = pos[1] + d[1]
    step += 1
