input = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

input = open('2023/input12.txt', 'r').read()

def runs(input):
    out = []
    l = 0
    for ch in input:
        if ch == '#':
            l += 1
        else:
            if l > 0:
                out.append(l)
                l = 0
    if l > 0:
        out.append(l)
    return out

def variations(input):
    pos = []
    for i, ch in enumerate(input):
        if ch == '?':
            pos.append(i)
    for i in range(2**len(pos)):
        opts = ('0' * len(input) + bin(i)[2:])[-len(pos):]
        chs = []
        j = 0
        for ch in input:
            if ch == '?':
                if opts[j] == '1':
                    ch = '#'
                else:
                    ch = '.'
                j += 1
            chs.append(ch)
        yield(''.join(chs))

def options(row):
    springs, sequences = row.strip().split(' ')
    sequences = [int(a) for a in sequences.split(',')]
    for v in variations(springs):
        r = runs(v)
        if r == sequences:
            # print(v, runs(v), sequences)
            yield v
 
counts = []
for row in input.strip().split('\n'):
    opts = list(options(row))
    counts.append(len(opts))
    print(len(opts))
    
print(sum(counts))