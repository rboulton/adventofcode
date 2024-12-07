import os, sys, math

data = list('''3   4
4   3
2   5
1   3
3   9
3   3'''.split("\n"))
data = list(open(os.path.join(os.path.dirname(__file__), "input1.txt")).readlines())

data = [line.split() for line in data]
data = [
    (int(a), int(b))
    for (a, b) in data
]
col1, col2 = zip(*data)
total = 0
for a, b in zip(sorted(col1), sorted(col2)):
    total += abs(a-b)

print(col1, col2, total)