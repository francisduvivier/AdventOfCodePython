import re
import time

import numpy as np

from util import map_to_numbers, sub_map_to_numbers
from dotmap import DotMap

test_input = open('day13-testinput.txt').read().strip()
real_input = open('day13-input.txt').read().strip()
BUTTON_COST = DotMap({
    'A':3,
    'B':1
})

print("BUTTON_COST['A']",BUTTON_COST['A'])


def parse_button(line:str):
    pattern = r'Button\s(?P<letter>[A-Z]):\sX\+(?P<X>\d+),\sY\+(?P<Y>\d+)'
    match = re.match(pattern, line)
    parsed = DotMap(match.groupdict())
    parsed.X = int(parsed.X)
    parsed.Y = int(parsed.Y)
    return parsed


def parse_prize(line:str):
    pattern = r'Prize:\sX=(?P<X>\d+),\sY=(?P<Y>\d+)'
    match = re.match(pattern, line)
    parsed = DotMap(match.groupdict())
    parsed.X = int(parsed.X)
    parsed.Y = int(parsed.Y)
    return parsed


def parse_input(input):
    claw_machines = []
    for claw_machine_lines in input.split('\n\n'):
        claw_machine = DotMap()
        claw_machines.append(claw_machine)
        claw_machine.button_map = DotMap()
        for line in claw_machine_lines.splitlines():
            if line.startswith('Button'):
                button_config = parse_button(line)
                claw_machine.button_map[button_config.letter] = button_config
            else:
                claw_machine.prize = parse_prize(line)
    return claw_machines


def part1(input):
    parsed = parse_input(input)
    result = parsed[0].toDict()
    print(result)
    return result

assert part1(test_input) == 480
part1(real_input)
