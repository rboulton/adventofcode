input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''
_input = '''
U 4 (#7a21e3)
R 6 (#7a21e3)
D 4 (#7a21e3)
L 2 (#7a21e3)
U 2 (#7a21e3)
L 2 (#7a21e3)
D 2 (#7a21e3)
L 2 (#7a21e3)
'''

input = open('2023/input18.txt', 'r').read()

def pairwise(s):
    i = iter(s)
    return zip(i, i)

def overlap(a1, a2, b1, b2):
    r = max(a1, b1)
    l = min(a2, b2)
    if r > l:
        return 0
    return 1 + l - r

class Grid:
    def __init__(self):
        self.vertical_edges = set()
        self.horizontals = set()
        
    def add_edge(self, x1, y1, x2, y2):
        if y2 < y1:
            y1, y2 = y2, y1
        if x1 == x2:
            self.vertical_edges.add((x1, y1, y2))
            self.horizontals.add(y1)
            self.horizontals.add(y2)
        else:
            assert y1 == y2
            
    def filled(self):
        return self.area_between_verticals()

    def area_between_verticals(self):
        # Find size of full rows between verticals
        split_edges = set()
        sorted_horizontals = list(sorted(self.horizontals))
        for x, y1, y2 in self.vertical_edges:
            for y in sorted_horizontals:
                if y <= y1:
                    continue
                if y >= y2:
                    split_edges.add((x, y1, y2))
                    break
                split_edges.add((x, y1, y))
                y1 = y
        lastx = None
        lasty1 = None
        boxes = []
        for e1, e2 in pairwise(sorted(split_edges, key=lambda e: (e[1], e[2], e[0]))):
            if lasty1 != e2[1]:
                lastx = None
                lasty1 = e2[1]
            if lastx is not None:
                assert lastx < e1[0]
                
            assert e1[1] == e2[1]
            assert e1[2] == e2[2]
            x1, y1, x2, y2 = e1[0], e1[1], e2[0], e1[2]
            boxes.append((x1, y1, x2, y2))
            lastx = e2[0]
            
        size = 0
        boxes_at_top = {}
        for box in boxes:
            x1, y1, x2, y2 = box
            boxes_at_top.setdefault(y2, []).append(box)

        for box in boxes:
            x1, y1, x2, y2 = box
            h = 1 + y2 - y1
            w = 1 + x2 - x1
            a = h * w
            #print("Adding", x1, y1, x2, y2, "=", a)
            size += a
            
            for box2 in boxes_at_top.get(y1, []):
                bx1, bx2 = box2[0], box2[2]
                o = overlap(x1, x2, bx1, bx2)
                #print("Subtracting overlap", x1, x2, bx1, bx2, "=", o)
                size -= o
            
        return size

offsets = {
    'R': (1, 0),
    'D': (0, -1),
    'L': (-1, 0),
    'U': (0, 1),
}

g = Grid()

x, y = 0, 0
for row in input.strip().split('\n'):
    _, _, code = row.split(' ')
    code = code[2:-1]
    dir = 'RDLU'[int(code[-1])]
    dist = int(code[:5], 16)
    
    # dir, dist, _ = row.split(' ')
    # dist = int(dist)
    
    o = offsets[dir]
    nx = x + o[0] * dist
    ny = y + o[1] * dist
    g.add_edge(x, y, nx, ny)
    x, y = nx, ny
 
print("End at", x, y) 
print(g.filled())