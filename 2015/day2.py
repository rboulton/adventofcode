import sys

def needed(a, b, c):
    a1 = a * b
    a2 = b * c
    a3 = a * c
    return (a1 + a2 + a3) * 2 + min(a1, a2, a3)

print(
    sum(needed(*map(lambda x: int(x), line.split('x')))
        for line in open(sys.argv[1]).readlines()
    )
)

def ribbon_needed(a, b, c):
    a1 = a + b
    a2 = b + c
    a3 = a + c
    return min(a1, a2, a3) * 2 + a * b * c

print(
    sum(ribbon_needed(*map(lambda x: int(x), line.split('x')))
        for line in open(sys.argv[1]).readlines()
    )
)
