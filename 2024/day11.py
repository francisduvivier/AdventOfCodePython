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


blink_map = {}


def blink_rec(stone, times):
    key = to_key(stone, times)
    if times == 0:
        return 1
    if key in blink_map:
        return blink_map[key]
    result = sum([blink_rec(blink_part, times - 1) for blink_part in blink([stone])])
    blink_map[key] = result
    return result


def start_blink_rec(stones, amount):
    return sum([blink_rec(stone, amount) for stone in stones])


def to_key(stone, times):
    return stone + ',' + str(times)



def part1(input):
    print('part1')
    stones = parseInput(input)
    print(stones)
    result = start_blink_rec(stones, 25)
    print(result)
    return result


assert part1(tInput) == 55312
part1(rInput)

def part2(input):
    print('part2')
    stones = parseInput(input)
    print(stones)

    result = start_blink_rec(stones, 75)
    print(result)
    return result

part2(rInput)
