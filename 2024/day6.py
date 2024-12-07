import math, os, re

data = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

data = open(os.path.join(os.path.dirname(__file__), "input6.txt")).read()
data = data.strip().split('\n')

class Grid:
    def __init__(self, rows):
        self.rows = list(map(list, rows))

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def get(self, x, y):
        if x < 0 or y < 0: return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None

    def set(self, x, y, ch):
        if x < 0 or y < 0: return None
        try:
            self.rows[y][x] = ch
        except IndexError:
            pass

    def find(self, ch):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == ch:
                    return x, y

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)

g = Grid(data)
x, y = g.find('^')

count = 0
dx, dy = 0, -1
while True:
    print(x, y, dx, dy)
    if g.get(x, y) != 'X':
        count += 1
        g.set(x, y, 'X')
    nx, ny = x + dx, y + dy
    c = g.get(nx, ny)
    if c is None:
        break
    if c == '#':
        dx, dy = dy * -1, dx
    else:
        x, y = nx, ny

print(str(g))
print(count)
