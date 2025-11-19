from ecd import data


def find_parents(i0, ps):
    results = []
    for i, p0 in enumerate(ps):
        if i == i0:
            continue
        for j, p1 in enumerate(ps[i + 1 :], start=i + 1):
            if j == i0:
                continue
            for x, y0, y1 in zip(ps[i0], p0, p1):
                if x != y0 and x != y1:
                    break
            else:
                results.append((i, j))
    return results


def similarity_degree(child, parent0, parent1):
    x0 = sum(x == y for x, y in zip(child, parent0))
    x1 = sum(x == y for x, y in zip(child, parent1))
    return x0 * x1


for part, raw in data.items():
    sequences = [x.split(":")[-1] for x in raw.splitlines()]
    graph = {}
    result = 0
    for i in range(len(sequences)):
        try:
            [(i0, i1)] = find_parents(i, sequences)
        except ValueError:
            pass
        else:
            graph[i] = i0, i1
            result += similarity_degree(sequences[i], sequences[i0], sequences[i1])
    if part in "12":
        print(f"Part {part}: {result}")
    else:
        components = [frozenset([i]) for i in range(len(sequences))]
        for i, (i0, i1) in graph.items():
            merge = components[i] | components[i0] | components[i1]
            for i in merge:
                components[i] = merge
            t = {i + 1 for i in merge}
        biggest_family = max(components, key=len)
        result = sum(biggest_family) + len(biggest_family)
        print("Part 3:", result)
