from ecd import data


class Sword:
    def __init__(self, pk, ns):
        self.pk = pk
        fishbone = []
        for n in ns:
            for f in fishbone:
                if n < f[1] and f[0] is None:
                    f[0] = n
                    break
                if n > f[1] and f[2] is None:
                    f[2] = n
                    break
            else:
                fishbone.append([None, n, None])
        self.fishbone = fishbone

    @classmethod
    def fromstr(cls, s):
        pk, ns = s.split(":")
        ns = [int(x) for x in ns.split(",")]
        return cls(int(pk), ns)

    @property
    def quality(self):
        spine = [x for _, x, _ in self.fishbone]
        result = int("".join(map(str, spine)))
        return result

    @property
    def numbers(self):
        result = []
        for row in self.fishbone:
            result.append(int("".join([str(x) for x in row if x is not None])))
        return result


print("Part 1:", Sword.fromstr(data["1"]).quality)

qualities = [Sword.fromstr(x).quality for x in data["2"].split()]
print("Part 2:", max(qualities) - min(qualities))

swords = [Sword.fromstr(x) for x in data["3"].split()]
swords.sort(key=lambda s: (s.quality, s.numbers, s.pk), reverse=True)
checksum = sum(i * s.pk for i, s in enumerate(swords, 1))
print("Part 3:", checksum)
