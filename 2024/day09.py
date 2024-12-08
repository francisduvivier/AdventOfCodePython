import time

from util import map_to_numbers

tInput = open('day09-testinput.txt').read().strip()
rInput = open('day09-input.txt').read().strip()

def parseInput(input):
    lines = input.splitlines()
    lineToNumbers = lambda line: map_to_numbers(line.split(' '))
    numbersMatrix = list(map(lineToNumbers, lines))
    return numbersMatrix


def part1(input):
    parsed = parseInput(input)
    result = sum(parsed[0])
    print(result)
    return result

assert part1(tInput) == 20
part1(rInput)
