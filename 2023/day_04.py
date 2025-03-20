import re
from collections import namedtuple

import text_input

Card = namedtuple('Card', ('id', 'winning', 'numbers'))
# file_name = '04_example_input.txt'
file_name = '04_input.txt'


def parse_numbers(num_string):
    return {
        int(n) for n in num_string.split()
    }


def calculate_winnings(card):
    matches = len(card.winning.intersection(card.numbers))
    if matches:
        return pow(2, matches - 1)
    else:
        return 0


def count_matches(card):
    matches = len(card.winning.intersection(card.numbers))
    return matches

def parse_card(line):
    match = re.search(r'Card\s+(\d+): ([0-9 ]+) \| ([0-9 ]+)', line)
    card = Card(
        id=int(match.group(1)),
        winning=parse_numbers(match.group(2)),
        numbers=parse_numbers(match.group(3)),
    )

    # print(card)
    return card


def part1():
    amounts = []

    for line in text_input.file_line_by_line(file_name):
        card = parse_card(line)
        winnings = calculate_winnings(card)

        amounts.append(winnings)

    return sum(amounts)


def increment_card_count(card_id, cards, increment=1):
    if card_id in cards.keys():
        cards[card_id] += increment
    else:
        cards[card_id] = increment


def part2():
    cards = {}

    for line in text_input.file_line_by_line(file_name):
        card = parse_card(line)
        increment_card_count(card.id, cards)
        card_multiplier = cards[card.id]

        matches = count_matches(card)
        for match in range(matches):
            increment_card_count(
                card_id=card.id + match + 1, 
                cards=cards, 
                increment=card_multiplier
            )
            print(cards)

    return sum(cards.values())


p1 = part1()
p2 = part2()

print(p1)
print(p2)


