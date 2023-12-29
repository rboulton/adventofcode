input='''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''.strip()
area = (7, 27)

input = open('2023/input24.txt', 'r').read()
area = (200000000000000, 400000000000000)

def parse_row(row):
    p, v = row.split(' @ ')
    p = [int(a) for a in p.split(', ')]
    v = [int(a) for a in v.split(', ')]
    assert v[0] != 0
    assert v[1] != 0
    assert v[2] != 0
    return tuple(p), tuple(v)

stones = [
    parse_row(row) for row in input.strip().split('\n')
]


def intersect_pos(stone1, stone2):
    (p1x, p1y, p1z), (v1x, v1y, v1z) = stone1
    (p2x, p2y, p2z), (v2x, v2y, v2z) = stone2
    
    # p1x + a v1x = p2x + b v2x
    # p1y + a v1y = p2y + b v2y
    
    # At x=x
    # p1x + a v1x = x  ->   a = (x - p1x) / v1x
    # y1 = p1y + (x - p1x) * v1y / v1x
    # y1 = (x * v1y + p1y * v1x - p1x * v1y) / v1x
    # 
    # y2 = (x * v2y + p2y * v2x - p2x * v2y) / v2x
    # 
    # At y1 = y2
    # (x * v1y + p1y * v1x - p1x * v1y) / v1x  = (x * v2y + p2y * v2x - p2x * v2y) / v2x
    # v2x * (x * v1y + p1y * v1x - p1x * v1y) = v1x * (x * v2y + p2y * v2x - p2x * v2y)
    # v2x * v1y * x + (v2x * p1y * v1x - v2x * p1x * v1y) = v1x * v2y * x + (v1x * p2y * v2x - v1x * p2x * v2y)
    # x * (v2x * v1y - v1x * v2y) = (v1x * p2y * v2x - v1x * p2x * v2y) - (v2x * p1y * v1x - v2x * p1x * v1y)
    if (v2x * v1y - v1x * v2y) == 0:
        # Parallel, compute y at x=0, to see if intersect
        y1 = p1y + (- p1x) * v1y / v1x
        y2 = p2y + (- p2x) * v2y / v2x
        assert abs(y1 - y2) > 0.0001
        return None, None, None, None
            
    x  = ((v1x * p2y * v2x - v1x * p2x * v2y) - (v2x * p1y * v1x - v2x * p1x * v1y)) / (v2x * v1y - v1x * v2y)
    y1 = p1y + (x - p1x) * v1y / v1x
    y2 = p2y + (x - p2x) * v2y / v2x
    
    # x = p1x + t * v1x
    # => t = (x - p1x) / v1x
    t1 = (x - p1x) / v1x
    t2 = (x - p2x) / v2x
    
    # assert abs(y1 - y2) < 2, (y1 - y2, y1, y2, stone1, stone2)
    return (x, y1, t1, t2)

count = 0
for i in range(len(stones)):
    for j in range(i + 1, len(stones)):
        x, y, t1, t2 = intersect_pos(stones[i], stones[j])
        if t1 is None or t1 < 0 or t2 < 0:
            continue
        if x < area[0] or x > area[1]:
            continue 
        if y < area[0] or y > area[1]:
            continue 
        #print(i, j, stones[i], stones[j], x, y, t1, t2)
        count += 1
print(count)