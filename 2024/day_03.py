import re

from readfile import read


class Solution:
    # file_name = '03_example2.txt'
    file_name = '03_input.txt'
    lines = None


    def read_input(self, file_name):
        self.lines = []
        for line in read(file_name):
            self.lines.append(line)

    def part1(self):
        self.read_input(self.file_name)
        sums = 0

        for line in self.lines:
            # print(line)
            # match = re.search(r'(mul\(\d+,\d+\))', line)
            matches = re.finditer(r'(mul\(\d+,\d+\))', line)

            for m in matches:
                expr = re.search(r'mul\((\d+),(\d+)\)', m.group())
                # print(m.group())
                # print(expr.group(1), expr.group(2))
                sums += int(expr.group(1)) * int(expr.group(2))

        return sums

    def part2(self):
        self.read_input(self.file_name)
        sums = 0

        for line in self.lines:
            # print('scanning line')
            matches = re.finditer(r'(mul\(\d+,\d+\)|(do\(\))|(don\'t\(\)))', line)

            contribute = True
            for m in matches:
                if m.group() == 'do()':
                    # print('ON!')
                    contribute = True
                elif m.group() == "don't()":
                    # print('OFF!')
                    contribute = False
                else:
                    if contribute:
                        expr = re.search(r'mul\((\d+),(\d+)\)', m.group())
                        # print(m.group())
                        sums += int(expr.group(1)) * int(expr.group(2))

        return sums

if __name__ == '__main__':
    s = Solution()
    print(f'part 1 equals {s.part1()}')
    print(f'part 2 equals {s.part2()}')
    # part 2: too high: 105264641
