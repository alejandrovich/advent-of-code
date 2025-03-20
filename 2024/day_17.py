import math


class Solution:
    a_reg = 0
    b_reg = 0
    c_reg = 0
    position = 0
    program = None
    output = None

    def __init__(self):
        self.output = []

    def combo_operand(self, value):
        if value < 4:
            return value
        elif value == 4:
            return self.a_reg
        elif value == 5:
            return self.b_reg
        elif value == 6:
            return self.c_reg

    def adv(self, operand):
        self.a_reg = self.a_reg // int(math.pow(2, self.combo_operand(operand)))
        return 2

    def bdv(self, operand):
        self.b_reg = self.a_reg // int(math.pow(2, self.combo_operand(operand)))
        return 2

    def cdv(self, operand):
        self.c_reg = self.a_reg // int(math.pow(2, self.combo_operand(operand)))
        return 2

    def bxl(self, operand):
        self.b_reg = self.b_reg ^ operand
        return 2

    def bst(self, operand):
        self.b_reg = self.combo_operand(operand) % 8
        return 2

    def jnz(self, operand):
        if self.a_reg == 0:
            return 2
        else:
            self.position = operand
            return 0

    def bxc(self, operand):
        self.b_reg = self.b_reg ^ self.c_reg
        return 2

    def out(self, operand):
        value = self.combo_operand(operand) % 8
        self.output.append(value)
        return 2

    def opcode_map(self, opcode):
        OPCODES = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        return OPCODES[opcode]

    def exec(self, bounded=False):
        self.position = 0
        while self.position < len(self.program):
            func = self.opcode_map(self.program[self.position])
            operand = self.program[self.position + 1]

            increment = func(operand)

            self.position = self.position + increment

            # break early for brute-force optimization
            if bounded:
                progress = self.check_output()

                # print(f'checking good={progress} {self.output}, {self.program}')

                if not progress:
                    break

    def check_output(self):
        # if no output, continue
        if not self.output:
            return True

        for i, output in enumerate(self.output):
            if output != self.program[i]:
                return False

        return True


def example_1():
    '''
    Register A: 729
    Register B: 0
    Register C: 0

    Program: 0,1,5,4,3,0
    '''
    s = Solution()
    s.a_reg = 729
    s.b_reg = 0
    s.c_reg = 0
    s.program = [0,1,5,4,3,0]
    s.exec()
    print(','.join(str(t) for t in s.output))


def part1():
    '''
    Register A: 17323786
    Register B: 0
    Register C: 0

    Program: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
    '''
    s = Solution()
    s.a_reg = 17323786
    s.b_reg = 0
    s.c_reg = 0
    s.program = [2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0]
    s.exec()
    print(','.join(str(t) for t in s.output))


def part2_solve():
    '''
    Register A: 17323786
    Register B: 0
    Register C: 0

    Program: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
    '''
    best = []
    s = Solution()
    tries = 1
    increment = 2000000
    start = 400000000 + (tries * increment)
    for i in range(start, start + increment, 1):
        s.a_reg = i
        s.b_reg = 0
        s.c_reg = 0
        s.program = [2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0]
        s.output = []

        expected = ','.join(str(t) for t in s.program)

        s.exec(bounded=True)
        actual = ','.join(str(t) for t in s.output)
        if len(s.output) > 5:
            best.append((i, s.output))


        # print(f'Tried {i} {expected} {actual}')
        if actual == expected:
            print(f'Solved! {i}')
            break

    for thing in best:
        print(thing)


def part2_example_solve():
    '''
    Register A: 2024
    Register B: 0
    Register C: 0

    Program: 0,3,5,4,3,0
    117440
    '''
    s = Solution()
    for i in range(200000):
        s.a_reg = i
        s.b_reg = 0
        s.c_reg = 0
        s.program = [0,3,5,4,3,0]
        s.output = []
        expected = ','.join(str(t) for t in s.program)

        s.exec(bounded=True)
        actual = ','.join(str(t) for t in s.output)

        print(f'Tried {i} {expected} {actual}')
        if actual == expected:
            print(f'Solved! {i}')
            break


def part2_example():
    '''
    Register A: 2024
    Register B: 0
    Register C: 0

    Program: 0,3,5,4,3,0
    117440
    '''
    s = Solution()
    s.a_reg = 117440
    s.b_reg = 0
    s.c_reg = 0
    s.program = [0,3,5,4,3,0]

    expected = ','.join(str(t) for t in s.program)

    s.exec(bounded=True)
    actual = ','.join(str(t) for t in s.output)

    print(f'Tried {117440} {expected} {actual}')
    if actual == expected:
        print(f'Solved! {117440}')


if __name__ == '__main__':
    part2_example()
    part2_solve()
