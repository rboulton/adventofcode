input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

input = open('2023/input18.txt', 'r').read()

class Cell:
    def __init__(self):
        self.hole = False
        self.up = False
        
    def __repr__(self):
        if self.hole:
            if self.up:
                return '^'
            return '#'
        if self.up:
            return ':'
        return '.'
        
class Grid:
    def __init__(self):
        self.xshift = 0
        self.yshift = 0
        self.rows = [[]]
        self.rows = [[]]
        
    def add_left_column(self):
        for row in self.rows:
            row.insert(0, Cell())
        self.xshift += 1
            
    def add_right_column(self):
        for row in self.rows:
            row.insert(len(row), Cell())
            
    def add_bottom_row(self):
        w = len(self.rows[0])
        newrow = [Cell() for _ in range(w)]
        self.rows.insert(0, newrow)
        self.yshift += 1
        
    def add_top_row(self):
        w = len(self.rows[0])
        newrow = [Cell() for _ in range(w)]
        self.rows.insert(len(self.rows), newrow)
        
    def at(self, x, y):
        try:
            return self.rows[y + self.yshift][x + self.xshift]
        except IndexError:
            return Cell()
        
    def set(self, x, y, hole=None, up=None):
        while x + self.xshift < 0:
            self.add_left_column()
        while y + self.yshift < 0:
            self.add_bottom_row()
        while x + self.xshift >= len(self.rows[0]):
            self.add_right_column()
        while y + self.yshift >= len(self.rows):
            self.add_top_row()
        cell = self.at(x, y)
        self.rows[y + self.yshift][x + self.xshift] = cell
        if hole is True:
            cell.hole = True
        if up is True:
            cell.up = True

    def format(self):
        return '\n'.join(
            ''.join(repr(cell) for cell in row)
            for row in reversed(self.rows)
        )
        
    def holes(self):
        return sum(
            1 if c.hole else 0
            for row in self.rows
            for c in row
        )

offsets = {
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0),
    'U': (0, 1),
}

g = Grid()

x, y = 0, 0
for row in input.strip().split('\n'):
    dir, dist, rgb = row.split(' ')
    dist = int(dist)
    o = offsets[dir]
    for _ in range(int(dist)):
        x += o[0]
        y += o[1]
        g.set(x, y, hole=True)
        if o[1] == 1:
            g.set(x, y - 1, up=True)
        if o[1] == -1:
            g.set(x, y, up=True)
        
for row in g.format().split('\n'):
    print(row)
print(g.holes())

print()
    
for row in g.rows:
    inside = False
    for i in range(len(row)):
        if row[i].up:
            inside = not inside
        if inside:
            row[i].hole = True

for row in g.format().split('\n'):
    print(row)
print(g.holes())