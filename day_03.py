# --------------------------------------------------------------------------- #
#    Day 3                                                                    #
# --------------------------------------------------------------------------- #
from argparse import ArgumentParser
from pprint import pprint


# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day 3")

parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
EXAMPLE = parser.parse_args().example

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

file_name = f"2025/input/day_03{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    BANKS = tuple(tuple(map(int, line.rstrip())) for line in file)
LENGTH = len(BANKS[0])
if EXAMPLE:
    print(f"length of a bank: {LENGTH}")
    print("banks:")
    pprint(BANKS)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #


def solve(num_digits):
    total = 0
    for bank in BANKS:
        joltage, start, stop = 0, 0, LENGTH - num_digits + 1
        for _ in range(num_digits):
            i = max(range(start, stop), key=lambda i: bank[i])
            joltage = 10 * joltage + bank[i]
            start, stop = i + 1, stop + 1
        total += joltage
    return total
 

# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

print(solution := solve(2))
assert solution == (357 if EXAMPLE else 17142)
 
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")

print(solution := solve(12))
assert solution == (3121910778619 if EXAMPLE else 169935154100102)
