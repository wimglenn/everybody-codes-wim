from ecd import data


def parsed(data, offset=0):
    d = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            z = complex(x, y)
            d[z + offset] = char
    return d


def evolve(d0):
    d1 = {}
    dzs = -1-1j, 1-1j, 1+1j, -1+1j
    for z, g in d0.items():
        n = sum(d0.get(z + dz) == "#" for dz in dzs)
        s = ".#" if g == "#" else "#."
        d1[z] = s[n % 2]
    return d1


for part, it in zip("12", (10, 2025)):
    d = parsed(data[part])
    result = 0
    for i in range(it):
        d = evolve(d)
        result += sum(v == "#" for v in d.values())
    print(f"Part {part}:", result)


d = parsed(data["3"], offset=13+13j)
grid = {complex(x, y): "." for x in range(34) for y in range(34)}
results = {}
seen = {frozendict(grid)}
N = 1_000_000_000
for i in range(N):
    grid = evolve(grid)
    k = frozendict(grid)
    if k in seen:
        break
    seen.add(k)
    if d.items() <= grid.items():
        results[i] = sum(v == "#" for v in grid.values())
q, r = divmod(N, i)
result = sum(results.values()) * q
for k, v in results.items():
    if k < r:
        result += v
print("Part 3:", result)
