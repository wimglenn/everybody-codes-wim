from ecd import data


ns = [int(x) for x in data["1"].split("\n")]
right = ns[0::2]
left = ns[1::2]
dial = [1, *right, *reversed(left)]
i = 2025 % len(dial)
result = dial[i]
print("Part 1:", result)


for part in "23":
    ranges = []
    for line in data[part].splitlines():
        left, right = line.split("-")
        ranges.append((int(left), int(right)))
    right = ranges[0::2]
    left = [(y, x) for x, y in reversed(ranges[1::2])]
    dial = [(1, 1), *right, *left]
    N = sum([abs(y - x) + 1 for x, y in dial])
    i = int("2025" * int(part)) % N
    for x, y in dial:
        count = abs(y - x) + 1
        if count <= i:
            i -= count
            continue
        if x <= y:
            result = range(x, y + 1)[i]
        else:
            result = range(x, y - 1, -1)[i]
        break
    print(f"Part {part}:", result)
