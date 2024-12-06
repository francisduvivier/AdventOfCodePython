DIR = {
    '^': {'dx': 0, 'dy': -1},
    '>': {'dx': 1, 'dy': 0},
    'v': {'dx': 0, 'dy': 1},
    '<': {'dx': -1, 'dy': 0},
}
DIRS = [DIR[key] for key in DIR.keys()]

class GridRobot:
    def __init__(self, x, y, dxy: {'dx': int, 'dy': int}):
        self.x = x
        self.y = y
        self.dxy = dxy

    def move_forward(self):
        self.x += self.dxy['dx']
        self.y += self.dxy['dy']

    def move_backward(self):
        self.x += -self.dxy['dx']
        self.y += -self.dxy['dy']

    def turn_right(self):
        self.dxy = DIRS[(DIRS.index(self.dxy) + 1) % len(DIRS)]

    def __str__(self):
        return f'[{self.x}, {self.y}]'
