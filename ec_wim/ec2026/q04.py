from dataclasses import dataclass
from operator import itemgetter
from collections import Counter
from collections import defaultdict
from ecd import data


@dataclass(frozen=True)
class Result:
    id: int
    quest: int
    part: int
    time: int


class User:
    def __init__(self, id):
        self.id = id
        self.results = defaultdict(lambda: {1: None, 2: None, 3: None})

    def add_result(self, r):
        if r.id != self.id:
            raise Exception("wrong user")
        self.results[r.quest][r.part] = r

    def ctime(self, quest, part):
        results = self.results[quest]
        if any(results[p] is None for p in range(1, part + 1)):
            return
        return sum(results[p].time for p in range(1, part + 1))


results = Counter()
for line in data["1"].splitlines():
    ns = [int(x.split("=")[1]) for x in line.split()]
    r = Result(*ns)
    results[r.id] += r.time
result = sum(i*v for i, v in enumerate(sorted(results.values()), start=1))
print("Part 1:", result)


results = defaultdict(list)
for line in data["2"].splitlines():
    ns = [int(x.split("=")[1]) for x in line.split()]
    r = Result(*ns)
    results[r.id].append(r.time)
results = sorted(results.values(), key=lambda x: (-len(x), sum(x)))
result = sum(i*sum(vs) for i, vs in enumerate(results, start=1))
print("Part 2:", result)


users = {}
for line in data["3"].splitlines():
    ns = [int(x.split("=")[1]) for x in line.split()]
    r = Result(*ns)
    if r.id not in users:
        users[r.id] = User(r.id)
    users[r.id].add_result(r)

score = Counter()
for q in range(1, 21):
    for part in (1, 2, 3):
        ctimes = {}
        for uid, user in users.items():
            t = user.ctime(q, part)
            if t is not None:
                ctimes[uid] = t
        ctimes = sorted(ctimes.items(), key=itemgetter(1))
        pts = []
        maxp = [0, 50, 100, 150][part]
        i = 0
        for i, (p, (uid, time)) in enumerate(zip(range(maxp, 0, -1), ctimes)):
            if i and time == ctimes[i - 1][1]:
                pts.append(pts[-1])
            else:
                pts.append(p)
        i += 1
        while i < len(ctimes):
            if ctimes[i][1] == ctimes[i - 1][1]:
                pts.append(pts[-1])
                i += 1
            else:
                break
        for ((id, time), points) in zip(ctimes, pts):
            score[id] += points

ranks = []
ranking = sorted(score.items(), key=itemgetter(1), reverse=True)
for i, (uid, pts) in enumerate(ranking):
    if i and pts == ranking[i - 1][1]:
        ranks.append(ranks[-1])
    else:
        ranks.append(i + 1)

result = sum(i*pts for i, (_, pts) in zip(ranks, ranking))
print("Part 3:", result)
