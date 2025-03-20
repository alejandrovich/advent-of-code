import re


from readfile import read


file_name = '01_input.txt'


def part1():

    l1 = []
    l2 = []
    for line in read(file_name):
        # print(line)
        match = re.search(r'(\d+)\s+(\d+)$', line)
        print(match.group(1), match.group(2))
        l1.append(int(match.group(1)))
        l2.append(int(match.group(2)))

    l1 = sorted(l1)
    l2 = sorted(l2)


    diffs = sum(
        abs(id1 - id2)
        for id1, id2 in zip(l1, l2)
    )
    print(diffs)


def part2():
    l1 = []
    l2 = {}
    for line in read(file_name):
        match = re.search(r'(\d+)\s+(\d+)$', line)

        d1 = int(match.group(1))
        d2 = int(match.group(2))
        print(d1, d2)

        l1.append(d1)

        l2[d2] = l2[d2] + 1 if d2 in l2.keys() else 1

    freqs = [
        d1 * l2[d1] if d1 in l2.keys() else 0
        for d1 in l1
    ]
    print(freqs)
    print(sum(freqs))


part1()
part2()
