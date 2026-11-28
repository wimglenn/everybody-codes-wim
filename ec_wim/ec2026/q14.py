from collections import Counter
from collections import defaultdict
from ecd import data


def parsed(data):
    lines = data.splitlines()
    h = len(lines)
    [w] = {len(x) for x in lines}
    pad = [f" {x} " for x in lines]
    data = [" "*(w+2), *pad, " "*(w+2)]
    edges = Counter()
    for y in range(1, h + 2):
        for x in range(1, w + 2):
            left = data[y][x-1]
            up = data[y-1][x]
            val = data[y][x]
            if val != up:
                edges[frozenset([up, val])] += 1
            if val != left:
                edges[frozenset([left, val])] += 1
    graph = defaultdict(set)
    for k1, k2 in edges:
        graph[k1].add(k2)
        graph[k2].add(k1)
    edges = {k: edges[k] for k in sorted(edges, key=edges.get)}
    return graph, edges


def find_root(x, parent):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # flatten parent lookup as we traverse
        x = parent[x]
    return x


def union(a, b, parent):
    root_a = find_root(a, parent)
    root_b = find_root(b, parent)
    if root_a == root_b:
        return False
    parent[root_b] = root_a
    return True


def minimum_spanning_tree(graph, edges, initial=()):
    parent = {x: x for x in graph}
    n = len(graph) - 1  # number of connections remaining
    for i0 in initial:
        for i1 in graph[i0]:
            n -= union(i0, i1, parent)
    connections = {}
    for (r0, r1), k in edges.items():
        if union(r0, r1, parent):
            connections[r0, r1] = k
            n -= 1
            if not n:
                break
    return connections


_graph, edges = parsed(data["1"])
result = sum(edges.values())
print("Part 1:", result)


graph, edges = parsed(data["2"])
min_edges = minimum_spanning_tree(graph, edges)
print("Part 2:", sum(min_edges.values()))


graph, edges = parsed(data["3"])
regions = [x for x in graph if x != " "]
result = None
for i, r0 in enumerate(regions):
    for r1 in regions[i+1:]:
        mst = minimum_spanning_tree(graph, edges, initial=(r0, r1))
        k = sum(mst.values())
        if result is None or k < result:
            result = k
print("Part 3:", result)
