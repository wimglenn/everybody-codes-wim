from ecd import data

for part, chunks in data.items():
    names, steps = chunks.split("\n\n")
    names = names.split(",")
    steps = [int(x) for x in steps.replace("R", "").replace("L", "-").split(",")]
    N = len(names)
    if part == "1":
        i = 0
        for step in steps:
            i += step
            i = max(0, min(i, N - 1))
        print(f"Part {part}:", names[i])
    if part == "2":
        print(f"Part {part}:", names[sum(steps) % N])
    if part == "3":
        for step in steps:
            i = step % N
            names[0], names[i] = names[i], names[0]
        print(f"Part {part}:", names[0])
