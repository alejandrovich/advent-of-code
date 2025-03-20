

add_subtract = 1
calculated_pi: float = 0

for i in range(1, 20000000, 2):
    calculated_pi += float((1/i) * add_subtract)
    add_subtract *= -1
    if 0 == i % 201:
        print(calculated_pi * 4)


print(calculated_pi * 4)
