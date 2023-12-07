import string

tests = [
    ('cqjxjnds', 'cqjxxyzz'),
    ('cqjxxyzz', 'cqkaabcc'),
    ('aaaaz', 'aabcc'),
    ('abcdefgh', 'abcdffaa'),
    ('ghijklmn', 'ghjaabcc'),
]

def inc_letter(l):
    if l == 'z':
        return 'a', True
    return chr(ord(l) + 1), False
    
def inc(pw):
    pw = list(pw)
    for i in range(1, len(pw) + 1):
        nl, carry = inc_letter(pw[-i])
        pw[-i] = nl
        if not carry:
            break
    return ''.join(pw)

def has_triple_seq(pw):
    run = 0
    prev = '0'
    for ch in pw:
        if ord(ch) == ord(prev) + 1:
            run += 1
            if run >= 3:
                return True
        else:
            run = 1
        prev = ch
    return False

def has_two_pairs(pw):
    pairs = set()
    prev = '0'
    for ch in pw:
        if ch == prev:
            pairs.add(ch)
            if len(pairs) >= 2:
                return True
        prev = ch
    return False



def is_valid(pw):
    if not has_triple_seq(pw):
        return False
    if 'i' in pw or 'o' in pw or 'l' in pw:
        return False
    if not has_two_pairs(pw):
        return False
    return True

def next_pw(pw):
    while True:
        pw = inc(pw)
        if is_valid(pw):
            return pw

for pw, nextpw in tests:
    out = next_pw(pw)
    print(pw, out)
    assert out == nextpw