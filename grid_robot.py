import numpy as np

DIR = {
    '^': {'dx': 0, 'dy': -1},
    '>': {'dx': 1, 'dy': 0},
    'v': {'dx': 0, 'dy': 1},
    '<': {'dx': -1, 'dy': 0},
}
SKEWED_DIR = {
    'R': {'dx': 1, 'dy': -1},
    'r': {'dx': 1, 'dy': 1},
    'L': {'dx': -1, 'dy': -1},
    'l': {'dx': -1, 'dy': 1},
}
DIRS = [DIR[key] for key in DIR.keys()]
SKEWED_DIRS = [SKEWED_DIR[key] for key in SKEWED_DIR.keys()]
DIR_LETTERS = [key for key in DIR.keys()]


class GridRobot:
    def __init__(self, row, col, dyx: {'dy': int, 'dx': int} = DIR['^'], grid: np.array or None = None,
                 cost_calc_fn=None, turn_cost_fn=None, wrap=False, cost=0, path = None, path_tiles = None):
        self.x = col
        self.y = row
        self.set_dir(dyx)
        self.grid = grid
        self.cost = cost
        self.cost_calc_fn = cost_calc_fn
        self.turn_cost_fn = turn_cost_fn
        self.wrap = wrap
        self.path = [] if path is None else path
        self.path_tiles = [self.yx_key()] if path_tiles is None else path_tiles
    def clone(self, dyx=None, grid=None):
        if dyx is None:
            dyx = self.dyx
        if grid is None:
            grid = self.grid
        cloned = GridRobot(self.y, self.x, dyx, grid, self.cost_calc_fn, turn_cost_fn=self.turn_cost_fn, wrap=self.wrap,
                           cost=self.cost, path= self.path.copy(), path_tiles = self.path_tiles.copy())
        return cloned

    def set_dir(self, dyx):
        self.dyx = dyx
        if self.dyx in DIRS:
            self.dir_index = DIRS.index(self.dyx)
            self.dir_str = DIR_LETTERS[self.dir_index]
        else:
            self.dir_index = None
            self.dir_str = str(self.dyx['dy']) + 'dy,' + str(self.dyx['dx']) + 'dx'

    def move_forward(self, amount=1):
        self.x += self.dyx['dx'] * amount
        if self.wrap:
            self.x = self.x % len(self.grid[self.y])
        self.y += self.dyx['dy'] * amount
        if self.wrap:
            self.y = self.y % len(self.grid)
        if self.cost_calc_fn is not None:
            self.cost += self.cost_calc_fn(amount)
            self.path.append(str(self))
            self.path_tiles.append(self.yx_key())

    def get_move_cost(self, amount):
        return self.cost_calc_fn(amount)

    def move_backward(self):
        return self.move_forward(-1)

    def turn_right(self, amount=1):
        self.set_dir(DIRS[(self.dir_index + amount) % len(DIRS)])
        if self.turn_cost_fn is not None:
            self.cost += self.turn_cost_fn(amount)
            self.path.append(str(self))

    def turn_left(self):
        return self.turn_right(3)

    def __str__(self):
        return self.state_key()

    def state_key(self):
        return f'{self.yx_key()}:{self.dir_str}'

    def yx_key(self):
        return yx_key(self.y, self.x)

    def out_of_bounds(self):
        return self.y < 0 or self.y >= len(self.grid) or self.x < 0 or self.x >= len(self.grid[self.y])

    def tile_value(self):
        return self.grid[self.y][self.x]

    def set_tile_value(self, value):
        self.grid[self.y][self.x] = value

    def clone_forward(self, dir):
        clone = self.clone(dyx=dir)
        clone.move_forward()
        return clone


def yx_key(y, x):
    return f'{y},{x}'


def parse_state_key(state_key: str):
    split1 = state_key.split(':')
    split2 = split1[0].split(',')
    return int(split2[0]), int(split2[1]), split1[1],


def find_value(search_val, grid: np.array):
    result_tuple = np.where(grid == search_val)
    y = result_tuple[0][0]
    x = result_tuple[1][0]
    return y, x


def print_grid(tile_grid):
    print('\n'.join([''.join(line) for line in tile_grid]))
