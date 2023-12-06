input = '''123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i'''

input = open('2015/input7.txt').read()

wirevals = {}

def get_val(lhs):
    if lhs.startswith('NOT '):
        return 0xffff ^ get_val(lhs[4:])
    if ' AND ' in lhs:
        a, b = lhs.split(' AND ')
        return get_val(a) & get_val(b)
    if ' OR ' in lhs:
        a, b = lhs.split(' OR ')
        return get_val(a) | get_val(b)
    if ' LSHIFT ' in lhs:
        a, b = lhs.split(' LSHIFT ')
        return (get_val(a) << int(b)) & 0xffff
    if ' RSHIFT ' in lhs:
        a, b = lhs.split(' RSHIFT ')
        return get_val(a) >> int(b)
    assert(' ' not in lhs)
    try:
        return int(lhs) & 0xffff
    except ValueError:
        pass
    return wirevals[lhs]

wirevals['b'] = 3176
while 'a' not in wirevals:
    changed = False
    for line in input.strip().split('\n'):
        lhs, wire = line.split(' -> ')
        try:
            val = get_val(lhs)
        except(KeyError):
            continue
        if wire not in wirevals:
            changed = True
            print('{}: setting {} to {}'.format(lhs, wire, val))
            wirevals[wire] = val
    if not changed:
        break

print(sorted(wirevals.items()))
print(wirevals['a'])

