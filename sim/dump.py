"""Print one topic's questions compactly, in bank order, for answering. Usage: python3 sim/dump.py D01"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
b = json.loads((ROOT / "app/dist/bank.js").read_text()[len("window.BANK = "):-2])
d = sys.argv[1]
print(d, next(x["name"] for x in b["domains"] if x["id"] == d))
for k, i in enumerate(b["order"][d]):
    it = b["items"][i]
    extra = ""
    if it.get("show_if"): extra = " [only if " + ", ".join(f"{p} in {v}" for p, v in it["show_if"].items()) + "]"
    print(f"\n{k+1}. {i} ({it['format']}){extra}: {it['stem']}")
    if it["format"] == "tradeoff":
        print(f"   sides: A={it['sides'][0]['label']}: {it['sides'][0]['text']} | B={it['sides'][1]['label']}: {it['sides'][1]['text']}")
        print("   0=Strongly A 1=Somewhat A 2=Somewhat B 3=Strongly B")
    else:
        print("   " + " | ".join(f"{c}={o}" for c, o in enumerate(it["options"])))
    if it.get("cases"):
        print("   cases: " + " | ".join(f"[{j}] {c['text']}" for j, c in enumerate(it["cases"])))
