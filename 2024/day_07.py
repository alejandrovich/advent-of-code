from itertools import product

from readfile import read


class Solution:
    # file_name = '07_example.txt'
    file_name = '07_input.txt'
    problems = None
    memo = None

    def __init__(self):
        self.problems = {}
        self.memo = {}

        for line in read(self.file_name):
            problem = line.split(':')
            test = int(problem[0])

            operands = [int(i) for i in problem[1].strip().split(' ')]
            self.problems[test] = operands

        # print(self.problems)

    def do_calculation(self, operators, operands):
        partial = operands[0]

        for i in range(len(operators)):
            memo_key = str(partial) + operators[i] + str(operands[i+1])
            if memo_key in self.memo.keys():
                return self.memo[memo_key]

            if operators[i] == '+':
                partial += operands[i+1]
            elif operators[i] == '*':
                partial *= operands[i+1]
            elif operators[i] == '&':
                partial = int(str(partial) + str(operands[i+1]))
            else:
                raise ValueError('Missing an operator handling')

        self.memo[memo_key] = partial

        return partial


    def find_solution(self, test, operator_class):
        operands = self.problems[test]
        operator_count = len(operands) - 1
        all_operators = list(
            product(operator_class, repeat=operator_count)
        )

        # print(test, all_operators, operands)
        for i in range(len(all_operators)):

            # print('trying', all_operators[i], operands)

            if test == self.do_calculation(all_operators[i], operands):
                return test

        return 0

    def solve(self, operator_class):
        sums = 0

        for test in self.problems.keys():
            result = self.find_solution(test, operator_class)
            # print(result)
            sums += result

        return sums


if __name__ == '__main__':
    s = Solution()
    part1 = s.solve('*+')

    print('part1', part1)
    print()

    part2 = s.solve('*+&')
    print('part2', part2)

