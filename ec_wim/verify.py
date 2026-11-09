import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from ecd._impl import get_keys
from ecd._impl import get_seed
from ecd._impl import top


here = Path(__file__).parent

ok = "✅"
wrong = "❌"

parser = argparse.ArgumentParser()
parser.add_argument("-k", nargs="+", help="filter by substring")
parser.add_argument("-x", nargs="+", help="exclude by substring")
args = parser.parse_args()
sub = args.k
exclude = args.x

seed = get_seed()
for path in sorted(here.glob("ec*/q*.py")):
    relpath = path.relative_to(here)
    if sub and not any(x in str(relpath) for x in sub):
        continue
    if exclude and any(x in str(relpath) for x in exclude):
        continue
    event = int(path.parent.name[2:])
    quest = int(path.name[1:-3])
    cache = top / f"{event}-{quest:02d}.{seed}.answers.json"
    if not cache.exists():
        k = get_keys(quest, event)
        if k.keys() >= {"answer1", "answer2", "answer3"}:
            cache.write_text(json.dumps(k, indent=2))
        else:
            print(relpath, " ❓ answer caches not avail, skipping")
            continue
    else:
        k = json.loads(cache.read_text())
    t0 = time.time()
    print(relpath, flush=True, end="")
    proc = subprocess.run([sys.executable, path], text=True, capture_output=True)
    t = time.time() - t0
    results = {}
    for line in proc.stdout.splitlines():
        if line.startswith("Part "):
            part, result = line[5:].split(":", maxsplit=1)
            results[f"answer{part.strip()}"] = result.strip()
    glyphs = []
    for part in "123":
        expected = k[f"answer{part}"]
        actual = results.get(f"answer{part}")
        if expected == actual:
            glyphs.append(f"{ok} {actual:<20}")
        else:
            glyphs.append(f"{wrong} ({actual=} {expected=})")
    print(f"{t: 6.2f}s  ", *glyphs)
