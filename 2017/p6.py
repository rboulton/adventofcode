import sys

num = int(sys.argv[1])

values = {}
dirs = [
 (1, 0),
 (0, 1),
 (-1, 0),
 (0, -1),
]

def set(x, y, value):
    values.setdefault(x, {})[y] = value
    print(x, y, value)

def get(x, y):
    return values.get(x, {}).get(y, 0)

def walk():
    x = 0
    y = 0

    set(x, y, 1)

    while True:
        for i in range(len(dirs)):
            dx, dy = dirs[i]
            next_dx, next_dy = dirs[(i + 1) % len(dirs)]
            # print(dx, dy, next_dx, next_dy)
            while True:
                x += dx
                y += dy
                newval = (
                    get(x - 1, y - 1) +
                    get(x - 1, y) +
                    get(x - 1, y + 1) +
                    get(x, y - 1) +
                    get(x, y + 1) +
                    get(x + 1, y - 1) +
                    get(x + 1, y) +
                    get(x + 1, y + 1)
                )
                set(x, y, newval)
                if get(x + next_dx, y + next_dy) == 0:
                    break
                if newval > num:
                    return newval

print(walk())