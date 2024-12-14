import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

data = '''
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''

data = open(os.path.join(os.path.dirname(__file__), "input15.txt")).read()
data = data.strip()
data = data.split('\n')

class vec:
    def __init__(self, v):
        self.v = list(v)

    def __mul__(self, other):
        if isinstance(other, vec):
            assert len(self.v) == len(other.v)
            return vec([a*b for (a, b) in zip(self.v, other.v)])
        else:
            return vec([a*other for a in self.v])

    def __add__(self, other):
        assert len(self.v) == len(other.v)
        return vec([a+b for (a, b) in zip(self.v, other.v)])

    def __len__(self):
        return len(self.v)

    def __iter__(self):
        return iter(self.v)

    def __repr__(self):
        return f'vec({self.v})'

def to_int(v):
    v = v.strip(',')
    try:
        return int(v)
    except ValueError:
        return None

ingredients = []
for row in data:
    row = list(filter(lambda x: x is not None, map(to_int, row.split())))
    ingredients.append(vec(row[:-1]))

def proportions(num_ingredients, total):
    if num_ingredients == 1:
        yield [total]
        return
    for i in range(total + 1):
        for v in proportions(num_ingredients - 1, total - i):
            yield [i] + v

def score(ingredients, props):
    total = vec([0] * len(ingredients[0]))
    for ingredient, prop in zip(ingredients, props):
        total += ingredient * prop
    r = 1
    for v in total:
        if v <= 0:
            return 0
        r *= v
    return r

m = 0
for props in proportions(len(ingredients), 100):
    props = vec(props)

    val = score(ingredients, props)
    m = max(val, m)
    print(f"proportions({props}) = {val}")
print(m)
