

input = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''

input = open("input1.txt", "r").read()

rows = input.strip().split("\n")

c = 0
v = 50
for row in rows:
    inc = {'L': -1, 'R': +1}[row[0]] * int(row[1:])
    v = (v + inc) % 100
    print(v)
    if v == 0: c += 1

print(v, c)
