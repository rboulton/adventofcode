input = '''
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''

input = open('2015/input9.txt', 'r').read()

distances = {}

for line in input.strip().split('\n'):
    a, _, b, _, d = line.split()
    d = int(d)
    distances.setdefault(a, {})[b] = d
    distances.setdefault(b, {})[a] = d

def routelen(start, visited, depth):
    # Return shortest route, starting at start, without going to anything in visited
    # print(' ' * depth, "From", start, 'excluding', ', '.join(sorted(visited)))
    ds = []
    next_visited = visited.union(set((start,)))
    for n, d in distances[start].items():
        if n in next_visited:
            continue
        rl = routelen(n, next_visited, depth + 1)
        ds.append(rl + d)
    if len(ds) == 0:
        return 0
    # print(' ' * depth, "Result: ", start, n, distances[start], ds, min(ds))
    return min(ds)

dists = []
for start in distances.keys():
    rl = routelen(start, set(), 0)
    dists.append(rl)
    print(start, rl)
print(min(dists))