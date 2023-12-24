'''Brute force attempt - would never get there'''

import collections
from re import A
import sys

from numpy import kaiser

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
        
    def __repr__(self):
        return "{} {} -> {}".format(self.source, self.value, ''.join(self.dest))

class Module:
    def downstream(self, visited=None):
        s = ['{}={} '.format(self.name, self.state)]
        # print(s, visited)
        if visited is None:
            visited = set()
        for name in self.dests:
            if name in visited:
                # print("visited", name)
                continue
            else:
                # print("visiting", name)
                visited.add(name)
            m = modules[name]
            d = m.downstream(visited)
            # print("slen", len(s), self.name, repr(s[:200]))
            s.append(d)
            # print(m.name, m.state)
        return ''.join(s)
    
    def set_downstream(self, value):
        # print("setting downstream of", self.name, repr(value))
        assert value[-1] == ' '
        for v in value[:-1].split(' '):
            name, state = v.split('=')
            m = modules[name]
            m.state = state
 
class Ender(Module):
    def __init__(self, name='Ender'):
        self.name = name
        self.dests = ()
        self.inputs = {}
        self.state = ''
        super().__init__()
        
    def connect(self, source):
        self.inputs[source] = 0
        
    def signal(self, pulse: Pulse):
        if pulse.value == 0:
            print(button_presses)
            yield None
            
    def __repr__(self):
        return 'Ender<>'
        
class Broadcaster(Module):
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.inputs = {}
        self.state = ''
        super().__init__()
        
    def connect(self, source):
        self.inputs[source] = 0
    
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        for dest in self.dests:
            yield Pulse(self.name, dest, pulse.value)
            
    def __repr__(self):
        return 'Broadcaster<{}: {}>'.format(self.name, self.dests)
            
class FlipFlop(Module):
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self._state = 0
        self.inputs = {}
        super().__init__()

    @property
    def state(self):
        return str(self._state)
    
    def connect(self, source):
        self.inputs[source] = 0
    
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        if pulse.value == 0:
            self._state = 1 - self._state
            for dest in self.dests:
                yield Pulse(self.name, dest, self._state)
                
    def __repr__(self):
        return 'FlipFlop<{}: -> {}>'.format(self.name, ', '.join(self.dests))
        return 'FlipFlop<{}: {} -> {}>'.format(self.name, self._state, self.dests)
            
class Conjunction(Module):
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.inputs = {}
        super().__init__()

    @property
    def state(self):
        return ''.join(str(v) for k,v in sorted(self.inputs.items()))

    def connect(self, source):
        self.inputs[source] = 0
        
    def signal(self, pulse: Pulse):
        assert pulse.dest == self.name
        assert pulse.source in self.inputs, (pulse.source, self.inputs)
        self.inputs[pulse.source] = pulse.value
        vs = set(self.inputs.values())
        if 0 in vs:
            v = 1
        else:
            v = 0
        for dest in self.dests:
            yield Pulse(self.name, dest, v)

    def __repr__(self):
        return 'Conjunction<{}: {} -> {}>'.format(self.name, ', '.join(self.inputs.keys()), ', '.join(self.dests))
        return 'Conjunction<{}: {} -> {}>'.format(self.name, self.inputs, self.dests)
            
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

modules['rx'] = Ender('rx')
for m in list(modules.values()):
    for d in m.dests:
        if d not in modules:
            modules[d] = Broadcaster(d, ())
            
for m in modules.values():
    for d in m.dests:
        modules[d].connect(m.name)

def display_tree(modules):
    row = [modules['rx']]
    shown = set()
    print(row[0])
    while len(row) > 0:
        next_row = []
        for m in row:
            for s in m.inputs:
                if s in shown:
                    continue
                sourcemod = modules[s]
                print(sourcemod, end=' ')
                shown.add(s)
                next_row.append(sourcemod)
        print()
        row = next_row

pulse_queue = []
counts = collections.Counter()
button_presses = 0
print("D", modules['broadcaster'].downstream())

def process_pulse(p):
    counts[p.value] += 1
    m = modules[p.dest]
    for p in m.signal(p):
        if p is None:
            STOP
        process_pulse(p)

for i in range(1000000):
    p = Pulse('button', 'broadcaster', 0)
    button_presses += 1
    process_pulse(p)
    # display_tree(modules)
    # print()
    # print(i, modules['bh'].state)
    # print("D", modules['broadcaster'].downstream())
print(i)
print("D", modules['broadcaster'].downstream())