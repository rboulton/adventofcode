input = open('2015/input8.txt', 'r').read()

_input = r'''
""
"abc"
"aaa\"aaa"
"\x27"
'''

def unescape(line):
    out = []
    state = 0
    h1 = None
    for c in line:
        if state == 1: # Just had a \
            if c == '\\' or c == '"':
                out.append(c)
                state = 0
                continue
            if c == 'x':
                state = 2
                continue
            else:
                out.append('\\')
                out.append(c)
                state = 0
                
        if state == 3: # Just had \x?
            if c.isdigit() or c in 'abcdef':
                out.append(chr(int(h1+c, 16)))
                state = 0
                continue
            out.append('\\')
            out.append('x')
            out.append(h1)
            state = 0
            
        if state == 2: # Just had \x
            if c.isdigit() or c in 'abcdef':
                h1 = c
                state = 3
            else:
                out.append('\\')
                out.append('x')
                state = 0
        
        if state == 0:
            if c == '\\':
                state = 1
                continue
            out.append(c)
            continue

            
    assert state == 0
    return ''.join(out)

def escape(line):
    out = []
    for c in line:
        if c in '\\"':
            out.append('\\')
        out.append(c)
    return '"' + ''.join(out) + '"'
            
def size(line):
    assert line[0] == '"'
    assert line[-1] == '"'
    return len(unescape(line[1:-1]))

r = 0
for line in input.strip().split('\n'):
    l = len(line)
    s = size(line)
    print(l, s, repr(line), '!' + str(unescape(line[1:-1])) + '!')
    r += l - s
print(r)
print()

r = 0
for line in input.strip().split('\n'):
    l = len(line)
    s = len(escape(line))
    print(l, s, repr(line), str(escape(line)))
    r += s - l
print(r)