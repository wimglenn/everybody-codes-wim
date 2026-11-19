from ecd import data


def parsed(data):
    d = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            z = complex(x, y)
            d[z] = int(char)
    return d


def dfs(d, initial, exclude=()):
    seen = set()
    stack = list(initial)
    while stack:
        z0 = stack.pop()
        if z0 in seen:
            continue
        seen.add(z0)
        for dz in -1j, 1, 1j, -1:
            z1 = z0 + dz
            if z1 not in exclude and z1 in d and d[z1] <= d[z0]:
                stack.append(z1)
    return seen


d = parsed(data["1"])
destroyed = dfs(d, initial=[0])
print("Part 1:", len(destroyed))


d = parsed(data["2"])
destroyed = dfs(d, initial=[0, next(reversed(d))])
print("Part 2:", len(destroyed))


d = parsed(data["3"])
result = 0
exclude = set()
for _ in range(3):
    seen = exclude.copy()
    chains = {}
    while len(seen) < len(d):
        z0 = next(z for z in d if z not in seen)
        destroyed = dfs(d, initial=[z0], exclude=exclude)
        seen.update(destroyed)
        chains[z0] = destroyed
    z0 = max(chains, key=lambda z: len(chains[z]))
    chain = chains[z0]
    exclude.update(chain)
    result += len(chain)
print("Part 3:", result)
