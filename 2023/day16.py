from re import I


input = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''

input = open('2023/input16.txt', 'r').read()

dirs = 'rdlu'
def rot_clock(d):
    return dirs[(dirs.index(d) + 1) % 4]
def rot_anti(d):
    return dirs[(dirs.index(d) + 3) % 4]

class Cell:
    def __init__(self, ch):
        self.ch = ch
        self.dirs = set()
        
    def __repr__(self):
        return (self.ch + ''.join(sorted(self.dirs)) + '     ')[:5]
        return self.ch
        
class Grid:
    def __init__(self, input):
        self.grid = []
        for row in input.strip().split('\n'):
            self.grid.append([Cell(ch) for ch in row])
        self.w = len(self.grid[0])
        self.h = len(self.grid)
            
    def at(self, r, c):
        return self.grid[r][c]
    
    def __repr__(self):
        return '\n'.join(
            ' '.join(repr(cell) for cell in row)
            for row in self.grid
        )
        
    def next(self, r, c, dir):
        if dir == 'l':
            if c <= 0: return (None, None)
            return (r, c - 1)
        if dir == 'r':
            if c >= self.w - 1: return (None, None)
            return (r, c + 1)
        if dir == 'u':
            if r <= 0: return (None, None)
            return (r - 1, c)
        if dir == 'd':
            if r >= self.h - 1: return (None, None)
            return (r + 1, c)
        assert False, dir
 
    def add_beam(self, r, c, dir):
        while True:
            steps = self.beam_step(r, c, dir)
            if len(steps) == 0:
                return
            if len(steps) == 1:
                r, c, dir = steps[0]
                continue
            for s in steps:
                self.add_beam(*s)
            return
        
    def beam_step(self, r, c, dir):
        if r is None or c is None:
            return ()
        cell = self.at(r, c)
        if dir in cell.dirs:
            return ()
        cell.dirs.add(dir)
        if cell.ch == '.':
            r, c = self.next(r, c, dir)
            return ((r, c, dir),)
        elif cell.ch == '/':
            if dir in 'lr':
                dir = rot_anti(dir)
            else:
                dir = rot_clock(dir)
            r, c = self.next(r, c, dir)
            return ((r, c, dir),)
        elif cell.ch == '\\':
            if dir in 'lr':
                dir = rot_clock(dir)
            else:
                dir = rot_anti(dir)
            r, c = self.next(r, c, dir)
            return ((r, c, dir),)
        elif cell.ch == '|':
            if dir in 'lr':
                dir1 = rot_clock(dir)
                r1, c1 = self.next(r, c, dir1)
                dir2 = rot_anti(dir)
                r2, c2 = self.next(r, c, dir2)
                return ((r1, c1, dir1), (r2, c2, dir2))
            else:
                r, c = self.next(r, c, dir)
                return ((r, c, dir),)
        elif cell.ch == '-':
            if dir in 'ud':
                dir1 = rot_clock(dir)
                r1, c1 = self.next(r, c, dir1)
                dir2 = rot_anti(dir)
                r2, c2 = self.next(r, c, dir2)
                return ((r1, c1, dir1), (r2, c2, dir2))
            else:
                r, c = self.next(r, c, dir)
                return ((r, c, dir),)

        else:
            assert False, cell
            
    def energised(self):
        count = 0
        for row in self.grid:
            for cell in row:
                if len(cell.dirs) > 0:
                    count += 1
        return count
        
    
g = Grid(input)
print(repr(g))
print()
g.add_beam(0, 0, 'r')
print(repr(g))
print(g.energised())