from tkinter import EW, W


input = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

input = open("2023/input5.txt", "r").read()

class Range:
    def __init__(self, start, end):
        assert end >= start
        self.start = start
        self.end = end
        
    def __repr__(self):
        return "[{}: {}]".format(self.start, self.end)
    
    def __lt__(self, other):
        return self.start < other.start
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
    
    def __add__(self, offset):
        return Range(self.start + offset, self.end + offset)
    
    def intersect(self, other):
        a, b = self, other
        if a > b:
            a, b = b, a
        if a.end <= b.start:
            return None
        istart = max(a.start, b.start)
        iend = min(a.end, b.end)
        return Range(istart, iend)
    
    def subtract(self, other):
        # print(self, " - ", other)
        if other is None:
            return [self]
        result = []
        if self.start < other.start:
            if self.end <= other.start:
                return [self]
            result.append(Range(self.start, other.start))
        if self.end <= other.end:
            return result
        assert other.start <= self.end
        if other.end >= self.end:
            return result
        return result + [Range(other.end, self.end)]
        
    def size(self):
        return self.end - self.start


class RangeList:
    def __init__(self, ranges):
        self.ranges = list(sorted(ranges))
        
    def __repr__(self):
        return "RangeList<{}, size={}>".format(self.ranges, self.size())
        
    def apply(self, range, offset):
        mapped, non_mapped = [], []
        for r in self.ranges:
            intersect = r.intersect(range)
            assert intersect == range.intersect(r), (intersect, range.intersect(r))
            non_intersect = r.subtract(intersect)
            if intersect is not None:
                mapped.append(intersect + offset)
                # print(r, intersect + offset, non_intersect)
            # else:
                # print(r, non_intersect)
            non_mapped.extend(non_intersect)
        return mapped, non_mapped
    
    def size(self):
        return sum(r.size() for r in self.ranges)
            

        
class Map:
    def __init__(self, line):
        assert line.endswith(" map:")
        self.source, self.dest = line.split()[0].split('-to-')
        self.ranges = []
        
    def add_line(self, line):
        dest, source, length = [int(v) for v in line.strip().split()]
        new_range = Range(source, source + length)
        for r, offset in self.ranges:
            assert r.intersect(new_range) is None
        self.ranges.append((new_range, dest - source))
        
    def __repr__(self):
        return "{} -> {}: {}".format(self.source, self.dest, self.ranges)

    def map(self, ranges):
        init_size = ranges.size()
        out = []
        for range, offset in sorted(self.ranges):
            # print("Applying {} {} to {}".format(range, offset, ranges))
            mapped, non_mapped = ranges.apply(range, offset)
            out.extend(mapped)
            ranges = RangeList(non_mapped)
            # print("Mapped {}, left {}".format(mapped, ranges))
        result = RangeList(out + ranges.ranges)
        assert result.size() == init_size, (result.size(), init_size)
        return result

            
lines = input.strip().split('\n')
seeds = [int(s) for s in lines[0][7:].strip().split()]
seed_ranges = RangeList(
    Range(seeds[i], seeds[i] + seeds[i+1])
    for i in range(0, len(seeds), 2)
)

maps = []
m = None
for line in lines[2:]:
    if line.strip() == "":
        m = None
        continue
    if m is None:
        m = Map(line)
        maps.append(m)
        continue
    m.add_line(line)
    
locations = []
print(seed_ranges)
for m in maps:
    print()
    print(m)
    seed_ranges = m.map(seed_ranges)
    print(seed_ranges)
    
print(seed_ranges.ranges[0].start)