from dotmap import DotMap

test_input = open('day17-testinput.txt').read().strip()
test_input2 = open('day17-testinput2.txt').read().strip()
real_input = open('day17-input.txt').read().strip()

glob_states = {}


class OpCodeMachine:
    def __init__(self, register_map, program, instruction_pointer=0, ticks=0, output=None):
        global glob_states
        self.register_map = register_map
        self.program = program
        self.ticks = ticks
        self.output = [] if output is None else output
        self.instruction_pointer = instruction_pointer
        self.states = {}

    def clone(self):
        cloned = OpCodeMachine(self.register_map.copy(), self.program, self.instruction_pointer, self.ticks,
                               self.output.copy())
        return cloned

    def state_key(self):
        return str(self.register_map) + str(self.instruction_pointer)

    def run_program(self, part2=False):
        while self.instruction_pointer < len(self.program):
            prev_pointer = self.instruction_pointer
            self.instruction_pointer += 2
            self._do_op(prev_pointer)
            # if part2 and len(self.output) > len(self.program):
            #     self.output = []
            #     return
            # if part2 and self.program[prev_pointer] == 5 and self.program[:len(self.output)] != self.output:
            #     self.output = []
            #     return

    def _do_op(self, pointer):
        opcode = self.program[pointer]
        operand = self.program[pointer + 1]
        self.ticks += 1
        match opcode:
            case 0:
                # The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
                # The denominator is found by raising 2 to the power of the instruction's combo operand.
                # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
                # The result of the division operation is truncated to an integer and then written to the A register.
                numerator = self.register_map.A
                denominator = 2 ** self.combo(operand)
                self.register_map.A = int(numerator / denominator)
            case 1:
                # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the
                # instruction's literal operand, then stores the result in register B.
                self.register_map.B = self.register_map.B ^ operand
            case 2:
                # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
                # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
                self.register_map.B = self.combo(operand) % 8
            case 3:
                # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
                # it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps,
                # the instruction pointer is not increased by 2 after this instruction.
                if self.register_map.A != 0:
                    self.instruction_pointer = operand
            case 4:
                # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
                # then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
                self.register_map.B = self.register_map.B ^ self.register_map.C
            case 5:
                # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
                # (If a program outputs multiple values, they are separated by commas.)
                output = self.combo(operand) % 8
                # print('pointer', self.instruction_pointer, 'output', output)
                self.output.append(output)

            case 6:
                # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result
                # is stored in the B register. (The numerator is still read from the A register.)
                numerator = self.register_map.A
                denominator = 2 ** self.combo(operand)
                self.register_map.B = int(numerator / denominator)
            case 7:
                # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result
                # is stored in the C register. (The numerator is still read from the A register.)
                numerator = self.register_map.A
                denominator = 2 ** self.combo(operand)
                self.register_map.C = int(numerator / denominator)
        pass

    def combo(self, operand):
        match operand:
            case 0:
                return operand
            case 1:
                return operand
            case 2:
                return operand
            case 3:
                return operand
            case 4:
                return self.register_map.A
            case 5:
                return self.register_map.B
            case 6:
                return self.register_map.C
            case 7:
                raise NotImplementedError('Invalid program')

    def run_clone_part2(self, try_solution):
        clone = self.clone()
        clone.register_map.A = try_solution
        clone.run_program()
        return clone.output


def advance(self):
    self.ticks += 1


def parse_registers(lines: list[str]):
    register_map = DotMap()
    for line in lines:
        # Register A: 729
        splits = line.split(' ')
        letter = splits[1][0]
        register_map[letter] = int(splits[2])
    return register_map


def parse_input(input):
    register_lines, operations_line = input.split('\n\n')
    register_map = parse_registers(register_lines.splitlines())
    program = [int(val) for val in operations_line.split(': ')[1].split(',')]
    return program, register_map


def join_nbs(nbs: list[int]):
    return ','.join([str(nb) for nb in nbs])


def part1(input):
    program, register_map = parse_input(input)
    print(program, register_map)
    runner = OpCodeMachine(register_map, program)
    runner.run_program()
    result = join_nbs(runner.output)
    print(result)
    return result


assert part1(test_input) == '4,6,3,5,6,3,5,2,1,0'
part1(real_input)


def combo_name(operand):
    match operand:
        case 0:
            return operand
        case 1:
            return operand
        case 2:
            return operand
        case 3:
            return operand
        case 4:
            return 'A'
        case 5:
            return 'B'
        case 6:
            return 'C'
        case 7:
            raise NotImplementedError('Invalid program')


def get_ops_name(opcode, operand):
    match opcode:
        case 0:
            return 'adv', combo_name(operand)
        case 1:
            return 'bxl', operand
        case 2:
            return 'bst', combo_name(operand)
        case 3:
            return 'jnz', operand
        case 4:
            return 'bxc', '_'
        case 5:
            return 'out', combo_name(operand)
        case 6:
            return 'bdv', combo_name(operand)
        case 7:
            return 'cdv', combo_name(operand)
    pass


DEBUG = False

def part2(input):
    program, register_map = parse_input(input)
    print('\n', program, register_map)
    start_runner = OpCodeMachine(register_map, program)
    program_explanation = '\n'.join(
        [str(get_ops_name(code, program[index + 1])) for index, code in enumerate(program) if index % 2 == 0])
    print(program_explanation)
    solutions = [{"pos": 0, "most_significant_bits": 0}]
    while len(solutions) != 0:
        if DEBUG: print('len(solutions)', len(solutions))
        partial = solutions.pop()
        pos = partial['pos']
        most_significant_bits = partial['most_significant_bits']
        if DEBUG: print('pos', pos, 'solution', bin(most_significant_bits))
        for new_bits in range(8):
            try_solution = (most_significant_bits << 3) + new_bits
            run_output = start_runner.run_clone_part2(try_solution)
            if run_output[-pos - 1:] == program[-pos - 1:]:
                possibility = {"pos": pos + 1, "most_significant_bits": try_solution}
                if DEBUG: print('possibility', possibility)
                solutions.insert(0, possibility)
                if pos == len(program) - 1:
                    print('\npart2 solution!', try_solution)
                    return try_solution

    raise NotImplementedError('no solution')


# B = A % 3 (011) : B=a1-!a1-!a1
# B = B XOR 3 (011) : B=a1-!a1-!a1
# C = A/(2**B): C=Abits[0:-B] c is a but with 0 to 8 least signif bits less
# A = A/(2**3): A=Abits[0:-3] a is a but 3 least sign bits less
# B = B XOR 4 (100) : B=!a1-!a1-!a1
# B = B XOR C : B = Abits[0:-B] XOR !a1-!a1-!a1
# out B % 8: output 3 least significant bits of B
# jump 0 until A = 0

assert part2(test_input2) == 117440
assert part2(real_input) == 266932601404433
