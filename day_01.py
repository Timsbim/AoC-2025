# --------------------------------------------------------------------------- #
#    Day 1                                                                    #
# --------------------------------------------------------------------------- #
from argparse import ArgumentParser
from pprint import pprint


# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day 1")

parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
EXAMPLE = parser.parse_args().example

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

file_name = f"2025/input/day_01{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    ROTATIONS = tuple((line[:1], int(line[1:])) for line in file)

if EXAMPLE:
    pprint(ROTATIONS)
    pass

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    position, count = 50, 0
    for direction, no in ROTATIONS:
        if direction == "R":
            position = (position + no) % 100
        else:
            position = (position - no) % 100
        if position == 0:
            count += 1
    return count


print(solution := part_1())
assert solution == (3 if EXAMPLE else 1102)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    position, count = 50, 0
    for direction, no in ROTATIONS:
        full, rest = divmod(no, 100)
        count += full
        if rest == 0:
            continue
        if direction == "R":
            position_new = position + rest
            count += position_new >= 100
        else:
            position_new = position - rest
            count += position and position_new <= 0
        position = position_new % 100
    return count


print(solution := part_2())
assert solution == (6 if EXAMPLE else 6175)
