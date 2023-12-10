input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

input = open('2023/input9.txt', 'r').read()

def diffs(seq):
    return [
        seq[i+1] - seq[i]
        for i in range(len(seq) - 1)
    ]
    
def not_all_zeros(seq):
    if max(seq) != 0: return True
    if min(seq) != 0: return True
    return False

sum = 0
for line in input.strip().split('\n'):
    seq = [int(v) for v in line.split(' ')]
    starts = []
    while not_all_zeros(seq):
        print(seq)
        starts.append(seq[0])
        seq = diffs(seq)
    n = 0
    for start in reversed(starts):
        n = start - n
    print(starts, n)
    sum += n

print()
print(sum)