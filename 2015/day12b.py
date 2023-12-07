import json

input = open('2015/input12.txt', 'r').read().strip()
tests = [
    (r'[1,2,3]', 6),
    (r'{"a":2,"b":4}', 6),
    (r'[[[3]]]', 3),
    (r'{"a":{"b":4},"c":-1}', 3),
    (r'[1,{"c":"red","b":2},3]', 4),
    (r'{"d":"red","e":[1,2,3,4],"f":5}', 0),
    (r'[1,"red",5]', 6),
]

def flatten(*iters):
    out = []
    for iter in iters:
        for item in iter:
            out.extend(item)
    return out

def check_red(val):
    for v in val.values():
        if v == 'red':
            return True
        continue

def nums(val):
    if isinstance(val, list):
        return flatten(nums(v) for v in val)
    if isinstance(val, dict):
        if check_red(val):
            return ()
        return flatten((nums(v) for v in val.keys()), (nums(v) for v in val.values()))
    if isinstance(val, str):
        return ()
    if isinstance(val, int):
        return (val,)
    print(type(val))
    
def score(input):
    doc = json.loads(input)
    n = nums(doc)
    return sum(n)

for i, e in tests:
    assert score(i) == e, (score(i), e)
print(score(input))