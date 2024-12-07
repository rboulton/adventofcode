import math, os

data = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input2.txt")).readlines())

def is_safe(report):
    row = list(map(int, report.split()))
    row2 = list(sorted(row))
    row3 = list(reversed(row2))
    if row != row2 and row != row3: return False
    print(row)
    for v1, v2 in zip(row2, row2[1:]):
        d = abs(v1 - v2)
        print(v1, v2, d)
        if d < 1 or d > 3: return False
    return True

print(sum(1 for row in data if is_safe(row)))
