input = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''

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
    
n = 'AAA'
count = 0
while n != 'ZZZ':
    c = steps[count % len(steps)]
    if c == 'L':
        n = nodes[n][0]
    elif c == 'R':
        n = nodes[n][1]
    else:
        assert False, c
    count += 1
        
print(count)