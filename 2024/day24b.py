import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter
from itertools import combinations

data = open(os.path.join(os.path.dirname(__file__), "input24.txt")).read()
data = data.strip()
data = data.split('\n')

wires = {}
for row in data:
    if ':' in row:
        k, v = row.split(': ')
        wires[k] = int(v)

digits = int(max(w for w in wires.keys() if w[0] == 'x')[1:]) + 1
assert digits == int(max(w for w in wires.keys() if w[0] == 'y')[1:]) + 1

for inputs, output in (row.split(' -> ') for row in data if '->' in row):
    in1, op, in2 = inputs.split(' ')
    if in1 > in2:
        in1, in2 = in2, in1
    wires[output] = (op, in1, in2)

def combine(op ,v1, v2):
    if op == 'AND':
        return v1 & v2
    if op == 'OR':
        return v1 | v2
    if op == 'XOR':
        return v1 ^ v2
    assert False, op

def calc_renames(wires):
    renames = {}
    todo = set()
    for out, val in wires.items():
        if out[0] in 'xy':
            renames[out] = out
            continue
        op, in1, in2 = val
        if in1[0] in 'xy':
            assert in2[0] in 'xy', (in1, in2)
            assert in1[1:] == in2[1:], (in1, in2)
            renames[out] = op[0] + in1[1:]
            continue
        todo.add(out)

    while todo:
        for out in tuple(todo):
            assert out not in renames, out
            val = wires[out]
            op, in1, in2 = val
            in1 = renames.get(in1)
            in2 = renames.get(in2)
            if in1 is None or in2 is None: continue
            #print(out, op, in1, in2)
            v1 = int(in1[1:])
            v2 = int(in2[1:])
            if v1 > v2:
                v1, v2 = v2, v1
            if op == 'OR':
                # assert v1 + 1 == v2
                rename = f'C{v2:02d}'
            elif op == 'AND':
                # assert v1 + 1 == v2
                rename = f'D{v2:02d}'
            elif op == 'XOR':
                # assert v1 + 1 == v2
                rename = f'Z{v2:02d}'
            else:
                assert False, out
            #print(f'{out} => {rename}')
            assert rename not in renames.values()
            renames[out] = rename
            todo.remove(out)

    return renames

def calc_corrections(wires, renames):
    result = []
    rev = dict((v, k) for (k, v) in renames.items())
    swapped = set()

    # Check that all the zXX wires got renamed to ZXX (for XX >= 01)
    for i in range(1, digits):
        k = f'Z{i:02d}'
        v = rev[k]
        v2 = f'z{i:02d}'
        if v != v2:
            print(k, v, v2, renames[v2])
            if v2 < v:
                v, v2 = v2, v
            result.append((v, v2))
            swapped.update((k, renames[v2]))

    # Check that all inputs to the ZXX wires are named C{XX-1} and X{XX}
    for i in range(2, digits):
        z = f'Z{i:02d}'
        c = f'C{i-1:02d}'
        x = f'X{i:02d}'
        op, in1, in2 = wires[rev[z]]
        r_in1 = renames[in1]
        r_in2 = renames[in2]
        if z in swapped or r_in1 in swapped or r_in2 in swapped: continue
        missed1 = set((c, x)).difference((r_in1, r_in2))
        missed2 = set((r_in1, r_in2)).difference((c, x))
        if not missed1: continue
        assert len(missed1) == 1
        assert len(missed2) == 1
        m1 = tuple(missed1)[0]
        m2 = tuple(missed2)[0]
        swapped.update((m1, m2))
        result.append((rev[m1], rev[m2]))
        print(r_in1, m1, m2)

    print(swapped)
    return result

def active(wires, renames, x, y):
    """Return the list of active wires"""
    states = {}
    for i in range(digits):
        states[f'x{i:02d}'] = 1 if (x & (1 << i)) else 0
        states[f'y{i:02d}'] = 1 if (y & (1 << i)) else 0

    already_seen = set()
    for i in range(digits + 1):
        seen = set()
        z_out = f'z{i:02d}'
        stack = [z_out]
        newly_calculated = []
        while stack:
            target = stack[-1]
            if target in states:
                stack.pop()
            else:
                (op, in1, in2) = wires[target]
                if renames[in2] < renames[in1]:
                    in1, in2 = in2, in1
                seen.add(target)
                seen.add(in1)
                seen.add(in2)
                if in1 not in states:
                    stack.append(in1)
                if in2 not in states:
                    stack.append(in2)
                if in1 in states and in2 in states:
                    states[target] = combine(op, states[in1], states[in2])
                    newly_calculated.append(target)
        print(f"calculating {z_out} : {renames[z_out]}")
        for target in newly_calculated:
            (op, in1, in2) = wires[target]
            print(f'{renames[target]} = {op}, {renames[in1]}, {renames[in2]}')
        print("newly_calculated", list(sorted(map(lambda x: renames[x], newly_calculated))))
        print(z_out, list(sorted(seen)))
        print()
        already_seen.update(seen)


