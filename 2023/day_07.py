import re
from collections import namedtuple

from text_input import file_line_by_line


# file_name = '07_example_input.txt'
file_name = '07_input.txt'

Hand = namedtuple('Hand', ('rank', 'cards', 'bid'))

CARD_RANKS = (
    '5-of-a-kind',
    '4-of-a-kind',
    'full-house',
    '3-of-a-kind',
    '2-pair',
    'pair',
    'high-card',
    'A',
    'K',
    'Q',
    'J-part1', # part 1 broken, because joker moved to end
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    'J',
)

CARD_VALUE = {
    card_rank: i
    for i, card_rank in enumerate(CARD_RANKS)
}

def _zero_joker(hand_value):
    if hand_value == [5]:
        rank_value = '5-of-a-kind'
    elif hand_value == [4, 1]:
        rank_value = '4-of-a-kind'
    elif hand_value == [3, 2]:
        rank_value = 'full-house'
    elif hand_value == [3, 1, 1]:
        rank_value = '3-of-a-kind'
    elif hand_value == [2, 2, 1]:
        rank_value = '2-pair'
    elif hand_value == [2, 1, 1, 1]:
        rank_value = 'pair'
    elif hand_value == [1, 1, 1, 1, 1]:
        rank_value = 'high-card'
    else:
        raise 'missing card rank'

    return rank_value


def _one_joker(hand_value):
    if hand_value == [4]:
        rank_value = '5-of-a-kind'  # joker can only match to other cards
    elif hand_value == [3, 1]:
        rank_value = '4-of-a-kind'  # match joker with 3-pair
    elif hand_value == [2, 2]:
        rank_value = 'full-house'  # joker increases 1 pair
    elif hand_value == [2, 1, 1]:
        rank_value = '3-of-a-kind'  # joker skips over 2 pair
    elif hand_value == [1, 1, 1, 1]:
        rank_value = 'pair'  # joker makes high card a pair
    else:
        raise ValueError(f'missing card rank (one joker) {hand_value}')

    return rank_value


def _two_joker(hand_value):
    if hand_value == [3]:
        rank_value = '5-of-a-kind'
    elif hand_value == [2, 1]:
        rank_value = '4-of-a-kind'
    elif hand_value == [1, 1, 1]:
        rank_value = '3-of-a-kind'
    else:
        raise 'missing card rank (2 jokers)'

    return rank_value


def _three_joker(hand_value):
    if hand_value == [2]:
        rank_value = '5-of-a-kind'
    elif hand_value == [1, 1]:
        rank_value = '4-of-a-kind'
    else:
        raise 'missing card rank (3 joker)'

    return rank_value


def _four_joker(hand_value):
    return '5-of-a-kind'


def _get_rank_with_joker(cards):
    # count the number of jokers
    # get hand_value without joker cards

    jokerless_cards = [
        card for card in cards
        if card != 'J'
    ]
    joker_count = 5 - len(jokerless_cards)


    hand_value = _get_hand_value(jokerless_cards)

    # print(f'{jokerless_cards} mapped to: {hand_value}')

    # transform the rank_value by the joker count
    joker_mapping = {
        0: _zero_joker,
        1: _one_joker,
        2: _two_joker,
        3: _three_joker,
        4: _four_joker,
        5: _four_joker,  # 4 and 5 have same behavior
    }

    joker_rank = joker_mapping[joker_count](hand_value)

    return (CARD_VALUE[joker_rank], tuple(
        CARD_VALUE[card_face] for card_face in cards
    ))



def _get_hand_value(cards):
    card_count = {}
    for card in cards:
        card_count[card] = (
            card_count[card] + 1 
            if card in card_count.keys() 
            else 1
        )

    hand_value = sorted(card_count.values(), reverse=True)
    return hand_value

def _get_rank(cards):
    hand_value = _get_hand_value(cards)

    if hand_value == [5]:
        rank_value = '5-of-a-kind'
    elif hand_value == [4, 1]:
        rank_value = '4-of-a-kind'
    elif hand_value == [3, 2]:
        rank_value = 'full-house'
    elif hand_value == [3, 1, 1]:
        rank_value = '3-of-a-kind'
    elif hand_value == [2, 2, 1]:
        rank_value = '2-pair'
    elif hand_value == [2, 1, 1, 1]:
        rank_value = 'pair'
    elif hand_value == [1, 1, 1, 1, 1]:
        rank_value = 'high-card'
    else:
        raise 'missing card rank'

    return (
        CARD_VALUE[rank_value],
        tuple(CARD_VALUE[card_face] for card_face in cards)
    )



def read_input():
    for line in file_line_by_line(file_name):
        match = re.search(r'(\w\w\w\w\w) (\d+)$', line)
        cards = match.group(1)
        bid = int(match.group(2))
        hand = Hand(rank=_get_rank(cards), cards=cards, bid=bid)
        # print(hand)
        yield hand


def part1():
    hands = read_input()
    sorted_hands = sorted(hands, key=lambda h: h.rank, reverse=True)
    hand_count = len(sorted_hands)

    hand_values = []
    for position, hand in enumerate(sorted_hands):
        hand_value = hand.bid * (position + 1)

        print(hand.bid, hand.cards, hand_value, _get_rank(hand.cards))
        hand_values.append(hand_value)

    final_sum = sum(hand_values)
    print('final sum part 1', final_sum)
    print()


def part2():
    hands = []
    for line in file_line_by_line(file_name):
        match = re.search(r'(\w\w\w\w\w) (\d+)$', line)
        cards = match.group(1)
        bid = int(match.group(2))
        hand = Hand(rank=_get_rank_with_joker(cards), cards=cards, bid=bid)
        hands.append(hand)

    sorted_hands = sorted(hands, key=lambda h: h.rank, reverse=True)
    hand_count = len(sorted_hands)

    hand_values = []
    for position, hand in enumerate(sorted_hands):
        hand_value = hand.bid * (position + 1)

        print((position + 1), hand.bid, hand.cards, hand_value, hand.rank)
        hand_values.append(hand_value)

    
    final_sum = sum(hand_values)
    print(f'hand count {hand_count}')
    print(f'final sum part 2 {final_sum}')

    # too high: 251908276
    # too high: 251532562


part1()
part2()

