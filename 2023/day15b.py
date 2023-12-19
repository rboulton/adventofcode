input = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''
input = open('2023/input15.txt', 'r').read()

def hash(input):
    v = 0
    for ch in input:
        v = ((v + ord(ch)) * 17) % 256
    return v

boxes = {}
for s in input.strip().replace('\n', '').split(','):
    if '=' in s:
        label, f = s.split('=')
        f = int(f)
    else:
        assert s.endswith('-')
        label = s[:-1]
        f = None
    boxnum = hash(label)
    box = boxes.setdefault(boxnum, [])
    if f is None:
        for i, l in enumerate(box):
            if l[0] == label:
                del box[i]
                break
    else:
        for i, l in enumerate(box):
            if l[0] == label:
                box[i] = (label, f)
                break
        else:
            box.append((label, f))
    print(label, boxnum, f, box)

power = 0
for i in range(256):
    box = boxes.get(i)
    if box is None: continue
    for j, (label, f) in enumerate(box, 1):
        power += (i+1) * j * f
print(power)