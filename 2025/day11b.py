from collections import Counter
import re

input = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''

input = open('input11.txt', 'r').read()

# Assume acyclic network, otherwise our algorithm won't terminate
# If there's a route from A to B using only C, D, E then there must be only *one* route from A to B using C, D, E

links = []
fwdlinks = {}
revlinks = {}
nodes = set()

for row in input.strip('\n').split('\n'):
    a, b = row.split(':')
    b = b.strip(' ').split(' ')
    for c in b:
        links.append((a, c))
        nodes.add(a)
        nodes.add(c)
        fwdlinks.setdefault(a, set()).add(c)
        revlinks.setdefault(c, set()).add(a)

# Sort the nodes by maximum path distance to out:
max_dist = {'out': 0}
while True:
    changed = False
    for a, b in links:
        b_dist = max_dist.get(b, 0)
        if b_dist is None: continue
        a_dist = max_dist.get(a, 0)
        if a_dist < b_dist + 1:
            max_dist[a] = b_dist + 1
            changed = True
    if not changed:
        break

nodes_by_distance = list(sorted((d, k) for k, d in max_dist.items()))
print(nodes_by_distance)

# Add in nodes in increasing distance order, adding up the number of paths from the node to 'out'.
# Doing in distance order guarantees that we don't miss some longer paths that later get added.
special_nodes = ('dac', 'fft')
routes = {'out': Counter({0: 1})}
for _, node in nodes_by_distance[1:]: # First node is 'out'
    count = Counter()
    for a, b in links:
        if a == node:
            if a in special_nodes:
                for special_node_count, num in routes[b].items():
                    count[special_node_count + 1] += num
            else:
                for special_node_count, num in routes[b].items():
                    count[special_node_count] += num
    routes[node] = count

print(routes['svr'][2])
