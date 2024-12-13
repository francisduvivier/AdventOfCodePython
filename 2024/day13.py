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
    # a*Ax+b*Bx = Px
    # a*Ay+b*By = Py
    #
    # Examples
    #
    # Solve the system of equations: x0 + 2 * x1 = 1 and 3 * x0 + 5 * x1 = 2:
    #
    # import numpy as np
    # a = np.array([[1, 2], [3, 5]])
    # b = np.array([1, 2])
    # x = np.linalg.solve(a, b)
    # x
    left = np.array([[button_A.X, button_B.X],
                     [button_A.Y, button_B.Y]])
    right = np.array([prize_X, prize_Y])
    solutions = np.linalg.solve(left, right)
    print(solutions)
    a = round(solutions[0])
    b = round(solutions[1])
    if a * button_A.X + b * button_B.X == prize_X and a * button_A.Y + b * button_B.Y == prize_Y:
        return solutions[0] * BUTTON_COST.A + solutions[1] * BUTTON_COST.B
    return None


def part1(input):
    claw_machines = parse_input(input)
    result = sum([calc_prize(machine) or 0 for machine in claw_machines])
    print(result)
    return result


assert part1(test_input) == 480
part1(real_input)


def calc_prize2(machine):
    machine.prize.X = machine.prize.X + 10_000_000_000_000
    machine.prize.Y = machine.prize.Y + 10_000_000_000_000
    return calc_prize(machine)


def part2(input):
    claw_machines = parse_input(input)
    result = sum([calc_prize2(machine) or 0 for machine in claw_machines])
    print(result)
    return result


part2(real_input)
