def read_lengths(data):
    return [ord(ch) for ch in data.strip()] + [17, 31, 73, 47, 23]

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
    for round in range(64):
        for l in lens:
            reverse(data, pos, l)
            pos = (pos + l + skip) % len(data)
            skip = (skip + 1) % len(data)

def condense(data):
    return [
        reduce(lambda a, b: a ^ b, data[pos:pos + 16], 0)
        for pos in range(0, 256, 16)
    ]

def tohex(condensed):
    return ''.join(
        '%02x' % num
        for num in condensed
    )

def calc_hash(s):
    """Calculate a knot hash for a string"""
    data = list(range(256))
    lens = read_lengths(s)
    apply(data, lens)
    return tohex(condense(data))

def calc_hash_binary(s):
    h = calc_hash(s)
    b = '0'*128 + (bin(eval("0x%s" % h))[2:])
    return b[-128:]
