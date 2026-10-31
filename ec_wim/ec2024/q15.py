import string
from collections import defaultdict
from collections import deque
from ecd import data


def parsed(data):
    start = None
    herb_glyphs = set(string.ascii_uppercase)
    zs = set()
    herbs = defaultdict(list)
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            z = complex(x, y)
            if char == ".":
                if start is None:
                    start = z
                zs.add(z)
            elif char in herb_glyphs:
                herbs[char].append(z)
                zs.add(z)
    graph = {}
    for z in zs:
        graph[z] = []
        for dz in -1, -1j, 1, 1j:
            if z + dz in zs:
                graph[z].append(z + dz)
    return start, graph, herbs


def shortest_path(graph, start, targets):
    q = deque([(start, [start])])
    seen = {start}
    while q:
        z0, path = q.popleft()
        for z1 in graph[z0]:
            if z1 in targets:
                return path + [z1]
            if z1 not in seen:
                seen.add(z1)
                q.append((z1, path + [z1]))


start, graph, herbs = parsed(data["1"])
path = shortest_path(graph, start, targets=set(herbs["H"]))
print("Part 1:", 2 * len(path) - 2)


def bfs(graph, start, all_herbs):
    q = deque([(0, start, 0)])
    seen = {(0, start)}
    while q:
        h0, z0, d0 = q.popleft()
        for z1 in graph[z0]:
            if z1 == start and h0 == all_herbs:
                return d0 + 1
            h1 = h0
            if z1 in herbz:
                h1 |= herbz[z1]
            if (h1, z1) not in seen:
                seen.add((h1, z1))
                q.append((h1, z1, d0 + 1))


start, graph, herbs = parsed(data["2"])
herb_mask = {h: 1 << i for i, h in enumerate(herbs)}
herbz = {z: herb_mask[k] for k, zs in herbs.items() for z in zs}
all_herbs = (1 << len(herbs)) - 1
result = bfs(graph, start, all_herbs)
print(f"Part 2:", result)


start, graph, herbs = parsed(data["3"])
z = start
herb_order = "GIACDJPNQ"  # by manual inspection :(
paths = []
for h in herb_order:
    p = shortest_path(graph, start=z, targets=set(herbs[h]))
    paths.append(p)
    z = p[-1]
paths.append(shortest_path(graph, start=z, targets={start}))
result = sum(len(p) for p in paths) - len(paths)
print("Part 3:", result)
