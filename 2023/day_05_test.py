from collections import namedtuple

import day_05


Range = namedtuple('Range', ('start', 'end', 'modifier', 'name'))
infinity = float('inf')


def sort_start(ranges):
    return sorted(
        ranges, key=lambda r: r.start)


def populate_numberline(maps):
    ranges = []

    for m in maps:
        ranges.append(
            Range(
                start=m.source,
                end=m.source + m.range - 1,
                modifier=m.destination - m.source,
                name=m.name
            )
        )

    ranges = sort_start(ranges)
    blank_ranges = []

    # range leapfrog
    start = 0
    rc = 0  # range counter

    while rc < len(ranges):
        if ranges[rc].start > start:
            # make blank range
            blank = Range(
                start=start,
                end=ranges[rc].start - 1,
                modifier=0,
                name=ranges[rc].name
            )
            blank_ranges.append(blank)

        start = ranges[rc].end + 1
        rc += 1

    # make trailing range infinite
    last_range = ranges[rc - 1]

    blank = Range(
        start=last_range.end + 1,
        end=infinity,
        modifier=0,
        name=last_range.name
    )
    blank_ranges.append(blank)

    return sort_start(ranges + blank_ranges)


def interlace_ranges(item_start, item_end, ranges):
    '''
    take a single range (i.e. seeds) and break it into
    parts that are contiguous (cross no boundaries) with
    the next layer (i.e. soils) across the given (seed-soil) ranges.
    '''
    out_ranges = []

    while item_start is not None:
        r = get_overlap(item_start, item_end, ranges)

        out_ranges.append(r)
        if item_end > r.end:
            item_start = r.end + 1
        else:
            item_start = None

    return out_ranges


def get_containing_map(item_start, maps):
    container_map = [
        m for m in maps
        if m.start <= item_start and m.end > item_start
    ]
    if not container_map:
        raise 'Out of bounds'

    return container_map[0]


def get_overlap(item_start, item_end, maps):
    # cases handled
    # 1. item_start inside a map

    overlap_map = get_containing_map(item_start, maps)

    # find the end, either item_end or the range end, whichever
    # is smallest
    overlap_end = min(item_end, overlap_map.end)

    return Range(
        start=item_start,
        end=overlap_end,
        modifier=overlap_map.modifier,
        name=overlap_map.name,
    )


def traverse_type(ranges):
    new_type = ranges[0].name.split('-')[-1]
    return [
        Range(
            start=r.start + r.modifier,
            end=r.end + r.modifier,
            modifier=None,
            name=new_type
        )
        for r in ranges
    ]


def pp_ranges(ranges):
    for r in sort_start(ranges):
        print(r)

    print()


def test_interlace_ranges():
    print('TESTING interlace_ranges')
    soil_fert = [
        day_05.Map(name='soil-to-fertilizer', source=0, destination=39, range=15),
        day_05.Map(name='soil-to-fertilizer', source=15, destination=0, range=37),
        day_05.Map(name='soil-to-fertilizer', source=52, destination=37, range=2),
    ]
    numberline_ranges = populate_numberline(soil_fert)
    print('numberline_ranges')
    pp_ranges(numberline_ranges)

    output = interlace_ranges(10, 55, numberline_ranges)
    pp_ranges(output)


    print('target far outside')
    output = interlace_ranges(55, 101, numberline_ranges)
    pp_ranges(output)

    output = traverse_type(numberline_ranges)
    print('after traversal')
    pp_ranges(output)


def test_generating_number_line():
    print('TESTING populate_numberline')
    seed_soil_map_1 = day_05.Map(name='seed-to-soil', source=50, destination=52, range=48)
    seed_soil_map_2 = day_05.Map(name='seed-to-soil', source=98, destination=50, range=2)

    soil_fert = [
        day_05.Map(name='soil-to-fertilizer', source=0, destination=39, range=15),
        day_05.Map(name='soil-to-fertilizer', source=15, destination=0, range=37),
        day_05.Map(name='soil-to-fertilizer', source=52, destination=37, range=2),
    ]

    output = populate_numberline([seed_soil_map_1, seed_soil_map_2]) 
    print(output)

    output = populate_numberline(soil_fert)
    print(output)
    print()


test_generating_number_line()


test_interlace_ranges()


def algo():
    print()
    print('PART 2 deux')

    # get transformational ranges

    modern_ranges = {}

    for map_name in day_05.TRAVERSE_ORDER:
        maps = day_05.get_maps(map_name)
        ranges = populate_numberline(maps)
        modern_ranges[map_name] = ranges

    # print all the transforms
    for map_name in day_05.TRAVERSE_ORDER:
        print(map_name)
        pp_ranges(modern_ranges[map_name])

    # get seed ranges (modifier = None)
    print('algo seeds')
    seed_ranges = [
        Range(
            start=r[0],
            end=r[0] + r[1] - 1,
            modifier=None,
            name='seed',
        )
        for r in day_05.parse_seed_ranges()
    ]
    pp_ranges(seed_ranges)

    print('here')

    print('seed_soil populated')
    seed_soil_ranges = modern_ranges['seed-to-soil']
    pp_ranges(seed_soil_ranges)

    for seed_range in seed_ranges:
        output = interlace_ranges(
            seed_range.start, 
            seed_range.end, 
            seed_soil_ranges,
        )
        print('seed_soil interlaced')
        pp_ranges(output)

        print('seed_soil traversed')
        soil_ranges = traverse_type(output)
        pp_ranges(soil_ranges)

    soil_fert_ranges = populate_numberline(
        day_05.get_maps('soil-to-fertilizer')
    )

    print('master looping begins')

    # initial condition: starts with seeds
    loop_ranges = seed_ranges

    i = 0

    while i < len(day_05.TRAVERSE_ORDER):  # THE LOOP
        # set map from item to next
        loop_trans_map = modern_ranges[day_05.TRAVERSE_ORDER[i]]

        interlaced = [
            ir
            for r in loop_ranges
            for ir in interlace_ranges(
                r.start, 
                r.end, 
                loop_trans_map,
            )
        ]

        print(f'interlace {loop_ranges[0].name}')
        pp_ranges(interlaced)

        print(f'traversed {loop_ranges[0].name}')
        loop_ranges = traverse_type(interlaced)
        print(f'into {loop_ranges[0].name}')

        pp_ranges(loop_ranges)
        print(i, 'is done')
        i += 1

        print()


    
    # interlace seeds with seed/soil

algo()
