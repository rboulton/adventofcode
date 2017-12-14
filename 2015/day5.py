import sys
import re

def nice1(s):
    if not re.search(r'[aeiou].*[aeiou].*[aeiou]', s):
        return False
    if not re.search(r'([a-z])\1', s):
        return False
    if re.search(r'ab|cd|pq|xy', s):
        return False
    return True

def nice2(s):
    if not re.search(r'([a-z][a-z]).*\1', s):
        return False
    if not re.search(r'([a-z]).\1', s):
        return False
    return True


c1 = 0
c2 = 0
for line in open(sys.argv[1]).readlines():
    if nice1(line):
        c1 += 1
    if nice2(line):
        c2 += 1
print(c1)
print(c2)
