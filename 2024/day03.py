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
    result = sum([a * b for (a, b) in parsed])
    print(result)


part1(tInput)
part1(rInput)


def parseInput2(input):
    multiplications = re.findall(r'((mul)\((\d+),(\d+)\)|(do|don\'t)\(\))', input)
    return list(
        map(lambda x: {"op": x[1] if x[1] == 'mul' else x[4], "vals": mapToNumbers(x[2:4]) if x[1] == 'mul' else []},
            multiplications))


def part2(input):
    parsed = parseInput2(input)
    result = 0
    do = True
    for instruct in parsed:
        if instruct["op"] == "don't":
            do = False
        if instruct["op"] == "do":
            do = True
        if instruct["op"] == 'mul' and do:
            (a, b) = instruct["vals"]
            result += a * b
    print(result)


part2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
part2(rInput)
