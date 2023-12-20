input = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

_input = '''111111111111
999999999991
999999999991
999999999991
999999999991'''

input = open('2023/input17.txt', 'r').read()

min_dist = 4
max_dist = 10

# directions: up right down left == 0 1 2 3
def left(dir):
    return (dir + 3) % 4
def right(dir):
    return (dir + 1) % 4
def next(dir, pos):
    r, c = pos
    if dir == 0:
        return (r - 1, c)
    if dir == 1:
        return (r, c + 1)
    if dir == 2:
        return (r + 1, c)
    if dir == 3:
        return (r, c - 1)
    assert False

class Cell:
    def __init__(self, cost):
        self.cost = int(cost)
        # Minimum cost paths to get to the cell, keyed by incoming direction and run length
        self.min_paths = {}
        
    def __repr__(self):
        return "c{} ".format(self.cost) + ' '.join("{}{}={}".format('urdl'[d], r, v) for (d, r), v in sorted(self.min_paths.items()))
    
    def get(self, dir, run):
        return self.min_paths.get((dir, run))
    
    def get_best(self, dir, run):
        r = None
        for n_dir in range(4):
            if (n_dir + 2) % 4 == dir:
                continue
            start = 0
            end = max_dist + 1
            if n_dir == dir:
                start = run
                assert run <= max_dist
                end = run + 1
            else:
                start = min_dist

            for n_run in range(start, end):
                nr = self.min_paths.get((n_dir, n_run))
                if nr is not None and (r is None or nr < r): r = nr
        return r
    
    def add(self, cost, dir, run):
        oldcost = self.min_paths.get((dir, run))
        if oldcost is not None and oldcost < cost:
            return False
        self.min_paths[(dir, run)] = cost
        return True

class Grid:
    def __init__(self, input):
        self.rows = [
            [Cell(ch) for ch in row]
            for row in input.strip().split('\n')
        ]
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        
    def __repr__(self):
        return '\n\n'.join('\n'.join(repr(cell) for cell in row) for row in self.rows)
    
    def at(self, pos):
        return self.rows[pos[0]][pos[1]]
    
    def neighbours(self, pos):
        r, c = pos
        if r > 0:
            yield (r - 1, c), 0
        if c < self.w - 1:
            yield (r, c + 1), 1
        if r < self.h - 1:
            yield (r + 1, c), 2
        if c > 0:
            yield (r, c - 1), 3

g = Grid(input)
pos = (0,0)
stack = set((pos,))
g.at(pos).add(0, 0, 0)
g.at(pos).add(0, 1, 0)
g.at(pos).add(0, 2, 0)
g.at(pos).add(0, 3, 0)
print()
count = 8
while len(stack) > 0:
    # if count == 0: break
    count -= 1
    pos = stack.pop()
    cell = g.at(pos)
    for newpos, newdir in g.neighbours(pos):
        newcell = g.at(newpos)
        for runlen in range(max_dist):

            mincosts = []
            for n_dir in range(4):
                if (n_dir + 2) % 4 == newdir:
                    continue
                if n_dir == newdir:
                    # print(pos, newpos, n_dir, runlen)
                    cost = cell.min_paths.get((n_dir, runlen))
                    if cost is not None:
                        mincosts.append(cost)
                else:
                    if runlen == 0:
                        for n_run in range(min_dist, max_dist + 1):
                            cost = cell.min_paths.get((n_dir, n_run))
                            if cost is not None:
                                mincosts.append(cost)
            if len(mincosts) == 0:
                continue
            mincost = min(mincosts)
                
            # print(pos, newpos, runlen, mincost)
            
            newcellmincost = newcell.get(newdir, runlen + 1)
            mincost += newcell.cost
            # print("{} dir={} runlen={} mincost={} {}".format(newpos, newdir, runlen, mincost, newcellmincost))
            if newcellmincost is None or newcellmincost > mincost:
                if newcell.add(mincost, newdir, runlen + 1):
                    stack.add(newpos)
                
    # print(g.at(pos))
print()
print(g)
print(g.at((g.h-1, g.w-1)))
c = g.at((g.h-1, g.w-1))

result = []
for (dir, run), cost in c.min_paths.items():
    if run >= min_dist:
        print(dir, run, cost)
        result.append(cost)
print(min(result))