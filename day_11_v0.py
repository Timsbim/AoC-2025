from functools import cache, partial


print("Day 11")
EXAMPLE = False


file_name = f"2025/input/day_11{'_example_1' if EXAMPLE else ''}.txt"
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

if EXAMPLE:
    CONNECTS = {}
    with open("2025/input/day_11_example_2.txt", "r") as file:
        for line in file:
            left, right = line.rstrip().split(": ")
            CONNECTS[left] = set(right.split())
    pprint(CONNECTS)


def part_2():
    graph = {}
    for n0, nodes in CONNECTS.items():
        for n1 in nodes:
            graph.setdefault(n1, set()).add(n0)
    
    @cache
    def count(node):
        if node == "svr":
            return {"none": 1, "fft": 0, "dac": 0, "both": 0}
        
        counts_new = {"none": 0, "fft": 0, "dac": 0, "both": 0}
        for n in graph[node]:
            counts = count(n)
            if node == "fft":
                counts_new["fft"] += counts["none"]
                counts_new["both"] += counts["dac"]
            elif node == "dac":
                counts_new["dac"] += counts["none"]
                counts_new["both"] += counts["fft"]
            else:
                for state in "none", "fft", "dac", "both":
                    counts_new[state] += counts[state]
        
        return counts_new
        
    return count("out")["both"]


print("Part 2:", solution := part_2())
assert solution == (2 if EXAMPLE else 358564784931864)
