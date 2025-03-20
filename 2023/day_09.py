from text_input import file_line_by_line


class Solution:
    # file_name = '09_example.txt'
    file_name = '09_input.txt'

    def __init__(self):
        self.lines = list(file_line_by_line(self.file_name))

    def part1(self):
        # read a line of input
        # e.g. 0 3 6 9 12 15

        # calculate the next_array (i - j)
        # save next_array
        # e.g. 3 3 3 3 3
        # then  0 0 0 0

        # loop above while sum(next_array) != 0

        # calculate last element for prior_array

        # Add last element of last 2 arrays and append it to 2nd array

        # loop back up the stack of arrays, calculating new last element

        inputs = []
        for line in self.lines:
            inputs.append(list(map(int, line.split())))

        for line in inputs:
            next_array = line

            all_are_0 = all(i == 0 for i in next_array)
            partial_arrays = [next_array]

            while not all_are_0:
                next_array = [
                    next_array[i] - next_array[i - 1]
                    for i in range(1, len(next_array))
                ]

                partial_arrays.append(next_array)
                all_are_0 = all(i == 0 for i in next_array)

            for i in range(len(partial_arrays) - 1, 0, -1):
                a = partial_arrays[i - 1]
                b = partial_arrays[i]
                a.append(a[-1] + b[-1])
                print(i, a)

        for a in inputs:
            print(a)
        return sum(a[-1] for a in inputs)

    def part2(self):
        # read a line of input
        # e.g. 0 3 6 9 12 15

        # calculate the next_array (i - j)
        # save next_array
        # e.g. 3 3 3 3 3
        # then  0 0 0 0

        # loop above while sum(next_array) != 0

        # calculate first element for prior_array
        # Add first element of last 2 arrays and insert it to 2nd array

        # loop back up the stack of arrays, calculating new first element

        inputs = []
        for line in self.lines:
            inputs.append(list(map(int, line.split())))

        for line in inputs:
            next_array = line

            all_are_0 = all(i == 0 for i in next_array)
            partial_arrays = [next_array]

            while not all_are_0:
                next_array = [
                    next_array[i] - next_array[i - 1]
                    for i in range(1, len(next_array))
                ]

                partial_arrays.append(next_array)
                all_are_0 = all(i == 0 for i in next_array)

            for i in range(len(partial_arrays) - 1, 0, -1):
                a = partial_arrays[i - 1]
                b = partial_arrays[i]
                print('checking', a, b)
                a.insert(0, a[0] - b[0])
                print(i, a)

        for a in inputs:
            print(a)
        return sum(a[0] for a in inputs)


if __name__ == '__main__':
    s = Solution()
    p1 = s.part1()
    print(p1)
    print()
    # too high: 1873333168
    # answer: 1868368343

    p2 = s.part2()
    print(p2)
    # too high: 1910


