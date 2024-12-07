import math, os

data = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.split('\n')

data = '''47 48 51 50 55'''.split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input2.txt")).readlines())

# Incorrect attempt - doesn't handle the problem being the first element. Might have other bugs
def is_safe(report):
    row = list(map(int, report.split()))
    dir = 1 if row[1] - row[0] > 0 else -1
    print(row, dir)
    problems = 0
    v1 = row[0]
    for v2 in row[1:]:
        d = (v2 - v1) * dir
        print(v1, v2, d)
        if d < 1 or d > 3:
            print("Problem")
            problems += 1
        else:
            v1 = v2
    return problems <= 1

def problem_position(row):
    dir = 1 if row[1] - row[0] > 0 else -1
    for i in range(len(row) - 1):
        v1 = row[i]
        v2 = row[i+1]
        d = (v2 - v1) * dir
        if d < 1 or d > 3:
            return i
    return None

def is_safe(report):
    row = list(map(int, report.split()))
    pos = problem_position(row)
    if pos is None:
        return True

    for j in range(len(row)):
        row2 = list(row)
        del row2[j]
        if problem_position(row2) is None:
            return True

print(sum(1 for row in data if is_safe(row)))
