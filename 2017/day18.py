import sys
from collections import defaultdict

prog = [
    line.strip().split()
    for line in open(sys.argv[1]).readlines()
]

registers = defaultdict(lambda: 0)
last_snd = None

def val(v):
    try:
        return int(v)
    except ValueError:
        return registers[v]

def run(prog):
    pos = 0
    while pos >= 0 and pos < len(prog):
        ins = prog[pos]
        pos += 1
        if ins[0] == 'snd':
            last_snd = val(ins[1])
        elif ins[0] == 'set':
            registers[ins[1]] = val(ins[2])
        elif ins[0] == 'add':
            registers[ins[1]] += val(ins[2])
        elif ins[0] == 'mul':
            registers[ins[1]] *= val(ins[2])
        elif ins[0] == 'mod':
            registers[ins[1]] = registers[ins[1]] % val(ins[2])
        elif ins[0] == 'rcv':
            if val(ins[1]) != 0:
                print(last_snd)
                return
        elif ins[0] == 'jgz':
            x = val(ins[1])
            y = val(ins[2])
            if x  > 0:
                pos += y - 1

run(prog)
