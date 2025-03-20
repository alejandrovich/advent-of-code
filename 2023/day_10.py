from text_input import file_line_by_line



class Solution:
    # file_name = '10_example.txt'
    file_name = '10_example2.txt'
    # file_name = '10_input.txt'

    seen = None
    start = None
    distance = None
    moves = None

    def __init__(self):
        self.lines = []
        self.seen = set()
        self.moves = set()

        self.lines = [
            line
            for line in file_line_by_line(self.file_name)
        ]
        self.start = self.find_start()

    def find_start(self):
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line):
                if char == 'S':
                    return x, y
    
    def print_path(self, in_path=True, path_char=None):
        new_lines = []
        for y, line in enumerate(self.lines):
            new_line = []
            for x, char in enumerate(line):
                if in_path is True:
                    if (x, y) in self.seen:
                        if char != 'S':
                            char = char if path_char is None else path_char
                            
                        new_line.append(char)
                    else:
                        new_line.append(' ')
                else:
                    if (x, y) in self.seen:
                        new_line.append(' ')
                    else:
                        new_line.append('O')
            new_lines.append(new_line)

        for i, line in enumerate(new_lines):
            print(''.join(line), i)

    def neighbor_pipes(self, x, y):
        # print(f'Neighbor pipes called with {x, y}')
        # clockwise
        # up neighbor:    F 7 |
        # right neighbor: 7 J -
        # down neighbor:  L J |
        # left neighbor:  F L -

        UP = ['F', '7', '|', 'S']
        RIGHT = ['7', 'J', '-', 'S']
        DOWN = ['L', 'J', '|', 'S']
        LEFT = ['F', 'L', '-', 'S']

        # starting position can be any shape
        # otherwise, ensure pipes can couple
        current_shape = self.get_char(x, y)

        if current_shape in DOWN:
            next_p = self.get_char(x, y - 1)
            if next_p in UP:
                self.moves.add(f'{current_shape}^{next_p}')
                yield x, y - 1

        if current_shape in LEFT:
            next_p = self.get_char(x + 1, y)
            if next_p in RIGHT:
                self.moves.add(f'{current_shape}>{next_p}')
                yield x + 1, y

        if current_shape in UP:
            next_p = self.get_char(x, y + 1)
            if next_p in DOWN:
                self.moves.add(f'{current_shape}!{next_p}')
                yield x, y + 1

        if current_shape in RIGHT:
            next_p = self.get_char(x - 1, y)
            if next_p in LEFT:
                self.moves.add(f'{current_shape}<{next_p}')
                yield x - 1, y

    def get_char(self, x, y):
        if (
            0 <= x < len(self.lines[0]) and
            0 <= y < len(self.lines)
        ):
            return self.lines[y][x]

    def print(self):
        print(f'Start {self.start}')
        for line in self.lines:
            print(line)

    def part1(self):
        # From starting position, find all pipe connected to it

        # loop until reach another seen node
        # track distance at each loop

        self.print()

        unseen_pipes = [self.start]
        distance = 0

        while unseen_pipes:
            distance += 1

            self.seen.update(unseen_pipes)
            next_pipes = set()

            # add all the next points
            for point in unseen_pipes:
                tuple(map(next_pipes.add, self.neighbor_pipes(*point)))

                # possible_next = tuple(self.neighbor_pipes(*point))
                # for p in possible_next:
                #     print(f'poss_next {self.get_char(*p)} ({p}) from ({point})')
                tuple(map(next_pipes.add, self.neighbor_pipes(*point)))

            # filter possible next pipes to those not yet visited
            next_pipes -= self.seen

            unseen_pipes = next_pipes
            # print(f'seen {self.seen}')
            # print(f'unseen_pipes {unseen_pipes}')
            # print(f'distance {distance}')
            # print()


        return distance - 1

'''
Symbols with current
Flow determination algo:

<         >     <
-   ^|v   7v   vF   Jv   vL
>                   <     >
'''
# flow is the *OUTSIDE* "handedness" of direction
# direction (the input to if/else) is the way the path is being traced
# "exit direction" (i.e. how to leave the shape)
# will inform the "handedness" of the encountered flow

if symbol == '-' and path_direction == RIGHT:
    flow = 
if symbol == '-' and path_direction == LEFT:
    flow = RIGHT
if symbol == '|' and path_direction == UP:


        def flow_traversal():
            # for every point we want to know if in/out:

            # calculate the distances to each map edge (up, down, left, right)
            # head towards the nearest boundary

            # when encountering a path character
            # Save the location and direction-of-entry
            # nothing to do while on a path location
            # at path exit, save location and direction of entry
            # Trace the path



if __name__ == '__main__':
    s = Solution()
    answer = s.part1()
    print('answer', answer)
    s.print_path()
    s.print_path(in_path=True, path_char='.')
    

