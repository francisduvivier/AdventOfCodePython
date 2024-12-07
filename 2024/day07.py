import time

tInput = open('day07-testinput.txt').read().strip()
rInput = open('day07-input.txt').read().strip()
def mapToNumbers(arr):
    return list(map(int, arr))

def parseInput(input):
    lines = input.split('\n')
    lineToNumbers = lambda line: mapToNumbers(line.split(' '))
    numbersMatrix = list(map(lineToNumbers, lines))
    return numbersMatrix


def part1(input):
    parsed = parseInput(input)
    print(parsed)
    return parsed

assert part1(tInput)== 3749
part1(rInput)
