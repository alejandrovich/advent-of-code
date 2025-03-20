
# Definitions:
# Ms = Max shortcut distance
# Sh = Set of pairs of points (possible shortcuts)
# Pp = path point, x, y and Ds (distance from start)
# Sd = Shortcut Distance = abs(p2.x - p1.x) + abs(p2.y - p1.y)

# 1. solve the maze
# output: list of points that comprise the path
# output: each point corresponds to a value (the distance from the start)

# 2. investigate pairs of points
# Add all point-pairs to Sh
# Filter Sh for points that are reachable by Ms
# For each remaining pair:
# Calculate shortcut distance Sd
# calculate Sv (shortcut Value) = P2.Ds - Sd


from collections import defaultdict, namedtuple
from itertools import combinations

from readfile import read


# file_name = '20_example.txt'
file_name = '20_input.txt'
Point = namedtuple('Point', ('x', 'y'))


class Solution:
    walls = set()
    start = None
    end = None
    mapa = None
    x_max = 0
    y_max = 0
    racetrack = None
    savings = defaultdict(list)

    def in_map(self, point):
        return (
            0 <= point.x < self.x_max
            and 0 <= point.y < self.y_max
        )

    def on_track(self, point):
        return point in self.racetrack.keys()

    def is_wall(self, point):
        return point in self.walls

    def skips(self, point):
        possible_skips = [
            # wall, landing
            (Point(point.x, point.y + 1), Point(point.x, point.y + 2)),
            (Point(point.x, point.y - 1), Point(point.x, point.y - 2)),
            (Point(point.x + 1, point.y), Point(point.x + 2, point.y)),
            (Point(point.x - 1, point.y), Point(point.x - 2, point.y)),
        ]

        # filter for in mapa

        shortcuts = [
            wall_landing for wall_landing in possible_skips

            # landing place is on the map
            if self.on_track(wall_landing[1])
            and self.is_wall(wall_landing[0])
        ]
        for shortcut in shortcuts:
            start_count = self.racetrack[point]
            end_count = self.racetrack[shortcut[1]]

            savings = self.distance_saved(point, shortcut[1])

            # print(f'from {point} to {shortcut[1]} ({savings})')
            self.savings[savings].append((point, shortcut[1]))

    def char(self, point):
        return self.mapa[point.y][point.x]

    def neighbors(self, point):
        possible_points = [
            Point(point.x, point.y + 1),
            Point(point.x, point.y - 1),
            Point(point.x + 1, point.y),
            Point(point.x - 1, point.y),
        ]
        tracks = [
            n for n in possible_points
            if self.in_map(n)
            and self.char(n) != '#'
            and n not in self.visited
        ]
        # print(f'tracks {tracks}, current {point}')
        return tracks

    def next_track(self, current: Point):
        if self.char(current) == 'E':
            return None

        adj = self.neighbors(current)
        return adj[0]

    def print(self):
        for line in self.mapa:
            print(line)

        print()

    def print_track(self):
        for y in range(self.y_max):
            line = ''
            for x in range(self.x_max):
                p = Point(x, y)
                if p in self.racetrack.keys():
                    line += 'x'
                else:
                    line += ' '
            print(line)

    def read_grid(self):
        '''
        Save information about the input (walls, start, end, track)
        '''
        self.mapa = []
        self.visited = set()
        self.racetrack = {}

        for y, line in enumerate(read(file_name)):
            self.mapa.append(line)
            for x, char in enumerate(line):
                point = Point(x, y)
                if char == '#':
                    self.walls.add(point)
                elif char == 'S':
                    self.start = point
                elif char == 'E':
                    self.end = point
        self.x_max = len(self.mapa[0])
        self.y_max = len(self.mapa)

    def count_greater(self, savings_amount):
        sum_greater = sum(
            len(self.savings[amount])
            for amount in sorted(self.savings.keys())
            if amount >= savings_amount
        )
        return sum_greater

    def save_racetrack(self):
        counter = 0
        track = self.start

        while track:
            # print(counter, track, self.char(track))
            self.visited.add(track)

            self.racetrack[track] = counter
            track = self.next_track(track)
            counter += 1

    def part1(self):
        self.read_grid()
        self.save_racetrack()

        target_saving = 100

        for track in self.racetrack.keys():
            self.skips(track)

        saves = self.count_greater(target_saving)
        print(f'part1 {saves} @ {target_saving}')
    
    def distance(self, point1, point2):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    def distance_saved(self, point1, point2):
        # calculate savings between 2 points
        cost1 = self.racetrack[point1]
        cost2 = self.racetrack[point2]
        distance = self.distance(point1, point2)

        return cost2 - cost1 - distance

    def part2(self):
        # 2. investigate pairs of points
        # Add all point-pairs to Sh
        # Filter Sh for points that are reachable by Ms
        # For each remaining pair:
        # Calculate shortcut distance Sd
        # calculate Sv (shortcut Value) = P2.Ds - Sd

        target_saving = 100
        cheat_distance = 20

        shortcuts = list(combinations(self.racetrack.keys(), 2))
        reachable_shortcuts = list(filter(
            lambda sh: self.distance(sh[0], sh[1]) <= cheat_distance,
            shortcuts
        ))

        valuable_shortcuts = list(filter(
            lambda sh: self.distance_saved(sh[0], sh[1]) >= target_saving,
            reachable_shortcuts
        ))

        saves = len(valuable_shortcuts)

        print(f'part2 {saves} @ {target_saving}')


if __name__ == '__main__':
    s = Solution()
    s.part1()

    s.part2()

