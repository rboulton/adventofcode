from tkinter import Y


input = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

input = open('2023/input13.txt', 'r').read()

def is_single_bit(num):
    return num != 0 and num & (num-1) == 0


def hsympos(rows):
    # print('checking hsym')
    return sympos(rows)

def sympos(rows):
    brows = [
        int(r.replace('.', '0').replace('#', '1'), base=2)
        for r in rows
    ]
    
    close_pairs = []
    
    for i, r in enumerate(brows):
        for j, o in enumerate(brows[i+1:], i+1):
            diff = r ^ o
            if is_single_bit(diff):
                close_pairs.append((i, j))
    # print(close_pairs)

    result = None
    l = len(rows)
    for i in range(1, l):
        diffs = 0
        for j in range(min(i, l-i)):
            r1 = i - 1 - j
            r2 = i + j
            if rows[r1] != rows[r2]:
                if diffs != 0:
                    # print("fail", diffs, i, j, r1, r2)
                    break
                if (r1, r2) in close_pairs:
                    # print("close pair", i, j, r1, r2)
                    diffs = 1
                else:
                    break
        else:
            # print("end", i)
            if diffs == 1:
                assert result is None, (result, i)
                result = i
    return result

def vsympos(rows):
    # print('checking vsym')
    cols = []
    for i in range(len(rows[0])):
        cols.append(''.join(ch for row in rows for ch in row[i]))
    return sympos(cols)


total = 0
for pattern in input.strip().split('\n\n'):
    rows = pattern.split('\n')
    hsym = hsympos(rows)
    vsym = vsympos(rows)
    print(hsym, vsym)
    if vsym is None:
        assert hsym is not None
        total += hsym * 100
    else:
        assert hsym is None
        total += vsym
        
print(total)