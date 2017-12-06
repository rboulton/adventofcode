import sys

a = sys.argv[1]
b = a + a[0]
total = 0
half_len = len(a) / 2
for i in range(len(b) - 1):
    if b[i] == b[(i + half_len)%len(a)]: total += int(b[i])
print(total)
