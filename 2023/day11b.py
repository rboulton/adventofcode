input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

input = open('2023/input11.txt', 'r').read()

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
    def dist(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)
        
    def __repr__(self):
        return '({}, {})'.format(self.row, self.col)

class Grid:
    def __init__(self):
        self.galaxies = []
        self.rows_used = set()
        self.cols_used = set()

    @property
    def maxrow(self):
        return max(self.rows_used)
        
    @property
    def maxcol(self):
        return max(self.cols_used)
        
    def add(self, position):
        self.galaxies.append(position)
        self.rows_used.add(position.row)
        self.cols_used.add(position.col)
        
    def expand(self):
        factor = 1000000
        empty_rows = list(sorted(set(range(self.maxrow + 1)) - self.rows_used))
        empty_cols = list(sorted(set(range(self.maxcol + 1)) - self.cols_used))
        print(self.maxrow, self.maxcol)
        print(empty_rows, empty_cols)
        self.row_map = {}
        newrow = 0
        for row in range(self.maxrow + 1):
            self.row_map[row] = newrow
            newrow += 1
            if row in empty_rows:
                newrow += factor - 1
                
        self.col_map = {}
        newcol = 0
        for col in range(self.maxcol + 1):
            self.col_map[col] = newcol
            newcol += 1
            if col in empty_cols:
                newcol += factor - 1
                
        print(self.row_map, self.col_map)
        
        self.new_galaxies = []
        for pos in self.galaxies:
            self.new_galaxies.append(Position(self.row_map[pos.row], self.col_map[pos.col]))
            
    def new_distances(self):
        dists = []
        for i in range(len(self.new_galaxies)):
            for j in range(i + 1, len(self.new_galaxies)):
                a = self.new_galaxies[i]
                b = self.new_galaxies[j]
                d = a.dist(b)
                dists.append(d)
        print(len(dists))
        return dists
    
 
g = Grid()       
for rownum, row in enumerate(input.strip().split('\n')):
    for colnum, col in enumerate(row):
        if col == '#':
            g.add(Position(rownum, colnum))
        else:
            assert col == '.'
print(g.galaxies)
g.expand()

print(g.galaxies)
print(g.new_galaxies)
print(sum(g.new_distances()))