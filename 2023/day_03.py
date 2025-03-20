import re
from collections import namedtuple

import text_input

PartNumber = namedtuple('PartNumber', ('number', 'start', 'end', 'bounds'))
Symbol = namedtuple('Symbol', ('number', 'start', 'end', 'bounds', 'line_number'))


def parse_symbols(line, line_number):
    match = re.finditer(r'([^\d\.])', line)
    return [
        Symbol(
            number=m.group(), 
            start=m.start(), 
            end=m.end(), 
            bounds={
                i for i in range(m.start() - 1, m.end() + 1)
            },
            line_number=line_number
        )
        for m in match
    ]

def parse_numbers(line):
    match = re.finditer(r'(\d+)', line)
    return [
        PartNumber(int(m.group()), m.start(), m.end(), bounds={
            i for i in range(m.start(), m.end())
        })
        for m in match
    ]


def get_overlaps(symbol, numbers):
    return [
        n.number
        for n in numbers
        if n.bounds.intersection(symbol.bounds)
    ]


def get_symbol_overlaps(symbol, lines):
    line_num = symbol.line_number

    if line_num - 1 in lines.keys():
        up_line = lines[line_num - 1]

    curr_line = lines[line_num]

    if line_num + 1 in lines.keys():
        down_line = lines[line_num + 1]

    overlaps = (
        get_overlaps(
            symbol=symbol,
            numbers=parse_numbers(up_line),
        ) + get_overlaps(
            symbol=symbol,
            numbers=parse_numbers(curr_line),
        ) + get_overlaps(
            symbol=symbol,
            numbers=parse_numbers(down_line),
        )
    )

    print(f'{symbol.number} overlaps {overlaps}')
    return overlaps



def part1():
    lines = {}
    symbols = {}
    stored_overlaps = []

    # input_file = '03_example_input.txt'
    input_file = '03_input.txt'

    for line_number, l in enumerate(text_input.file_line_by_line(input_file)):
        lines[line_number] = l
        symbols[line_number] = parse_symbols(l, line_number)

    print()

    # match numbers adjacent to symbols
    for line_number, symbol_list in symbols.items():

        print(f'Line {line_number} symbols processing', symbols[line_number])
        if symbol_list:
            if line_number - 1 in lines.keys():
                print(f'{line_number - 1:>3}, {lines[line_number - 1]}')
            print(f'{line_number:>3}, {lines[line_number]}')
            if line_number + 1 in lines.keys():
                print(f'{line_number + 1:>3}, {lines[line_number + 1]}')


        line_overlaps = []
        for symbol in symbol_list:
            symbol_overlaps = get_symbol_overlaps(symbol, lines)
            line_overlaps += symbol_overlaps

        print(f'Line overlaps {sorted(line_overlaps)}')

        stored_overlaps += line_overlaps

        print()

    print(stored_overlaps)
    return sum(stored_overlaps)


def part2():
    lines = {}
    symbols = {}
    stored_overlaps = []

    # input_file = '03_example_input.txt'
    input_file = '03_input.txt'

    for line_number, l in enumerate(text_input.file_line_by_line(input_file)):
        lines[line_number] = l
        symbols[line_number] = [
            symbol
            for symbol in parse_symbols(l, line_number)
            if symbol.number == "*"
        ]

    print(symbols)
    print()

    # match numbers adjacent to * symbols
    for line_number, gear_list in symbols.items():

        print(f'Line {line_number} gears processing', symbols[line_number])
        if gear_list:
            if line_number - 1 in lines.keys():
                print(f'{line_number - 1:>3}, {lines[line_number - 1]}')
            print(f'{line_number:>3}, {lines[line_number]}')
            if line_number + 1 in lines.keys():
                print(f'{line_number + 1:>3}, {lines[line_number + 1]}')


        for symbol in gear_list:
            gear_overlaps = get_symbol_overlaps(symbol, lines)

            if len(gear_overlaps) == 2:
                stored_overlaps.append(tuple((gear_overlaps[0], gear_overlaps[1])))


        print(f'Gear overlaps {stored_overlaps}')


        print()

    print(stored_overlaps)
    return sum(
        o[0] * o[1]
        for o in stored_overlaps
    )


# p1 = part1()
# too high: 527634
# too low : 338734

p2 = part2()
# too low : 4247082

# print(p1)
print(p2)
