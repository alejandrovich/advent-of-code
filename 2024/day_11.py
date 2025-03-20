from collections import defaultdict
from itertools import chain

from readfile import read

# file_name = '11_example.txt'
file_name = '11_input.txt'


class Solution:
    stones = None

    def __init__(self):
        for line in read(file_name):
            self.stones = [int(stone) for stone in line.split()]

    def should_split(self, stone):
        # if # digits is even
        digits_length = len(str(stone))
        return digits_length % 2 == 0

    def split(self, stone):
        digits = str(stone)
        digits_length = len(digits)

        half_length = digits_length // 2
        return (
            int(digits[0:half_length]), 
            int(digits[half_length:]),
        )

    def multiply(self, stone):
        return stone * 2024

    def should_become_1(self, stone):
        return stone == 0

    def multiple_evolve(self, stones, count):

        evolutions = stones

        for i in range(count):
            evolutions = self.evolve(evolutions)

        return evolutions

    def blink_at_stone(self, stone):
        if self.should_become_1(stone):
            return [1]

        elif self.should_split(stone):
            split = self.split(stone)
            return [split[0], split[1]]
        else:
            return [self.multiply(stone)]

    def evolve(self, stones):
        evolved = []
        for stone in stones:
            if self.should_become_1(stone):
                evolved.append(1)
            elif self.should_split(stone):
                split = self.split(stone)
                evolved.append(split[0])
                evolved.append(split[1])
            else:
                evolved.append(self.multiply(stone))
        return evolved

    def part1(self):
        # evolve stones 25 times, brute force works.

        evolutions = self.stones
        for i in range(25):
            evolutions = self.evolve(evolutions)
            # print(evolutions)

        return evolutions

    def calc(self, stone, blinks):
        calc_key = (stone, blinks)

        if calc_key in self.calculations.keys():
            return self.calculations[calc_key]

        elif blinks > 1:
            sub_calcs = self.blink_at_stone(stone)

            total = 0
            for c in sub_calcs:
                ans = self.calc(c, blinks - 1)
                self.calculations[(c, blinks - 1)] = ans
                # print(f'calc mid {(c, blinks - 1)} = {ans}')
                total += ans
            return total
        else:
            # one last blink
            return len(self.blink_at_stone(stone))

    def part23(self, blinks):
        self.calculations = {}

        final = 0
        for stone in self.stones:
            # stone_spawns = self.calc(stone, blinks)
            stone_spawns = self.calc(stone, blinks)
            final += stone_spawns
            print(f'stone {stone} spawned {stone_spawns} after {blinks} blinks')

        print(f'part2 ans: {final}')

        stones = set()
        stone_perms = set()
        for k, v in self.calculations.items():
            stone, blinks = k[0], k[1]
            stones.add(stone)
            stone_perms.add(k)

        print(f'Saw {len(stones)} stone numbers')
        print(f'Estimate {len(stones) * 75} stone calc perms')
        print(f'Actual {len(stone_perms)} keys')


if __name__ == '__main__':
    s = Solution()
    e = s.part1()
    print(f'part1 {len(e)}')

    
    s.part23(75)

