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

data = open(os.path.join(os.path.dirname(__file__), "input15.txt")).read()
data = data.strip()
data = data.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

layout, moves = data.split('\n\n')
g = Grid(layout.split('\n'))
print(g)
print(moves)

robot = g.find('@')
g.set(robot, '.')

dirs = {
    '^': Coord(0, -1),
    '>': Coord(1, 0),
    '<': Coord(-1, 0),
    'v': Coord(0, 1),
}

def push(pos, d):
    if d.y == 0:
        assert g.get(pos) == '.'
        p = pos + d
        while g.get(p) in ('[', ']'):
            p = p + d
        if g.get(p) != '.':
            return False
        while p != pos:
            np = p - d
            g2.set(p, g.get(np))
            p = np
        return True

    # print(f"Testing push {pos} {d}")

    p = pos + d
    v = g.get(p)
    if v == '#':
        return False
    if v =='[':
        if not (push(p, d) and push(p + Coord(1, 0), d)):
            return False
        p2 = p + d
        g2.set(p2, g.get(p))
        g2.set(p2 + Coord(1, 0), g.get(p + Coord(1, 0)))
        g2.set(p, '.')
        g2.set(p + Coord(1, 0), '.')
        return True
    if v ==']':
        if not (push(p, d) and push(p + Coord(-1, 0), d)):
            return False
        p2 = p + d
        g2.set(p2, g.get(p))
        g2.set(p2 + Coord(-1, 0), g.get(p + Coord(-1, 0)))
        g2.set(p, '.')
        g2.set(p + Coord(-1, 0), '.')
        return True
    assert v == '.'
    return True


for move in moves:
    d = dirs.get(move)
    if d is None:
        continue

    # assert g.get(robot) == '.'
    # g.set(robot, '@')
    # print(g)
    # print(robot, d)
    # g.set(robot, '.')

    g2 = copy.deepcopy(g)
    if push(robot, d):
        robot = robot + d
        g = g2
print(g)
print(sum(c.x + c.y*100 for c in g.findall('[')))
