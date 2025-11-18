from ecd import data


def parsed(raw):
    names, rules = raw.split("\n\n")
    names = names.split(",")
    graph = {}
    for rule in rules.splitlines():
        x, ys = rule.split(" > ")
        if x not in graph:
            graph[x] = []
        for y in ys.split(","):
            if y not in graph:
                graph[y] = []
            graph[x].append(y)
    indices = []
    for i, name in enumerate(names):
        for x, y in zip(name, name[1:]):
            if y not in graph[x]:
                break
        else:
            indices.append(i)
    return names, graph, indices


names, _, [i] = parsed(data["1"])
print("Part 1:", names[i])

_, _, indices = parsed(data["2"])
print("Part 2:", sum(indices) + len(indices))

names, graph, indices = parsed(data["3"])
min_length = 7
max_length = 11
stack = [names[i] for i in indices]
results = set()
while stack:
    prefix = stack.pop()
    for x in graph[prefix[-1]]:
        name = prefix + x
        if min_length <= len(name) <= max_length:
            results.add(name)
        if len(name) < max_length:
            stack.append(name)
print("Part 3:", len(results))
