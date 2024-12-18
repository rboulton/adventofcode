import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''

data = open(os.path.join(os.path.dirname(__file__), "input17.txt")).read()
data = data.strip()
data = data.split('\n')

class Computer:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.pc = 0
        self.out = []

    def asm(self):
        out = []
        for pc in range(0, len(self.program), 2):
            opcode = self.program[pc]
            operand = self.program[pc + 1]
            if opcode in (0, 2, 5, 6, 7):
                combo = self.asm_combo_operand(operand)
            else:
                combo = None

            if opcode == 0:
                out.append(f'a = a >> {combo}')
            elif opcode == 1:
                out.append(f'b = (b ^ {operand}) % 8')
            elif opcode == 2:
                out.append(f'b = {combo} % 8')
            elif opcode == 3:
                out.append(f'if a != 0: pc = {operand}')
            elif opcode == 4:
                out.append(f'b = b ^ c')
            elif opcode == 5:
                out.append(f'out({combo} % 8)')
            elif opcode == 6:
                out.append(f'b = a >> {combo}')
            elif opcode == 7:
                out.append(f'c = a >> {combo}')
        return out

    def asm_combo_operand(self, operand):
        if operand <= 3:
            return str(operand)
        if operand == 4:
            return 'a'
        if operand == 5:
            return 'b'
        if operand == 6:
            return 'c'
        assert False, operand

    def run(self):
        while self.pc < len(self.program) - 1:
            self.do()
        return self.out

    def do(self):
        opcode = self.program[self.pc]
        operand = self.program[self.pc + 1]
        self.pc += 2
        if opcode == 0:
            combo = self.combo_operand(operand)
            self.a = self.a // (2 ** combo)
        elif opcode == 1:
            self.b = self.b ^ operand
        elif opcode == 2:
            self.b = self.combo_operand(operand) % 8
        elif opcode == 3:
            if self.a != 0:
                self.pc = operand
        elif opcode == 4:
            self.b = self.b ^ self.c
        elif opcode == 5:
            self.out.append(self.combo_operand(operand) % 8)
        elif opcode == 6:
            combo = self.combo_operand(operand)
            self.b = self.a // (2 ** combo)
        elif opcode == 7:
            combo = self.combo_operand(operand)
            self.c = self.a // (2 ** combo)

    def combo_operand(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        assert False, operand


a = int(data[0].split()[-1])
b = int(data[1].split()[-1])
c = int(data[2].split()[-1])
program_str = data[4].split()[-1]
program = tuple(map(int, program_str.split(',')))

computer = Computer(a, b, c, program)
steps = computer.asm()
print('\n'.join(steps))

possible_a = set()
for a in range(2**10):
    computer = Computer(a, b, c, program)
    r = computer.run()
    if r[0] == program[0]:
        possible_a.add(a)
        #print(repr(a), repr(r[0]), repr(program[0]))
#print(tuple(bin(a) for a in possible_a))

pos = 1
while pos < len(program):
    next_possible = set()
    for a1 in possible_a:
        for a2 in range(8):
            a = a1 + (a2 << (pos * 3 + 7))
            #print(bin(a), bin(a1), bin(a2))
            computer = Computer(a, b, c, program)
            r = computer.run()
            #print('pos', pos, r[:pos + 1], program[:pos + 1])
            if len(r) > pos and r[pos] == program[pos]:
                next_possible.add(a)
                #print(repr(a), repr(r[:pos+1]), repr(program[:pos+1]))
    pos += 1
    possible_a = next_possible
    print(min(next_possible))
