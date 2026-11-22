import argparse
import itertools as it
import json
import queue
import subprocess
import sys
import threading
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


def pump(stream, q):
    """Read lines from the subprocess in a thread so the main loop never blocks."""
    for line in stream:
        q.put(line)
    q.put(None)  # sentinel: EOF


yellow = "\x1b[33m"
red = "\x1b[31m"
reset = "\x1b[0m"


def fmt(cs):
    """
    Yellow at >= 10s, red at >= 60s.
    Padding is applied before the color codes so columns stay aligned.
    """
    text = f"{cs / 100:6.2f}s"
    if cs >= 6000:
        return f"{red}{text}{reset}"
    if cs >= 1000:
        return f"{yellow}{text}{reset}"
    return text


def run_streaming(path, relpath, k):
    """Run one puzzle script, printing each part result and time as they arrive"""
    row = str(relpath)
    spinner = it.cycle(r"\|/-")
    durations = {}
    t0 = time.time()
    mark = t0  # start of the part currently being solved

    def draw(spin=True):
        tail = f"  {next(spinner)} {fmt(round((time.time() - mark) * 100))}" if spin else ""
        print(f"\r{row}{tail}\x1b[K", end="", flush=True)

    def finish_part(part, result):
        """Close out a part: stamp its time and append its glyph + answer."""
        nonlocal mark, row
        now = time.time()
        durations[part] = round((now - mark) * 100)
        mark = now
        expected = k[f"answer{part}"]
        if expected == result:
            row += f"  {ok} {result:<20} {fmt(durations[part])}"
        else:
            row += f"  {wrong} ({result=} {expected=}) {fmt(durations[part])}"

    proc = subprocess.Popen(
        [sys.executable, "-u", path],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    q = queue.Queue()
    threading.Thread(target=pump, args=(proc.stdout, q), daemon=True).start()

    draw()
    while True:
        try:
            line = q.get(timeout=0.1)
        except queue.Empty:
            draw()  # nothing new: just advance the spinner / elapsed time
            continue
        if line is None:
            break
        if line.startswith("Part "):
            part, _, result = line[5:].partition(":")
            part, result = part.strip(), result.strip()
            if part in {"1", "2", "3"} and part not in durations:
                finish_part(part, result)
        draw()

    proc.wait()

    # Parts the script never printed: the first one absorbs the remaining
    # time, the rest get zero, so the total still equals the wall time.
    for part in "123":
        if part not in durations:
            finish_part(part, None)
            mark = time.time()  # later missing parts start "now" -> ~0.00s

    total = sum(durations.values())
    row += f"   (total {fmt(total)})"
    draw(spin=False)
    print()


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
    run_streaming(path, relpath, k)
