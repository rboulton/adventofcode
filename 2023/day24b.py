from typing import Self
from sympy import symbols, Eq, solve

input='''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''.strip()

input = open('2023/input24.txt', 'r').read()

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '[{} {} {}]'.format(self.x, self.y, self.z)
    
    def __mul__(self, mult):
        return Vector(self.x * mult, self.y * mult, self.z * mult)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return self + other * -1
    
    def dist_square(self, other):
        d = self + other * -1
        return d.x * d.x + d.y * d.y + d.z * d.z
    
    def cross(self, other: Self):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )
        
class Stone:
    def __init__(self, p, v):
        self.p = Vector(*p)
        self.v = Vector(*v)
        
    def __repr__(self):
        return 'Stone<{} {}>'.format(self.p, self.v)

def parse_row(row):
    p, v = row.split(' @ ')
    p = [int(a) for a in p.split(', ')]
    v = [int(a) for a in v.split(', ')]
    return Stone(p, v)

stones = [
    parse_row(row) for row in input.strip().split('\n')
]

def calc_dist(args):
    # First 6 args are the rock start position and velocity
    # Following args are the intersection times
    # assert len(args) == 6 + len(stones)
    rp = Vector(*args[:3])
    rv = Vector(*args[3:6])
    t = args[6:]
    dist_square = 0
    for i in range(len(t)):
        rock_pos = rp + rv * t[i]
        stone_pos = stones[i][0] + stones[i][1] * t[i]
        dist_square += rock_pos.dist_square(stone_pos)
    return math.sqrt(dist_square)


def calc_intersect(stones):
    # r is the rock, si is stone i
    # r.p + t1 * r.v == s1.p + t1 * s1.v
    # r.p + t2 * r.v == s2.p + t2 * s2.v
    # r.p + t3 * r.v == s3.p + t3 * s3.v
    # ...
    # r.p + tN * r.v == sN.p + tN * sN.v
    
    # 6 + N unknowns, 3 * N equations
    # N == 1  => 7 unknowns, 3 equations
    # N == 2  => 8 unknowns, 6 equations
    # N == 3  => 9 unknowns, 9 equations
    # So should be able to solve with 3 equations, then verify
    
    # Note - we want to use 3 dimensions, though it's possible just using 2
    # If we just look at x: 2 + N unknowns, N equations - can never solve
    # If we just look at x and y: 4 + N unknowns, 2 * N equations -> need 4 equations
    
    rp_x, rp_y, rp_z, rv_x, rv_y, rv_z, t1, t2, t3 = symbols("rp_x rp_y rp_z rv_x rv_y rv_z t1 t2 t3")
    
    eqs = [
        Eq(rp_x + t1 * rv_x, stones[0].p.x + t1 * stones[0].v.x),
        Eq(rp_y + t1 * rv_y, stones[0].p.y + t1 * stones[0].v.y),
        Eq(rp_z + t1 * rv_z, stones[0].p.z + t1 * stones[0].v.z),
        Eq(rp_x + t2 * rv_x, stones[1].p.x + t2 * stones[1].v.x),
        Eq(rp_y + t2 * rv_y, stones[1].p.y + t2 * stones[1].v.y),
        Eq(rp_z + t2 * rv_z, stones[1].p.z + t2 * stones[1].v.z),
        Eq(rp_x + t3 * rv_x, stones[2].p.x + t3 * stones[2].v.x),
        Eq(rp_y + t3 * rv_y, stones[2].p.y + t3 * stones[2].v.y),
        Eq(rp_z + t3 * rv_z, stones[2].p.z + t3 * stones[2].v.z),
    ]
    print(eqs)
 
    r = solve(eqs, (rp_x, rp_y, rp_z, rv_x, rv_y, rv_z, t1, t2, t3))
    print(r)
    return r[0][:3]

r = calc_intersect(stones)
print(sum(r))