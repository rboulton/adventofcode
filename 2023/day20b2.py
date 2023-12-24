'''This gets the right answer - there are 4 subgraphs, which have to all output
0 at the same time - and each emit a 1 every N steps'''

import math

input='''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

input='''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''

input = open('2023/input20.txt', 'r').read()

def add_pulse(pulse):
    pulse_queue.append(pulse)
    # print(str(pulse))

class Pulse:
    def __init__(self, source, dest, value):
        self.source = source
        self.dest = dest
        self.value = value
        
    def __str__(self):
        return "{} {} -> {}".format(self.source, self.value, self.dest)
        
    def __repr__(self):
        return "{} {} -> {}".format(self.source, self.value, ''.join(self.dest))
        
class Broadcaster:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        
    def connect(self, source):
        pass
    
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        for dest in self.dests:
            add_pulse(Pulse(self.name, dest, pulse.value))
            
    def __repr__(self):
        return 'Broadcaster<{}>'.format(self.dests)
            
class FlipFlop:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.state = 0
        
    def connect(self, source):
        pass
    
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        if pulse.value == 0:
            self.state = 1 - self.state
            for dest in self.dests:
                add_pulse(Pulse(self.name, dest, self.state))
                
    def __repr__(self):
        return 'FlipFlop<{} -> {}>'.format(self.state, self.dests)
            
class Conjunction:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.inputs = {}
        
    def connect(self, source):
        self.inputs[source] = 0
        
    def out(self):
        vs = set(self.inputs.values())
        if 0 in vs:
            return 1
        else:
            return 0
       
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        assert pulse.source in self.inputs, (pulse.source, self.inputs)
        self.inputs[pulse.source] = pulse.value
        v = self.out()
        for dest in self.dests:
            add_pulse(Pulse(self.name, dest, v))

    def __repr__(self):
        return 'Conjunction<{} -> {}>'.format(self.inputs, self.dests)
            
def make_module(row):
    m, dest = row.split(' -> ')
    dests = dest.split(', ')
    if m == 'broadcaster':
        return Broadcaster(m, dests)
    if m[0] == '%':
        return FlipFlop(m[1:], dests)
    assert m[0] == '&'
    return Conjunction(m[1:], dests)

modules = {}
modules['output'] = Broadcaster('output', ())
for row in input.strip().split('\n'):
    m = make_module(row)
    assert m.name not in modules
    modules[m.name] = m

for m in list(modules.values()):
    for d in m.dests:
        if d not in modules:
            modules[d] = Broadcaster(d, ())
            
for m in modules.values():
    for d in m.dests:
        modules[d].connect(m.name)
print(modules)

def process_queue():
    zeros = set()
    while len(pulse_queue) > 0:
        p = pulse_queue.pop(0)
        if p.source in ('xc', 'cn', 'gh', 'hz'):
            if p.value == 0:
                zeros.add(p.source)
        m = modules[p.dest]
        m.signal(p)
    return zeros
        
pulse_queue = []
cycles = {}
for i in range(1, 10000):
    add_pulse(Pulse('button', 'broadcaster', 0))
    zeros = process_queue()
    if len(zeros) > 0:
        print(i, zeros)
    for n in zeros:
        cycles.setdefault(n, i)
    if len(cycles) == 4:
        break

print(math.lcm(*cycles.values()))