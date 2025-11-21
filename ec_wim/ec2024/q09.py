from ecd import data

stamps = 1, 3, 5, 10
result = 0
for n in map(int, data["1"].split()):
    for d in reversed(stamps):
        q, n = divmod(n, d)
        result += q
print("Part 1:", result)


def gen_table(stamps, limit):
    result = dict.fromkeys(stamps, 1)
    while limit not in result:
        update = {}
        for total, count in result.items():
            for stamp in stamps:
                k = total + stamp
                update[k] = min(update.get(k, count + 1), count + 1)
        for k, v in update.items():
            result[k] = min(result.get(k, v), v)
    return result


ns = [int(x) for x in data["2"].split()]
limit = max(ns)
stamps += 15, 16, 20, 24, 25, 30
counts = gen_table(stamps, limit)
result = sum(counts[n] for n in ns)
print("Part 2:", result)


ns = [int(x) for x in data["3"].split()]
limit = 100 + max(ns) // 2
stamps += 37, 38, 49, 50, 74, 75, 100, 101
counts = gen_table(stamps, limit)
result = 0
for n in ns:
    n0 = n // 2
    n1 = n - n0
    b = counts[n0] + counts[n1]
    while True:
        n0 -= 1
        n1 += 1
        if n1 - n0 > 100:
            break
        b = min(b, counts[n0] + counts[n1])
    result += b
print(f"Part 3:", result)
