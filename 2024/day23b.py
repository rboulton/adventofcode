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

links = {}

for row in data:
    a, b = sorted(row.split('-'))
    links.setdefault(a, []).append(b)
    links.setdefault(b, []).append(a)

groups = set((node,) for node in links.keys())

def enlarge(groups):
    result = set()
    for g in groups:
        additions = None
        for a in g:
            if additions is None:
                additions = set(links[a])
            else:
                additions.intersection_update(links[a])
        for new in additions:
            result.add(tuple(sorted(g + (new,))))
    return result

while len(groups) > 0:
    print(len(groups))
    print(','.join(tuple(groups)[0]))
    groups = enlarge(groups)
