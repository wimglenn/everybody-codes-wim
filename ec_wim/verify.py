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
parser.add_argument("-k", help="filter by substring")
parser.add_argument("-x", help="exclude by substring")
args = parser.parse_args()
sub = args.k
exclude = args.x

seed = get_seed()
for path in sorted(here.glob("ec*/q*.py")):
    relpath = path.relative_to(here)
    if sub is not None and sub not in str(relpath):
        continue
    if exclude is not None and exclude in str(relpath):
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
    proc = subprocess.run([sys.executable, path], text=True, capture_output=True)
    t = time.time() - t0
    results = {}
    for line in proc.stdout.splitlines():
        if line.startswith("Part "):
            part, result = line[5:].split(":")
            results[f"answer{part.strip()}"] = result.strip()
    glyphs = []
    for part in "123":
        expected = k[f"answer{part}"]
        actual = results.get(f"answer{part}")
        if expected == actual:
            glyphs.append(f"{ok} {actual}")
        else:
            glyphs.append(f"{wrong} ({actual=} {expected=})")
    print(relpath, f"{t: 5.2f}s", *glyphs)
