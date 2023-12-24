'''This one doesn't work - but it did show the structure needed

I then went back and used my cleaner solution to part 1, and made it into
day20b2.py which finds the right answer
'''

import collections
import sys

input = open('2023/input20.txt', 'r').read()

class Pulse:
    def __init__(self, source, dest, value):
        self.source = source
        self.dest = dest
        self.value = value
        
    def __repr__(self):
        return "{} {} -> {}".format(self.source, self.value, ''.join(self.dest))

class Module:
    def downstream_interesting_dests(self, visited=None, interesting=None):
        if visited is None:
            visited = set()
        result = []
        for name in self.dests:
            if name in visited:
                continue
            visited.add(name)
            if name in interesting:
                result.append(name)
            m = modules[name]
            result.extend(m.downstream_interesting_dests(visited, interesting))
        return result
        
    
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
            yield None
            
    def __repr__(self):
        return 'Ender<{}>'.format(self.name)
        
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
        return 'Broadcaster<{}: {}>'.format(
            self.name, ', '.join(
                "{}:{}".format(modules[d].name, modules[d].depth)
                for d in self.dests)
            )

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
        return 'FlipFlop<{}: -> {}>'.format(self.name, ', '.join(
            "{}:{}".format(modules[d].name, modules[d].depth)
            for d in self.dests
        ))
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
        return 'Conjunction<{}: {} -> {}>'.format(
            self.name,
            ', '.join(
                "{}:{}".format(modules[d].name, modules[d].depth)
                for d in self.inputs.keys()
            ), ', '.join(
                "{}:{}".format(modules[d].name, modules[d].depth)
                for d in self.dests
            )
        )
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

def calc_level(modules):
    row = [modules['rx']]
    shown = {}
    depth = 0
    while len(row) > 0:
        next_row = []
        for m in row:
            m.depth = depth
            print(m.name, "=", depth)
            for s in m.inputs:
                if s in shown:
                    continue
                sourcemod = modules[s]
                shown[s] = depth
                next_row.append(sourcemod)
        row = next_row
        depth += 1


def display_tree(modules):
    depth = 0
    while True:
        row = [m for m in modules.values() if m.depth == depth]
        if len(row) == 0:
            break
        for m in row:
            print(depth, m)
        depth += 1
    return

def separate_tree(modules):
    interesting = set(m.name for m in modules.values() if m.depth == 2)
    groups = {}
    for m in modules.values():
        group = m.downstream_interesting_dests(None, interesting)
        if len(group) == 1:
            groups.setdefault(group[0], []).append(m)
    return groups
    

def process_pulse(p):
    m = modules[p.dest]
    for p in m.signal(p):
        if p is None:
            STOP
        process_pulse(p)

calc_level(modules)
groups = separate_tree(modules)
print(groups)

prev_states = {}
def group_state(name):
    state = [
        m.state
        for m in groups[name]
    ]
    return ''.join(state)

loop_times = {}
button_presses = 0
while True:
    p = Pulse('button', 'broadcaster', 0)
    button_presses += 1
    process_pulse(p)
    for name in groups.keys():
        s = group_state(name)
        # print(button_presses, name, modules[name], modules[name].state)
        k = (name, s)
        if k in prev_states:
            c = prev_states[k]
            # print("Found!", k, c)
            if name not in loop_times:
                loop_times[name] = c
                print("Loop:", k, c, button_presses, button_presses - c)
        else:
            prev_states[k] = button_presses
    display_tree(modules)
    # print()
print(i)