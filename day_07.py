print("Day 7")
EXAMPLE = False


file_name = f"2025/input/day_07{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    MANIFOLD = tuple(file.read().splitlines())


def part_1():
    splits = 0
    beams = [MANIFOLD[0].index("S")]
    for row in MANIFOLD[1:]:
        beams_new = []
        for b in beams:
            if row[b] == ".":
                if not beams_new or beams_new[-1] != b:
                    beams_new.append(b)
            else:
                splits += 1
                b_new = b - 1
                if not beams_new or beams_new[-1] != b_new:
                    beams_new.append(b_new)
                beams_new.append(b + 1)
        beams = beams_new
    return splits


print("Part 1:", solution := part_1())
assert solution == (21 if EXAMPLE else 1490)


def part_2():
    beams = {MANIFOLD[0].index("S"): 1}
    for row in MANIFOLD[1:]:
        beams_new = {}
        for b, count in beams.items():
            if row[b] == ".":
                beams_new[b] = beams_new.get(b, 0) + count
            else:
                b_new = b - 1
                beams_new[b_new] = beams_new.get(b_new, 0) + count
                beams_new[b + 1] = count
        beams = beams_new
    return sum(beams.values())


print("Part 2:", solution := part_2())
assert solution == (40 if EXAMPLE else 3806264447357)
