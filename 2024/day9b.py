import math, os, re, copy

data = '''
2333133121414131402
'''

data = open(os.path.join(os.path.dirname(__file__), "input9.txt")).read()
data = data.strip()

class Chunk:
    def __init__(self, num, start, length):
        self.num = num
        self.start = start
        self.length = length

    def __repr__(self):
        return f"{self.num}: {self.start}-{self.length}"

    def checksum(self):
        r = 0
        for i in range(self.start, self.start + self.length):
            r += i * self.num
        return r

def parse(data):
    files = []
    gaps = []
    pos = 0
    num = 0
    for c in data:
        l = int(c)
        if num >= 0:
            files.append(Chunk(num, pos, l))
            num = -(num + 1)
        else:
            num = -num
            gaps.append(Chunk(None, pos, l))
        pos += l
    return files, gaps

def find_gap(gaps, min_length):
    for i, gap in enumerate(gaps):
        if gap.length >= min_length:
            return i, gap
    return None, None

def compact(files, gaps):
    for file in reversed(files):
        i, gap = find_gap(gaps, file.length)
        if i is None:
            continue
        if gap.start >= file.start:
            continue
        print(f"Moving {file} to {gap}")
        file.start = gap.start
        if gap.length == file.length:
            del gaps[i]
        else:
            gap.start += file.length
            gap.length -= file.length

def checksum(files):
    return sum(file.checksum() for file in files)

files, gaps = parse(data)
print(files, gaps)
compact(files, gaps)
print(files, gaps)
print(checksum(files))

