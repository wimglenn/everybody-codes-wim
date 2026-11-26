from ecd import data
import itertools as it
from collections import defaultdict


def parsed(data):
    portals, edges_raw = data.split("\n\n")
    n = int(portals.split()[-1])
    ns = [int(x) - 1 for x in edges_raw.split()]
    edges = list(zip(ns[0::2], ns[1::2]))
    return n, edges


def initial_edges(N, n=1):
    result = []
    for i in range(N):
        for di in range(1, n + 1):
            result.append((i, (i + di) % N))
            result.append((i, (i - di) % N))
    return result


def path_lengths(n, edges):
    graph = {i: [] for i in range(n)}
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)
    dist = defaultdict(lambda: float("inf"))
    for k, vs in graph.items():
        dist[k, k] = 0
        for v in vs:
            dist[k, v] = dist[v, k] = 1
    # https://en.wikipedia.org/wiki/Floyd-Warshall_algorithm
    for k, i, j in it.product(range(n), repeat=3):
        dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
    return dist


def strain(dist, n):
    return sum(dist[i,j] for i in range(n) for j in range(n))


n, edges = parsed(data["1"])
edges0 = initial_edges(n)
dist0 = path_lengths(n, edges0)
dist1 = path_lengths(n, edges0 + edges)
print("Part 1:", strain(dist0, n) - strain(dist1, n))


def edge_scores(dist, candidates, n):
    result = dict.fromkeys(candidates, 0)
    for a, b in candidates:
        for x in range(n):
            for y in range(x + 1, n):
                via_ab = dist[x, a] + 1 + dist[b, y]
                via_ba = dist[x, b] + 1 + dist[a, y]
                delta = dist[x, y] - min(via_ab, via_ba)
                if delta > 0:
                    result[a, b] += delta * 2
    result = {k: result[k] for k in sorted(result, key=result.get, reverse=True)}
    return result


n, edges = parsed(data["2"])
edges0 = initial_edges(n, 3)
dist0 = path_lengths(n, edges0)
edges1 = set(edges0 + edges)
dist1 = path_lengths(n, edges1)
candidates = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in edges1]
improvement = edge_scores(dist1, candidates, n)
result = strain(dist0, n) - strain(dist1, n) + max(improvement.values())
print("Part 2:", result)


def pair(ns):
    if len(ns) == 2:
        return [(ns[0], ns[1])]
    result = []
    n0 = ns[0]
    for i, n1 in enumerate(ns[1:], start=1):
        remaining = ns[1:i] + ns[i + 1:]
        result += [(n0, n1) + r for r in pair(remaining)]
    return result


n, edges = parsed(data["3"])
edges0 = initial_edges(n, 3)
dist0 = path_lengths(n, edges0)
r0 = strain(dist0, n)
q = n // 8
result = 0
for i in range(q):
    for p in pair([i + n * q for n in range(8)]):
        new_edges = [p[2*i:2*i+2] for i in range(4)]
        dist = path_lengths(n, edges + edges0 + new_edges)
        r = r0 - strain(dist, n)
        if r > result:
            result = r
print("Part 3:", result)
