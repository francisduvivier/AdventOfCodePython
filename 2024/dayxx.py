import time

tInput = open('dayxx-testinput.txt').read().strip()
rInput = open('dayxx-input.txt').read().strip()
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

part1(tInput)
part1(rInput)
