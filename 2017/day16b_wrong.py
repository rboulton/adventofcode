import sys

l = int(sys.argv[1])

order = [
    chr(ord('a') + i)
    for i in range(l)
]

def dance(moves):
    global order
    for move in moves:
        if move[0] == 's':
            num = int(move[1:])
            order = order[-num:] + order[:-num]
        elif move[0] == 'x':
            a, b = map(lambda x: int(x), move[1:].split('/'))
            order[a], order[b] = order[b], order[a]
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            a = order.index(a)
            b = order.index(b)
            order[a], order[b] = order[b], order[a]
        else:
            assert False, move

dance(open(sys.argv[2]).read().strip().split(','))
perm = [
    ord(c) - ord('a')
    for c in order
]

def do_perm(data):
    return [
        data[perm[i]]
        for i in range(l)
    ]


#for _ in range(9):
for _ in range(1):
    o = list(range(l))
    for _ in range(10):
        o = do_perm(o)
        print(''.join(
            chr(ord('a') + v)
            for v in o
        ))
    perm = o

print(o)
print(''.join(
    chr(ord('a') + v)
    for v in perm
))
