import math, os, re

data = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''.strip().split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input4.txt")).readlines())

class Grid:
    def __init__(self, rows):
        self.rows = list(rows)

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def at(self, x, y):
        if x < 0 or y < 0: return None
        try:
            return self.rows[y][x]
        except IndexError:
            return None

    def check(self, word, x, y, dx, dy):
        for ch in word:
            if self.at(x, y) != ch:
                return False
            x += dx
            y += dy
        return True


g = Grid(data)
c = 0
for x in range(g.width):
    for y in range(g.height):
        if (
                (g.check('MAS', x, y, 1, 1) or g.check('SAM', x, y, 1, 1))
                and
                (g.check('MAS', x, y + 2, 1, -1) or g.check('SAM', x, y + 2, 1, -1))
        ):
            c += 1
print(c)
