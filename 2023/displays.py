
def array_10(items):
    i = 0
    while (i*10) < len(items):
        yield items[i*10:(i + 1) * 10]
        i += 1
