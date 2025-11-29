from ecd import data


def parsed(raw):
    d = {}
    for line in raw.split():
        x, y = line.split(":")
        ys = y.split(",")
        d[x] = dict.fromkeys(ys, 0)
        for y in ys:
            d[x][y] += 1
    return d


def evolve(t0, n, d):
    for _ in range(n):
        t1 = dict.fromkeys(d, 0)
        for k0, v0 in t0.items():
            dt = d[k0]
            for k1, v1 in dt.items():
                t1[k1] += v0 * v1
        t0 = t1
    return t0


pop1 = evolve(t0={"A": 1}, n=4, d=parsed(data["1"]))
print("Part 1:", sum(pop1.values()))

pop2 = evolve(t0={"Z": 1}, n=10, d=parsed(data["2"]))
print("Part 2:", sum(pop2.values()))

d = parsed(data["3"])
results = {}
for k in d:
    popk = evolve(t0={k: 1}, n=20, d=d)
    results[k] = sum(popk.values())
result = max(results.values()) - min(results.values())
print("Part 3:", result)
