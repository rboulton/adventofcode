import math, os, re

data = '''
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''.split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input3.txt")).readlines())
data = '\n'.join(data)

pattern = re.compile(r'(mul)\((\d{1,3}),(\d{1,3})\)')
r = 0
for op, v1, v2 in pattern.findall(data):
     r += int(v1) * int(v2)
print(r)
