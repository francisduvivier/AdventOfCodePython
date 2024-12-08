import time

from util import map_to_numbers

tInput = open('day08-testinput.txt').read().strip()
rInput = open('day08-input.txt').read().strip()

def parseInput(input):
    lines = input.splitlines()
    lineToNumbers = lambda line: map_to_numbers(line.split(' '))
    numbersMatrix = list(map(lineToNumbers, lines))
    return numbersMatrix


# condition for anitnode is that -given dx=x2-x1, dy=y2-y1: dx1/dy1 == dx2/dy2 and also dx1 == dx2 and dy1 == dy2 wit right polarity
# but can be more than 2, so for each pair ...
#  so I will need a map from char to list of locations with that char, so let's make a function that takes a charmatrix and converts it to a dict of
# char to list of [row, col] (or [y, x])
# then with this list, I can do O(N2) loop for so I get a the combination of pairs
# then for each pair I can calculate the dx and dy and then with that calculate an antinode location and check if it is out of bounds
# so that will be a function that takes a pair and updates a set of antinodes, it actually does not need to do both dirs, I can use the O(N2) loop for that since I will always get the pair double.

# Q before we start: are anitinodes unique for the freq or is that then the same antinode? No, In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency.
def part1(input):

    parsed = parseInput(input)
    result = sum(parsed[0])
    print(result)
    return result

assert part1(tInput) == 20
part1(rInput)
