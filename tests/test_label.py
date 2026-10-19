import sys; sys.path.insert(0, "sorter")
from label import label_v0, label_v1

def t(steps, answer=None, correct=False, gold="p1"):
    return {"steps": steps, "answer": answer, "correct": correct, "gold": gold}
S = lambda ids: {"type": "tool", "name": "search", "args": {}, "result": [{"id": i} for i in ids]}
O = lambda i: {"type": "tool", "name": "open_profile", "args": {}, "result": {"id": i}}

def test_pass():
    assert label_v1(t([S(["p1"])], {"id": "p1"}, True)) == "pass"
def test_never_seen_is_retrieval():
    assert label_v1(t([S(["p2", "p3"])])) == "retrieval_miss"
def test_seen_in_search_is_misuse():
    assert label_v1(t([S(["p2", "p1"]), O("p2")], {"id": "p2"})) == "tool_misuse"
def test_opened_but_no_answer_is_misuse():
    assert label_v1(t([S(["p1"]), O("p1")])) == "tool_misuse"
def test_v0_calls_no_answer_retrieval_even_when_seen():
    assert label_v0(t([S(["p1"]), O("p1")])) == "retrieval_miss"
