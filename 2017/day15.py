import sys

def gen1(val):
    while True:
        val = (val * 16807) % 2147483647
        yield val

def gen2(val):
    while True:
        val = (val * 48271) % 2147483647
        yield val

def match(v1, v2):
    return (v1 ^ v2) & 0xffff == 0

def judge(key1, key2):
    count = 0
    r = 40000000
    for (n, v1, v2) in zip(xrange(r), gen1(key1), gen2(key2)):
        if match(v1, v2):
            count += 1
    return count

print(judge(int(sys.argv[1]), int(sys.argv[2])))

