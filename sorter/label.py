"""Sort every miss into retrieval_miss or tool_misuse, then score the labeler against hand labels.

v0 is the shortcut many teams use: look only at the outcome.
v1 was written after reading the dev-split misses: look at what the tools returned."""
import glob, json, os

def gold_seen(t):
    """Did any tool result in the trace contain the gold profile id?"""
    for s in t["steps"]:
        if s["type"] != "tool": continue
        r = s["result"]
        hits = r if isinstance(r, list) else [r]
        if any(isinstance(h, dict) and h.get("id") == t["gold"] for h in hits): return True
    return False

def label_v0(t):
    if t["correct"]: return "pass"
    return "retrieval_miss" if not t["answer"] else "tool_misuse"

def label_v1(t):
    if t["correct"]: return "pass"
    return "tool_misuse" if gold_seen(t) else "retrieval_miss"

def load():
    out = []
    for path in sorted(glob.glob("runs/*/q*.json")):
        t = json.load(open(path)); t["run"] = path.split("/")[1]; t["key"] = f"{t['run']}/{t['id']}"
        out.append(t)
    return out

def agreement(rows, fn, hand, split):
    rs = [t for t in rows if not t["correct"] and t["split"] == split and t["key"] in hand]
    ok = sum(fn(t) == hand[t["key"]]["label"] for t in rs)
    return {"agree": ok, "n": len(rs), "disagree": [t["key"] for t in rs if fn(t) != hand[t["key"]]["label"]]}

if __name__ == "__main__":
    rows = load()
    hand = json.load(open("data/hand_labels.json")) if os.path.exists("data/hand_labels.json") else {}
    for t in rows:
        t["auto"] = label_v1(t); t["auto_v0"] = label_v0(t); t["gold_seen"] = gold_seen(t)
        t["hand"] = hand.get(t["key"])
    miss = [t for t in rows if not t["correct"]]
    unlabeled = [t["key"] for t in miss if t["key"] not in hand]
    rep = {
        "runs": len(rows), "queries": len({t["id"] for t in rows}), "misses": len(miss),
        "split": {k: sum(t["auto"] == k for t in miss) for k in ("retrieval_miss", "tool_misuse")},
        "by_run": {r: {"runs": sum(t["run"] == r for t in rows), "misses": sum(t["run"] == r and not t["correct"] for t in rows)} for r in sorted({t["run"] for t in rows})},
        "agreement": {v: {s: agreement(rows, f, hand, s) for s in ("dev", "heldout")} for v, f in (("v0", label_v0), ("v1", label_v1))},
        "unlabeled": unlabeled,
    }
    os.makedirs("docs", exist_ok=True)
    json.dump({"report": rep, "traces": rows}, open("docs/data.json", "w"))
    print(json.dumps(rep, indent=1))
