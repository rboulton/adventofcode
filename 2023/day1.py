import re

input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

_input=open("2023/input1.txt", "r").read()

vals = []

for line in input.strip().split("\n"):
    first = None
    last = None
    for ch in line:
        if ch in "0123456789":
            if first is None:
                first = ch
            last = ch
    val = int(first+last)
    vals.append(val)
    
print(sum(vals))

