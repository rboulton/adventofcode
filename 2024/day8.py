import math, os, re, copy

data = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

data = open(os.path.join(os.path.dirname(__file__), "input8.txt")).read()
data = data.strip().split('\n')

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Coord({self.x}, {self.y})'

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

class Grid:
    def __init__(self, rows):
        self.rows = list(map(list, rows))

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def clear(self, v):
        '''Set all cells to either v if v is an int, string or None, or v()'''
        if isinstance(v, int) or isinstance(v, str) or isinstance(v, None):
            v2 = v
            v = lambda: v2
        rows = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(v())
            rows.append(row)
        self.rows = rows

    def get(self, x_or_coord, y=None):
        if isinstance(x_or_coord, Coord):
            assert y is None
            x, y = x_or_coord.x, x_or_coord.y
        else:
            x, y = x_or_coord, y

        if x < 0 or y < 0: return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None

    def set(self, x_or_coord, y_or_v, v=None):
        if isinstance(x_or_coord, Coord):
            assert v is None
            x, y, v = x_or_coord.x, x_or_coord.y, y_or_v
        else:
            x, y, v = x_or_coord, y_or_v, v

        if x < 0 or y < 0: return None
        try:
            self.rows[y][x] = v
        except IndexError:
            pass

    def unique_contents(self):
        return set(v for row in self.rows for v in row)

    def findall(self, v):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == v:
                    yield Coord(x, y)

    def find(self, v):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) == v:
                    yield Coord(x, y)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)

def pairs(sequence):
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            yield (sequence[i], sequence[j])

grid = Grid(data)

def antinodes(grid):
    antinodes = copy.deepcopy(grid)
    antinodes.clear('.')
    for v in grid.unique_contents():
        if v == '.': continue
        print(v)
        positions = list(grid.findall(v))
        for a, b in pairs(positions):
            d = a - b
            antinodes.set(a + d, '#')
            antinodes.set(b - d, '#')
    return antinodes

a = antinodes(grid)
print(a)
print(len(list(a.findall('#'))))
