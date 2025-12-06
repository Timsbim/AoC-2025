from math import prod


print("Day 6")
EXAMPLE = False


file_name = f"2025/input/day_06{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    lines = file.read().splitlines()
NUMBERS, OPS = tuple(lines[:-1]), tuple(lines[-1].split())



def part_1():
    numbers = (tuple(map(int, line.split())) for line in NUMBERS)
    return sum(
        sum(ns) if op == "+" else prod(ns)
        for ns, op in zip(zip(*numbers), OPS)
    )


print("Part 1:", solution := part_1())
assert solution == (4277556 if EXAMPLE else 6209956042374)


def part_2():
    numbers, row = [], []
    for chars in zip(*NUMBERS):
        num = "".join(chars).strip()
        if num:
            row.append(int(num))
        else:
            numbers.append(tuple(row))
            row = []
    numbers.append(tuple(row))
    return sum(
        sum(ns) if op == "+" else prod(ns)
        for ns, op in zip(numbers, OPS)
    )


print("Part 2:", solution := part_2())
assert solution == (3263827 if EXAMPLE else 12608160008022)
