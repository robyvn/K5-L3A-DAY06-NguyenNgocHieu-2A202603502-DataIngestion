import os
import sys
import json
import time
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))
from dotenv import load_dotenv

from src.embeddings import MyEmbedder
from src.store import PgVectorStore
from src.evaluation import evaluate_query, summarize

root_dir = Path(__file__).resolve().parents[1]
load_dotenv(root_dir / ".env")

db_url = os.getenv("DATABASE_URL")
benchmark_path = root_dir / "data" / "benchmark_questions.json"
results_dir = root_dir / "results"

with open(benchmark_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

embedder = MyEmbedder(model_name="google/embeddinggemma-2")
store = PgVectorStore(database_url=db_url, dimensions=embedder.dimensions)

print("Pre-computing query embeddings...")
q_vectors = {q["id"]: embedder.embed_query(q["question"]) for q in questions}

all_summaries = {}
for strat_key in ["A", "B", "C"]:
    print(f"Evaluating Strategy {strat_key}...")
    traces = []
    for q in questions:
        q_vec = q_vectors[q["id"]]
        filters = q.get("filter") if strat_key == "C" else None
        hits = store.search(strategy=strat_key, query_vector=q_vec, top_k=3, filters=filters)
        trace = evaluate_query(q, hits)
        traces.append(trace)

    trace_file = results_dir / f"strategy_{strat_key}_traces.json"
    with open(trace_file, "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    summary = summarize(traces)
    all_summaries[strat_key] = summary

summary_file = results_dir / "benchmark_summary.json"
with open(summary_file, "w", encoding="utf-8") as f:
    json.dump(all_summaries, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("BENCHMARK RETRIEVAL METRICS SUMMARY (AFTER CASE-INSENSITIVE FILTER)")
print("=" * 60)
print(f"{'Strategy':<12} | {'Split':<6} | {'Hit@1 (Ratio)':<16} | {'Hit@1 (%)':<10} | {'Hit@3 (Ratio)':<16} | {'Hit@3 (%)':<10}")
print("-" * 80)
for s_key in ["A", "B", "C"]:
    for split in ["dev", "test", "all"]:
        d = all_summaries[s_key][split]
        print(f"Strategy {s_key:<3} | {split:<6} | {d['hit_at_1_ratio']:<16} | {d['hit_at_1_pct']:<10.1f} | {d['hit_at_3_ratio']:<16} | {d['hit_at_3_pct']:<10.1f}")
    print("-" * 80)
