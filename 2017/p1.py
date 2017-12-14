import sys

a = sys.argv[1]
b = a + a[0]
total = 0
for i in range(len(b) - 1):
    if b[i] == b[i+1]: total += int(b[i])
print(total)
