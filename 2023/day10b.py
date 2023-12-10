input = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''

input = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''

input = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''

input = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''

input = open('2023/input10.txt', 'r').read()

class Tile:
    def __init__(self, ch):
        self.left = ch in '-J7'
        self.right = ch in '-LF'
        self.up = ch in '|LJ'
        self.down = ch in '|7F'
        self.start = ch == 'S'
        self.distance = None
        self.out = None
        
    def verbose(self):
        return '{:d}{:d}{:d}{:d}{:d}{}_{}'.format(self.left, self.right, self.up, self.down, self.start, self.out, self.distance)
    
    def ch(self):
        if self.left and self.right: return '-'
        if self.up and self.down: return '|'
        if self.left and self.up: return 'J'
        if self.left and self.down: return '7'
        if self.right and self.down: return 'F'
        if self.right and self.up: return 'L'
        if self.out is True: return 'O'
        if self.out is False: return 'I'
        return '.'
        
    
    def check(self):
        assert sum((self.left, self.right, self.up, self.down)) == 2

        
class Map:
    def __init__(self, input):
        tiles = []
        self.tiles = tiles
        self.start = None
        
        for line in input.strip().split('\n'):
            line = line.strip()
            if 'S' in line:
                assert self.start is None
                self.start = [len(tiles), line.index('S')]
            tiles.append([Tile(ch) for ch in line])
        assert self.start is not None
        
        row, col = self.start
        start_tile = self.at(row, col)
        assert start_tile.start
        if self.at(row, col - 1).right:
            start_tile.left = True
        if self.at(row, col + 1).left:
            start_tile.right = True
        if self.at(row - 1, col).down:
            start_tile.up = True
        if self.at(row + 1, col).up:
            start_tile.down = True
        start_tile.check()
        
    def just_mainloop(self):
        for i in range(len(self.tiles)):
            self.tiles[i] = [
                t
                if t.distance is not None
                else Tile('.')
                for t in self.tiles[i]
            ]
        
    def at(self, row, column):
        try:
            return self.tiles[row][column] 
        except IndexError:
            return Tile('.')
        
    def joined(self, row, column):
        tile = self.at(row, column)
        res = []
        if tile.left:
            res.append((row, column - 1))
        if tile.right:
            res.append((row, column + 1))
        if tile.up:
            res.append((row - 1, column))
        if tile.down:
            res.append((row + 1, column))
        assert len(res) == 2
        return res
    
    def joined_unfilled(self, row, column):
        n1, n2 = self.joined(row, column)
        if self.at(*n1).distance is None:
            return n1
        else:
            return n2
        
    def verbose(self):
        return '\n'.join(' '.join(i.verbose() for i in l) for l in self.tiles) + '\n' + repr(self.start)
    
    def compact(self):
        return '\n'.join(''.join(i.ch() for i in l) for l in self.tiles) + '\n' + repr(self.start)
    
    def crossings(self, row, column):
        # How many crossings of pipes occur from the top left of this position, to the left
        count = 0
        while column > 0:
            column -= 1
            if self.at(row, column).up:
                count += 1
        return count
    
    def all(self):
        for rownum, row in enumerate(self.tiles):
            for colnum in range(len(row)):
                yield (rownum, colnum)

m = Map(input)
m.at(*m.start).distance = 0 
for l in m.compact().split('\n'): print(l)

p1, p2 = m.joined(*m.start)
dist = 0
while m.at(*p1).distance is None:
    dist += 1
    assert m.at(*p2).distance is None
    m.at(*p1).distance = dist
    m.at(*p2).distance = dist
    p1 = m.joined_unfilled(*p1)
    p2 = m.joined_unfilled(*p2)

m.just_mainloop()

count = 0
for row, column in m.all():
    t = m.at(row, column)
    if t.ch() != '.':
        continue
    c = m.crossings(row, column)
    t.out = c % 2 == 0
    if not t.out:
        count += 1
    
for l in m.compact().split('\n'): print(l)
print(dist)
print(count)