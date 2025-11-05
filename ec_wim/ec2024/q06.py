from ecd import data


for part, raw in data.items():
    graph = {}
    for line in raw.splitlines():
        n0, n1s = line.split(":")
        n1s = n1s.split(",")
        for n1 in n1s:
            if n0 not in graph:
                graph[n0] = []
            graph[n0].append(n1)

    paths = []
    stack = [("RR",)]
    while stack:
        p0 = stack.pop()
        n1s = graph.get(p0[-1], [])
        for n1 in n1s:
            if part == "3" and n1 in ("BUG", "ANT"):
                continue
            p1 = p0 + (n1,)
            if n1 == "@":
                paths.append(p1)
            else:
                stack.append(p1)

    d = {}
    for path in paths:
        path_length = len(path)
        if path_length not in d:
            d[path_length] = []
        d[path_length].append(path)

    [[path]] = [x for x in d.values() if len(x) == 1]
    if part == "1":
        result = "".join(path)
    else:
        result = "".join([x[0] for x in path])
    print(f"Part {part}: {result}")
