from ecd import data
import heapq
import itertools as it


def parsed(data):
    grid = {}
    S = []
    E = []
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            z = complex(x, y)
            if char == "S":
                S.append(z)
                char = "0"
            elif char == "E":
                E.append(z)
                char = "0"
            if char.isdigit():
                grid[complex(x, y)] = int(char)
    graph = {}
    for z0, h0 in grid.items():
        graph[z0] = {}
        for dz in -1, -1j, 1, 1j:
            z1 = z0 + dz
            if z1 in grid:
                h1 = grid[z1]
                h0_, h1_ = sorted([h0, h1])
                dh = min(h1_ - h0_, h0_ + 10 - h1_)
                graph[z0][z1] = 1 + dh
    return graph, S, E


def dijkstra(graph, start):
    prev = {}
    best = {start: 0}
    c = it.count()
    q = [(0, next(c), start)]
    while q:
        d0, _, z0 = heapq.heappop(q)
        for z1, d1 in graph[z0].items():
            if z1 not in best or d0 + d1 < best[z1]:
                prev[z1] = z0
                best[z1] = d0 + d1
                heapq.heappush(q, (d0 + d1, next(c), z1))
    return prev, best


graph1, [start1], [target1] = parsed(data["1"])
prev1, best1 = dijkstra(graph1, start1)
print("Part 1:", best1[target1])

graph2, [start2], [target2] = parsed(data["2"])
prev2, best2 = dijkstra(graph2, start2)
print("Part 2:", best2[target2])

graph3, S3, E3 = parsed(data["3"])
start = E3[0]
targets = set(S3)
prev3, best3 = dijkstra(graph3, start)
print("Part 3:", min(best3[x] for x in targets))
