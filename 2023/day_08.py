import re
from functools import reduce

from text_input import file_line_by_line


END_NODE_NAME = 'ZZZ'

class Node:
    name = None
    paths = None

    def __init__(self, name, left_path, right_path):
        self.name = name
        self.paths = {'L': left_path, 'R': right_path}

    def get_next(self, direction):
        return self.paths[direction]


class Solution:
    # file_name = '08_example.txt'
    # file_name = '08_ex2.txt'
    file_name = '08_input.txt'

    directions = ''
    direction_length = 0
    network = None

    def __init__(self):
        self.network = {}
        self.read_input()

    def read_input(self):
        for i, line in enumerate(file_line_by_line(self.file_name)):
            if i == 0:
                self.directions = line
                self.directions_length = len(self.directions)
                print(f'{self.directions} have {self.directions_length} routes')
            elif i == 1:
                # blank line between directions and nodes
                pass
            else:
                # match = re.search(r'(\w\w\w) = \(\w\w\w\)\, \(\w\w\w\)', line)
                match = re.search(r'(\w\w\w) = \((\w\w\w), (\w\w\w)\)', line)

                name = match.group(1)
                left = match.group(2)
                right = match.group(3)

                node = Node(name, left, right)

                self.network[name] = node

    def get_next_direction(self, position):
        next_position = position

        # compare position (0-based) to 0-based length
        if position > (self.directions_length - 1):
            next_position = position % self.directions_length

            # print(f'wrapping at {position} to {next_position}')

        return self.directions[next_position]


    def follow_directions(self):
        current = self.network['AAA']

        # print(self.directions)
        distance = 0
        route = self.directions[distance]

        while distance < 100000:
            if current.name == END_NODE_NAME:
                return distance

            next_name = current.get_next(route)
            # print(f'{distance} -> {route} from {current.name} to {next_name}')

            current = self.network[next_name]
            distance += 1
            route = self.get_next_direction(distance)

        raise ValueError(f'took too long! ({distance})')

    def is_at_end(self, node_names):
        return all(
            node_name[-1] == 'Z'
            for node_name in node_names
        )


    def follow_complicated_directions(self):
        # get starting nodes (nodes ending with A)
        # traverse them
        # check if ending condition

        current_node_names = [
            node_name
            for node_name in self.network.keys()
            if node_name[-1] == 'A'
        ]
        starting_node_names = current_node_names
        distance = 0
        route = self.directions[distance]

        seen_positions = {''.join(current_node_names)}

        print(f'{seen_positions} out of {len(self.network.keys())} seen')

        print(f'{current_node_names}')

        while distance < 10000000:
            # ending condition: all nodes end with 'Z'
            is_at_end = self.is_at_end(current_node_names)
            if is_at_end:
                return distance

            m = tuple(
                distance if name[-1] == 'Z' else 0
                for name in current_node_names
            )
            if any(d > 0 for d in m):
                print(m)


            # retrieve the current nodes by name
            current_nodes = [
                self.network[node_name]
                for node_name in current_node_names
            ]

            # traverse all current nodes
            current_node_names = [
                node.get_next(route)
                for node in current_nodes
            ]

            # debugging non-termination
            smashed_names = ''.join(current_node_names)
            if smashed_names in seen_positions:
                raise ValueError(f'{smashed_names} has a cycle')
            seen_positions.add(smashed_names)


            # print(f'{current_node_names} {current_node_names == starting_node_names}')

            # set variable(s)
            distance += 1
            route = self.get_next_direction(distance)

        raise ValueError(f'took too long! ({distance})')


def part1():
    s = Solution()
    distance = s.follow_directions()
    print(f'Part 1 took {distance} hops')
    print()


def test_is_at_end():
    s = Solution()
    nodes = ['JHA', 'NCA', 'MMA', 'AAA', 'TVA', 'DTA']
    print(f'{s.is_at_end(nodes)} for {nodes}')

    nodes = ['JHZ', 'NCZ', 'MMZ', 'ZZZ', 'TVZ', 'DTZ']
    print(f'{s.is_at_end(nodes)} for {nodes}')
    print()


def part2():
    s = Solution()
    distance = 0
    distance = s.follow_complicated_directions()
    print(f'Part 2 took {distance} hops')


def factorize(n):
    prime_numbers = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541)

    number = n
    found = []
    while number > 1:
        for p in prime_numbers:
            if 0 == number % p:
                # print(f'{n} is divisible by {p}')
                number = number / p
                found.append(p)

    return found


def lcm(n, m):
    n_factors = factorize(n)
    m_factors = factorize(m)
    common_factors = set(n_factors).intersection(set(m_factors))

    n_solo_factors = set(n_factors).difference(common_factors)
    m_solo_factors = set(m_factors).difference(common_factors)

    combined_factors = list(n_solo_factors) + list(m_solo_factors) + list(common_factors)

    return reduce(lambda a, b: a * b, combined_factors)


def test_factorize():
    '''
    (0, 13019, 0, 0, 0, 0)
    (0, 0, 0, 0, 0, 14681)
    (0, 0, 0, 16343, 0, 0)
    (0, 0, 0, 0, 18559, 0)
    (0, 0, 19667, 0, 0, 0)
    (21883, 0, 0, 0, 0, 0)
    '''

    print(factorize(13019))
    print(factorize(14681))
    print(factorize(16343))
    print(factorize(18559))
    print(factorize(19667))
    print(factorize(21883))
    cycles = [
        13019,
        14681,
        16343,
        18559,
        19667,
        21883,
    ]
    print(reduce(lambda a, b: lcm(a, b), cycles))


if __name__ == '__main__':
    part1()
    test_is_at_end()
    test_factorize()
    print(lcm(13019, 14681))
    # part2()

