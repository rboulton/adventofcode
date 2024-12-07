import os, sys, math, collections

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

counts1 = collections.Counter(col1)
counts2 = collections.Counter(col2)

total = 0
for (k, v) in counts1.items():
    total += k * v * counts2[k]

print(total)