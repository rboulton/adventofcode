import sys
from hashlib import md5

key = open(sys.argv[1]).read().strip()

def h(num):
    return md5("%s%d" % (key, num)).hexdigest()

n = 0
while True:
    if h(n).startswith("000000"):
        print(n)
        print(h(n))
        break
    n += 1
