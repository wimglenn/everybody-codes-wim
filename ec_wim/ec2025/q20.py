from collections import defaultdict
from collections import deque
from ecd import data


def parsed(data):
    S = E = None
    nodes = set()
    for y, line in enumerate(data.replace(".", "").splitlines()):
        for x, c in enumerate(line):
            if c == "E":
                E = x, y
            if c == "S":
                S = x, y
            if c in "EST":
                nodes.add((x, y))
    graph = defaultdict(list)
    n_edges = 0
    for x, y in nodes:
        if x > 0 and (x - 1, y) in nodes:
            graph[x, y].append((x - 1, y))
            graph[x - 1, y].append((x, y))
            n_edges += 1
        if y > 0 and x % 2 == 0 and (x + 1, y - 1) in nodes:
            graph[x, y].append((x + 1, y - 1))
            graph[x + 1, y - 1].append((x, y))
            n_edges += 1
    return S, E, graph, n_edges


_, _, _, n_edges = parsed(data["1"])
print("Part 1:", n_edges)


def bfs(graph, target, start):
    q = deque([(start, 0)])
    seen = set()
    while q:
        node, depth = q.popleft()
        if node == target:
            return depth
        if node not in seen:
            seen.add(node)
            q += [(n, depth + 1) for n in graph[node]]


S, E, graph, _ = parsed(data["2"])
result = bfs(graph, target=E, start=S)
print("Part 2:", result)


def parsed3(data):
    S = E = None
    nodes = set()
    lines = data.replace(".", "").splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "E":
                E = x, y
            if c == "S":
                S = x, y
            if c in "EST":
                nodes.add((x, y))
    graph = defaultdict(list)
    for x, y in nodes:
        p = 2*y + x%2
        q = len(lines) - 1 - y - x//2 - x%2
        for dx in -1, 0, 1:
            if (p + dx, q) in nodes:
                graph[x, y].append((p + dx, q))
        if p % 2 and (p - 1, q + 1) in nodes:
            graph[x, y].append((p - 1, q + 1))
        if p % 2 == 0 and (p + 1, q - 1) in nodes:
            graph[x, y].append((p + 1, q - 1))
    return S, E, graph


S, E, graph = parsed3(data["3"])
result = bfs(graph, target=E, start=S)
print("Part 3:", result)
