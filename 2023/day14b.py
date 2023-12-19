from numpy import kaiser


input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

input = open('2023/input14.txt', 'r').read()

class Grid:
    def __init__(self, input):
        self._init(input)
        
    def _init(self, input):
        self.rows = [
            [ch for ch in row]
            for row in input.strip().split('\n')
        ]
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        
    def at(self, r, c):
        return self.rows[r][c]
    
    def set(self, r, c, ch):
        self.rows[r][c] = ch
        
    def __repr__(self):
        return '\n'.join(''.join(r) for r in self.rows)
    
    def load(self):
        total = 0
        for r, row in enumerate(self.rows):
            weight = self.h - r
            for ch in row:
                if ch == 'O':
                    total += weight
        return total
    
    def roll_north(self):
        stop = [0] * len(self.rows[0])
        for r, row in enumerate(self.rows):
            for c, ch in enumerate(row):
                if ch == '#':
                    stop[c] = r + 1
                elif ch == 'O':
                    t = stop[c]
                    if t != r:
                        # print("Rolling in col {} from {} to {}".format(c, r, t))
                        assert self.at(t, c) == '.', self.at(t,c)
                        self.set(t, c, 'O')
                        self.set(r, c, '.')
                    stop[c] = t + 1

    def roll_south(self):
        stop = [self.h-1] * len(self.rows[0])
        for r in range(self.h-1, -1, -1):
            row = self.rows[r]
            for c, ch in enumerate(row):
                if ch == '#':
                    stop[c] = r - 1
                elif ch == 'O':
                    t = stop[c]
                    if t != r:
                        # print("Rolling in col {} from {} to {}".format(c, r, t))
                        assert self.at(t, c) == '.', self.at(t,c)
                        self.set(t, c, 'O')
                        self.set(r, c, '.')
                    stop[c] = t - 1

    def roll_west(self):
        for r, row in enumerate(self.rows):
            stop = 0
            for c, ch in enumerate(row):
                if ch == '#':
                    stop = c + 1
                elif ch == 'O':
                    if stop != c:
                        # print("Rolling in row {} from {} to {}".format(r, c, stop))
                        assert row[stop] == '.', row[stop]
                        row[stop] = 'O'
                        row[c] = '.'
                    stop = stop + 1
                    
    def roll_east(self):
        for r, row in enumerate(self.rows):
            stop = self.w - 1
            for c in range(self.w - 1, -1, -1):
                ch = row[c]
                if ch == '#':
                    stop = c - 1
                elif ch == 'O':
                    if stop != c:
                        # print("Rolling in row {} from {} to {}".format(r, c, stop))
                        assert row[stop] == '.', row[stop]
                        row[stop] = 'O'
                        row[c] = '.'
                    stop = stop - 1
                    
                    
    def spin_cycle(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()
            
    def state_hash(self):
        return repr(self)
            
    def spin_until_settled(self):
        prev_states = {self.state_hash(): 0}
        loads = [self.load()]
        spins = 1_000_000_000
        for c in range(1, spins + 1):
            self.spin_cycle()
            l = self.load()
            h = self.state_hash()
            print(c, l)
            #print(repr(self))
            #print()
            if h in prev_states:
                break
            prev_states[h] = c
            loads.append(l)
        prev = prev_states[h]
        cycle_time = c - prev
        print("State after {} spincycles previously seen at {}".format(c, prev))
        print("Cycle time {}".format(cycle_time))
        remaining = (spins - c) % cycle_time
        l = loads[prev + remaining]
        print("Load after {} will be {}".format(spins, l))


g = Grid(input)
print(g)
g.spin_until_settled()