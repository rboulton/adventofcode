input = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''

input = open('2023/input10.txt', 'r').read()

class Tile:
    def __init__(self, ch):
        self.left = ch in '-J7'
        self.right = ch in '-LF'
        self.up = ch in '|LJ'
        self.down = ch in '|7F'
        self.start = ch == 'S'
        self.distance = None
        
    def __repr__(self):
        return '{:d}{:d}{:d}{:d}{:d}_{}'.format(self.left, self.right, self.up, self.down, self.start, self.distance)
    
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
        
    def __str__(self):
        return '\n'.join(' '.join(repr(i) for i in l) for l in self.tiles) + '\n' + repr(self.start)

m = Map(input)
m.at(*m.start).distance = 0 
for l in str(m).split('\n'): print(l)

p1, p2 = m.joined(*m.start)
dist = 0
print(p1, p2)
while m.at(*p1).distance is None:
    dist += 1
    assert m.at(*p2).distance is None
    m.at(*p1).distance = dist
    m.at(*p2).distance = dist
    p1 = m.joined_unfilled(*p1)
    p2 = m.joined_unfilled(*p2)
   
    
for l in str(m).split('\n'): print(l)
print(dist)