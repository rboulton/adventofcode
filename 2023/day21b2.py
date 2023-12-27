input = '''...........
......##.#.
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
.##...#.##.
...........
'''
truth = [
    (0, 1),
    (1, 4),
(2, 7),
(3, 15),
(4, 18),
(5, 26),
(6, 36),
(7, 48),
(8, 63),
(9, 79),
(10, 90),
(11, 103),
(12, 125),
(13, 141),
(14, 173),
(15, 192),
(16, 216),
(17, 239),
(18, 269),
(19, 302),
(20, 338),
(21, 362),
(22, 387),
(23, 428),
(24, 457),
(25, 513),
(26, 548),
(27, 588),
(28, 624),
(29, 672),
(30, 723),
(31, 779),
(32, 816),
(33, 853),
(34, 913),
(35, 955),
(36, 1035),
(37, 1086),
(38, 1142),
(39, 1191),
(40, 1257),
(41, 1326),
(42, 1402),
(43, 1452),
(44, 1501),
(45, 1580),
(46, 1635),
(47, 1739),
(48, 1806),
(49, 1878),
(50, 1940),
(51, 2024),
(52, 2111),
(53, 2207),
(54, 2270),
(55, 2331),
(56, 2429),
(57, 2497),
(58, 2625),
(59, 2708),
(60, 2796),
]

input = open('2023/input21.txt', 'r').read()

input = input.strip()
assert input[len(input)//2] == 'S'
input = input.replace('S', '.') 

class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        assert self.w % 2 == 1
        assert self.h % 2 == 1
        
    def v(self):
        return '\n'.join(''.join(row) for row in self.rows)
        
    def count(self, ch):
        return sum(
            sum(1 if ch == 'O' else 0 for ch in row)
            for row in self.rows
        )
        
    def get(self, r, c):
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            return None
        return self.rows[r % self.h][c % self.w]
    
    def set(self, r, c, ch):
        self.rows[r][c] = ch
        
    def neighbours(self, r, c):
        return [v for v in (
            self.get(r - 1, c),
            self.get(r + 1, c),
            self.get(r, c - 1),
            self.get(r, c + 1),
        ) if v is not None]
        
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)
        
    def iterate(self):
        new = Grid([['#' if ch == '#' else '.' for ch in row] for row in self.rows])
        for r in range(self.h):
            for c in range(self.w):
                ch = self.get(r, c)
                if ch == '#':
                    continue
                n = self.neighbours(r, c)
                count = 0
                for ch in n:
                    if ch in 'SO':
                        count += 1
                if count == 0:
                    new.set(r, c, '.')
                else:
                    new.set(r, c, 'O')
        return new

def make_grid(input, pos):
    # Make a grid with the initial position indicated by pos
    # (x,y where -1 = left/top, 1=right/bottom)
    g = Grid([
        [ch for ch in row]
        for row in input.strip().split('\n')
    ])
    c = (g.w // 2) * (pos[0] + 1)
    r = (g.h // 2) * (pos[1] + 1)
    g.set(r, c, 'O')
    return g

def count_grid(input, pos):
    g = make_grid(input, pos)
    seen = set()
    result = []
    step = 0
    while True:
        v = g.v()
        if v in seen:
            break
        seen.add(v)
        c = g.count('O')
        result.append(c)
        # print(pos, step, c)
        step += 1
        g = g.iterate()
    # print(pos, result)
    # Time until the grid starts getting filled, and until the next grid along
    # starts getting filled Assume the initial row and column is unblocked (not
    # true of test pattern we're given, but true of real input).
    init_time = (g.w * abs(pos[0]) + 1) // 2 + (g.h * abs(pos[1]) + 1) // 2
    repeat_time = max(g.w * abs(pos[0]), g.h * abs(pos[1]))
    return result, init_time, repeat_time

class GridCounts:
    def __init__(self, input, pos):
        self.pos = pos
        self.counts, self.init_time, self.repeat_time = count_grid(input, pos)
        
    def total_active_at(self, step):
        if self.pos == (0, 0):
            return self.total_active_at_center(step)
        if 0 in self.pos:
            return self.total_active_on_line(step)
        return self.total_active_diagonal(step)
        
    def total_active_at_center(self, step):
        # Center square doesn't repeat
        assert self.init_time == 0
        return self.active_at(step)
        
    def total_active_on_line(self, step):
        assert 0 in self.pos
        
        i = step - self.init_time
        total = 0
        while i >= 0:
            total += self.active_at(i)
            i -= self.repeat_time
        return total
        
    def total_active_diagonal(self, step):
        assert 0 not in self.pos
        
        i = step - self.init_time
        total = 0
        mult = 1
        while i >= 0:
            total += self.active_at(i) * mult
            i -= self.repeat_time
            mult += 1
        return total
 
    def active_at(self, step_from_init):
        if step_from_init < len(self.counts):
            result = self.counts[step_from_init]
        else:
            p = (1 + step_from_init - len(self.counts)) % 2
            result = self.counts[-1-p]

        # print("Active at pos {}, step {} = {}".format(self.pos, step_from_init, result))
        return result

grid_counts = {}
for x in range(-1, 2):
    for y in range(-1, 2):
        grid_counts[(x, y)] = GridCounts(input, (x, y))
        
def count_pos(step, pos):
    counts = grid_counts[pos]
    r = counts.total_active_at(step)
    # print(pos, r, counts)
    return r

def count(step):
    r = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            r += count_pos(step, (x, y))
    return r
    
print(grid_counts[(0, 0)].counts)
for i in range(100):
    c = count(i)
    print(i, c)
    # assert c == truth[i][1], (truth[i], c)
print(count(6))
print(count(10))
print(count(50))
print(count(100))
print(count(500))
print(count(1000))
print(count(5000))
print(count(26501365))