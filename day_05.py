# --------------------------------------------------------------------------- #
#    Day 5                                                                    #
# --------------------------------------------------------------------------- #
from argparse import ArgumentParser
from pprint import pprint


# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day 5")

parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
EXAMPLE = parser.parse_args().example

# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

file_name = "2025/input/day_05" + ("_example" if EXAMPLE else "") + ".txt"
with open(file_name, "r") as file:
    ranges = []
    for line in file:
        if not (line := line.rstrip()):
            break
        ranges.append(tuple(map(int, line.split("-"))))
    RANGES = tuple(ranges)
    IDS = tuple(map(int, file))
 
if EXAMPLE:
    pprint(RANGES)
    pprint(IDS)
 
# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")
 

def part_1():
    count = 0
    for n in IDS:
        for left, right in RANGES:
            if left <= n <= right:
                count += 1
                break
    return count
 

print(solution := part_1())
assert solution == (3 if EXAMPLE else 885)
 
# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")
 

def part_2():
    ranges, count, start, stop = sorted(RANGES), 0, 0, -1
    for left, right in ranges:
        if left <= stop:
            stop = max(stop, right)
        else:
            count += stop - start + 1
            start, stop = left, right
    return count + stop - start + 1
 

print(solution := part_2())
assert solution == (14 if EXAMPLE else 348115621205535)
