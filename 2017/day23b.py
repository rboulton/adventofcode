
def run():
    h = 0
    b = 81
    c = b
    b = b * 100
    b = b + 100000
    c = b + 17000

    while True:  # E
        f = 1
        d = 2
        e = 2

        print (b,c,d,e,f,h)

        while True:  # B
            if b % d == 0:
                f = 0
            d = d + 1
            if d != b:
                continue
            if f == 0:
                h = h + 1
            if b == c:
                return(h)
            b = b + 17
            break

print(run())
