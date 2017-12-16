import sys

l = 16

perm_pos = list(range(l))
perm_id = {
    chr(ord('a') + i): chr(ord('a') + i)
    for i in range(l)
}

moves = open(sys.argv[2]).read().strip().split(',')

for move in moves:
    if move[0] == 's':
        num = int(move[1:])
        perm_pos = perm_pos[-num:] + perm_pos[:-num]
    elif move[0] == 'x':
        a, b = map(lambda x: int(x), move[1:].split('/'))
        perm_pos[a], perm_pos[b] = perm_pos[b], perm_pos[a]
    elif move[0] == 'p':
        a, b = move[1:].split('/')
        perm_id[a], perm_id[b] = perm_id[b], perm_id[a]
    else:
        assert False, move

def do_perm(data_pos, data_id, perm_pos, perm_id):
    return [
        data_pos[perm_pos[i]]
        for i in range(l)
    ], {
        k: data_id[v]
        for (k, v) in perm_id.items()
    }


for m in range(9):
    data_pos = list(range(l))
    data_id = {
        chr(ord('a') + i): chr(ord('a') + i)
        for i in range(l)
    }

    for index in range(10):
        data_pos, data_id = do_perm(data_pos, data_id, perm_pos, perm_id)

        data = data_pos
        print(m, index, ''.join(
            data_id[chr(ord('a') + v)]
            for v in data
        ))
    perm_pos, perm_id = data_pos, data_id

data = data_pos
print(''.join(
    chr(ord('a') + v)
    for v in data
))
