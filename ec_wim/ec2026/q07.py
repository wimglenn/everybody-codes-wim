from collections import Counter
from collections import defaultdict
from ecd import data


def parsed(data):
    energy = {}
    graph = {}
    for line in data.splitlines():
        i, e, cs = line.split(", ")
        i = int(i.split("=")[1])
        energy[i] = int(e.split("=")[1])
        graph[i] = [int(x) for x in cs.split("=")[1].split(",")]
    return energy, graph


energy, graph = parsed(data["1"])
first_cloud = max(graph, key=lambda k: len(graph[k]))
stack = [(5, first_cloud)]
while stack:
    impulse, cloud_id = stack.pop()
    energy[cloud_id] += impulse
    if impulse - 1:
        stack += [(impulse - 1, x) for x in graph[cloud_id]]
print("Part 1:", sum(energy.values()))


energy, graph = parsed(data["2"])
first_cloud = max(graph, key=lambda k: len(graph[k]))
stack = [(10, first_cloud)]
while stack:
    impulse, cloud_id = stack.pop()
    energy[cloud_id] += impulse
    if impulse - 1:
        stack += [(impulse - 1, x) for x in graph[cloud_id]]
print("Part 2:", sum(energy.values()))


energy0, graph = parsed(data["3"])
max_energy = 1_000_000
results = {}
for first_cloud in energy0:
    energy = energy0.copy()
    exploded = set()
    impulses = {first_cloud: Counter({10: 1})}
    stage = 1
    while impulses:
        # print(f"Stage {stage}:")
        new_impulses = defaultdict(Counter)
        explosions = {}
        for i, counter in sorted(impulses.items()):
            if i in exploded:
                continue
            for strength, count in counter.items():
                inc = strength * count
                # s = "" if count == 1 else "s"
                # print(
                #     f"cloud {i} received {count} impulse{s} with strength {strength}: +{inc} "
                #     f"(energy {energy[i]} -> {energy[i] + inc})"
                # )
                energy[i] += inc
                if strength > 1:
                    for n in graph[i]:
                        if n not in exploded:
                            new_impulses[n][strength - 1] += count

        explosions = {k: v for k, v in energy.items() if v >= max_energy and k not in exploded}
        if explosions:
            # print("Explosions after this stage:")
            for k, e in explosions.items():
                # print(f"cloud {k} exploded at energy {e}")
                for n in graph[k]:
                    if n not in exploded:
                        # print(f"  new impulse with strength 10: cloud {k} -> cloud {n}")
                        new_impulses[n][10] += 1

        exploded.update(explosions)

        # print()
        stage += 1
        impulses = new_impulses

    # print("Remaining clouds:")
    # for k, v in energy.items():
    #     if k not in exploded:
    #         print(f"cloud {k}: {energy[k]}")
    # print()

    total = sum(v for k, v in energy.items() if k not in exploded)
    results[first_cloud] = total

# for k, v in results.items():
#     print(f"cloud {k}: {v}")

result = max(results.values())
print("Part 3:", result)
