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

class Map:
    def __init__(self, line):
        assert line.endswith(" map:")
        self.source, self.dest = line.split()[0].split('-to-')
        self.ranges = []
        
    def add_line(self, line):
        dest, source, length = [int(v) for v in line.strip().split()]
        self.ranges.append((dest, source, length))
                               
    def __repr__(self):
        return "{} -> {}: {}".format(self.source, self.dest, self.ranges)

    def map(self, num):
        for dest, source, length in self.ranges:
            if num < source:
                continue
            if num >= source + length:
                continue
            return num + dest - source
        return num

            
lines = input.strip().split('\n')
seeds = [int(s) for s in lines[0][7:].strip().split()]
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
    
print(seeds, maps)

locations = []
for s in seeds:
    for m in maps:
        s = m.map(s)
    locations.append(s)
print(min(locations))