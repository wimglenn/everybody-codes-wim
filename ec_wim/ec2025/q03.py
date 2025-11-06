from ecd import data

for part, raw in data.items():
    ns = [int(x) for x in raw.split(",")]
    counter = dict.fromkeys(ns, 0)
    for n in ns:
        counter[n] += 1
    if part == "1":
        print("Part 1:", sum(counter))
    elif part == "2":
        ordered = sorted(counter)
        print("Part 2:", sum(ordered[:20]))
    elif part == "3":
        print("Part 3:", max(counter.values()))
