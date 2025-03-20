from collections import namedtuple, defaultdict

from readfile import read


Point = namedtuple('Point', ('x', 'y', 'h'))

# file_name: str = '10_example.txt'
file_name: str = '10_input.txt'


class Solution:
    mapa = None
    trailheads: list = None
    xmax = 0
    ymax = 0
    trails = None

    def __init__(self):
        self.mapa = []  # (0,0) at top-left
        self.trailheads = []
        self.trails = defaultdict(list)

        for line in read(file_name):
            self.mapa.append([int(c) for c in line])

        print(self.mapa)
        self.xmax, self.ymax = len(self.mapa[0]), len(self.mapa)

        for y, row in enumerate(self.mapa):
            for x, c in enumerate(row):
                if c == 0:
                    self.trailheads.append(Point(x, y, 0))

        print(self.trailheads)

    def print_trails(self):
        for head_tail, trails in self.trails.items():
            print(len(trails), head_tail)

            for trail in trails:
                print('-> ', ', '.join(
                        f'{p.h}=({p.x},{p.y})'
                        for p in trail
                    )
                )
            print()

    def get_point(self, x, y):
        if 0 <= x < self.xmax and 0 <= y < self.ymax:
            return Point(x, y, self.mapa[y][x])

    def get_neighbors(self, point):
        # 4 neighbors, up, left, right, left
        x, y = point.x, point.y
        neighbor_points = (
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        )
        # filter for in-map points
        points = filter(
            bool,
            [
                self.get_point(np[0], np[1])
                for np in neighbor_points
            ]
        )
        # filter for upward-sloping points
        points = list(
            filter(lambda p: p.h == point.h + 1, points)
        )
        return points

    def find_trail(self, trail):
        '''
        get the latest point on the path
        find its neighbors,
        search each trail including that neighbor
        '''
        # print('debug find-trail', trail)
        
        # exit condition
        if trail[-1].h == 9:
            self.trails[
                (trail[0], trail[-1])
            ].append(trail)
            return

        neighbors = self.get_neighbors(trail[-1])
        print('neighbors', neighbors)

        for neighbor in neighbors:
            self.find_trail(trail + [neighbor])

    def search_map(self):
        for trailhead in self.trailheads:
            self.find_trail([trailhead])

        self.print_trails()


if __name__ == '__main__':
    s = Solution()
    s.search_map()
    print()

    print('part1', len(s.trails.keys()))

    print('part2', sum(
        len(trails)
        for key, trails in s.trails.items()
    ))
