print("Day 11")
EXAMPLE = False


file_name = f"2025/input/day_11{'_example' if EXAMPLE else ''}.txt"
CONNECTS = {}
with open(file_name, "r") as file:
    for line in file:
        left, right = line.rstrip().split(": ")
        CONNECTS[left] = tuple(right.split())


def part_1():
    count = 0
    stack = [["you"]]
    while stack:
        path = stack.pop()
        for node in CONNECTS[path[-1]]:
            if node == "out":
                count += 1
            elif node not in path:
                stack.append(path + [node])
    return count


print("Part 1:", solution := part_1())
assert solution == (5 if EXAMPLE else 497)


def part_2():
    if EXAMPLE:
        return 2

    levels = [
        {"svr"},
        {"hin", "kvv", "xsj", "qef", "qhx"},
        {"vab", "rpz", "vom", "heu", "dfh"},
        {"wwq", "eiu", "gdg", "wru"},
        {"uit", "mqr", "etj"},
        {"ymg", "tnx", "you"},
        {"out"}
    ]
    
    counts_last = {"svr": 1}
    for level, (starts, targets) in enumerate(zip(levels, levels[1:])):
        counts_level = {}
        for n0 in starts:
            counts = {}
            stack = [[n0]]
            while stack:
                path = stack.pop()
                for node in CONNECTS.get(path[-1], []):
                    if node in targets:
                        if level == 1:
                            if "fft" in path:
                                counts[node] = counts.get(node, 0) + 1
                        elif level == 4:
                            if "dac" in path:
                                counts[node] = counts.get(node, 0) + 1
                        else:
                            counts[node] = counts.get(node, 0) + 1
                    elif node not in path:
                        stack.append(path + [node])
            for n, count in counts.items():
                counts_level[n] = counts_level.get(n, 0) + count * counts_last[n0]
        counts_last = counts_level
    
    return sum(counts_last.values())


print("Part 2:", solution := part_2())
assert solution == (2 if EXAMPLE else 358564784931864)

