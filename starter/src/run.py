"""Pipeline orchestration: Ingestion, Chunking, Embedding, Vector Storage & Benchmark Evaluation."""
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

from .ingestion import load_pdf
from .chunking import fixed_size, by_paragraph
from .embeddings import MyEmbedder
from .store import PgVectorStore
from .evaluation import evaluate_query, summarize


def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    env_path = root_dir / ".env"
    load_dotenv(env_path)

    db_url = os.getenv("DATABASE_URL", "postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab")
    pdf_path = root_dir / "data" / "luat_duong_bo_35_2024_qh15.pdf"
    benchmark_path = root_dir / "data" / "benchmark_questions.json"
    results_dir = root_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("DAY 06 · DATA INGESTION ENGINEERING PIPELINE")
    print("=" * 60)

    # 1. Load Corpus
    print("\n[Step 1/5] Loading and normalizing PDF corpus...")
    start_time = time.time()
    pages = load_pdf(pdf_path, document_id="luat_duong_bo_2024", source="luat_duong_bo_35_2024_qh15.pdf")
    non_empty_pages = [p for p in pages if not p.metadata.get("is_empty")]
    total_chars = sum(p.metadata["char_count"] for p in pages)
    print(f"  -> Total physical pages: {len(pages)}")
    print(f"  -> Valid content pages: {len(non_empty_pages)} (Requirement >= 30: {'PASS' if len(non_empty_pages) >= 30 else 'FAIL'})")
    print(f"  -> Total characters normalized: {total_chars:,}")

    # 2. Load Benchmark Questions
    print("\n[Step 2/5] Loading benchmark questions...")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    dev_q = [q for q in questions if q["split"] == "dev"]
    test_q = [q for q in questions if q["split"] == "test"]
    filter_q = [q for q in questions if q.get("filter")]
    print(f"  -> Total questions: {len(questions)} ({len(dev_q)} dev / {len(test_q)} test)")
    print(f"  -> Questions with metadata filter: {len(filter_q)} (Requirement >= 3: {'PASS' if len(filter_q) >= 3 else 'FAIL'})")

    # 3. Initialize Embedder and Store
    print("\n[Step 3/5] Initializing Embedding Model & Vector Store...")
    model_name = "google/embeddinggemma-2"
    embedder = MyEmbedder(model_name=model_name)
    print(f"  -> Model: {model_name}")
    print(f"  -> Embedding dimensions: {embedder.dimensions}")

    store = PgVectorStore(database_url=db_url, dimensions=embedder.dimensions)
    store.create_schema()
    print("  -> PostgreSQL + pgvector schema created successfully.")

    # 4. Generate Chunks and Ingest for Strategy A, B, C
    print("\n[Step 4/5] Chunking and Indexing 3 Data Strategies...")
    
    # Strategy A: Fixed-size (500 chars, overlap 50)
    print("  -> Building Strategy A (Fixed-size: 500 chars, overlap 50)...")
    chunks_a = []
    for p in pages:
        chunks_a.extend(fixed_size(p, size=500, overlap=50))
    print(f"     Total chunks A: {len(chunks_a)}")
    vectors_a = embedder.embed_documents([c.text for c in chunks_a])
    store.upsert("A", chunks_a, vectors_a)
    print("     Indexed Strategy A in pgvector.")

    # Strategy B: Structure-aware / Paragraph (max_size=800)
    print("  -> Building Strategy B (Structure / Article-based: max 800 chars)...")
    chunks_b = []
    for p in pages:
        chunks_b.extend(by_paragraph(p, max_size=800))
    print(f"     Total chunks B: {len(chunks_b)}")
    vectors_b = embedder.embed_documents([c.text for c in chunks_b])
    store.upsert("B", chunks_b, vectors_b)
    print("     Indexed Strategy B in pgvector.")

    # Strategy C: Same chunks as B, but with metadata filter enabled at retrieval time
    print("  -> Building Strategy C (Structure-aware + Metadata Filter)...")
    chunks_c = []
    for c in chunks_b:
        c_copy = type(c)(
            chunk_id=c.chunk_id.replace("_struct_", "_stratC_"),
            document_id=c.document_id,
            source=c.source,
            page=c.page,
            text=c.text,
            metadata=dict(c.metadata)
        )
        c_copy.metadata["strategy"] = "C"
        chunks_c.append(c_copy)
    store.upsert("C", chunks_c, vectors_b)
    print("     Indexed Strategy C in pgvector.")

    # 5. Evaluate Benchmark across Strategies
    print("\n[Step 5/5] Running top-3 retrieval benchmark across all strategies...")
    
    all_summaries = {}
    
    # Pre-embed question queries
    print("  -> Pre-computing question embeddings...")
    q_vectors = {q["id"]: embedder.embed_query(q["question"]) for q in questions}

    for strat_key in ["A", "B", "C"]:
        print(f"  -> Evaluating Strategy {strat_key}...")
        traces = []
        for q in questions:
            q_vec = q_vectors[q["id"]]
            filters = q.get("filter") if strat_key == "C" else None
            hits = store.search(strategy=strat_key, query_vector=q_vec, top_k=3, filters=filters)
            trace = evaluate_query(q, hits)
            traces.append(trace)

        # Save individual strategy trace
        trace_file = results_dir / f"strategy_{strat_key}_traces.json"
        with open(trace_file, "w", encoding="utf-8") as f:
            json.dump(traces, f, ensure_ascii=False, indent=2)

        summary = summarize(traces)
        all_summaries[strat_key] = summary

    # Save summary report
    summary_file = results_dir / "benchmark_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(all_summaries, f, ensure_ascii=False, indent=2)

    elapsed = round(time.time() - start_time, 2)
    print(f"\nPipeline finished in {elapsed}s!")
    print(f"Results saved to: {results_dir}\n")

    # Print Final Markdown Results Table
    print("=" * 60)
    print("BENCHMARK RETRIEVAL METRICS SUMMARY")
    print("=" * 60)
    print(f"{'Strategy':<12} | {'Split':<6} | {'Hit@1 (Ratio)':<16} | {'Hit@1 (%)':<10} | {'Hit@3 (Ratio)':<16} | {'Hit@3 (%)':<10}")
    print("-" * 80)
    for s_key in ["A", "B", "C"]:
        for split in ["dev", "test", "all"]:
            d = all_summaries[s_key][split]
            print(f"Strategy {s_key:<3} | {split:<6} | {d['hit_at_1_ratio']:<16} | {d['hit_at_1_pct']:<10.1f} | {d['hit_at_3_ratio']:<16} | {d['hit_at_3_pct']:<10.1f}")
        print("-" * 80)


if __name__ == "__main__":
    main()
