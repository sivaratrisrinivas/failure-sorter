"""A small find-this-person agent. Two tools over the synthetic corpus, one answer call.
Every message, tool call and tool result is logged to traces/<id>.json."""
import json, math, os, re, sys, time, urllib.request
MODEL = os.environ.get("AGENT_MODEL", "openai/gpt-oss-20b")
K, MAX_STEPS = 3, 4
P = json.load(open("data/profiles.json")); BY = {p["id"]: p for p in P}
tok = lambda s: re.findall(r"[a-z0-9_]+", s.lower())
# Run 1 harness: the index covers name and headline only. Bios are only visible after open_profile.
FIELDS = os.environ.get("INDEX_FIELDS", "name,headline").split(",")
DOCS = {p["id"]: tok(" ".join(p[f] for f in FIELDS)) for p in P}
N = len(DOCS); AVG = sum(map(len, DOCS.values())) / N
DF = {}
for d in DOCS.values():
    for t in set(d): DF[t] = DF.get(t, 0) + 1
def search(query):
    q = tok(query); sc = []
    for pid, d in DOCS.items():
        s = 0
        for t in q:
            f = d.count(t)
            if f: s += math.log(1 + (N - DF[t] + .5) / (DF[t] + .5)) * f * 2.2 / (f + 1.2 * (.25 + .75 * len(d) / AVG))
        sc.append((s, pid))
    sc.sort(reverse=True)
    return [{"id": pid, "name": BY[pid]["name"], "headline": BY[pid]["headline"]} for s, pid in sc[:K] if s > 0]
def open_profile(pid):
    p = BY.get(pid); return p if p else {"error": f"no profile {pid}"}
TOOLS = [
 {"type":"function","function":{"name":"search","description":f"Keyword search over public profiles. Returns the top {K} hits with id, name, headline.","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}},
 {"type":"function","function":{"name":"open_profile","description":"Open one profile by id. Returns name, headline, city and bio.","parameters":{"type":"object","properties":{"id":{"type":"string"}},"required":["id"]}}},
 {"type":"function","function":{"name":"answer","description":"Submit the id of the person you found. Call once.","parameters":{"type":"object","properties":{"id":{"type":"string"},"why":{"type":"string"}},"required":["id","why"]}}},
]
SYS = "You find one specific person in a profile index. Use search and open_profile, then call answer with the profile id. Be quick: you have at most 4 tool calls, so do not open profiles unless you must."
def chat(msgs):
    body = json.dumps({"model": MODEL, "messages": msgs, "tools": TOOLS, "temperature": float(os.environ.get("TEMP", "0")), "seed": int(os.environ.get("SEED", "1"))}).encode()
    for a in range(10):
        try:
            r = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", body,
                {"Authorization": "Bearer " + os.environ["GROQ_API_KEY"], "Content-Type": "application/json", "User-Agent": "failure-sorter"})
            return json.load(urllib.request.urlopen(r, timeout=60))["choices"][0]["message"]
        except Exception as e:
            time.sleep(int(e.headers.get("retry-after", 0) or 0) + 10 * (a + 1) if hasattr(e, "headers") and e.headers else 10 * (a + 1)); err = str(e)
    raise RuntimeError(err)
def run(q):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": q["query"]}]
    steps, final = [], None
    for i in range(MAX_STEPS + 1):
        m = chat(msgs); msgs.append({k: v for k, v in m.items() if k in ("role", "content", "tool_calls")})
        calls = m.get("tool_calls") or []
        if not calls:
            steps.append({"type": "text", "content": m.get("content")}); break
        for c in calls:
            name = c["function"]["name"]
            try: args = json.loads(c["function"]["arguments"] or "{}")
            except Exception: args = {}
            if name == "search": out = search(args.get("query", ""))
            elif name == "open_profile": out = open_profile(args.get("id", ""))
            elif name == "answer": final = args; out = {"ok": True}
            else: out = {"error": "unknown tool"}
            steps.append({"type": "tool", "name": name, "args": args, "result": out, "thought": m.get("reasoning") or m.get("content")})
            msgs.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(out)})
        if final: break
    return {**q, "model": MODEL, "temperature": float(os.environ.get("TEMP", "0")), "seed": int(os.environ.get("SEED", "1")), "index_fields": FIELDS, "steps": steps, "answer": final, "correct": bool(final and final.get("id") == q["gold"])}
if __name__ == "__main__":
    OUT = os.environ.get("OUT", "traces"); os.makedirs(OUT, exist_ok=True)
    for line in open("data/queries.jsonl"):
        q = json.loads(line)
        if os.environ.get("SPLIT") and q["split"] != os.environ["SPLIT"]: continue
        path = f"{OUT}/{q['id']}.json"
        if os.path.exists(path) and "--fresh" not in sys.argv: continue
        t = run(q); json.dump(t, open(path, "w"), indent=1)
        print(q["id"], "OK " if t["correct"] else "MISS", (t["answer"] or {}).get("id"), "gold", q["gold"], len(t["steps"]), "steps", flush=True)
