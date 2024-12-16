import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

data_ = '''
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''

data_ = '''
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
'''

data_ = '''
#######
#.....#
#.OOO.#
#..OO@#
#..O..#
#.....#
#######

<v<v<<^
'''

data = open(os.path.join(os.path.dirname(__file__), "input15.txt")).read()
data = data.strip()
data = data.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

layout, moves = data.split('\n\n')
g = Grid(layout.split('\n'))
print(g)
print(moves)

robot = g.find('@')

dirs = {
    '^': Coord(0, -1),
    '>': Coord(1, 0),
    '<': Coord(-1, 0),
    'v': Coord(0, 1),
}

def find_moves(pos, d):
    r = (set(), set())
    if d.y == 0:
        p = pos + d
        v = g.get(p)
        if v == '#':
            return None
        if v == '.':
            r[0].add((p, g.get(pos)))
            r[1].add(pos)
            return r
        assert v in ('[', ']'), v
        r = find_moves(p, d)
        if r is None:
            return None
        r[0].add((p, g.get(pos)))
        r[1].add(pos)
        return r

    else:
        p = pos + d
        v = g.get(p)
        if v == '#':
            return None
        if v == '.':
            r[0].add((p, g.get(pos)))
            r[1].add(pos)
            return r
        assert v in ('[', ']'), v
        r1 = find_moves(p, d)
        if v == '[':
            r2 = find_moves(p + Coord(1, 0), d)
        else:
            r2 = find_moves(p + Coord(-1, 0), d)
        if r1 is None or r2 is None:
            return None
        r1[0].update(r2[0])
        r1[1].update(r2[1])
        r1[0].add((p, g.get(pos)))
        r1[1].add(pos)
        return r1

def push(pos, d):
    # print(f"find_moves({pos}, {d})")
    moves = find_moves(pos, d)
    if moves is None:
        # print("no moves")
        return False
    # print(f"moves = {moves[0]} {moves[1]}")
    for p in moves[1]:
        g.set(p, '.')
    for p, v in moves[0]:
        g.set(p, v)
    return True

for move in moves:
    d = dirs.get(move)
    if d is None:
        continue

    # print(g)
    # print(robot, d)

    if push(robot, d):
        robot = robot + d

print(g)
print(sum(c.x + c.y*100 for c in g.findall('[')))
