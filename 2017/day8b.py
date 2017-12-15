import sys
import re
from collections import namedtuple

Instruction = namedtuple('Intstruction', [
    'reg', 'val', 'cond_reg', 'cond_func', 'cond_val',
])

conditions = {
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
}

def parse_instruction(text):
    mo = re.match(r'^([a-z]+)\s+(inc|dec)\s+([-0-9]+)\s+if\s+([a-z]+)\s([<>=!]+)\s+([-0-9]+)$', text)
    assert mo
    reg, d, val, cond_reg, cond, cond_val = mo.groups()
    cond_func = conditions[cond]
    if d == 'dec':
        val = -int(val)
    else:
        val = int(val)
    cond_val = int(cond_val)
    return Instruction(reg, val, cond_reg, cond_func, cond_val)

def parse(filename):
    return [
        parse_instruction(line.strip())
        for line in open(filename).readlines()
        if line.strip()
    ]

def run(instructions, registers):
    highest = 0
    for instruction in instructions:
        if instruction.cond_func(registers.get(instruction.cond_reg, 0), instruction.cond_val):
            new_val = registers.get(instruction.reg, 0) + instruction.val
            highest = max(highest, new_val)
            registers[instruction.reg] = new_val
    return highest

instructions = parse(sys.argv[1])
registers = {}
print(run(instructions, registers))
print(max(registers.values()))
