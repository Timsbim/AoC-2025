print("Day 2")
EXAMPLE = False


file_name = f"2025/input/day_02{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    ranges = file.read().rstrip()
RANGES = tuple(tuple(map(int, r.split("-"))) for r in ranges.split(","))


def part_1():
    pwd = 0
    for start, end in RANGES:
        for n in range(start, end + 1):
            mid, rest = divmod(len(n_str := str(n)), 2)
            if rest == 0 and n_str[:mid] == n_str[mid:]:
                pwd += n            
    return pwd


print("Part 1:", solution := part_1())
assert solution == (1227775554 if EXAMPLE else 30608905813)


def part_2():
    pwd = 0
    for length in range(2, max(len(str(end)) for _, end in RANGES) + 1):
        invalids = set()
        for n in range(1, length):
            if length % n != 0:
                continue
            reps = length // n
            for part in range(10 ** (n - 1), 10 ** n):
                invalids.add(int(str(part) * reps))
        for n in invalids:
            for start, end in RANGES:
                if start <= n <= end:
                    pwd += n
                    break
    return pwd


print("Part 2:", solution := part_2())
assert solution == (4174379265 if EXAMPLE else 31898925685)
