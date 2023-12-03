import re

input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

input=open("2023/input1.txt", "r").read()

text_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def get_digit(text):
    if text[0] in "0123456789":
        return text[0]
    for k, v in text_numbers.items():
        if text.startswith(k):
            return v
    return None

vals = []

for line in input.strip().split("\n"):
    first = None
    last = None
    for pos in range(len(line)):
        text = line[pos:]
        digit = get_digit(line[pos:])
        if digit is not None:
            if first is None:
                first = digit
            last = digit
    val = int(first+last)
    print(line, val)
    vals.append(val)
    
print(sum(vals))

