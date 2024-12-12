DIR = {
    '^': {'dx': 0, 'dy': -1},
    '>': {'dx': 1, 'dy': 0},
    'v': {'dx': 0, 'dy': 1},
    '<': {'dx': -1, 'dy': 0},
}
DIRS = [DIR[key] for key in DIR.keys()]
DIR_LETTERS = [key for key in DIR.keys()]


class GridRobot:
    def __init__(self, x, y, dyx: {'dy': int, 'dx': int} = DIR['^']):
        self.x = x
        self.y = y
        self.dyx = dyx
        self.dir_index = DIRS.index(self.dyx)

    def move_forward(self):
        self.x += self.dyx['dx']
        self.y += self.dyx['dy']

    def move_backward(self):
        self.x += -self.dyx['dx']
        self.y += -self.dyx['dy']

    def turn_right(self):
        self.dyx = DIRS[(self.dir_index + 1) % len(DIRS)]

    def __str__(self):
        return self.state_key()

    def state_key(self):
        return f'{self.yx_key()}:{DIR_LETTERS[self.dir_index]}'

    def yx_key(self):
        return yx_key(self.y, self.x)


def yx_key(y, x):
    return f'{y},{x}'


def parse_state_key(state_key: str):
    split1 = state_key.split(':')
    split2 = split1[0].split(',')
    return int(split2[0]), int(split2[1]), split1[1],
