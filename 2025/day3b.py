

input = '''987654321111111
811111111111119
234234234234278
818181911112111'''

input = open("input3.txt", "r").read()

banks = input.strip().split("\n")

def maxjolt(bank, digits):
    assert digits != 0
    if digits == 1: return max(bank)
    d1 = max(bank[:-(digits - 1)])
    d2 = maxjolt(bank[bank.index(d1)+ 1:], digits - 1)
    print(f"maxjolt({bank}, {digits}) = {d1} + {d2}")
    return d1 + d2

r = 0
for bank in banks:
    inc = int(maxjolt(bank, 12))
    r += inc
    print(r, inc)
print(r)
