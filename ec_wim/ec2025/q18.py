from ecd import data


class Plant:
    def __init__(self, pk, thickness):
        self.pk = pk
        self.thickness = thickness
        self.incoming = []
        self.outgoing = []

    def __repr__(self):
        return f"Plant({self.pk}, {self.thickness})"

    @property
    def incoming_energy(self):
        result = 0
        for k, v in self.incoming:
            if isinstance(k, int):
                result += k * v
            else:
                result += k.energy * v
        return result

    @property
    def energy(self):
        incoming_energy = self.incoming_energy
        if incoming_energy >= self.thickness:
            return incoming_energy
        return 0


def parsed(data):
    plants = {}
    test_cases = []
    for line in data.splitlines():
        parts = line.rstrip(":").split()
        if line.startswith("Plant"):
            pk, thickness = int(parts[1]), int(parts[-1])
            plants[pk] = plant = Plant(pk, thickness)
        elif line.startswith("- free branch"):
            thickness = int(parts[-1])
            plant.incoming.append([1, thickness])
        elif line.startswith("- branch"):
            branch, thickness = int(parts[4]), int(parts[-1])
            plants[branch].outgoing.append((plant, thickness))
            plant.incoming.append((plants[branch], thickness))
        elif line.startswith(("0", "1")):
            test_cases.append([int(x) for x in line.split()])
    return plants, test_cases


def energy_test(test, plants):
    for i, n in enumerate(test, start=1):
        plants[i].incoming[0][0] = n
    return next(iter(reversed(plants.values()))).energy


plants, _ = parsed(data["1"])
_, plant = plants.popitem()
print("Part 1:", plant.energy)

plants, test_cases = parsed(data["2"])
result = sum(energy_test(t, plants) for t in test_cases)
print("Part 2:", result)

plants, test_cases = parsed(data["3"])
n = len(test_cases[0])
best = []
for p1 in plants.values():
    if len(p1.incoming) > 1:
        for p0, thickness in p1.incoming:
            best.append(int(thickness > 0))
    if len(best) == n:
        break
E = energy_test(best, plants)
es = [energy_test(t, plants) for t in test_cases]
result = sum(E - e for e in es if e > 0)
print("Part 3:", result)
