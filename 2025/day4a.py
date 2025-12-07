import grid

input = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.'''

input = open("input4.txt", "r").read()

g = grid.Grid(input.strip().split("\n"))
g2 = grid.Grid(input.strip().split("\n"))

count = 0
for c in g.coords(lambda x: x == '@'):
    v = 0
    for n in g.all_neighbours(c):
        if g.get(n) == '@':
            v += 1
    if v < 4:
        count +=1 
        g2.set(c, 'x')

print(g2)
print(count)
