import sys

num = int(sys.argv[1])

def calc_dist(num):
    x = 0
    y = 0
    value = 1

    while True:
        new_value = value + (8 * x + 1)
        print(x, y, new_value)
        if new_value > num:
            break
        value = new_value
        x += 1

    radius = x

    dirs = [
        (0, 1),
        (-1, 0),
        (-1, 0),
        (0, -1),
        (0, -1),
        (1, 0),
        (1, 0),
        (0, 1),
    ]

    for dx, dy in dirs:
        dist = min(num - value, radius)
        x += dist * dx
        y += dist * dy
        value += dist
        print(x, y, value)
        if dist < radius:
            return(abs(x) + abs(y))
    raise ValueError

print(calc_dist(num))