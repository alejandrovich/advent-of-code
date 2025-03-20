from itertools import combinations
from collections import defaultdict, namedtuple

from readfile import read


P = namedtuple('P', ('x', 'y', 'f'))



class Solution:
    # file_name = '08_example.txt'
    file_name = '08_input.txt'
    area = None
    antenna = None
    height = 0
    width = 0
    part1 = True

    def __init__(self):
        self.area = []
        self.antenna = defaultdict(list)

        for y, line in enumerate(read(self.file_name)):
            row = []
            for x, char in enumerate(line):
                if char != '.':
                    p = P(x=x, y=y, f=char)
                    self.antenna[char].append(p)
                row.append(char)
            self.area.append(row)
        self.height = len(self.area)
        self.width = len(self.area[0])

    def print(self):
        print('Square {self.width} x {self.height}')
        for l in self.area:
            print(''.join(l))

    def an(self, a, b):  # an = Antinode
        xdiff = a.x - b.x
        ydiff = a.y - b.y

        an1 = P(a.x + xdiff, a.y + ydiff, '#')
        an2 = P(b.x - xdiff, b.y - ydiff, '#')
        # print(a, b, an1, an2)

        yield an1
        yield an2

    def make_antinode(self, locus, vector, distance):
        an = P(
            locus.x + (vector.x * distance),
            locus.y + (vector.y * distance),
            '#'
        )
        return an


    def an2(self, a, b):  # an = Antinode
        xdiff = a.x - b.x
        ydiff = a.y - b.y

        vector = P(xdiff, ydiff, 'V')  # V for vector :)
        dir1_count, dir2_count = 0, 0

        an = self.make_antinode(a, vector, dir1_count)
        while self.is_antinode_valid(an):
            dir1_count += 1
            yield an
            an = self.make_antinode(a, vector, dir1_count)

        # reverse vector
        vector = P(-1 * vector.x, -1 * vector.y, 'V')

        an = self.make_antinode(b, vector, dir2_count)
        while self.is_antinode_valid(an):
            dir2_count += 1
            yield an
            an = self.make_antinode(a, vector, dir2_count)

    def list_antinodes(self, station_id):
        typed_antinodes = []
        combos = combinations(self.antenna[station_id], 2)

        for i, c in enumerate(combos):
            if self.part1:
                typed_antinodes.extend(self.an(*c))
            else:
                typed_antinodes.extend(self.an2(*c))

            # print(i, typed_antinodes)

        return iter(typed_antinodes)

    def is_antinode_valid(self, antinode):
        return (
            0 <= antinode.x <= self.width - 1 and
            0 <= antinode.y <= self.height - 1
        )

    def all_antinodes(self):
        nodes = [
            a
            for an_key in self.antenna.keys()
            for a in self.list_antinodes(an_key)
            if self.is_antinode_valid(a)
        ]
        return iter(nodes)



if __name__ == '__main__':
    s = Solution()
    s.print()
    s.list_antinodes('A')

    s.part1 = True
    all_an = set(s.all_antinodes())
    print(sorted(all_an))
    print(len(all_an))

    s.part1 = False
    all_an = set(s.all_antinodes())
    print(sorted(all_an))
    print(len(all_an))
