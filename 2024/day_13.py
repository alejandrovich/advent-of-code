import re
from readfile import read


# file_name = '13_example.txt'
file_name = '13_input.txt'

def main(modifier=0):
    sums = 0

    for line in read(file_name):
        print(line)
        if line.startswith('Button A'):
            match = re.search(r'Button A\: X\+(\d+), Y\+(\d+)', line)
            x1 = int(match.group(1))
            y1 = int(match.group(2))
        if line.startswith('Button B'):
            match = re.search(r'Button B\: X\+(\d+), Y\+(\d+)', line)
            x2 = int(match.group(1))
            y2 = int(match.group(2))

        if line.startswith('Prize'):
            match = re.search(r'Prize\: X=(\d+), Y=(\d+)', line)
            dx = (int(match.group(1)) + 10000000000000) * -1
            dy = (int(match.group(2)) + 10000000000000) * -1

            ans = calc_cost(x1, x2, dx, y1, y2, dy)
            if ans:
                sums += ans
            print('answer', ans)

    print(f'part1 {sums}')



def calc_cost(a1, b1, c1, a2, b2, c2):
    ans = calc_intersection(a1, b1, c1, a2, b2, c2)

    if ans[0][1] == 0 and ans[1][1] == 0:
        return ans[0][0] * 3 + ans[1][0]


def calc_intersection(a1, b1, c1, a2, b2, c2):
    p1, r1 = divmod( ((b1 * c2) - (b2 * c1) ), ( (a1 * b2) - (a2 * b1) ))
    p2, r2 = divmod( ((a2 * c1) - (a1 * c2) ), ( (a1 * b2) - (a2 * b1) ))
    return (p1, r1), (p2, r2)


main()
