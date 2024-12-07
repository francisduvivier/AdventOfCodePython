import time

tInput = open('dayxx-testinput.txt').read().strip()
rInput = open('dayxx-input.txt').read().strip()
def mapToNumbers(arr):
    return list(map(int, arr))

def parseInput(input):
    lines = input.splitlines()
    lineToNumbers = lambda line: mapToNumbers(line.split(' '))
    numbersMatrix = list(map(lineToNumbers, lines))
    return numbersMatrix


def part1(input):
    parsed = parseInput(input)
    result = sum(parsed[0])
    print(result)
    return result

assert part1(tInput) == 20
part1(rInput)
