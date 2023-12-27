# This attempt failed - too complicated to get right.
# Restarted from a fresh copy of day21 in day21b2

input = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''

_input = open('2023/input21.txt', 'r').read()

class Cell:
    def __init__(self, ch):
        self.rock = ch == '#'
        self.first_reached = {}
        self.even = False
        self.odd = False
        
        if ch == 'S':
            self.reached(0, ('.'))
            
    def __repr__(self):
        if self.rock:
            return '#'
        if self.even and self.odd:
            return '3'
        if self.even:
            return '2'
        if self.odd:
            return '1'
        return '.'
            
    def reached(self, step, dirs):
        if self.rock:
            return
        for dir in dirs:
            if dir not in self.first_reached:
                self.first_reached[dir] = step
        if step % 2 == 0:
            self.even = True
        else:
            self.odd = True
            
    def count(self, steps):
        repeats = 0
        for dir in ('l', 'u', 'r', 'd'):
            fr = self.first_reached.get(dir, None)
            if fr is not None:
                repeats += (steps - fr) // repeat_time
                
                print(dir, fr, repeats)
            
        if self.even and steps % 2 == 0:
            return 1 + repeats
        if self.odd and steps % 2 == 1:
            return 1 + repeats
        return repeats

class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        
    def count(self, steps):
        return sum(
            sum(cell.count(steps) for cell in row)
            for row in self.rows
        )
        
    def get(self, r, c):
        dir = '.'
        if r < 0: dir = 'u'
        if r >= self.h: dir = 'd'
        if c < 0: dir = 'l'
        if c >= self.w: dir = 'r'
        return self.rows[r % self.h][c % self.w], dir
    
    def neighbours(self, r, c):
        return (
            self.get(r - 1, c),
            self.get(r + 1, c),
            self.get(r, c - 1),
            self.get(r, c + 1),
        )
        
    def __str__(self):
        return '\n'.join(''.join(str(c) for c in row) for row in self.rows)
        
    def iterate(self, step):
        for r in range(self.h):
            for c in range(self.w):
                cell, _ = self.get(r, c)
                if cell.rock:
                    continue
                reached_dirs = set()
                even = step % 2 == 0
                for n, dir in self.neighbours(r, c):
                    if even and n.odd:
                        reached_dirs.add(dir)
                    if not even and n.even:
                        reached_dirs.add(dir)
                if reached_dirs:
                    cell.reached(step, reached_dirs)
                    


g = Grid([
        [Cell(ch) for ch in row]
        for row in input.strip().split('\n')
    ])
repeat_time = g.w + g.h


# print(g)
assert g.w == g.h
print(g.count(0))
steps = 10
for step in range(1, steps + 1):
    g.iterate(step)
    print(g)
    print(step, g.count(step))
print(g.count(steps))