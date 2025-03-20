def file_line_by_line(file_name: str):
    with open(file_name, "r") as f:
        for line in f:
            yield line.rstrip('\n')


