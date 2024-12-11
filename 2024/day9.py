import math, os, re, copy

data = '''
2333133121414131402
'''

data = open(os.path.join(os.path.dirname(__file__), "input9.txt")).read()
data = data.strip()

def expand(data):
    out = []
    num = 0
    for c in data:
        if num >= 0:
            out.extend([num]*int(c))
            num = -(num + 1)
        else:
            num = -num
            out.extend([None]*int(c))
    return out

def compact(disk):
    j = len(disk) - 1
    i = 0
    while True:
        while i < j and disk[i] is not None:
            i += 1
        while i < j and disk[j] is None:
            j -= 1
        if not (i < j):
            break
        disk[i], disk[j] = disk[j], disk[i]

def checksum(disk):
    r = 0
    for i, num in enumerate(disk):
        if num is None:
            break
        r += i * num
    return r

disk = expand(data)
compact(disk)
print(disk)
print(checksum(disk))

