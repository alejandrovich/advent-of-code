import re
from collections import namedtuple

from text_input import file_line_by_line


file_name = '02_input.txt'
Game = namedtuple('Game', ('id', 'red', 'green', 'blue'))

red_cubes, green_cubes, blue_cubes = 12, 13, 14


def get_color(color, roll):
    match = re.search(rf'(\d+) {color}', roll)
    count = int(match.group(1)) if match else 0
    print(f'found {count} {color}')
    return count

def part1():
    possible_game_ids = []

    for l in file_line_by_line(file_name):
        print(l)
        match = re.search(r'Game (\d+): (.*)$', l)
        roll_check = []

        # create a game
        game_id = int(match.group(1))
        rolls = match.group(2).split(';')

        for roll_num, roll in enumerate(rolls):
            greens = get_color('green', roll)
            reds = get_color('red', roll)
            blues = get_color('blue', roll)

            # test game against rules
            roll_result = all((
                (greens <= green_cubes),
                (reds <= red_cubes),
                (blues <= blue_cubes)
            ))
            print(f'{game_id} roll {roll_num} {roll_result}')
            roll_check.append(roll_result)

        # save matching game(s)
        if all(roll_check):
            possible_game_ids.append(game_id)
        print(possible_game_ids)

        print()

    return sum(possible_game_ids)

def part2():
    powers = []

    for l in file_line_by_line(file_name):
        print(l)
        match = re.search(r'Game (\d+): (.*)$', l)
        red_max, blue_max, green_max = 0, 0, 0

        # create a game
        game_id = int(match.group(1))
        rolls = match.group(2).split(';')

        for roll_num, roll in enumerate(rolls):
            greens = get_color('green', roll)
            reds = get_color('red', roll)
            blues = get_color('blue', roll)

            # save the largest cube counts from each row
            if greens > green_max:
                green_max = greens
            if reds > red_max:
                red_max = reds
            if blues > blue_max:
                blue_max = blues

        # compute the power
        cube_power = green_max * blue_max * red_max
        powers.append(cube_power)
        print(powers)

        print()

    return sum(powers)

p1 = part1()
# too high: 14403

p2 = part2()

print(f'part1 {p1}')
print(f'part2 {p2}')

