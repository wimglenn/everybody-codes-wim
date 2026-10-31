from ecd import data


def parsed(data):
    result = []
    for line in data.splitlines():
        left, right = line.split()
        _, left = left.split("-")
        bases = [int(x) for x in left[::-1]]
        values = [int(x) for x in right[::-1]]
        while len(bases) < len(values):
            bases += bases
        bases = [b ** i for i, b in enumerate(bases)]
        result.append((bases, values, right))
    return result


for part in "12":
    result = 0
    for bases, values, _ in parsed(data[part]):
        result += sum(b * v for b, v in zip(bases, values))
    print(f"Part {part}:", result)

result = 0
for bases, values, raw in parsed(data["3"]):
    r = sum(b * v for b, v in zip(bases, values))
    for i in reversed(range(int(raw))):
        digits = [int(x) for x in reversed(str(i))]
        total = sum(b * d for b, d in zip(bases, digits))
        if total == r:
            break
    else:
        result += r
print("Part 3:", result)
