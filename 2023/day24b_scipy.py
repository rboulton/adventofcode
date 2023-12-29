import math
import scipy
import numpy

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
    
    def dist_square(self, other):
        d = self + other * -1
        return d.x * d.x + d.y * d.y + d.z * d.z

def parse_row(row):
    p, v = row.split(' @ ')
    p = Vector(*[int(a) for a in p.split(', ')])
    v = Vector(*[int(a) * 10**14 for a in v.split(', ')])
    return p, v

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
    
    # 6 + N unknowns, N equations
    # N == 1  => 7 unknowns, 3 equations
    # N == 2  => 8 unknowns, 6 equations
    # N == 3  => 9 unknowns, 9 equations
    # So should be able to solve with 3 equations, then verify
    
    # si.p - r.p     == ti * (r.v - si.v)
    #
    # s1.p - r.p     == t1 * (r.v - s1.v)
    # s2.p - r.p     == t2 * (r.v - s2.v)
    # s3.p - r.p     == t3 * (r.v - s3.v)
    # s4.p - r.p     == t4 * (r.v - s4.v)
    
    # r.p            == s4.p - t4 * (r.v - s4.v)
    # s3.p - r.p     == t3 * (r.v - s3.v)
    # s3.p - s4.p    == t3 * (r.v - s3.v) + t4 (r.v - s4.v)
    # s3.p - s4.p    == (t3 + t4) * r.v - t3 * s3.v - t4 * s4.v
    # s3.p - s4.p    == (t3 + t4) * r.v - (t3 + t4) * s3.v + t4 * s3.v - t4 * s4.v
    # s3.p - s4.p    == (t3 + t4) * r.v - (t3 + t4) * s3.v + t4 * (s3.v - s4.v)
    # (s3.p - s4.p)    == (t3 + t4) * r.v - (t3 + t4) * s3.v + t4 * (s3.v - s4.v)
    
    # For each component, eg, x
    # I is identity vector, length N
    # T is vector of intersection times
    # Sp is vector of stone positions
    # Sv is vector of stone velocities
    # * is integer-vector multiplication
    # . is dot-product
    # 
    # r.px * I + r.vx * T == Spx + Svx . T
    # r.vx * T  - Svx . T == Spx - r.px * I
    
    print(stones[:3])
    
    
for i in range(len(stones)):
    print(stones[i])
calc_intersect(stones)


s_to_use = len(stones)
s_to_use = 5
f0 = numpy.ndarray(shape=(6 + s_to_use,))
f0[:6] = [
    stones[0][0].x, stones[0][0].y, stones[0][0].z,
    stones[0][1].x, stones[0][1].y, stones[0][1].z,
]
print("F",f0)
res = scipy.optimize.minimize(calc_dist, f0)
print(res)
print(res.x)
rock_p = Vector(*(int(v + 0.5) for v in res.x[:3]))
rock_v = Vector(*(int(v + 0.5) for v in res.x[3:6]))
times = [v for v in res.x[6:]]
for t in times:
    assert t > 0

print(rock_p, rock_v, times)
print(rock_p.x + rock_p.y + rock_p.z)