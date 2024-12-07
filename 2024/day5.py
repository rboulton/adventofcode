import math, os, re

data = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip().split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input5.txt")).readlines())

after = {}
before = {}
i = 0
while True:
    row = data[i].strip()
    i += 1
    if row == '':
        break
    a, b = map(int, row.split('|'))
    after.setdefault(a, set()).add(b)
    before.setdefault(b, set()).add(a)

def ok(row):
    disallowed = set()
    for v in row:
        if v in disallowed:
            return False
        disallowed.update(before.get(v, ()))
    return True

r = 0
for row in data[i:]:
    row = list(map(int, row.split(',')))
    if ok(row):
        assert len(row) % 2 == 1
        r += row[(len(row) - 1)// 2]
print(r)
