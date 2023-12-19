input = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''
input = open('2023/input15.txt', 'r').read()

def hash(input):
    v = 0
    for ch in input:
        v = ((v + ord(ch)) * 17) % 256
    return v

total = 0
for s in input.strip().replace('\n', '').split(','):
    h = hash(s)
    print(h)
    total += h
print(total)