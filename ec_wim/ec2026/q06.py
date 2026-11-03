from ecd import data


def parsed(data):
    nodes = set()
    graph = {}
    for line in data.splitlines():
        left, right = line.split(":")
        rights = set(right.split(","))
        graph[left] = rights
        nodes.add(left)
        nodes |= rights
    for node in nodes:
        if node not in graph:
            graph[node] = set()
    return graph


graph = parsed(data["1"])
stack = ["NULL"]
ingredients = set()
while stack:
    node = stack.pop()
    if node not in ingredients:
        ingredients.add(node)
        stack += graph[node]
result = len(ingredients) - 1
print("Part 1:", result)


graph = parsed(data["2"])
for key, vals in graph.items():
    if key == "NULL":
        continue
    while True:
        len_before = len(vals)
        tmp = set()
        for val in vals:
            tmp.update(graph[val])
        vals.update(tmp)
        if len(vals) == len_before:
            break
result = sum("NULL" in vals for vals in graph.values())
print("Part 2:", result)


graph = parsed(data["3"])
for key, vals in graph.items():
    if key.startswith("NULL"):
        continue
    while True:
        len_before = len(vals)
        tmp = set()
        for val in vals:
            tmp.update(graph[val])
        vals.update(tmp)
        if len(vals) == len_before:
            break
result = sum(sum(x.startswith("NULL") for x in vals) > 1 for vals in graph.values())
print("Part 3:", result)
