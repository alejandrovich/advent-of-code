import re
from collections import namedtuple

from readfile import read


Point = namedtuple('Point', ('x', 'y'))
Robot = namedtuple('Robot', ('vector', 'position'))
Vector = namedtuple('Vector', ('x', 'y'))
Floor = namedtuple('Floor', ('w', 'h'))


# file_name = '14_example.txt'
file_name = '14_input.txt'

class Solution:
    robots = None

    def move(self, p, v):
        '''
        item is at point p,
        v is their velocity vector
        return: where they will be after 1 move
        '''
        xnew = p.x + v.x
        ynew = p.y + v.y

        if xnew < 0:
            xnew += self.floor.w
        if xnew >= self.floor.w:
            xnew = xnew % self.floor.w
        if ynew < 0:
            ynew += self.floor.h
        if ynew >= self.floor.h:
            ynew = ynew % self.floor.h
        return Point(xnew, ynew)

    def animate(self, time=0):
        robots = self.robots
        self.robots = []

        for robot in robots:
            new_location = robot.position
            vector = robot.vector
            for t in range(time):
                new_location = self.move(new_location, vector)
                
            new_robot = Robot(vector=vector, position=new_location)
            # self.positions.append(new_robot)
            self.robots.append(new_robot)


    def print_robots(self):
        for robot in self.robots:
            print(robot)

    def print(self, space_char='.'):
        robot_locations = {
            row: sorted(
                r.position.x
                for r in self.robots
                if r.position.y == row
            )
            for row in range(self.floor.h)
        }
        # print(robot_locations)

        for row in range(self.floor.h):
            robots = robot_locations[row]
            line = ''
            for col in range(self.floor.w):
                line += (
                    str(len(list(x 
                        for x in robot_locations[row]
                        if x == col
                    )))
                    if col in robot_locations[row]
                    else space_char
                )
            print(line)

        # self.safety_factor()

    def __init__(self):
        self.floor = Floor(h=103, w=101)
        self.robots = []

        for line in read(file_name):
            match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
            self.robots.append(
                Robot(
                    position=Point(x=int(match.group(1)), y=int(match.group(2))),
                    vector=Vector(x=int(match.group(3)), y=int(match.group(4))),
                )
            )

    def safety_factor(self):
        q1 = [
            r for r in self.robots
            if r.position.x < (self.floor.w - 1) / 2
            and r.position.y < (self.floor.h - 1) / 2
        ]
        q2 = [
            r for r in self.robots
            if r.position.x > (self.floor.w - 1) / 2
            and r.position.y < (self.floor.h - 1) / 2
        ]
        q3 = [
            r for r in self.robots
            if r.position.x < (self.floor.w - 1) / 2
            and r.position.y > (self.floor.h - 1) / 2
        ]
        q4 = [
            r for r in self.robots
            if r.position.x > (self.floor.w - 1) / 2
            and r.position.y > (self.floor.h - 1) / 2
        ]
        sf = len(q1) * len(q2) * len(q3) * len(q4)
        print(sf)


def test1():
    s = Solution()
    robots = s.robots
    # positions = s.positions

    for i in range(len(robots)):
        s.time = 100
        s.robots = [robots[i]]
        # s.positions = [positions[i]]

        s.print_robots()
        s.print()
        s.animate()

        s.print()

        print()

def test2():
    s = Solution()
    s.time = 10
    s.robots = [
        Robot(
            position=Point(x=1, y=1),
            vector=Vector(x=-2, y=1)
        )
    ]
    # positions = [s.robots[0]]
    s.animate()
    s.print()


if __name__ == '__main__':
    s = Solution()
    for i in range(10000):
        s.animate(time=1)
        print(f'seconds elapsed: {i}')
        s.print(space_char=' ')
        # part 2: 8086 (too low)

