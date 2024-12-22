import time
from functools import cache

import numpy as np

from util import map_to_numbers, sub_map_to_numbers
import sys

test_input = open('day22-testinput.txt').read().strip()
test_input_2 = open('day22-testinput2.txt').read().strip()
real_input = open('day22-input.txt').read().strip()
sys.setrecursionlimit(3000)


def parse_input(input):
    lines = input.splitlines()
    numbers = map_to_numbers(lines)
    return numbers


@cache
def mix(secret, new_val):
    return secret ^ new_val


assert mix(42, 15) == 37


@cache
def prune(secret):
    return secret % 16777216


assert prune(100000000) == 16113920

@cache
def get_next_secret(secret):
    secret = mult_64(secret)
    secret = div_32(secret)
    return prune(mix(secret, secret << 11))


def div_32(secret):
    return prune(mix(secret, int(secret >> 5)))


def mult_64(secret):
    return prune(mix(secret, secret << 6))


@cache
def get_next_secret_rec(secret, times):
    if times == 0:
        return secret
    return get_next_secret_rec(get_next_secret(secret), times - 1)


assert get_next_secret_rec(123, 0) == 123
assert get_next_secret_rec(123, 1) == 15887950
assert get_next_secret_rec(15887950, 1) == 16495136
assert get_next_secret_rec(123, 2) == 16495136
assert get_next_secret_rec(16495136, 1) == 527345
assert get_next_secret_rec(527345, 1) == 704524
assert get_next_secret_rec(704524, 1) == 1553684
assert get_next_secret_rec(1553684, 1) == 12683156
assert get_next_secret_rec(12683156, 1) == 11100544
assert get_next_secret_rec(11100544, 1) == 12249484
assert get_next_secret_rec(12249484, 1) == 7753432
assert get_next_secret_rec(7753432, 1) == 5908254
assert get_next_secret_rec(123, 10) == 5908254

assert get_next_secret_rec(1, 2000) == 8685429
assert get_next_secret_rec(10, 2000) == 4700978
assert get_next_secret_rec(100, 2000) == 15273692
assert get_next_secret_rec(2024, 2000) == 8667524


def part1(input):
    secrets = parse_input(input)
    result = sum([get_next_secret_rec(secret, 2000) for secret in secrets])
    print(result)
    return result

DEBUG = False
assert part1(test_input) == 37327623
if DEBUG: assert part1(real_input) == 13022553808


def last_digit(number):
    return number % 10

assert last_digit(0) == 0
assert last_digit(1) == 1
assert last_digit(10) == 0
assert last_digit(113) == 3

@cache
def count_win(seq: tuple[int], secret: int, times: int):
    prev = last_digit(secret)
    change = [None, None, None, None]
    next_secret = secret
    for i in range(times):
        next_secret = get_next_secret(next_secret)
        change.pop(0)
        new_price = last_digit(next_secret)
        change.append(new_price - prev)
        prev = new_price
        if seq == tuple(change):
            return new_price
    return 0


assert count_win((-2, 1, -1, 3), 1, 2000) == 7
assert count_win((-2, 1, -1, 3), 2, 2000) == 7
assert count_win((-2, 1, -1, 3), 3, 2000) == 0
assert count_win((-2, 1, -1, 3), 2024, 2000) == 9


def part2(input):
    secrets = parse_input(input)
    result = sum([get_next_secret_rec(secret, 2000) for secret in secrets])
    print(result)
    return result


assert part2(test_input_2) == 23
part2(real_input)
