import sys
import re

def parse(line):
    line = line.strip()
    if not line:
        return
    mo = re.search(r'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>', line)
    return Particle(*mo.groups())

class Particle(object):
    def __init__(self, *args):
        assert(len(args) == 9)
        self.p = list(map(lambda x: int(x), args[:3]))
        self.v = list(map(lambda x: int(x), args[3:6]))
        self.a = list(map(lambda x: int(x), args[6:]))

    def move(self):
        self.v[0] += self.a[0]
        self.v[1] += self.a[1]
        self.v[2] += self.a[2]
        self.p[0] += self.v[0]
        self.p[1] += self.v[1]
        self.p[2] += self.v[2]

    def dist(self):
        return sum(map(lambda x: abs(x), self.p))

def run(data):
    particles = []
    for line in data:
        p = parse(line)
        if p:
            particles.append(p)

    for _ in range(10000):
        for p in particles:
            p.move()
        posns = {}
        for n,p in enumerate(particles):
            posns[tuple(p.p)] = posns.get(tuple(p.p), []) + [n]
        remove = []
        for p, ns in posns.items():
            if len(ns) > 1:
                remove.extend(ns)
        remove.sort()
        for n in reversed(remove):
            del particles[n]

        d = {
            p.dist(): n
            for n, p in enumerate(particles)
        }
        m = min(d.keys())
        print len(particles), m, d[m]

data = open(sys.argv[1]).readlines()
print(run(data))
