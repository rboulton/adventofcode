import scipy.sparse.csgraph
from scipy.sparse import csr_matrix, csr_array

input = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''

_input = open("2023/input25.txt", "r").read()

components = {}
wires = set()
wires_from = {}

def add_wire(a, b):
    i = components.setdefault(a, len(components))
    j = components.setdefault(b, len(components))
    if i > j: i, j = j, i
    wires.add((i, j))
    wires_from.setdefault(i, set()).add(j)
    wires_from.setdefault(j, set()).add(i)

for row in input.strip().split('\n'):
    name, targets = row.split(': ')
    targets = targets.split(' ')
    for target in targets:
        add_wire(name, target)

graph = csr_matrix([[0] * len(components)] * len(components))
for wire in wires:
    i, j = wire
    graph[i, j] = 1
    graph[j, i] = 1
    
def max_flow(start, end):
    r = scipy.sparse.csgraph.maximum_flow(graph, start, end)
    # print("max_flow {} {} = {} ({})".format(start, end, r.flow_value, r.flow))
    return r.flow_value

print(len(wires))
    
start = 0
connected_more_than_3 = set()
connected_more_than_3.add(start)
for end in range(1, len(components)):
    f = max_flow(start, end)
    print(start, end, f)
    if f > 3:
        connected_more_than_3.add(end)
    
print(connected_more_than_3)
g1_size = len(connected_more_than_3)
g2_size = len(components) - len(connected_more_than_3)
print(g1_size, g2_size, g1_size * g2_size)