print("Day 3")
EXAMPLE = False


file_name = f"2025/input/day_03{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    BANKS = tuple(tuple(map(int, line.rstrip())) for line in file)
LENGTH = len(BANKS[0])


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
 

print("Part 1:", solution := solve(2))
assert solution == (357 if EXAMPLE else 17142)
print("Part 2:", solution := solve(12))
assert solution == (3121910778619 if EXAMPLE else 169935154100102)
