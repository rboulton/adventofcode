# Brute force calculation of the right answer for a copied grid, for use in
# debugging the full scale solution

input = '''...........
......##.#.
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
.##...#.##.
...........
'''

_input = open('2023/input21.txt', 'r').read()

input = input.strip()
assert input[len(input)//2] == 'S'
input = input.replace('S', '.') 

mult = 11
input = '\n'.join([
    row * mult
    for row in input.split('\n')
] * mult)

input = input[:len(input)//2] + 'S' + input[1 + len(input)//2:]
assert input[len(input)//2] == 'S'

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

#print(g)
max = g.w // 2
for i in range(1, max + 1):
    g = g.iterate()
    print(repr((i, g.count('O'))) + ",")
print(g, i, g.count('O'))