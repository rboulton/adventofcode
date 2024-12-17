import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''

data = open(os.path.join(os.path.dirname(__file__), "input17.txt")).read()
data = data.strip()
data = data.split('\n')

class Computer:
    def __init__(self, rows):
        self.a = int(rows[0].split()[-1])
        self.b = int(rows[1].split()[-1])
        self.c = int(rows[2].split()[-1])
        self.program = tuple(map(int, rows[4].split()[-1].split(',')))
        self.pc = 0
        self.out = []

    def run(self):
        while self.pc < len(self.program) - 1:
            self.do()
        return ','.join(self.out)

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
            self.out.append(str(self.combo_operand(operand) % 8))
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


c = Computer(data)
print(c.run())
