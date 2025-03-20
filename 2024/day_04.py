from itertools import product

from readfile import read


class Solution:
    file_name = '04_example.txt'
    # file_name = '04_input.txt'
    lines = None
    puzzle = None
    xmax = None
    ymax = None

    def __init__(self):
        self.puzzle = list(read(self.file_name))
        xmax = len(self.puzzle) if self.puzzle else 0
        xmax = len(self.puzzle[0]) if self.puzzle else 0

    def part1(self):
        # define the ways XMAS can appear in an array
        '''
       -3     S  S  S
       -2      A A A
       -1       MMM
        0     SAMXMAS
        1       MMM
        2      A A A
        3     S  S  S
        '''

        xmas_count = 0

        # for each x on a line
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                # check for XMAS rooted in that spot
                xmas_count += self.check_xmas(x, y)

        print(xmas_count)

    def get_letter(self, x, y):
        if (
            0 <= x < len(self.puzzle) and 
            0 <= y < len(self.puzzle)
        ):
            return self.puzzle[x][y]

        return ''

    def check_xmas(self, x, y):
        word = 'XMAS'
        found = 0

        x_changes = (1, 0, -1)
        y_changes = (1, 0, -1)
        for change in list(product(x_changes, y_changes)):
            print(change, x, y)

            spelled = ''.join([
                self.get_letter(
                    x + i * change[0],
                    y + i * change[1],
                )
                for i in range(4)
            ])
            print(spelled)
            if spelled == 'XMAS':
                print(f'found at {(x, y)}')
                found += 1

        return found

    def check_xmas2(self, x, y):
        A, M, S = 'A', 'M', 'S'

        if self.puzzle[x][y] != A:
            return 0
        left_to_right_diag = (
            self.get_letter(x - 1, y - 1) +
            self.get_letter(x + 1, y + 1)
        )
        right_to_left_diag = (
            self.get_letter(x + 1, y - 1) +
            self.get_letter(x - 1, y + 1)
        )
        print(left_to_right_diag, right_to_left_diag)
        if (
            left_to_right_diag in ('MS', 'SM') and 
            right_to_left_diag in ('MS', 'SM')
        ):
            return 1
        return 0


    def part2(self):
        xmas_count = 0

        # for each x on a line
        for x in range(len(self.puzzle)):
            for y in range(len(self.puzzle)):
                # check for XMAS rooted in that spot
                xmas_count += self.check_xmas2(x, y)

        print(xmas_count)

        pass


if __name__ == '__main__':
    s = Solution()
    # s.part1()
    s.part2()
            

