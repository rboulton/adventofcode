input = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''

input='''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

input = open('2023/input8.txt', 'r').read()


steps = input.strip().split('\n')[0]

nodes = {}
for line in input.strip().split('\n')[1:]:
    line = line.strip()
    if line == '':
        continue
    n,b = line.split(' = ')
    l,r = b.strip()[1:][:-1].split(', ')
    assert n not in nodes
    nodes[n] = (l, r)


def next(n):
    if c == 'L':
        return nodes[n][0]
    assert c == 'R'
    return nodes[n][1]

current = [n for n in nodes.keys() if n.endswith('A')][:1]
count = 0
while True:
    # print(count, current)
    if len([n for n in current if n.endswith('Z')]) == len(current):
        break
    c = steps[count % len(steps)]
    current = [next(n) for n in current]
    count += 1
        
print(count)