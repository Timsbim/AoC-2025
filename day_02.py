# --------------------------------------------------------------------------- #
#    Day 2                                                                    #
# --------------------------------------------------------------------------- #
import re
from argparse import ArgumentParser
from pprint import pprint


# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day 2")

parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
EXAMPLE = parser.parse_args().example

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

file_name = f"2025/input/day_02{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    ranges = file.read().rstrip()
RANGES = tuple(tuple(map(int, r.split("-"))) for r in ranges.split(","))
if EXAMPLE:
    pprint(RANGES)

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")


def part_1():
    pwd = 0
    for start, end in RANGES:
        for n in range(start, end + 1):
            mid, rest = divmod(len(n_str := str(n)), 2)
            if rest == 0 and n_str[:mid] == n_str[mid:]:
                pwd += n            
    return pwd


print(solution := part_1())
assert solution == (1227775554 if EXAMPLE else 30608905813)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2():
    re_rep = re.compile(r"^(\d+)\1+$")
    return sum(
        n
        for start, end in RANGES
        for n in range(start, end + 1)
        if re_rep.match(str(n))
    )
 

print(solution := part_2())
assert solution == (4174379265 if EXAMPLE else 31898925685)
