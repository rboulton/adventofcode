import math, os, re

data = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

data = open(os.path.join(os.path.dirname(__file__), "input7.txt")).read()
data = data.strip().split('\n')

def check_target(target, numbers):
    if target < numbers[0]:
        return False
    if len(numbers) == 1:
        return numbers[0] == target
    if check_target(target, [numbers[0] * numbers[1]] + numbers[2:]):
        return True
    if check_target(target, [numbers[0] + numbers[1]] + numbers[2:]):
        return True
    return False

c = 0
for row in data:
    target, numbers = row.split(': ')
    target = int(target)
    numbers = list(map(int, numbers.split()))
    if check_target(target, numbers):
        c += target
        print (target, numbers)
print(c)
