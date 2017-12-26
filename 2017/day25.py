import sys

lines = map(lambda x: x.strip().strip(':').strip('.'), open(sys.argv[1]).readlines())

tape = []

def set(p, v):
    pos = abs(p * 2) - (1 if p < 0 else 0)
    while len(tape) <= pos:
        tape.append(0)
    tape[pos] = v

def get(p):
    pos = abs(p * 2) - (1 if p < 0 else 0)
    try:
        return tape[pos]
    except IndexError:
        return 0

start = lines[0].split(' ')[-1]
steps = int(lines[1].split(' ')[-2])
rules = {}
for group in range(3, len(lines), 10):
    group = [
        line.split()[-1]
        for line in lines[group:group+9]
    ]
    state = group[0]
    assert group[1] == '0'
    assert group[5] == '1'
    rules[state] = [
        [int(group[2]), group[3], group[4]],
        [int(group[6]), group[7], group[8]],
    ]
    print repr((start, steps, group, state, rules[state]))

p = 0
state = start
print [get(i) for i in range(-10, 10)], state
for step in xrange(steps):
    newval, direction, nextstate = rules[state][int(get(p))]
    set(p, newval)
    if direction == 'right':
        p += 1
    elif direction == 'left':
        p -= 1
    else:
        assert False, direction
    state = nextstate
    #print [get(i) for i in range(-10, 10)], state
    if step % 1000000 == 0:
        print step, steps, len(tape)
print step, steps, len(tape)
print tape.count(1)
