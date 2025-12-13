from collections import Counter
from grid import Coord

input = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''

input = open('input9.txt', 'r').read()

class Rect:
    def __init__(self, p1, p2):
        if p1.x < p2.x:
            self.x1, self.x2 = p1.x, p2.x
        else:
            self.x1, self.x2 = p2.x, p1.x
        if p1.y < p2.y:
            self.y1, self.y2 = p1.y, p2.y
        else:
            self.y1, self.y2 = p2.y, p1.y

    def __str__(self):
        return f'Rect({self.x1}, {self.y1}, {self.x2}, {self.y2})'

    def intersects(self, line):
        # Does the line have any part of it inside the rectangle (not just at the edge)
        if line.vertical:
            if line.start.x <= self.x1 or line.start.x >= self.x2:
                return False
            if line.end.y <= self.y1 or line.start.y >= self.y2:
                return False
        else:
            if line.start.y <= self.y1 or line.start.y >= self.y2:
                return False
            if line.end.x <= self.x1 or line.start.x >= self.x2:
                return False
        return True

    def check(self):
        for l in lines:
            # print(f"Checking {self} {l}")
            if self.intersects(l):
                print(f"Intersect: {self} {l}")
                return False
        return True

    def area(self):
        return (abs(self.x1 - self.x2) + 1) * (abs(self.y1 - self.y2) + 1)

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.vertical = (start.x == end.x)
        if self.vertical:
            if self.start.y > self.end.y:
                self.start, self.end = self.end, self.start
        else:
            assert start.y == end.y
            if self.start.x > self.end.x:
                self.start, self.end = self.end, self.start

    def __str__(self):
        return f'Line({self.start}, {self.end}, {self.vertical})'


lines = []
points = []
prev = None
for row in input.strip('\n').split('\n'):
    p = Coord(*list(map(int, row.split(','))))
    points.append(p)
    if prev is not None:
        lines.append(Line(prev, p))
    prev = p
lines.append(Line(prev, points[0]))

for i in range(len(points) - 1):
    lines.append(Line(points[i], points[i+1]))

max_area = 0
for i1, p1 in enumerate(points):
    for i2, p2 in enumerate(points[i1 + 1:], i1 + 1):
        r = Rect(p1, p2)
        if r.check():
            a = r.area()
            print(p1, p2, r, a)
            max_area = max(a, max_area)

print(max_area)
