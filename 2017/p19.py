# Arg1: length of list
# Arg2: filename holding lengths

import sys

def read_lengths(filename):
    return [int(l) for l in open(filename).read().strip().split(',')]

def reverse(data, pos, l):
    assert l <= len(data)
    end = pos + l - 1
    while pos < end:
        data[pos % len(data)], data[end % len(data)] = data[end % len(data)], data[pos % len(data)]
        pos += 1
        end -= 1

def apply(data, lens):
    pos = 0
    skip = 0
    for l in lens:
        reverse(data, pos, l)
        pos = (pos + l + skip) % len(data)
        skip = (skip + 1) % len(data)

data = list(range(int(sys.argv[1])))
lens = read_lengths(sys.argv[2])
apply(data, lens)

print(data)
print(data[0] * data[1])
