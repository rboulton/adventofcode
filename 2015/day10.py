input = '1'
input = '1113122113'

def iter(input):
    out = []
    prev_ch = None
    count = 0
    for ch in input:
        if ch != prev_ch:
            if prev_ch is not None:
                out.append(str(count))
                out.append(prev_ch)
            prev_ch = ch
            count = 1
        else:
            count += 1
    out.append(str(count))
    out.append(prev_ch)
    return ''.join(out)
            
for _ in range(50):
    new = iter(input)
    print(input, '->', new)
    input = new
    
print(len(input))