import sys

ins = open(sys.argv[1]).read().strip()

f = 0
c = 1
d = 0
for i in ins:
    if i == '(':
        f += 1
    if i == ')':
        f -= 1
    if f < 0 and d == 0:
        print("2", c)
        d = 1
    c += 1
print("1", f)
