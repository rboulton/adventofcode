import sys
from collections import defaultdict

edges = [
    map(lambda x: int(x), line.strip().split('/'))
    for line in open(sys.argv[1]).readlines()
]

edgecost = {
    edgenum: sum(edge)
    for edgenum, edge in enumerate(edges)
}

# Find longest path without reusing edges, starting at node 0

nodes = defaultdict(lambda: set())
for edgenum, edge in enumerate(edges):
    nodes[edge[0]].add(edgenum)
    nodes[edge[1]].add(edgenum)
nodes = dict(nodes)

def walk_edges(node, visited_edges):
    yield visited_edges
    for edgenum in (n for n in nodes[node] if n not in visited_edges):
        edge = edges[edgenum]
        assert node in edge, (node, edge)
        other_node = edge[0] if edge[1] == node else edge[1]
        for v in walk_edges(other_node, list(visited_edges) + [edgenum]):
            yield v

max_cost = 0
max_len = 0
for path in walk_edges(0, []):
    if len(path) >= max_len:
        max_len = len(path)
        cost = sum([edgecost[edge] for edge in path])
        max_cost = max(cost, max_cost)
print max_cost
