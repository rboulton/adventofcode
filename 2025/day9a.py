input = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''

input = open('input9.txt', 'r').read()

points = []
for row in input.strip('\n').split('\n'):
    points.append(tuple(map(int, row.split(','))))

max_area = 0
for i1, p1 in enumerate(points):
    for i2, p2 in enumerate(points[i1 + 1:], i1 + 1):
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        print(i1, i2, p1, p2, area, max_area)
        max_area = max(area, max_area)

print(max_area)
