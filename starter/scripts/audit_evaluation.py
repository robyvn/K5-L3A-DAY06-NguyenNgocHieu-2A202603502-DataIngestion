import json
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"

with open(RESULTS_DIR / "strategy_A_traces.json", "r", encoding="utf-8") as f:
    traces_a = json.load(f)

with open(RESULTS_DIR / "strategy_B_traces.json", "r", encoding="utf-8") as f:
    traces_b = json.load(f)

with open(RESULTS_DIR / "strategy_C_traces.json", "r", encoding="utf-8") as f:
    traces_c = json.load(f)

print("Traces loaded successfully!")
test_a = [t for t in traces_a if t["split"] == "test"]
test_b = [t for t in traces_b if t["split"] == "test"]
test_c = [t for t in traces_c if t["split"] == "test"]

print(f"Test queries count: {len(test_a)}")

for i, q in enumerate(test_b):
    print(f"\n--- Test Question {q['question_id']} ({q['type']}) ---")
    print(f"Q: {q['question']}")
    print(f"Gold Page: {q['gold_page']}")
    print(f"Filter: {q['filter']}")
    print(f"Hit@1: A={test_a[i]['hit_at_1']}, B={test_b[i]['hit_at_1']}, C={test_c[i]['hit_at_1']}")
    print(f"Hit@3: A={test_a[i]['hit_at_3']}, B={test_b[i]['hit_at_3']}, C={test_c[i]['hit_at_3']}")
    print("Top 1 hit text snippet (Strat B):", repr(test_b[i]['top_hits'][0]['text'][:120]))

