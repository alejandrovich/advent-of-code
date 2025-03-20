import re
from typing import List
from collections import namedtuple

import text_input


Map = namedtuple('Map', ('name', 'source', 'destination', 'range'))

# file_name = '05_example_input.txt'
file_name = '05_input.txt'

mappings: List = []
TRAVERSE_ORDER = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]


def parse_map(file_name, map_name):
    parse = False
    maps = []

    for line in text_input.file_line_by_line(file_name):
        if line.startswith(map_name):
            parse = True
            continue
        elif line == '' and parse:
            break

        if parse:
            match = re.search(r'(\d+) (\d+) (\d+)', line)
            maps.append(
                Map(
                    name=map_name, 
                    destination=int(match.group(1)), 
                    source=int(match.group(2)), 
                    range=int(match.group(3)),
                )
            )

    return maps


def parse_seed_ranges():
    for line in text_input.file_line_by_line(file_name):
        match = re.search(r'seeds:\s+([\d ]+)$', line)
        if match:
            seeds = [int(s) for s in match.group(1).split()]
            ranges = [
                (seeds[i], seeds[i + 1])
                for i in range(0, len(seeds), 2)
            ]

    return ranges


def parse_seeds():
    for line in text_input.file_line_by_line(file_name):
        match = re.search(r'seeds:\s+([\d ]+)$', line)
        if match:
            seeds = [int(s) for s in match.group(1).split()]

    print(seeds)
    return seeds


def source_in_range(target, mapping):
    return (
        mapping.source <= target <= (mapping.source + mapping.range)
    )


def get_maps(map_name):
    global mappings

    return [
        m for m in mappings
        if m.name == map_name
    ]


def traverse_mapping(target, map_name):
    maps = get_maps(map_name)
    found = [
        m
        for m in maps
        if source_in_range(target, m)
    ]
    if not found:
        print(f'target {target} not found in {map_name}')
        return target
    else:
        destination = found[0].destination + (target - found[0].source)
        print(f'target {target} in {found[0]} maps to {destination}')
        return destination



def init():
    global mappings

    mapping = parse_map(file_name, 'seed-to-soil')
    mappings += mapping

    mapping = parse_map(file_name, 'soil-to-fertilizer')
    mappings += mapping

    mapping = parse_map(file_name, 'fertilizer-to-water')
    mappings += mapping

    mapping = parse_map(file_name, 'water-to-light')
    mappings += mapping

    mapping = parse_map(file_name, 'light-to-temperature')
    mappings += mapping

    mapping = parse_map(file_name, 'temperature-to-humidity')
    mappings += mapping

    mapping = parse_map(file_name, 'humidity-to-location')
    mappings += mapping

    for m in mappings:
        print(m)

def part1():
    seed_locations = []
    seeds = parse_seeds()

    for seed in seeds:
        item_id = seed
        for map_name in TRAVERSE_ORDER:
            item_id = traverse_mapping(item_id, map_name)

        print(f'seed {seed} to location {item_id}')
        seed_locations.append(item_id)
        print()

    print(f'seed locations: {sorted(seed_locations)}')
    return min(seed_locations)


def get_map_for_item(target, map_name):
    maps = get_maps(map_name)
    found = [
        m
        for m in maps
        if source_in_range(target, m)
    ]
    if not found:
        return None

    return found[0]


def traverse_range_map(item_range, map_name):
    # Get relevant maps
    maps = sorted(get_maps(map_name), key=lambda m: m.source)

    # get appropriate mappings for item->destination
    item_start = item_range[0]
    item_end = item_start + item_range[1] - 1

    # Helpfully show maps
    print(f'Mapping {item_start} to {item_end} in {map_name}')
    print(f'Mapped ranges')
    for m in maps:
        print(m)

    # define output var
    out_ranges = []
    safety = 0

    # get appropriate mappings for item->destination
    item_start = item_range[0]
    item_end = item_start + item_range[1] - 1

    while True and safety < 10:
        safety += 1

        # try find the start in a mapping
        mapping = get_map_for_item(item_start, map_name)
        print(f'Start {item_start} found? {mapping}')

        # When there is a mapping, find last dest in mapping's range.
        if mapping:
            end_dest_range = mapping.destination + mapping.range - 1

            # case: destination map includes item_end
            # done processing this item
            if mapping.range > (item_end - item_start):
                print(f'Entire range found in', mapping, item_start, item_end)
                destination_start = mapping.destination + (item_start - mapping.source)
                destination_end = mapping.destination + (item_end - mapping.source)

                out_ranges.append((destination_start, destination_end))
                break

            else:
                item_start = end_dest_range + 1
                print(f'new start: {item_start}')
        else:
            # Find next possible start range
            map_search = [
                next_map for next_map in sorted(maps, key=lambda m: m.source)
                if next_map.source > item_start
            ]

            # There is a mapping for higher items:
            # add a range for un-mapped items, set new item_start
            if map_search:
                next_map = map_search[0]
                print(f'Create pass-thru range', map_name, item_start, item_end)

                destination_start = item_start
                destination_end = next_map.source - 1
                item_start = next_map.source

            # There is no mapping for higher items:
            # add a range for all un-mapped items.
            else:
                print(f'Upper limit in pass-thru range', map_name, item_start, item_end)
                print(maps)
                destination_start = item_start
                destination_end = item_end

                out_ranges.append((destination_start, destination_end))
                break

            print('no map: abort')
            break

    if safety >= 10:
        print('BAD OUTPUT')

    return out_ranges


def part2():
    seed_locations = []
    current_ranges = parse_seed_ranges()
    print()

    for map_name in TRAVERSE_ORDER:

        next_ranges = []

        for r in current_ranges:
            traversed = traverse_range_map(r, map_name)
            next_ranges += traversed

        print('in-prog', map_name, next_ranges)

        print()
        current_ranges = next_ranges

    print()


init()

p1 = part1()
print(f'part 1: {p1}')

print('\n' * 4, 'START of PT2')
p2 = part2()
print(f'part 2: {p2}')

