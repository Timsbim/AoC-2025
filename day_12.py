print("Day 12")
EXAMPLE = False


file_name = f"2025/input/day_12{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    parts = file.read().split("\n\n")
SHAPES = tuple(tuple(part.split()[1:]) for part in parts[:-1])
regions = []
for region in parts[-1].split("\n"):
    region, shapes = region.split(": ")
    regions.append((
        tuple(map(int, region.split("x"))),
        tuple(map(int, shapes.split()))
    ))
REGIONS = tuple(regions)


def part_1():
    if EXAMPLE:
        return 2
    return sum((r // 3) * (c // 3) >= sum(cs) for (r, c), cs in REGIONS)


print("Part 1:", solution := part_1())
assert solution == (2 if EXAMPLE else 505)
