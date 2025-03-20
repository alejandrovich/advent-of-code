from itertools import chain
from collections import defaultdict, namedtuple

from readfile import read


# file_name = '15_example.txt'
file_name = '15_input.txt'

Point = namedtuple('Point', ('x', 'y'))
Box = namedtuple('Box', ('id', 'points'))
UP, RIGHT, DOWN, LEFT = '^', '>', 'v', '<'
VECTORS = {
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0)
}


class Solution:
    moves = None
    walls = None
    boxes = None
    position = None
    xmax = None
    ymax = None
    xmax_big = None

    def next(self, position, direction):
        vector = VECTORS[direction]

        return Point(
            position.x + vector[0],
            position.y + vector[1],
        )

    def move(self, direction):
        # peek at next position
        peek_point = self.next(self.position, direction)

        # EMPTY: move cursor
        if peek_point in self.spaces:
            self.spaces.add(self.position)
            self.position = peek_point
            self.spaces.remove(peek_point)

        # WALL: cursor unchanged
        elif peek_point in self.walls:
            pass

        # BOX: search direction
        elif peek_point in self.boxes:
            while peek_point in self.boxes:
                peek_point = self.next(peek_point, direction)
            if peek_point in self.walls:
                pass
            else:
                # must have been empty
                # move cursor to next direction 
                new_cursor = self.next(self.position, direction)
                self.spaces.add(self.position)
                self.position = new_cursor
                self.boxes.remove(new_cursor)

                self.boxes.add(peek_point)
                self.spaces.remove(peek_point)

    def parse_warehouse(self, y: int, line: str) -> None:
        print(line)
        for x, char in enumerate(line):
            p = Point(x, y)
            if char == '.':
                self.spaces.add(p)
            elif char == '#':
                self.walls.add(p)
            elif char == '@':
                self.position = p
            elif char == 'O':
                self.boxes.add(p)
            else:
                raise Exception('unexpected char type')

    def parse_warehouse_big(self, y: int, line: str) -> None:
        box_id = max(box.id for box in self.boxes) + 1 if self.boxes else 0
        for x, char in enumerate(line):
            position = x * 2
            p1 = Point(position, y)
            p2 = Point(position + 1, y)

            if char == '.':
                self.spaces.add(p1)
                self.spaces.add(p2)
            elif char == '#':
                self.walls.add(p1)
                self.walls.add(p2)
            elif char == '@':
                self.position = p1
                self.spaces.add(p2)
            elif char == 'O':
                self.boxes.add(
                    Box(box_id, (Point(position, y), Point(position + 1, y)))
                )
                box_id += 1
            else:
                raise Exception('unexpected char type')

    def init_warehouse(self):
        for y, line in enumerate(read(file_name)):
            if line.startswith('#'):
                self.parse_warehouse(y, line)
                self.ymax += 1
                self.xmax = len(line)
            else:
                self.moves += line
        print()
        self.print()
        self.print_moves()

    def init_warehouse_big(self):
        self.__init__()

        for y, line in enumerate(read(file_name)):
            if line.startswith('#'):
                self.parse_warehouse_big(y, line)
                self.ymax += 1
                self.xmax_big = len(line) * 2
            else:
                self.moves += line

        print()
        self.print_big()
        self.print_moves()

    def __init__(self):
        self.walls = set()
        self.boxes = set()
        self.spaces = set()
        self.moves = ''
        self.ymax = 0
        self.xmax = 0
        self.xmax_big = 0

    def print_moves(self):
        print(self.moves)
        print()

    def print(self):
        for y in range(self.ymax):
            line = ''
            for x in range(self.xmax):
                p = Point(x, y)
                if p in self.spaces:
                    line += ' '
                if p in self.walls:
                    line += '|'
                if p == self.position:
                    line += '*'
                if p in self.boxes:
                    line += 'o'
            print(line)

        print()

    def print_big(self):
        boxes_left = {
            box.points[0]:  box
            for box in self.boxes
        }
        for y in range(self.ymax):
            line = ''
            for x in range(self.xmax_big):
                p = Point(x, y)
                if p in self.spaces:
                    line += '.'
                if p in self.walls:
                    line += '#'
                if p == self.position:
                    line += '@'
                if p in boxes_left.keys():
                    # line += f'{boxes_left[p].id:02}'
                    line += '[]'

            print(line)

        print()

    def calculate_warehouse_hash(self):
        wh_hash = sum(
            p.x + p.y * 100
            for p in self.boxes
        )
        return wh_hash

    def calculate_warehouse_hash_big(self):
        wh_hash = 0
        for box in self.boxes:
            left_point = sorted(box.points, key=lambda p: p.x)[0]
            wh_hash += left_point.x + (left_point.y * 100)

        return wh_hash

    def part1(self):
        self.init_warehouse()
        move_count = len(self.moves)

        for i in range(move_count):
            self.move(self.moves[i])

        self.print()
        print('part1', self.calculate_warehouse_hash())

    def get_boxes(self, points):
        # return list of boxes that occupy the provided points
        box_segments = set(
            chain.from_iterable(
                box.points for box in self.boxes
                if set(box.points) & points
            )
        )
        overlapping_boxes = set(
            box for box in self.boxes
            if set(box.points) & box_segments
        )
        return overlapping_boxes

    def arrange_box(self, box, direction):
        pre_occupied_points = set(box.points)
        post_occupied_points = {
            self.next(box.points[0], direction),
            self.next(box.points[1], direction),
        }
        new_box = Box(box.id, points=tuple(post_occupied_points))
        self.boxes.remove(box)
        self.boxes.add(new_box)

        # free-up (a) previously occupied space
        freed_points = pre_occupied_points - post_occupied_points
        self.spaces = self.spaces - post_occupied_points
        self.spaces = self.spaces | freed_points

    def move_box(self, box, direction):
        # the set of points where the box will next occupy
        spaces_needed = {
            self.next(point, direction)
            for point in box.points
        }
        # if moving sideways, some points are already known to be free
        spaces_needed -= set(box.points)

        # if any destination is a wall, fail
        if spaces_needed & self.walls:
            return False

        boxes_to_move = self.get_boxes(spaces_needed)
        # if any boxes in the needed spaces, recurse to move it
        if boxes_to_move:
            if not all(self.move_box(m_box, direction) for m_box in boxes_to_move):
                return False

        self.arrange_box(box, direction)

        return True

    def move_robot(self, direction):
        target_destination = self.next(self.position, direction)
        boxes_at_destination = self.get_boxes({target_destination})

        if target_destination in self.walls:
            return
        elif boxes_at_destination:
            if not all(
                self.move_box(box, direction)
                for box in boxes_at_destination
            ):
                return

        new_position = target_destination
        self.spaces.add(self.position)
        self.spaces = self.spaces - {new_position}
        self.position = new_position

    def box_by_id(self, id):
        return [b for b in self.boxes if b.id == id][0]

    def display_move(self, direction, count=None):
        self.move_robot(direction)
        print(f'MOVED: {direction} {count if count is not None else ""}')
        self.print_big()

    def test_movements(self):
        print(f'START')
        self.print_big()

        self.display_move(LEFT)
        self.display_move(DOWN)
        self.display_move(LEFT)
        self.display_move(UP)
        self.display_move(LEFT)
        self.display_move(LEFT)
        self.display_move(LEFT)
        self.display_move(UP)
        self.display_move(UP)
        self.display_move(UP)
        self.display_move(RIGHT)
        self.display_move(DOWN)
        self.display_move(DOWN)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(RIGHT)
        self.display_move(DOWN)
        self.display_move(DOWN)
        self.display_move(DOWN)
        self.display_move(DOWN)

    def part2(self):
        print('BEGIN PART 2')

        self.init_warehouse_big()

        for move_number, direction in enumerate(self.moves):
            self.display_move(direction, count=move_number)

        self.print_big()
        calc_hash = self.calculate_warehouse_hash_big()

        # too high: 1561281
        print('part2', calc_hash)


if __name__ == '__main__':
    s = Solution()
    s.part1()
    s.part2()

