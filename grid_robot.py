DIR = {
    '^': {'dx': 0, 'dy': -1},
    '>': {'dx': 1, 'dy': 0},
    'v': {'dx': 0, 'dy': 1},
    '<': {'dx': -1, 'dy': 0},
}
DIRS = [DIR[key] for key in DIR.keys()]


class GridRobot:
    def __init__(self, x, y, dyx: {'dy': int, 'dx': int} = DIR['^']):
        self.x = x
        self.y = y
        self.dyx = dyx

    def move_forward(self):
        self.x += self.dyx['dx']
        self.y += self.dyx['dy']

    def move_backward(self):
        self.x += -self.dyx['dx']
        self.y += -self.dyx['dy']

    def turn_right(self):
        self.dyx = DIRS[(DIRS.index(self.dyx) + 1) % len(DIRS)]

    def __str__(self):
        return f'dyx{self.dyx},x{self.y},y{self.x}]'

    def state_key(self):
        return f'{self.dyx},{self.yx_key()}'

    def yx_key(self):
        return f'{self.y},{self.x}]'
