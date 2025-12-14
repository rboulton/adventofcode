from collections import Counter
import re

input = '''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out'''

input = open('input11.txt', 'r').read()

links = []

for row in input.strip('\n').split('\n'):
    a, b = row.split(':')
    b = b.strip(' ').split(' ')
    for c in b:
        links.append((a, c))

print(links)
routes = {}
routes['out'] = 1
while True:
    for a, b in list(links):
        if b in routes:
            routes.setdefault(a, []).append(routes[b])
            links.remove((a, b))

    if len(links) == 0:
        break
print(routes['you'])
print(len(re.sub('[^1]', '', str(routes['you']))))
