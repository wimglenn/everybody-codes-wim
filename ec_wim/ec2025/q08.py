from ecd import data

ns = [int(x) for x in data["1"].split(",")]
result = sum(2 * abs(y - x) == 32 for x, y in zip(ns, ns[1:]))
print("Part 1:", result)


def intersections(x0, y0, n=256):
    for x in range(x0 + 1, y0):
        for y in range(1, x0):
            yield y, x
        for y in range(y0 + 1, n + 1):
            yield x, y


pairs = [(j + 1, i + 1) for i in range(256) for j in range(i)]
ns = [int(x) for x in data["2"].split(",")]
d = dict.fromkeys(pairs, 0)
result = 0
for x, y in zip(ns, ns[1:]):
    if x > y:
        x, y = y, x
    result += sum([d[p] for p in intersections(x, y)])
    d[x, y] += 1
print("Part 2:", result)

ns = [int(x) for x in data["3"].split(",")]
d = dict.fromkeys(pairs, 0)
for x, y in zip(ns, ns[1:]):
    if x > y:
        x, y = y, x
    d[x, y] += 1
cuts = {x: sum(d[p] for p in intersections(*x)) + d[x] for x in pairs}
print("Part 3:", max(cuts.values()))
