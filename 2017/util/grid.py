import math


class TiledGrid(object):
    """A grid, represented as an infinite array of tiles.

    Coordinate system is (x, y), increasing when moving right or up.

    """
    def __init__(self, tile_size=16, default=' '):
        self.tile_size = tile_size
        self.default = default 
        self.tiles = {}
        self.mintx = None
        self.minty = None
        self.maxtx = None
        self.maxty = None
        self.minx = None
        self.miny = None
        self.maxx = None
        self.maxy = None

    def __repr__(self):
        return "<TiledGrid(tile_size=%r, default=%r, tile_count=%r, mintx=%r, minty=%r, maxtx=%r, maxty=%r)>" % (
            self.tile_size,
            self.default,
            len(self.tiles),
            self.mintx,
            self.minty, 
            self.maxtx,
            self.maxty,
        )

    def as_rows(self, rowfn=None, itemfn=None):
        if self.mintx is None:
            return []
        if rowfn is None:
            rowfn = lambda row: row
        if itemfn is None:
            itemfn = lambda item: item
        return [
            rowfn([
                itemfn(self[x, y])
                for x in range(self.mintx * self.tile_size, (self.maxtx + 1) * self.tile_size)
            ])
            for y in range((self.maxty + 1) * self.tile_size - 1, (self.minty * self.tile_size) - 1, -1)
        ]

    def _check_tile(self, x, y):
        tx = x / self.tile_size
        ty = y / self.tile_size
        return self.tiles.get((tx, ty), None)

    def _ensure_tile(self, x, y):
        tx = x / self.tile_size
        ty = y / self.tile_size
        key = (tx, ty)
        tile = self.tiles.get(key)
        if tile is None:
            tile = [
                [self.default] * self.tile_size
                for _ in xrange(self.tile_size)
            ]
            self.tiles[key] = tile
            if self.mintx is None:
                self.mintx = tx
                self.maxtx = tx
                self.minty = ty
                self.maxty = ty
            else:
                self.mintx = min(tx, self.mintx)
                self.maxtx = max(tx, self.maxtx)
                self.minty = min(ty, self.minty)
                self.maxty = max(ty, self.maxty)
        return tile

    def __getitem__(self, key):
        if not isinstance(key, tuple) or len(key) != 2:
            raise ValueError("Expected an x and y coordinate or slice")
        xs, ys = key
        if isinstance(xs, slice) or isinstance(ys, slice):
            if not isinstance(xs, slice):
                xs = slice(xs, xs + 1)
            if not isinstance(ys, slice):
                ys = slice(ys, ys + 1)
            xstep = xs.step if xs.step else 1
            ystep = ys.step if ys.step else 1
            tile_size = TiledGrid._calc_tile_size(max((
                xs.stop - xs.start,
                ys.stop - ys.start)))
            result = TiledGrid(tile_size=tile_size, default=self.default)
            for rx, x in enumerate(xrange(xs.start, xs.stop, xstep)):
                for ry, y in enumerate(xrange(ys.start, ys.stop, ystep)):
                    val = self._get(x, y)
                    if val != self.default:
                        result[x, y] = self._get(x, y)
            return result
        return self._get(xs, ys)

    def __setitem__(self, key, val):
        if not isinstance(key, tuple) or len(key) != 2:
            raise ValueError("Expected an x and y coordinate or slice")
        xs, ys = key
        if isinstance(xs, slice) or isinstance(ys, slice):
            raise ValueError("Assigning to slices not yet supported")

        tile = self._ensure_tile(xs, ys)
        tile[ys % self.tile_size][xs % self.tile_size] = val
        if self.minx is None:
            self.minx = xs
            self.maxx = xs
            self.miny = ys
            self.maxy = ys
        else:
            self.minx = min(xs, self.minx)
            self.maxx = max(xs, self.maxx)
            self.miny = min(ys, self.miny)
            self.maxy = max(ys, self.maxy)

    def _get(self, x, y):
        tile = self._check_tile(x, y)
        if tile is None:
            return self.default
        return tile[y % self.tile_size][x % self.tile_size]

    @staticmethod
    def _calc_tile_size(length):
        return max(min(
            int(
                math.pow(2, math.floor(math.log(length) / math.log(2)))
            ), 512), 8
        )

    @staticmethod
    def from_arrays(rows, default=' '):
        l = max(len(rows), 1)
        tile_size = TiledGrid._calc_tile_size(l)
        grid = TiledGrid(tile_size, default)
        height = len(rows)
        for y_offset, row in enumerate(rows):
            for x, item in enumerate(row):
                grid[x, height - 1 - y_offset] = item
        return grid

    @staticmethod
    def from_file(filename, default=' ', rowfn=lambda row: row, itemfn=lambda item: item):
        return TiledGrid.from_arrays([
            [
                itemfn(ch)
                for ch in rowfn(line.rstrip('\n'))
            ]
            for line in open(filename, "rb").readlines()
        ], default)

    def show(self):
        return self.as_rows(
            rowfn=lambda row: ''.join(row),
            itemfn=lambda val: str(val),
        )

    def flipped(self):
        return


class GridVector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "GridVector(%r, %r)" % (self.x, self.y)

    def __add__(self, other):
        return GridVector(self.x + other.x, self.y + other.y)

    def __mul(self, factor):
        return GridVector(self.x + factor, self.y + factor)

    def rotated_90_clockwise(self):
        return GridVector(self.y, -self.x)

    def rotate_90_anti_clockwise(self):
        return GridVector(-self.y, self.x)
