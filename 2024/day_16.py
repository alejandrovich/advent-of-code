import math
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List

from readfile import read


# location, current (x, y) place on the map
# direction, which way is being faced
# cost, score accumulated so far (lower is better)
State = namedtuple('State', ('location', 'direction', 'cost', 'path'))
Point = namedtuple('Point', ('x', 'y'))


# file_name = '16_example.txt'
# file_name = '16_example2.txt'
file_name = '16_example3.txt'
# file_name = '16_input.txt'

UP, RIGHT, DOWN, LEFT = '^', '>', 'v', '<'

class Solution:
    # overall process

    # save the initial state (location, direction)
    # at each point, examine the options
    # calculate the cost of each possible action
    # choose the lowest-cost action
    
    def reachable(self, state: State):
        current_cost = state.cost
        visited = state.path + [state.location]

        neighbor_points = [
            State(
                Point(state.location.x, state.location.y - 1), 
                UP,
                1 if state.direction == UP else 1001,
                []
            ),
            State(
                Point(state.location.x, state.location.y + 1),
                DOWN, 
                1 if state.direction == DOWN else 1001,
                []
            ),
            State(
                Point(state.location.x - 1, state.location.y),
                LEFT,
                1 if state.direction == LEFT else 1001,
                []
            ),
            State(
                Point(state.location.x + 1, state.location.y),
                RIGHT,
                1 if state.direction == RIGHT else 1001,
                []
            ),
        ]

        # mark new location seen
        unvisited_locations = [
            State(
                point_cost.location, 
                point_cost.direction, 
                current_cost + point_cost.cost,
                state.path + [point_cost.location],
            )
            for point_cost in neighbor_points
            if point_cost.location not in self.walls
            and point_cost.location not in visited
        ]

        return unvisited_locations

    def choices(self, state: State):
        possible = self.reachable(state)
        for p in possible:
            self.options.append(p)
        # print('Unvisited', self.options)

    def __init__(self):
        initial_direction = '>'
        self.walls = set()
        self.options = None
        self.width = 0
        self.height = 0
        self.start = None
        self.end = None
        self.paths = 0
        self.state_paths = {}

        for y, line in enumerate(read(file_name)):
            for x, char in enumerate(line):
                self.width = len(line)
                p = Point(x, y)
                if char == 'S':
                    initial_state = State(p, RIGHT, 0, [])
                    self.start = p
                elif char == '#':
                    self.walls.add(p)
                elif char == 'E':
                    self.end = p
            self.height = y + 1

        self.options = [initial_state]  # ideally options is a BST

    def lowest(self):
        l = min(self.options, key=lambda s: s.cost)

        # remove l from self.options
        # this is where a tree would be best

        self.options = [
            option for option in self.options
            if option != l
        ]

        return l

    def print(self, current_location: State):
        print(f'{self.height} X {self.width}')
        print(current_location)

        for y in range(self.height):
            line = ''
            for x in range(self.width):
                p = Point(x, y)
                if p in self.walls:
                    line += '#'
                elif p == current_location.location:
                    line += 'X'
                elif p in current_location.path:
                    line += '-'
                elif p == self.end:
                    line += 'E'
                elif p == self.start:
                    line += 'S'
                else:
                    line += '.'
            print(line)
        print()

    def has_lower_options(self, lowest_cost):
        return bool(list(
            option for option in self.options
            if option.cost <= lowest_cost
        ))

    def seek(self):
        # get minimum cost choice
        lowest_path = []
        lowest_cost = math.inf

        current_state = self.lowest()

        while len(lowest_path) == 0 or self.has_lower_options(lowest_cost):
            # self.print(current_state)

            self.choices(current_state)
            current_state = self.lowest()

            if current_state.location == self.end:
                if current_state.cost <= lowest_cost:
                    lowest_cost = current_state.cost
                    lowest_path.append(current_state)
                    self.paths += 1

                current_state = self.lowest()

        print('Complete', lowest_cost)
        print('Total paths', self.paths)

        for s in lowest_path:
            m = State(s.location, s.direction, s.cost, path=len(s.path))
            print(m)
        

if __name__ == '__main__':
    s = Solution()
    print('initial state', s.options)


    print()
    s.seek()
    # print(s.options)
