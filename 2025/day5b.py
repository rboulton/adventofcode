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

counted_to = 0
count = 0
for start, end in sorted(ranges.items()):
    if start <= counted_to: start = counted_to + 1
    if start > end: continue
    count += 1 + end - start
    counted_to = end

print(count)