def eval(wires, x, y):
    states = {}
    for output, val in wires.items():
        if type(val) == int:
            continue
        (op, in1, in2) = val
        if in1[0] in 'xy': states[in1] = 0
        if in2[0] in 'xy': states[in2] = 0
    for i, bit in enumerate(reversed(bin(x)[2:])):
        states[f'x{i:02d}'] = int(bit)
    for i, bit in enumerate(reversed(bin(y)[2:])):
        states[f'y{i:02d}'] = int(bit)

    connections = wires
    while connections:
        changed = False
        nconn = {}
        for output, val in connections.items():
            if type(val) == int:
                continue
            (op, in1, in2) = val
            v1 = states.get(in1)
            v2 = states.get(in2)
            if v1 is not None and v2 is not None:
                v = combine(op, v1, v2)
                states[output] = v
                changed = True
            else:
                nconn[output] = (op, in1, in2)
        if not changed:
            return None, None
        connections = nconn
    return wireval(states, 'z'), [w for (w, v) in states.items() if v]

def wireval(wires, prefix):
    out = ''.join(
        str(v) for (k, v) in reversed(sorted((k, v) for (k, v) in wires.items() if k[0] == prefix))
    )
    return int(out, 2)

def test_val(wires, i):
    involved = set()

    x = int('1' + '0' * i, 2)
    z, active = eval(wires, x, 0)
    if z is None: return None
    active = [w for w in active if w[0] not in 'xy']
    if (x != z):
        #print('x', i, x, z, active)
        involved.update(active)
        '''
        for w in active:
            print(f'  {w} = {wires[w]}')
            print(f'    {wires[w][1]} = {wires[wires[w][1]]}')
            print(f'    {wires[w][2]} = {wires[wires[w][2]]}')
        #'''

    x = int('1' + '0' * i, 2)
    z, active = eval(wires, x, x)
    if z is None: return None
    active = [w for w in active if w[0] not in 'xy']
    if (2 * x != z):
        #print('z', i, x, z, active)
        involved.update(active)
        '''
        for w in active:
            print(f'  {w} = {wires[w]}')
            print(f'    {wires[w][1]} = {wires[wires[w][1]]}')
            print(f'    {wires[w][2]} = {wires[wires[w][2]]}')
        #'''

    return involved

def test(wires, indicies):
    for i in range(min(indicies) - 1, max(indicies) + 2):
        involved = test_val(wires, i)
        if involved is None:
            # print(f'Fail: {i}, unsoluble')
            return False
        if involved:
            # print(f'Fail: {i}, {involved}')
            return False
    return True

def find_swapgroups():
    swapgroups = []
    for i in range(digits):
        involved = test_val(wires, i)
        if involved:
            # print(i, involved)
            for inputs, g in swapgroups:
                if g.intersection(involved):
                    g.update(involved)
                    inputs.add(i)
                    break
            else:
                swapgroups.append((set((i,)), involved))
    for g in swapgroups:
        print(g)
    return swapgroups

def test_swap(inputs, pair):
    a, b = pair
    w = copy.deepcopy(wires)
    w[b], w[a] = w[a], w[b]
    t = test(w, inputs)
    if t:
        print(pair, t)

'''
print()
swapgroups = find_swapgroups()
for inputs, group in swapgroups:
    print(f"Swapgroup {inputs}, {group}")
    for pair in combinations(group, 2):
        test_swap(inputs, pair)
'''

renames = calc_renames(wires)
corrections = calc_corrections(wires, renames)
result = []
for v in corrections:
    result.extend(v)
print('Result:', ','.join(sorted(result)))

print()
print(f"Corrections: {corrections}")
for a, b in corrections:
    wires[a], wires[b] = wires[b], wires[a]

print()
swapgroups = find_swapgroups()
for inputs, group in swapgroups:
    print(f"Swapgroup {inputs}, {group}")
    for pair in combinations(group, 2):
        test_swap(inputs, pair)

'''
print()
renames = calc_renames(wires)
print(active(wires, renames, 1, 2))
'''
