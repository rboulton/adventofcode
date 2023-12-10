import math

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


def next(n, count):
    c = steps[count % len(steps)]
    if c == 'L':
        return nodes[n][0]
    assert c == 'R'
    return nodes[n][1]

def sequence(start):
    sequence = []
    pos = 0
    n = start
    steplen = len(steps)
    while True:
        stepnum = pos % steplen
        # print(pos, stepnum, n)
        if (stepnum, n) in sequence:
            break
        sequence.append((stepnum, n))
        n = next(n, pos)
        pos += 1
    return sequence, sequence.index((stepnum, n))

def ends(seq):
    sequence, loopindex = seq
    i = 0
    ends = []
    while i < len(sequence):
        n = sequence[i][1]
        if n.endswith('Z'):
            assert i >= loopindex
            ends.append((i, loopindex))
        i += 1
    # All the sequences are constructed to have exactly one end position
    assert len(ends) == 1
    print(ends, len(sequence))
    # All the sequences have exactly the same number of items after the end
    # position as they do before the loop starts; so they end every N steps
    # after the start
    assert len(sequence) - ends[0][1] == ends[0][0]
    return ends[0][0]
        

starts = [n for n in nodes.keys() if n.endswith('A')]
print(starts)

lens = []
for s in starts:
    n = ends(sequence(s))
    lens.append(n)

print(lens)
print(math.lcm(*lens))