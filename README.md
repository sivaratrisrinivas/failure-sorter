# failure sorter

Live: https://sivaratrisrinivas.github.io/failure-sorter/

When a people-search agent gets the wrong answer, there are two very different bugs. Either search never returned the right person (a **retrieval miss**, fix the index or the query), or search did return them and the agent did not use it (a **tool misuse**, fix the harness or the model). This repo runs a small agent, logs every trace, sorts each miss into one of those two bins, and lets you open any trace.

## What is here

- `data/profiles.json`: 64 invented profiles. No real people. Many share names on purpose.
- `data/queries.jsonl`: 44 find-this-person queries. q01 to q32 are dev. q33 to q44 are held out.
- `sorter/agent.py`: the agent. Tools: `search` (BM25, top 3, name and headline only), `open_profile`, `answer`. At most 4 tool calls. Model on the Groq free tier.
- `runs/`: one JSON trace per run, every tool call and result.
- `sorter/label.py`: the labeler. `docs/`: the viewer.

## Results (verified: computed from the traces in this repo)

| | count |
|---|---|
| runs | 205 (32 with a harness that also indexed bios, 173 with the name and headline index) |
| misses | 29 |
| retrieval miss | 19 |
| tool misuse | 10 |

The harness that indexed bios (`runs/run0_full_index`) missed 0 of 32. Same queries, same model.

Labeler agreement with hand labels:

| labeler | dev (22 misses) | held out (7 misses) |
|---|---|---|
| v0: no answer means retrieval miss | 12/22 | 5/7 |
| v1: was the right id in any tool result | 22/22 | 7/7 |

## How it was built

Following the evals-skills workflow (error-discovery, write-code-eval, validate-evaluator):

1. Read every dev miss before writing any labeler.
2. What showed up: the agent sees the right person in search hits, opens a same-name stranger instead, then runs out of calls. Or it finds the right person, keeps searching, and never answers. An outcome-only rule (v0) calls all of those retrieval misses.
3. v1 checks one thing in the trace: did the right profile id appear in any tool result. Unit tests in `tests/`.
4. I froze v1 in a commit, then wrote 12 new queries and ran them as the held-out set.

## Honest caveats

- **Hand labels have one annotator**, the builder (an AI agent working for Srinivas), in one pass. Srinivas has not reviewed them. No inter-annotator agreement exists. (verified)
- **v1 encodes the same rule the annotator used**, so 100% agreement mostly shows the code matches the rule. It does not show the rule is the right one. (inferred)
- **The first split leaked.** I first split q01 to q32 by parity, then read misses from both halves. So I moved all 32 to dev and wrote new held-out queries. (verified)
- **Held-out has only retrieval misses, all from one model** (qwen3.8-27b). The gpt-oss-20b held-out runs hit the Groq free daily token cap. So v1 is not yet tested on held-out tool misuse. (verified)
- **29 misses is small.** Treat the split as a demo, not a rate. (verified)
- Whether this split matches what a production people-search agent sees: unknown.

## Sources showing this problem is real

- Autumn's Harness Lead job post asks to "distinguish regressions/gaps from poor retrieval or poor tool use, and improve the system at the layer where it matters." https://www.ycombinator.com/companies/autumn-ai/jobs/gj5dGt0-harness-lead (verified, read 2026-10-20)
- Anthropic, Writing effective tools for agents: "Agents might call the wrong tools, call the right tools with the wrong parameters, call too few tools, or process tool responses incorrectly." https://www.anthropic.com/engineering/writing-tools-for-agents (verified)
- TRAIL (arXiv 2505.08638, 2025) has separate error types for poor information retrieval and tool output misinterpretation, and reports that the best model scored 11% at trace debugging. https://arxiv.org/abs/2505.08638 (verified from the abstract)
- Patronus Percival error taxonomy lists "Poor Information Retrieval" and "Tool Output Misinterpretation" as separate errors. https://docs.patronus.ai/docs/percival/error-taxonomy (verified)

## Run it

```
export GROQ_API_KEY=...   # free tier
python3 sorter/make_corpus.py   # note: rewrites queries.jsonl with q01-q32 only
OUT=runs/mine python3 sorter/agent.py
python3 sorter/label.py
python3 -m http.server -d docs
```

MIT license.
