def getTestInput():
    return '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''


tInput = getTestInput().splitlines()
rInput = open('day11-input.txt').read().strip().splitlines()


def getAdjacentSeats(grid, row, col):
    adjacents = []
    for rowDiff in [0, 1, -1]:
        for colDiff in [0, 1, -1]:
            adjRow = row - rowDiff
            adjCol = col - colDiff
            if adjRow >= 0 and adjCol >= 0 and len(grid) > adjRow and len(grid[adjRow]) > adjCol and not (
                    rowDiff == 0 and colDiff == 0):
                adjacents.append(grid[adjRow][adjCol])
    return adjacents


def applyRules(grid: [str]):
    newGrid = list(map(lambda l: [char for char in l], grid))
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if grid[row][col] == 'L' and occs('#', ''.join(getAdjacentSeats(grid, row, col))) == 0:
                newGrid[row][col] = '#'
            #    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif grid[row][col] == '#' and occs('#', ''.join(getAdjacentSeats(grid, row, col))) >= 4:
                newGrid[row][col] = 'L'
            # Otherwise, the seat's state does not change.

    return list(map(lambda l: ''.join(l), newGrid))


import re


def occs(part: str, whole: str):
    return len(re.findall(part, whole))


assert occs('#', '#.L\n#..#') == 3


def part1(input):
    print(input)
    prevGrid = input
    newGrid = applyRules(prevGrid)
    while ''.join(newGrid) != ''.join(prevGrid):
        prevGrid = newGrid
        newGrid = applyRules(prevGrid)
    return occs('#', ''.join(newGrid))
    pass


if __name__ == '__main__':
    # p1 = part1(tInput)
    p1 = part1(rInput)
    print(['part1', p1])
