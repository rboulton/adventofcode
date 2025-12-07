

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
    d = {'L': -1, 'R': +1}[row[0]]
    inc = int(row[1:]) % 100
    c += int(row[1:]) // 100
    oldv = v
    v = v + d * inc
    if v == 0:
        c += 1
    elif oldv != 0 and v % 100 != v:
        c += 1
    v = v % 100
    print(row, v, c)

print(v, c)
