input = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''

input = open("2023/input23.txt", 'r').read().strip()

OFFSETS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

class Grid:
    def __init__(self, input):
        self.rows = [
            [ch for ch in row]
            for row in input.strip().split('\n')
        ]
        self.w = len(self.rows[0])
        self.h = len(self.rows)
        self.edges = {}
        for r in range(self.h):
            for c in range(self.w):
                for d in self.dirs(r, c):
                    self.edges.setdefault((r, c), {})[(r+d[0], c+d[1])] =  1
        
    def at(self, r, c):
        try:
            return self.rows[r][c]
        except IndexError:
            return '#'
        
    def dirs(self, r, c):
        ch = self.at(r, c)
        if ch == '#':
            return ()
        elif ch == '.':
            dirs = '^>v<'
        else:
            # dirs = ch
            dirs = '^>v<'
        if r == 0:
            dirs = 'v'

        result = []
        for o_r, o_c in (OFFSETS[ch] for ch in dirs):
            ch = self.at(r + o_r, c + o_c)
            if ch == '#':
                continue
            result.append((o_r, o_c))
        return tuple(result)
    
    def reduce_edges(self):
        while True:
          modified = False
          for middle, ends in self.edges.items():
            if len(ends) == 2:
                (end1, d1), (end2, d2) = list(ends.items())
                if (
                    len(self.edges[end1]) == 2 and
                    len(self.edges[end2]) == 2 and 
                    middle in self.edges[end1].keys() and
                    middle in self.edges[end2].keys()
                ):
                    # print("Joining {} {}".format(end1, end2))
                    self.edges[end1][end2] = self.edges[end1][middle] + self.edges[middle][end2]
                    self.edges[end2][end1] = self.edges[end2][middle] + self.edges[middle][end1]
                    del self.edges[end1][middle]
                    del self.edges[end2][middle]
                    del self.edges[middle]
                    modified = True
                    break
          if not modified:
              break
                
    def longest_path(self):
        for c in range(self.w):
            ch = self.at(0, c)
            if ch != '#':
                break
        start = (0, c)
        
        for c in range(self.w):
            ch = self.at(self.h - 1, c)
            if ch != '#':
                break
        end = (self.h - 1, c)
        assert self.at(end[0], end[1]) == '.'
        
        visited = []
        return self.longest(start, end, visited)
        
    def longest(self, start, end, visited):
        if start == end:
            return 0
        
        l = len(visited)
        visited.append(start)
        
        max_tail_d = None
        for next, d in self.edges[start].items():
            # print(start, next, d, visited)
            if next in visited:
                continue
            tail_d = self.longest(next, end, visited)
            if tail_d is None:
                continue
            tail_d += d
            if max_tail_d is None or tail_d > max_tail_d:
                max_tail_d = tail_d
            
        del visited[l:]
        if max_tail_d is None:
            return None
        return max_tail_d
        
    
g = Grid(input)
g.reduce_edges()
print(g.edges)
print(g.longest_path())