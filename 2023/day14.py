input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

input = open('2023/input14.txt', 'r').read()

class Grid:
    def __init__(self, input):
        self.rows = [
            [ch for ch in row]
            for row in input.strip().split('\n')
        ]
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        
    def at(self, r, c):
        return self.rows[r][c]
    
    def set(self, r, c, ch):
        self.rows[r][c] = ch
        
    def __repr__(self):
        return '\n'.join(''.join(r) for r in self.rows)
    
    def load(self):
        total = 0
        for r, row in enumerate(self.rows):
            weight = self.h - r
            for ch in row:
                if ch == 'O':
                    total += weight
        return total
    
    def roll_north(self):
        top = [0] * len(self.rows[0])
        for r, row in enumerate(self.rows):
            for c, ch in enumerate(row):
                if ch == '#':
                    top[c] = r + 1
                elif ch == 'O':
                    t = top[c]
                    if t != r:
                        print("Rolling in col {} from {} to {}".format(c, r, t))
                        assert self.at(t, c) == '.', self.at(t,c)
                        self.set(t, c, 'O')
                        self.set(r, c, '.')
                    top[c] = t + 1


g = Grid(input)
print(g)
print(g.load())
g.roll_north()
print(g)
print(g.load())