from math import floor, ceil
import math
import re
import functools
import text_input


# file_name = 'day_06_example_input.txt'
file_name = 'day_06_input.txt'

def part1():
    lines = [
        line for line in text_input.file_line_by_line(file_name)
    ]
    print(lines)
    if 'example' in file_name:
        match = re.search(r'Time:\s+(\d+)\s+(\d+)\s+(\d+)', lines[0])
        times = tuple(int(i) for i in (match.group(1), match.group(2), match.group(3)))
    else:
        match = re.search(r'Time:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[0])
        times = tuple(int(i) for i in (match.group(1), match.group(2), match.group(3), match.group(4)))
    print(times)

    if 'example' in file_name:
        match = re.search(r'Distance:\s+(\d+)\s+(\d+)\s+(\d+)', lines[1])
        dists = tuple(int(i) for i in (match.group(1), match.group(2), match.group(3)))
    else:
        match = re.search(r'Distance:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[1])
        dists = tuple(int(i) for i in (match.group(1), match.group(2), match.group(3), match.group(4)))
    print(dists)

    race_results = {}
    for i, race in enumerate(times):
        to_beat = dists[i]

        wins = 0
        for press_time in range(race + 1):
            result = (race - press_time) * press_time

            if result > to_beat:
                print(f'hold for {press_time} goes {result}')
            wins += 1 if result > to_beat else 0

        race_results[i] = wins

    print(race_results)
    print(functools.reduce(lambda a, b: a * b, race_results.values()))


def part2():
    lines = [
        line for line in text_input.file_line_by_line(file_name)
    ]
    if 'example' in file_name:
        match = re.search(r'Time:\s+(\d+)\s+(\d+)\s+(\d+)', lines[0])
        race_time = int(''.join((match.group(1), match.group(2), match.group(3))))
    else:
        match = re.search(r'Time:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[0])
        race_time = int(''.join((match.group(1), match.group(2), match.group(3), match.group(4))))

    if 'example' in file_name:
        match = re.search(r'Distance:\s+(\d+)\s+(\d+)\s+(\d+)', lines[1])
        distance = int(''.join((match.group(1), match.group(2), match.group(3))))
    else:
        match = re.search(r'Distance:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[1])
        distance = int(''.join((match.group(1), match.group(2), match.group(3), match.group(4))))

    print('time', race_time)
    print('distance', distance)

    # what is the formula?
    # 0 = (p*r - p^2) - distance
    # ax^2 + bx + c
    # -b +- sqrt(b^2 - (4.a.c)) / 2a

    # distance = (race_time - press_time) * press_time
    # distance = race_time * press_time - press_time * press_time
    # 0 = -press_time ^ 2 + racetime * press_time - distance
    a = -1
    b = race_time
    c = -1 * distance

    print('abc', a, b, c)
    one = (-1 * b + math.sqrt(b * b - (4 * a * c))) / ( 2 * a )
    two = (-1 * b - math.sqrt(b * b - (4 * a * c))) / ( 2 * a )
    print('one', one)
    print('two', two)
    print(ceil(one), floor(two))
    print(floor(two) - (ceil(one) - 1))

part1()
# too low: 5746
# too low: 28730

part2()
# too high: 41667266

