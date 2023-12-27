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
...........
'''

input = open('2023/input21.txt', 'r').read()

class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        
    def count(self, ch):
        return sum(
            sum(1 if ch == 'O' else 0 for ch in row)
            for row in self.rows
        )
        
    def get(self, r, c):
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            return None
        return self.rows[r][c]
    
    def set(self, r, c, ch):
        self.rows[r][c] = ch
        
    def neighbours(self, r, c):
        return [v for v in (
            self.get(r - 1, c),
            self.get(r + 1, c),
            self.get(r, c - 1),
            self.get(r, c + 1),
        ) if v is not None]
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)
        
    def iterate(self):
        new = Grid([['#' if ch == '#' else '.' for ch in row] for row in self.rows])
        for r in range(self.h):
            for c in range(self.w):
                if self.get(r, c) == '#':
                    continue
                n = self.neighbours(r, c)
                count = 0
                for ch in n:
                    if ch in 'SO':
                        count += 1
                if count == 0:
                    new.set(r, c, '.')
                else:
                    new.set(r, c, 'O')
        return new


g = Grid([
        [ch for ch in row]
        for row in input.strip().split('\n')
    ])

print(g)
print(g.count('O'))
for i in range(64):
    g = g.iterate()
    print(i, g.count('O'))