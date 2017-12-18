import sys
from collections import defaultdict

prog = [
    line.strip().split()
    for line in open(sys.argv[1]).readlines()
]

class Runner(object):
    def __init__(self, prog, in_pipe, out_pipe, pid):
        self.prog = prog
        self.in_pipe = in_pipe
        self.out_pipe = out_pipe
        self.waiting = False
        self.waiting_target = None
        self.running = True
        self.registers = defaultdict(lambda: 0)
        self.pos = 0
        self.registers['p'] = pid
        self.sent = 0

    def step(self):
        def val(v):
            try:
                return int(v)
            except ValueError:
                return self.registers[v]

        if self.pos < 0 or self.pos >= len(self.prog):
            self.running = False
        if not self.running:
            return

        if self.waiting:
            if len(self.in_pipe) > 0:
                self.registers[self.waiting_target] = self.in_pipe.pop(0)
                self.waiting = False
            return

        ins = self.prog[self.pos]
        self.pos += 1
        if ins[0] == 'snd':
            self.out_pipe.append(val(ins[1]))
            self.sent += 1
        elif ins[0] == 'rcv':
            self.waiting = True
            self.waiting_target = ins[1]
        elif ins[0] == 'set':
            self.registers[ins[1]] = val(ins[2])
        elif ins[0] == 'add':
            self.registers[ins[1]] += val(ins[2])
        elif ins[0] == 'mul':
            self.registers[ins[1]] *= val(ins[2])
        elif ins[0] == 'mod':
            self.registers[ins[1]] = self.registers[ins[1]] % val(ins[2])
        elif ins[0] == 'jgz':
            x = val(ins[1])
            y = val(ins[2])
            if x  > 0:
                self.pos += y - 1

    def stuck(self):
        return self.waiting and len(self.in_pipe) == 0

p1 = []
p2 = []

runner0 = Runner(prog, p1, p2, 0)
runner1 = Runner(prog, p2, p1, 1)

while runner0.running and runner1.running and not (runner0.stuck() and runner1.stuck()):
    runner0.step()
    runner1.step()
print(runner1.sent)
