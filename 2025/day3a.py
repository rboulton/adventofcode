

input = '''987654321111111
811111111111119
234234234234278
818181911112111'''

input = open("input3.txt", "r").read()

banks = input.strip().split("\n")

def maxjolt(bank):
    d1 = max(bank[:-1])
    d2 = max(bank[bank.index(d1)+ 1:])
    return int(d1 + d2)

r = 0
for bank in banks:
    inc = maxjolt(bank)
    r += inc
    print(r, inc)
print(r)
