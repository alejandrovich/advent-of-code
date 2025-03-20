import re
from collections import defaultdict
from functools import cmp_to_key
from math import floor

from readfile import read


# file_name = '05_example.txt'
file_name = '05_input.txt'


class Solution:
    # list of the ordered (mixed up) pages
    updates = None

    # dict: set
    # (pages keyed to a set of pages that are larger *must come after*
    page_orderings = None

    def __init__(self):
        self.updates = []
        self.page_orderings = defaultdict(set)

        self.parse()

    def key_func(self, a, b):
        # - for a < b
        # + for a > b
        # 0 for a = b

        if b in self.page_orderings[a]:
            return -1
        if a in self.page_orderings[b]:
            return 1
        return 0

    def parse(self):
        for line in read(file_name):
            if '|' in line:
                first, second = map(int, line.split('|'))
                self.page_orderings[first].add(second)

            if ',' in line:
                pages = list(map(int, line.split(',')))

                self.updates.append(pages)

    def part1(self):
        # sort each update and include its 
        # middle value in a running sum iff it was already sorted
        sums = 0
        for update in self.updates:
            fixed = sorted(update, key=cmp_to_key(self.key_func))
            if update == fixed:
                sums += int(fixed[floor(len(fixed) / 2)])

        print('sums', sums)

    def part2(self):
        # sort each update and include its 
        # middle value in a running sum iff it wasn't already sorted
        sums = 0
        for update in self.updates:
            fixed = sorted(update, key=cmp_to_key(self.key_func))
            if update != fixed:
                sums += int(fixed[floor(len(fixed) / 2)])

        print('sums', sums)


if __name__ == '__main__':
    s = Solution()
    s.part1()
    s.part2()
