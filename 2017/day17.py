import sys

step = int(sys.argv[1])

buf = [0]
pos = 0
for num in range(2017):
   pos = (pos + step) % len(buf)
   buf.insert(pos + 1, num + 1)
   pos += 1

print(buf[pos + 1])
