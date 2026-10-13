"""Read sim/answers/Dxx.txt into per-politician answers in the app's format.

File format, one topic per file, questions in bank order (see sim/dump.py):
  @GROUP t1 t2 ...        answer template for a group (sim/archetypes.py)
  id: 5=2 7=d             overrides for one politician (1-based question number)
  id@GROUP: 3=1           same, but starting from another group's template
  id1,id2,id3: 4=2        overrides for a sub-faction; one-person lines take priority
Tokens: a digit = answer code in bank order; d = "I don't know"; n = "none of
these fit"; - = skipped / not applicable. Exception questions take one character
per case (for example 0011), or a single - to skip all cases.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sim"))
from archetypes import G  # noqa: E402
from roster import R  # noqa: E402

BANK = json.loads((ROOT / "app/dist/bank.js").read_text()[len("window.BANK = "):-2])


def parse_topic(d):
    path = ROOT / "sim" / "answers" / f"{d}.txt"
    ids = BANK["order"][d]
    tmpl, over = {}, {}
    for ln, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("@"):
            g, *toks = line[1:].split()
            if len(toks) != len(ids):
                raise SystemExit(f"{path.name}:{ln} template {g} has {len(toks)} answers, expected {len(ids)}")
            tmpl[g] = toks
            continue
        m = re.match(r"^([a-z_0-9,]+)(?:@([A-Z]{2}))?:\s*(.*)$", line)
        if not m:
            raise SystemExit(f"{path.name}:{ln} can't read: {raw}")
        pids, grp, rest = m.groups()
        multi = "," in pids
        for pid in pids.split(","):
            o = over.setdefault(pid, {"g": None, "set": {}, "sub": {}})
            if grp:
                o["g"] = grp
            for kv in rest.split():
                k, v = kv.split("=")
                if not 1 <= int(k) <= len(ids):
                    raise SystemExit(f"{path.name}:{ln} question {k} out of range")
                # lines naming several politicians (a sub-faction) apply first; one-person lines win
                (o["sub"] if multi else o["set"])[int(k) - 1] = v
    out = {}
    for r in R:
        pid = r["id"]
        o = over.get(pid, {"g": None, "set": {}, "sub": {}})
        g = o["g"] or G[pid]
        if g not in tmpl:
            raise SystemExit(f"{path.name}: no template for group {g}")
        toks = list(tmpl[g])
        for k, v in o["sub"].items():
            toks[k] = v
        for k, v in o["set"].items():
            toks[k] = v
        out[pid] = toks
    unknown = set(over) - {r["id"] for r in R}
    if unknown:
        raise SystemExit(f"{path.name}: unknown ids {unknown}")
    return ids, out


def to_answers(ids, toks):
    """Convert one politician's tokens for one topic into app-style answers."""
    ans = {}
    for i, t in zip(ids, toks):
        it = BANK["items"][i]
        if it["format"] == "exceptions":
            cases = it["cases"]
            if t == "-":
                continue
            if len(t) != len(cases):
                raise ValueError(f"{i}: {len(cases)} cases, got {t!r}")
            for c, ch in zip(cases, t):
                if ch == "-":
                    continue
                if ch == "d":
                    ans[c["id"]] = {"e": 2}
                else:
                    k = int(ch)
                    if not 0 <= k < len(it["options"]):
                        raise ValueError(f"{c['id']}: code {k} out of range")
                    ans[c["id"]] = {"c": k}
            continue
        if t == "-":
            continue
        if t == "d":
            ans[i] = {"e": 2}
        elif t == "n":
            ans[i] = {"e": 1}
        else:
            k = int(t)
            n = 4 if it["format"] == "tradeoff" else len(it["options"])
            if not 0 <= k < n:
                raise ValueError(f"{i}: code {k} out of range (0..{n-1})")
            ans[i] = {"c": k}
    return ans


def load_all():
    people = {r["id"]: {} for r in R}
    done = []
    for d in sorted(BANK["order"]):
        if not (ROOT / "sim" / "answers" / f"{d}.txt").exists():
            continue
        ids, out = parse_topic(d)
        for pid, toks in out.items():
            try:
                people[pid].update(to_answers(ids, toks))
            except ValueError as e:
                raise SystemExit(f"{d} {pid}: {e}")
        done.append(d)
    return people, done


if __name__ == "__main__":
    people, done = load_all()
    print("topics answered:", len(done), done)
    print("answers per person:", min(len(a) for a in people.values()), "to", max(len(a) for a in people.values()))
