import sys

order = [
    chr(ord('a') + i)
    for i in range(int(sys.argv[1]))
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

moves = open(sys.argv[2]).read().strip().split(',')
dance(moves)

print(''.join(order))
