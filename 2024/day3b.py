import math, os, re

data = '''
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''.split('\n')

data = list(open(os.path.join(os.path.dirname(__file__), "input3.txt")).readlines())
data = '\n'.join(data)

pattern = re.compile(r'''(mul|do|don't)\((?:(\d{1,3}),)?(\d{1,3})?\)''')
r = 0
on = 1
for match in pattern.finditer(data):
     op, v1, v2 = match.groups()
     if op == 'mul':
         if v1 is not None and v2 is not None:
             r += int(v1) * int(v2) * on
     if op == 'do': on = 1
     if op == 'don\'t': on = 0
print(r)
