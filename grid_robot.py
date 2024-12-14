import numpy as np

DIR = {
    '^': {'dx': 0, 'dy': -1},
    '>': {'dx': 1, 'dy': 0},
    'v': {'dx': 0, 'dy': 1},
    '<': {'dx': -1, 'dy': 0},
}
DIRS = [DIR[key] for key in DIR.keys()]
DIR_LETTERS = [key for key in DIR.keys()]


class GridRobot:
    def __init__(self, row, col, dyx: {'dy': int, 'dx': int} = DIR['^'], grid: np.array or None = None,
                 cost_calc_fn=None, wrap=False):
        self.x = col
        self.y = row
        self.dyx = dyx
        if self.dyx in DIRS:
            self.dir_index = DIRS.index(self.dyx)
            self.dir_str = DIR_LETTERS[self.dir_index]
        else:
            self.dir_index = None
            self.dir_str = str(self.dyx['dy']) + 'dy,' + str(self.dyx['dx']) + 'dx'
        self.grid = grid
        self.cost = 0
        self.cost_calc_fn = cost_calc_fn
        self.wrap = wrap

    def move_forward(self, amount=1):
        self.x += self.dyx['dx'] * amount
        if self.wrap:
            self.x = self.x % len(self.grid[self.y])
        self.y += self.dyx['dy'] * amount
        if self.wrap:
            self.y = self.y % len(self.grid)
        if self.cost_calc_fn:
            self.cost += self.get_move_cost(amount)

    def get_move_cost(self, amount):
        return self.cost_calc_fn(self, amount)

    def move_backward(self):
        return self.move_forward(-1)

    def turn_right(self):
        self.dyx = DIRS[(self.dir_index + 1) % len(DIRS)]

    def __str__(self):
        return self.state_key()

    def state_key(self):
        return f'{self.yx_key()}:{self.dir_str}'

    def yx_key(self):
        return yx_key(self.y, self.x)

    def out_of_bounds(self):
        return self.y < 0 or self.y >= len(self.grid) or self.x < 0 or self.x >= len(self.grid[self.y])

    def clone(self):
        return GridRobot(self.y, self.x, self.dyx, self.grid)


def yx_key(y, x):
    return f'{y},{x}'


def parse_state_key(state_key: str):
    split1 = state_key.split(':')
    split2 = split1[0].split(',')
    return int(split2[0]), int(split2[1]), split1[1],
