input = '''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2'''

input = open('input12.txt', 'r').read()

class Shape:
    def __init__(self, rows):
        self.rows = rows
        self.pieces = sum(1 for row in rows for ch in row if ch == '#')

    def __repr__(self):
        return f'Shape({self.rows}, {self.pieces})'

shapes = {}
regions = []
rows = input.strip('\n').split('\n\n')
for lines in rows[:-1]:
    lines = lines.split('\n')
    assert lines[0] == f'{len(shapes)}:', lines[0]
    shapes[len(shapes)] = Shape(lines[1:])

for line in rows[-1].split('\n'):
    size, counts = line.split(': ')
    w, h = map(int, size.split('x'))
    counts = tuple(map(int, counts.split()))
    regions.append((w, h, counts))

print(shapes)
print(regions)

success = 0
for w, h, counts in regions:
    pieces = 0
    max_pieces = 0
    for i, c in enumerate(counts):
        pieces += shapes[i].pieces * c
        max_pieces += 9 * c
    allowed_waste = w * h - pieces
    if allowed_waste < 0:
        continue
    assert w * h - max_pieces >= 0
    success += 1
print("COUNT:", success)
