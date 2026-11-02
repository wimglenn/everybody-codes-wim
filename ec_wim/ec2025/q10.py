from functools import cache
from ecd import data


def parse_grid(raw):
    lines = raw.split()
    h = len(lines)
    [w] = {len(x) for x in lines}
    grid = {}
    locs = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            z = complex(x, y)
            grid[z] = char
            if char not in locs:
                locs[char] = []
            locs[char].append(z)
    return h, w, grid, locs


_h, _w, grid, locs = parse_grid(data["1"])
N = 4  # use 3 for the sample
dragons = locs["D"]
sheep = locs["S"]
dzs = [1 - 2j, 2 - 1j, 2 + 1j, 1 + 2j, -1 + 2j, -2 + 1j, -2 - 1j, -1 - 2j]
seen = set()
stack = [(0, z) for z in dragons]
while stack:
    n, z = stack.pop()
    seen.add(z)
    if n < N:
        for dz in dzs:
            if z + dz in grid:
                stack.append((n + 1, z + dz))
result = sum(s in seen for s in sheep)
print("Part 1:", result)


_h, _w, grid, locs = parse_grid(data["2"])
N = 20  # use 3 for the sample
dragons = [set() for i in range(N + 1)]
stack = [(0, z) for z in locs["D"]]
seen = set()
while stack:
    n, z = stack.pop()
    dragons[n].add(z)
    if (n, z) in seen:
        continue
    seen.add((n, z))
    if n < N:
        for dz in dzs:
            if z + dz in grid:
                stack.append((n + 1, z + dz))
sheep = set(locs["S"])
hides = set(locs["#"])
result = 0
dragons = [zs - hides for zs in dragons[1:]]
for i, zs in enumerate(dragons, 1):
    n_before = len(sheep)
    sheep = {z + 1j for z in sheep - zs}
    sheep -= zs
    result += n_before - len(sheep)
print("Part 2:", result)


class GameState:
    def __init__(self, dragon, sheep):
        self.sheep = sheep
        if all(s.imag < 0 for s in sheep):
            self.dragon = None
        else:
            self.dragon = dragon

    def __hash__(self):
        return hash((self.dragon, self.sheep))

    def __eq__(self, other):
        return (self.dragon, self.sheep) == (other.dragon, other.sheep)

    def __repr__(self):
        return f"GameState({self.dragon}, {self.sheep})"

    def neighbours(self):
        if self.any_sheep_safe():
            # prune these branches entirely, since we're only interested in
            # end states where all sheep got eaten.
            return []
        results = []
        for i, s in enumerate(self.sheep):
            if 0 <= s.imag < h:
                s += 1j
                if s in hides or s != self.dragon:
                    sheep = self.sheep[:i] + (s,) + self.sheep[i + 1:]
                    for z in z1s[self.dragon]:
                        if z in sheep and z not in hides:
                            # dragon eats one
                            results.append(GameState(z, tuple(s if s != z else s.real - 1j for s in sheep)))
                        else:
                            results.append(GameState(z, sheep))
        if not results:
            # dragon must move twice
            for z in z1s[self.dragon]:
                results.append(GameState(z, self.sheep))
        return results

    def any_sheep_safe(self):
        for s in self.sheep:
            if s.imag >= sheep_safe[int(s.real)]:
                return True


h, w, grid, locs = parse_grid(data["3"])
hides = set(locs["#"])
[d0] = locs["D"]
sheep = tuple(locs["S"])
z1s = {z: [z + dz for dz in dzs if z + dz in grid] for z in grid}
z1s[None] = []  # we put dragon to "None" if all sheep have been eaten
sheep_safe = [h] * w
for i in range(w):
    while complex(i, sheep_safe[i] - 1) in hides:
        sheep_safe[i] -= 1

initial = GameState(d0, sheep)
target = GameState(None, tuple(s.real-1j for s in sheep))
inv_graph = {initial: []}
graph = {}
stack = [initial]
while stack:
    s0 = stack.pop()
    if s0 not in graph:
        graph[s0] = []
        for s1 in s0.neighbours():
            if s1 not in inv_graph:
                inv_graph[s1] = []
            inv_graph[s1].append(s0)
            graph[s0].append(s1)
            stack.append(s1)


@cache
def path_count(source, target):
    if source == target:
        return 1
    return sum(path_count(s, target) for s in inv_graph[source])


print("Part 3:", path_count(target, initial))
