import sys

def calc_hash(s):
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

    data = list(range(256))
    lens = read_lengths(s)
    apply(data, lens)
    h = tohex(condense(data))
    b = '0'*128 + (bin(eval("0x%s" % h))[2:])
    r = list(b[-128:])
    assert(len(r) == 128)
    return r

def calc_grid(key):
    return [
        calc_hash("%s-%d" % (key, i))
        for i in range(128)
    ]

def count_regions(grid):
    def find_region():
        for y in range(len(grid)):
            try:
                x = grid[y].index('1')
                return x, y
            except ValueError:
                continue
        return None, None

    def clear_region(x, y):
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            return 0
        if grid[y][x] == '0':
            return 0
        grid[y][x] = '0'
        return 1 + clear_region(x - 1, y) + clear_region(x + 1, y) + clear_region(x, y + 1) + clear_region(x, y - 1)

    count = 0
    while True:
        x, y = find_region()
        if x is None:
            return count
        assert grid[y][x] == '1', [grid[y][x], x, y]
        count += 1
        print("Region %d, %d squares" % (count, clear_region(x, y)))
    return count

grid = calc_grid(sys.argv[1])
print(count_regions(grid))
