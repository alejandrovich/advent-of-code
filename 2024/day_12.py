import cProfile
import pstats

from collections import defaultdict, namedtuple
from itertools import chain
from typing import List


# file_name = '12_example.txt'
file_name = '12_input.txt'


Point = namedtuple('Point', ('x', 'y'))


def outside(point):
    right = Point(point.x + 1, point.y)
    down = Point(point.x, point.y + 1)
    left = Point(point.x - 1, point.y) if point.x > 0 else None
    up = Point(point.x, point.y - 1) if point.y > 0 else None

    return set(filter(bool, (right, down, left, up)))

def edges(point):
    return set((
        Point(point.x + 1, point.y),
        Point(point.x, point.y + 1),
        Point(point.x - 1, point.y),
        Point(point.x, point.y - 1),
    ))

def ups(points):
    return {
        Point(point.x, point.y - 1)
        for point in points
    }
def rights(points):
    return {
        Point(point.x + 1, point.y)
        for point in points
    }
def downs(points):
    return {
        Point(point.x, point.y + 1)
        for point in points
    }

def lefts(points):
    return {
        Point(point.x - 1, point.y)
        for point in points
    }

class Region:
    points = None
    name = None
    _area: int = None
    _perimiter: int = None
    intersection: List[Point] = None

    @property
    def perimiter(self):
        if self._perimiter is None:
            self._perimiter = sum(
                len(
                    list(
                        edge
                        for edge in edges(p)
                        if edge not in self.points
                    )
                )
                for p in self.points
            )
        return self._perimiter

    @property
    def area(self):
        if self._area is None:
            self._area = len(self.points)
        return self._area

    def _recalc(self):
        self._perimiter = None  # optimistic recalc

        self._area = None

        self.intersection = set(
            chain(
                (
                    outside_point 
                    for p in self.points
                    for outside_point in outside(p)
                ),
                self.points
            )
        )

    def __init__(self, points, name):
        self.points = points
        self.name = name
        self._recalc()

    def combine(self, new_points):
        self.points += new_points
        self._recalc()

    @property
    def sides(self):
        # get all the edges by direction
        # 4 sets (up, down, left, right)
        # count the regions the points will coalesce into

        right_regions = set()
        all_rights = rights(self.points) - set(self.points)
        for point in all_rights:
            region = Region(name='R', points=[point])
            combine_region(region, right_regions)

        left_regions = set()
        all_lefts = lefts(self.points) - set(self.points)
        for point in all_lefts:
            region = Region(name='L', points=[point])
            combine_region(region, left_regions)

        up_regions = set()
        all_ups = ups(self.points) - set(self.points)
        for point in all_ups:
            region = Region(name='U', points=[point])
            combine_region(region, up_regions)

        down_regions = set()
        all_downs = downs(self.points) - set(self.points)
        for point in all_downs:
            region = Region(name='D', points=[point])
            combine_region(region, down_regions)

        return sum((
            len(right_regions),
            len(left_regions),
            len(up_regions),
            len(down_regions),
        ))

    def __repr__(self):
        # return f'{self.name}(Area {self.area}, Per {self.perimiter} {self.sides}) {list(p for p in self.points)}'
        return f'{self.name}(Area {self.area}, Per {self.perimiter} {self.sides})'

def combine_region(region, all_regions):
    combined_region = set()

    for r in all_regions:
        if (
            r.intersection.intersection(set(region.points)) and
            r.name == region.name
        ):
            r.combine(region.points)
            combined_region = r
            break

    if not combined_region:
        # found no matches for region
        all_regions.add(region)
    else:
        # see if new region combines with any existing
        all_regions.remove(combined_region)
        combine_region(combined_region, all_regions)

class Solution:
    regions = None
    mapa = None

    def __init__(self):
        self.mapa = []
        self.regions = set()

        with open(file_name, "r") as f:
            for line in f:
                self.mapa.append(line.rstrip('\n'))

        for y, line in enumerate(self.mapa):
            for x, char in enumerate(line):
                # make a region
                # combine it with existing regions
                p = Point(x, y)
                region = Region(name=char, points=[p])

                combine_region(region, self.regions)

    def print(self):
        for line in self.mapa:
            print(line)

        for r in sorted(self.regions, key=lambda r: r.name):
            print(r)
            print()

    @property
    def cost(self):
        cost = sum(
            r.area * r.perimiter
            for r in self.regions
        )
        return cost

    @property
    def bulk_cost(self):
        cost = sum(
            r.area * r.sides
            for r in self.regions
        )
        return cost


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    s = Solution()


    # s.print()
    print(f'part1: {s.cost}')

    print(f'part2: {s.bulk_cost}')

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(10)  # Print top 10 functions by cumulative time


if __name__ == '__main__':
    main()

