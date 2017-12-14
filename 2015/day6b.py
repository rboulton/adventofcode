import sys

grid = [
    [0] * 1000
    for _ in range(1000)
]

def c(a, b):
    a = a.split(",")
    b = b.split(",")
    return (
        int(a[0]),
        int(a[1]),
        int(b[0]),
        int(b[1]),
    )

def on(x1, y1, x2, y2):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            grid[y][x] += 1

def off(x1, y1, x2, y2):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            grid[y][x] = max(0, grid[y][x] - 1)

def toggle(x1, y1, x2, y2):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            grid[y][x] += 2

print(sum(sum(l) for l in grid))

for line in open(sys.argv[1]).readlines():
    i = line.strip().split()
    if i[0] == 'turn':
        if i[1] == 'on':
            on(*c(i[2], i[4]))
        elif i[1] == 'off':
            off(*c(i[2], i[4]))
        else:
            FAIL
    elif i[0] == 'toggle':
        toggle(*c(i[1], i[3]))
    else:
        FAIL
    print(sum(sum(l) for l in grid))

print(sum(sum(l) for l in grid))
