import re
import time

import numpy as np

from util import map_to_numbers, sub_map_to_numbers
from dotmap import DotMap

test_input = open('day13-testinput.txt').read().strip()
real_input = open('day13-input.txt').read().strip()
BUTTON_COST = DotMap({
    'A': 3,
    'B': 1
})


def parse_button(line: str):
    pattern = r'Button\s(?P<letter>[A-Z]):\sX\+(?P<X>\d+),\sY\+(?P<Y>\d+)'
    match = re.match(pattern, line)
    parsed = DotMap(match.groupdict())
    parsed.X = int(parsed.X)
    parsed.Y = int(parsed.Y)
    return parsed


def parse_prize(line: str):
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


def calc_prize(machine):
    button_B = machine.button_map.B
    prize_X = machine.prize.X
    prize_Y = machine.prize.Y
    button_A = machine.button_map.A
    max_a_presses = min(int(prize_X / button_A.X),
                        int(prize_Y / button_A.Y))
    cost_A = 0
    min_cost = None
    for a_presses in range(max_a_presses):
        def get_cost_B():
            if min_cost is not None and cost_A >= min_cost:
                return
            if prize_X % button_B.X != 0:
                return
            if prize_Y % button_B.Y != 0:
                return
            B_presses_for_Y = int(prize_Y / button_B.Y)
            B_presses_for_X = int(prize_X / button_B.X)
            if B_presses_for_X != B_presses_for_Y:
                return

            cost_B = B_presses_for_X * BUTTON_COST.B
            return cost_B

        cost_B= get_cost_B()
        if cost_B is not None:
            total_cost = cost_B + cost_A
            if min_cost is None or total_cost < min_cost:
                min_cost = total_cost
        prize_X -= button_A.X
        prize_Y -= button_A.Y
        cost_A += BUTTON_COST.A
    return min_cost


def part1(input):
    claw_machines = parse_input(input)
    result = sum([calc_prize(machine) or 0 for machine in claw_machines])
    print(result)
    return result


assert part1(test_input) == 480
part1(real_input)
