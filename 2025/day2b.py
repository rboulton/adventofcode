

input = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''

input = open("input2.txt", "r").read()

ranges = input.strip().split(",")

def valid(v):
    r = str(v)
    for l in range(1, 1 + len(r) // 2):
        if len(r) % l != 0: continue
        if r[:l] * (len(r) // l) == r:
            return False
    return True

def invalid_ids(start, end):
    for v in range(start, end + 1):
        if not valid(v):
            print(v)
            yield v

val = 0
for r in ranges:
    start, end = map(int, r.split('-'))
    inc = sum(invalid_ids(start, end))
    print("!", start, end, inc)
    val += inc
print(val)
