from functools import total_ordering

@total_ordering
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Coord({self.x}, {self.y})'

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __eq__(self, other):
        return ((self.y, self.x) == (other.y, other.x))
    
    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return ((self.y, self.x) < (other.y, other.x))

    def rotate_right(self):
        return Coord(-self.y, self.x)


class Grid:
    def __init__(self, rows=None, convert=None, width=None, height=None):
        if convert is None:
            convert = lambda x: x
        if rows is None:
            rows = [[None] * width] * height
        self.rows = [
            [convert(ch) for ch in row]
            for row in rows
        ]

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def clear(self, v):
        '''Set all cells to either v if v is an int, string or None, or v()'''
        if isinstance(v, int) or isinstance(v, str) or v is None:
            v2 = v
            v = lambda: v2
        rows = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(v())
            rows.append(row)
        self.rows = rows

    def get(self, x_or_coord, y=None):
        '''Get a value from the grid.

        Returns None if out of bounds.
        '''
        if isinstance(x_or_coord, Coord):
            assert y is None
            x, y = x_or_coord.x, x_or_coord.y
        else:
            x, y = x_or_coord, y

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return self.rows[y][x]

    def set(self, x_or_coord, y_or_v, v=None):
        '''Set a value from the grid.

        Returns True if the value was in the grid, False if out of bounds.
        '''

        if isinstance(x_or_coord, Coord):
            assert v is None
            x, y, v = x_or_coord.x, x_or_coord.y, y_or_v
        else:
            x, y, v = x_or_coord, y_or_v, v

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        self.rows[y][x] = v
        return True

    def unique_contents(self):
        return set(v for row in self.rows for v in row)

    def coords(self, filter=None):
        """Get all coordinates, optionally matching a filter """
        if filter is None:
            filter = lambda _: True
        for y in range(self.height):
            for x in range(self.width):
                if filter(self.get(x, y)):
                    yield Coord(x, y)

    def findall(self, v):
        """Find all coordinates containing v"""
        for c in self.coords(lambda val: val == v):
            yield c

    def find(self, v):
        """Find the first coordinate containing v"""
        for c in self.coords(lambda val: val == v):
            return c

    def cartesian_neighbours(self, x_or_coord, y=None, include_out_of_bounds=False):
        if isinstance(x_or_coord, Coord):
            assert y is None
            x, y = x_or_coord.x, x_or_coord.y
        else:
            x, y = x_or_coord, y
        if include_out_of_bounds:
            bounds_check = lambda a, b: True
        else:
            bounds_check = lambda a, b: a >= 0 and b >= 0 and a < self.width and b < self.height
        return [
            Coord(a, b)
            for (a, b) in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))
            if bounds_check(a, b)
        ]

    def connected_same(self, x_or_coord, y=None):
        if isinstance(x_or_coord, Coord):
            assert y is None
            start = x_or_coord
        else:
            start = Coord(x_or_coord, y)
        result = set((start,))
        start_val = self.get(start)
        stack = [start]
        while len(stack) > 0:
            pos = stack.pop()
            for n in self.cartesian_neighbours(pos):
                if self.get(n) != start_val:
                    continue
                if n not in result:
                    stack.append(n)
                result.add(n)
        return result

    def __str__(self):
        return '\n'.join(''.join(str(ch) for ch in row) for row in self.rows)

    def rotate_right(self):
        rows = []
        for x in range(self.width):
            row = [self.get(x, y) for y in reversed(range(self.height))]
            rows.append(row)
        return Grid(rows)
