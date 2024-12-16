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

data = open(os.path.join(os.path.dirname(__file__), "input15.txt")).read()
data = data.strip()

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
for move in moves:
    d = dirs.get(move)
    if d is None:
        continue
    #print(g)
    #print(robot, d)
    p = robot + d
    if g.get(p) == 'O':
        while g.get(p) == 'O':
            p = p + d
        if g.get(p) == '.':
            g.set(p, 'O')
            robot = robot + d
            g.set(robot, '.')
    elif g.get(p) == '.':
        robot = robot + d
print(g)
print(sum(c.x + c.y*100 for c in g.findall('O')))
