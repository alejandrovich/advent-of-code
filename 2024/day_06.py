from itertools import combinations
from collections import namedtuple, defaultdict

from readfile import read

Point = namedtuple('Point', ('x', 'y'))


UP, DOWN, RIGHT, LEFT = '^', 'v', '>', '<'



class Solution:
    file_name = '06_example.txt'
    # file_name = '06_input.txt'

    area = None
    obstacles = None
    start = None
    initial_direction = None
    visited = defaultdict(list)  # point : direction-of-travel as we've passed


    def __init__(self):
        self.area = []
        self.obstacles = set()
        self.bounces = []  # list of obstacles actually encountered

        for y, line in enumerate(read(self.file_name)):
            self.area.append([c for c in line])
            for x, char in enumerate(line):
                if char in '<>^v':
                    self.start = Point(x, y)
                    self.initial_direction = self.cursor_direction(self.start)
                if char in '#':
                    self.obstacles.add(Point(x, y))

        self.xmax = len(self.area[0]) - 1
        self.ymax = len(self.area) - 1

    def print(self):
        for line in self.area:
            print(''.join(line))

    def char(self, point):
        try:
            return self.area[point.y][point.x]
        except:
            print(f'Error at {point}')
            raise

    @staticmethod
    def vector(direction):
        if direction == UP:
            return (0, -1)
        if direction == DOWN:
            return (0, 1)
        if direction == RIGHT:
            return (1, 0)
        if direction == LEFT:
            return (-1, 0)

    def peek(self, location: Point, direction):
        # return the next character in the given direction
        # special case, return None when guard goes off the screen
        offset = self.vector(direction)

        next_coord = Point(location.x + offset[0], location.y + offset[1])

        if 0 <= next_coord.x <= self.xmax and 0 <= next_coord.y <= self.ymax:
            return next_coord
        else:
            return None

    def turn(self, current_direction):
        if current_direction == UP:
            return RIGHT
        if current_direction == RIGHT:
            return DOWN
        if current_direction == DOWN:
            return LEFT
        if current_direction == LEFT:
            return UP

    def next_point(self, location, direction):
        possible_next = self.peek(location, direction)

        while True:
            # punt handling out-of-area to caller
            if not possible_next:
                return None, direction

            char = self.char(possible_next)
            if char in '#':  # in case there's more obstacles later
                # record the hitting of the obstacle
                self.bounces.append(possible_next)
                direction = self.turn(direction)
                possible_next = self.peek(location, direction)
            else:
                # record the passing of this point
                self.visited[possible_next].append(direction)

                # the next point
                return possible_next, direction

    def cursor_direction(self, point):
        char = self.char(point)
        if char == '^':
            return UP
        if char == '<':
            return LEFT
        if char == '>':
            return RIGHT
        if char == 'v':
            return DOWN

    def part1(self):
        self.print()

        location = self.start
        direction = self.initial_direction
        in_room = True
        steps = {location}


        while in_room:
            location, direction = self.next_point(location, direction)

            if location:
                steps.add(location)

            in_room = location is not None

        return len(steps)

    def part2(self):
        self.print()

        location = self.start
        direction = self.initial_direction
        in_room = True
        steps = {location}
        loops = 0  # store the count of loops

        print(
            f'{len(self.bounces)} obstacles encountered {self.bounces}',
            f'(out of {len(self.obstacles)})',
        )
        # clear bounce history
        self.bounces = []

        while in_room:
            location, direction = self.next_point(location, direction)

            if location:
                steps.add(location)
                can_loop = self.check_box(location)
                x_loop = self.check_perpendicular_path(location, direction)

                if x_loop or can_loop:
                    loops += 1

            in_room = location is not None

        return print(f'Part 2: Loops={loops}')

    def check_box(self, location):
        if len(self.bounces) < 3:
            return False

        # last 3 bounces
        obstacles = self.bounces[-3:] + [location]
        is_box = self.is_box(obstacles)
        print(is_box, location)

        return is_box

    def is_box(self, obstacles):
        '''
        description of 4 obstacles that sentry would loop on forever
        A
             B

       C
            D

        Order by Y coord
        A.y == B.y - 1
        A.x == C.x + 1
        C.y == D.y - 1
        B.x == D.x + 1
        B.x > A.x
        smallest y is 1 smaller than next smallest
        '''
        A, B, C, D = sorted(obstacles, key=lambda p: p.y)
        box_check = all((
            A.y == B.y - 1,
            A.x == C.x + 1,
            C.y == D.y - 1,
            B.x == D.x + 1,
            B.x > A.x,
        ))

        return box_check

    def check_perpendicular_path(self, point, direction):
        '''
        successful perpendicular crossings are
        up->right
        right->down
        down->left
        left->up
        '''
        perpendiculars = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
        perpendicular_crossing = (
            # current direction mapped to direction of interest
            perpendiculars[direction] in self.visited[point]
        )
        if perpendicular_crossing:
            print(f'located crossing @ {point}')
        return perpendicular_crossing

if __name__ == '__main__':
    s = Solution()
    steps = s.part1()
    print(steps)
    print()

    new_obs = s.part2()
    print(new_obs)

