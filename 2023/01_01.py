import displays
import re
from text_input import file_line_by_line


file_name = '01_01.txt'


numbers_as_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',]
word_2_num = {
    # 'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


running_sum = []
other_sum = 0

for index, l in enumerate(file_line_by_line(file_name)):
    num_word_matches = re.finditer(r"(?=(one|two|three|four|five|six|seven|eight|nine))", l)
    num_digit_matches = re.finditer(r"(0|1|2|3|4|5|6|7|8|9)", l)

    numbers_found = {}

    if num_word_matches:
        for m in num_word_matches:
            numbers_found[m.start()] = word_2_num[m.group(1)]
            if index < 20:
                print(m.group(), m.start(), m)

    if num_digit_matches:
        for m in num_digit_matches:
            numbers_found[m.start()] = m.group()

    # get first and last
    nums = ''.join((
        numbers_found[min(numbers_found.keys())], 
        numbers_found[max(numbers_found.keys())], 
    ))

    other_sum += int(nums)
    running_sum.append(int(nums))

    if index < 20:
        print(nums, l)
        print(numbers_found)


running = 0
for l in displays.array_10(running_sum):
    running += sum(l)
    print(l, sum(l), running)

print(f'helped: {sum(running_sum)} mine: {other_sum}')

