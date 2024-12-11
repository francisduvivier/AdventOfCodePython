import time

from util import map_to_numbers

tInput = open('day11-testinput.txt').read().strip()
rInput = open('day11-input.txt').read().strip()


def parseInput(input):
    lines = input.splitlines()
    return lines[0].split(' ')


def blink(stones: list[str]):
    new_stones = []
    for stone in stones:
        if stone == '0':
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            half = int(len(stone) / 2)
            new_stones.append(stone[:half])
            new_stones.append(str(int(stone[half:])))
        else:
            multiplied_int = int(stone) * 2024
            new_stones.append(str(multiplied_int))
    return new_stones


def part1(input):
    stones = parseInput(input)
    print(stones)
    for i in range(25):
        stones = blink(stones)
    result = len(stones)
    print(result)
    return result


assert part1(tInput) == 55312
part1(rInput)
