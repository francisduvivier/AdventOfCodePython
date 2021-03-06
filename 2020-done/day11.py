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
            if rowDiff == 0 and colDiff == 0: continue
            adjRow = row - rowDiff
            adjCol = col - colDiff
            if 0 <= adjRow < len(grid) and 0 <= adjCol < len(grid[adjRow]):
                adjacents.append(grid[adjRow][adjCol])
    return adjacents


def applyRules(grid: [str], getConsiderables, maxOccupied=4):
    newGrid = list(map(lambda l: [char for char in l], grid))
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if grid[row][col] == 'L' and occs('#', ''.join(getConsiderables(grid, row, col))) == 0:
                newGrid[row][col] = '#'
            #    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif grid[row][col] == '#' and occs('#', ''.join(getConsiderables(grid, row, col))) >= maxOccupied:
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
    newGrid = applyRules(prevGrid, getAdjacentSeats)
    while ''.join(newGrid) != ''.join(prevGrid):
        prevGrid = newGrid
        newGrid = applyRules(prevGrid, getAdjacentSeats)
    return occs('#', ''.join(newGrid))
    pass


def getVisibleSeats(grid, row, col):
    visibles = []
    for rowDiff in [0, 1, -1]:
        for colDiff in [0, 1, -1]:
            if rowDiff == 0 and colDiff == 0: continue
            adjRow = row - rowDiff
            adjCol = col - colDiff
            while 0 <= adjRow < len(grid) and 0 <= adjCol < len(grid[adjRow]) and grid[adjRow][adjCol] == '.':
                adjRow = adjRow - rowDiff
                adjCol = adjCol - colDiff
            if 0 <= adjRow < len(grid) and 0 <= adjCol < len(grid[adjRow]):
                visibles.append(grid[adjRow][adjCol])
    return visibles


testGrid = ['.##.##.',
            '#.#.#.#',
            '##...##',
            '...L...',
            '##...##',
            '#.#.#.#',
            '.##.##.']
assert len(getVisibleSeats(
    testGrid,
    3, 3)) == 0
assert len(getVisibleSeats(
    testGrid,
    0, 0)) == 3
assert len(getVisibleSeats(
    testGrid,
    1, 1)) == 7


def part2(input):
    print(input)
    prevGrid = input
    newGrid = applyRules(prevGrid, getVisibleSeats, 5)
    while ''.join(newGrid) != ''.join(prevGrid):
        prevGrid = newGrid
        newGrid = applyRules(prevGrid, getVisibleSeats, 5)
    return occs('#', ''.join(newGrid))
    pass


if __name__ == '__main__':
    # print(['part1', (part1(tInput))])
    print(['part1', (part1(rInput))])
    # print(['part2', (part2(tInput))])
    print(['part2', (part2(rInput))])
