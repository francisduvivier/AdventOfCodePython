from dotmap import DotMap

test_input = open('day17-testinput.txt').read().strip()
real_input = open('day17-input.txt').read().strip()


class OpCodeMachine:
    def __init__(self, register_map, program, instruction_pointer=0, ticks=0, output=None):
        self.register_map = register_map
        self.program = program
        self.ticks = ticks
        self.output = [] if output is None else output
        self.instruction_pointer = instruction_pointer

    def clone(self):
        cloned = OpCodeMachine(self.register_map.copy(), self.program.copy(), self.instruction_pointer, self.ticks,
                               self.output.copy())
        return cloned

    def run_program(self):
        while self.instruction_pointer < len(self.program):
            prev_pointer = self.instruction_pointer
            self.instruction_pointer += 2
            self._do_op(prev_pointer)

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
                print('pointer', self.instruction_pointer, 'output', output)
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


def part1(input):
    program, register_map = parse_input(input)
    print(program, register_map)
    runner = OpCodeMachine(register_map, program)
    runner.run_program()
    result = ','.join([str(nb) for nb in runner.output])
    print(result)
    return result


assert part1(test_input) == '4,6,3,5,6,3,5,2,1,0'
part1(real_input)
