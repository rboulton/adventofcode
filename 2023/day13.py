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


def hsympos(rows):
    l = len(rows)
    for i in range(1, l):
        for j in range(min(i, l-i)):
            # print(i, j)
            if rows[i + j] != rows[i - 1 - j]:
                break
        else:
            return i
    return None

def vsympos(rows):
    cols = []
    for i in range(len(rows[0])):
        cols.append(''.join(ch for row in rows for ch in row[i]))
    return hsympos(cols)


total = 0
for pattern in input.strip().split('\n\n'):
    rows = pattern.split('\n')
    hsym = hsympos(rows)
    vsym = vsympos(rows)
    print(hsym, vsym)
    if vsym is not None:
        total += vsym
    if hsym is not None:
        total += hsym * 100
        
print(total)