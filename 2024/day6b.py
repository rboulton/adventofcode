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

    def positions(self, test=None):
        for x in range(self.width):
            for y in range(self.height):
                v = self.get(x, y)
                if test is None:
                    yield (x, y, v)
                else:
                    if test(x, y, v):
                        yield (x, y, v)

    def __str__(self):
        result = []
        for row in self.rows:
            rv = []
            for c in row:
                if type(c) is set:
                    c = 'X'
                rv.append(c)
            result.append(''.join(rv))
        return '\n'.join(result)

dirs = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)

def do_walk(g):
    x, y = g.find('^')
    d = 0
    count = 0
    while True:
        dx, dy = dirs[d]
        v = g.get(x, y)
        if type(v) is not set:
            count += 1
            v = set()
            g.set(x, y, v)
        if d in v:
            # Same position and direction as before
            return None
        v.add(d)
        nx, ny = x + dx, y + dy
        c = g.get(nx, ny)
        if c is None:
            break
        if c == '#':
            d = (d + 1) % 4
        else:
            x, y = nx, ny
    return count

g = Grid(data)
start_x, start_y = g.find('^')
do_walk(g)

count = 0
for x, y, v in g.positions(test = lambda x, y, v: type(v) is set):
    print(x, y, v)
    if (start_x, start_y) == (x, y):
        continue
    g2 = Grid(data)
    g2.set(x, y, '#')
    w2 = do_walk(g2)
    print(w2)
    if w2 is None:
        count += 1
        print(x, y, v, w2, str(g2))

print(str(g))
print(count)
