import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

data = open(os.path.join(os.path.dirname(__file__), "input23.txt")).read()
data = data.strip()
data = data.split('\n')

graph = {}

for row in data:
    a, b = sorted(row.split('-'))
    graph.setdefault(a, []).append(b)

def triples():
    for a, nodes in sorted(graph.items()):
        for b in sorted(nodes):
            for c in graph.get(b, ()):
                if c in nodes:
                    yield a, b, c

def t_triples():
    for a, b, c in triples():
        if a.startswith('t') or b.startswith('t') or c.startswith('t'):
            yield a, b, c

print(len(tuple(t_triples())))
