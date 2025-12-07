import grid

input = '''3-5
10-14
16-20
12-18

1
5
8
11
17
32'''

input = open("input5.txt", "r").read()

fresh, ingredients = input.strip().split("\n\n")
ranges = {}
for r in fresh.split("\n"):
    start, end = map(int, r.split('-'))
    ranges[start] = max(ranges.get(start, end), end)
# shrink ranges if we need to

def in_range(v):
    for start, end in ranges.items():
        if start <= v and v <= end:
            return True
    return False

count = 0
for v in ingredients.split("\n"):
    if in_range(int(v)):
        count += 1

print(count)
