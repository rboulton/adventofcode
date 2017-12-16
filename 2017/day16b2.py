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

def asstr():
    return ''.join(order)

moves = open(sys.argv[2]).read().strip().split(',')
start = asstr()
vals = []

period = 0
while True:
    vals.append(asstr())
    dance(moves)
    period += 1
    if start == asstr():
        break
print("Period {}".format(period))

print(vals[1000000000 % period])
