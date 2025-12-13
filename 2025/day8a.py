input = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''

input = open('input8.txt', 'r').read()

class Point:
    def __init__(self, i, row):
        self.i = i
        self.x, self.y, self.z = map(int, row.split(','))
        self.c = None

points = []
for row in input.strip('\n').split('\n'):
    points.append(Point(len(points), row))

def dist(a, b):
    return (a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2

dists = []
for p1 in points:
    for p2 in points[p1.i+1:]:
        d = dist(p1, p2)
        dists.append((d, p1, p2))
dists.sort(key=lambda x: x[0])

clusters = {}
for i, (d, p1, p2) in enumerate(dists[:1000]):
    if p1.c is None:
        p1.c = i
        clusters[p1.c] = set((p1.i,))
    if p2.c is None:
        p2.c = p1.c
        clusters[p1.c].add(p2.i)
    elif p2.c != p1.c:
        old_c = p2.c
        for p_i in clusters[old_c]:
            clusters[p1.c].add(p_i)
            points[p_i].c = p1.c
        del clusters[old_c]
    print(i, clusters)

cluster_lens = [len(clusters[c]) for c in clusters]
cluster_lens.sort(reverse=True)
print(cluster_lens[0] * cluster_lens[1] * cluster_lens[2])

