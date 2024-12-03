import re
import time

tInput = open('day03-testinput.txt').read().strip()
rInput = open('day03-input.txt').read().strip()
def mapToNumbers(arr):
    return list(map(int, arr))

def parseInput(input):
    multiplications = re.findall(r'mul\((\d+),(\d+)\)', input)
    return list(map(mapToNumbers, multiplications))


def part1(input):
    parsed = parseInput(input)
    result = sum([a*b for (a,b) in parsed])
    print(result)

part1(tInput)
part1(rInput)
