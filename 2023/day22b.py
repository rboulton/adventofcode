input = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''

input = open('2023/input22.txt', 'r').read()

class Pos:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __repr__(self):
        return '<{},{},{}>'.format(self.x, self.y, self.z)
        
class Brick:
    def __init__(self, row, num):
        self.num = num
        a, b = row.strip().split('~')
        a = Pos(*[int(v) for v in a.split(',')])
        b = Pos(*[int(v) for v in b.split(',')])
        self.a = Pos(min(a.x, b.x), min(a.y, b.y), min(a.z, b.z))
        self.b = Pos(max(a.x, b.x), max(a.y, b.y), max(a.z, b.z))
        self.supports = set()
        self.supported_by = set()
        
    def fall_to(self, new_z):
        dz = new_z - self.a.z 
        assert dz <= 0
        self.a.z += dz
        self.b.z += dz
        
    def add_support(self, brick_num):
        self.supports.add(brick_num)
        
    def add_supported_by(self, brick_num):
        self.supported_by.add(brick_num)
        
    def __repr__(self):
        return 'B({}, {})'.format(self.a, self.b)
    
class Layer:
    def __init__(self, xrange, yrange, default=None):
        assert xrange[0] == 0
        assert yrange[0] == 0
        self.xmax = xrange[1]
        self.ymax = yrange[1]
        self.items = [
            [default] * (self.ymax + 1)
            for _ in range(self.xmax + 1)
        ]
        
    def brick_supports(self, brick):
        '''Return a list of bricks that a brick would be supported by'''
        result = set()
        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                i = self.items[x][y]
                if i is not None:
                    result.add(i)
        return list(result)

    def add_brick(self, brick, brick_num):
        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                self.items[x][y] = brick_num

class Grid:
    def __init__(self, bricks):
        self.bricks = list(bricks)
        self.bricks.sort(key = lambda b: (b.a.z, b.a.x, b.a.y))
        self.x_range = self._x_range()
        self.y_range = self._y_range()
        self.layers = [Layer(self.x_range, self.y_range, default='-')]
        
    def _x_range(self):
        return (
            min(min(brick.a.x, brick.b.x) for brick in self.bricks),
            max(max(brick.a.x, brick.b.x) for brick in self.bricks),
        )
        
    def _y_range(self):
        return (
            min(min(brick.a.y, brick.b.y) for brick in self.bricks),
            max(max(brick.a.y, brick.b.y) for brick in self.bricks),
        )
        
    def layer(self, z):
        # print("Getting layer {}".format(z))
        return self.layers[z]
        
    def ensure_layer(self, z):
        while z >= len(self.layers):
            # print("Adding empty layer {}".format(len(self.layers)))
            self.layers.append(Layer(self.x_range, self.y_range))
        
    def settle(self):
        for brick_num, brick in enumerate(self.bricks):
            # print("Brick {} {}".format(brick, len(self.layers)))
            z = brick.a.z
            if z >= len(self.layers):
                # print("z={} >= layers={}  so setting z = {}".format(z, len(self.layers), len(self.layers)))
                z = len(self.layers)
            while True:
                layer = self.layer(z - 1)
                supports =  layer.brick_supports(brick)
                if supports:
                    break
                z -= 1
            for support in supports:
                if support == '-':
                    break
                supporting_brick = self.bricks[support]
                # print("Brick {} supports brick {}".format(support, brick_num))
                supporting_brick.add_support(brick_num)
                brick.add_supported_by(support)
            brick.fall_to(z)
            while z <= brick.b.z:
                self.ensure_layer(z)
                layer = self.layer(z)
                layer.add_brick(brick, brick_num)
                z += 1
                
        # for brick_num, brick in enumerate(self.bricks):
            # print("{} supports={} supported_by={}".format(brick_num, brick.supports, brick.supported_by))
            
    def fall_if_delete(self, brick_num):
        brick = self.bricks[brick_num]
        # print("{} supports={} supported_by={}".format(brick_num, brick.supports, brick.supported_by))
        would_move = set()
        stack = []
        stack.extend(brick.supports)
        would_move.add(brick_num)
        
        while len(stack) > 0:
            brick_num = stack.pop(0)
            brick = self.bricks[brick_num]
            if len(brick.supported_by.difference(would_move)) == 0:
                if brick_num not in would_move:
                    would_move.add(brick_num)
                    stack.extend(brick.supports)
                    # print("brick {} {}: supported_by={}, would_move={}".format(brick.num, brick, brick.supported_by, would_move))
        # print("result: {}".format(len(would_move) - 1))
        return len(would_move) - 1
        
bricks = []    
for num, row in enumerate(input.strip().split('\n')):
    bricks.append(Brick(row, num))
g = Grid(bricks)
print(g.x_range, g.y_range)   
g.settle()

total = 0
for brick_num in range(len(g.bricks)):
    total += g.fall_if_delete(brick_num)
print(total)