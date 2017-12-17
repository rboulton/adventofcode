import sys

step = int(sys.argv[1])

pos = 0
val = 0
for num in xrange(50000000):
   pos = (pos + 1 + step) % (num + 1)
   if pos == 0:
       val = num + 1

print(val)
