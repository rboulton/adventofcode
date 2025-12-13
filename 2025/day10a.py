import re

input = '''
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
'''

input = open('input10.txt', 'r').read()

targets = []
toggles = []

def quickest(target, toggles):
    r = 1000000
    for i in range(2**len(toggles)):
        v = set()
        c = 0
        for j in range(len(toggles)):
            if i & 2**j:
                for k in toggles[j]:
                    if k in v: v.remove(k)
                    else: v.add(k)
                c += 1
        if v == target:
            print(target, bin(i), toggles, v, c)
            r = min(r, c)
    return r

total = 0
for row in input.strip('\n').split('\n'):
    mo = re.match(r'''\[(.*)\] (.*) (\{.*\})''', row)
    target, toggles, joltage = mo.groups()
    target = set(i for i, ch in enumerate(target) if ch == '#')
    toggles = [tuple(map(int, t[1:-1].split(','))) for t in toggles.split()]
    joltage = [int(j) for j in joltage[1:-1].split(',')]
    print(target, toggles, joltage)
    q = quickest(target, toggles)
    print(q)
    total += q

print(total)
