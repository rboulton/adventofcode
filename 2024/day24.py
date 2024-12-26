import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
'''

data = '''
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''

data = open(os.path.join(os.path.dirname(__file__), "input24.txt")).read()
data = data.strip()
data = data.split('\n')

wires = {}
for row in data:
    if ':' in row:
        k, v = row.split(': ')
        wires[k] = int(v)
connections = []
for inputs, output in (row.split(' -> ') for row in data if '->' in row):
    in1, op, in2 = inputs.split(' ')
    connections.append((in1, op, in2, output))

def combine(v1, v2, op):
    if op == 'AND':
        return v1 & v2
    if op == 'OR':
        return v1 | v2
    if op == 'XOR':
        return v1 ^ v2
    assert False, op

while connections:
    nconn = []
    for in1, op, in2, output in connections:
        v1 = wires.get(in1)
        v2 = wires.get(in2)
        if v1 is not None and v2 is not None:
            v = combine(v1, v2, op)
            wires[output] = v
        else:
            nconn.append((in1, op, in2, output))
    connections = nconn

print(wires)
out = ''.join(
    str(v) for (k, v) in reversed(sorted((k, v) for (k, v) in wires.items() if k[0] == 'z'))
)
print(out)
print(int(out, 2))
