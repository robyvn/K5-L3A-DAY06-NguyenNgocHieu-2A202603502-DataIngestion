"""Evaluate retrieved evidence and compute retrieval accuracy metrics."""
from typing import Any
import unicodedata
import re


def _normalize_eval_str(s: str) -> str:
    """Normalize string for robust quote matching."""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def check_hit(question: dict[str, Any], chunk: dict[str, Any]) -> bool:
    """Determine if a retrieved chunk matches the gold source, page, and contains the evidence quote."""
    # Check page alignment
    if chunk.get("page") != question.get("gold_page"):
        return False
        
    gold_quote = question.get("evidence_quote", "")
    chunk_text = chunk.get("text", "")
    
    norm_gold = _normalize_eval_str(gold_quote)
    norm_chunk = _normalize_eval_str(chunk_text)
    
    # Check if normalized evidence is inside normalized chunk
    if norm_gold in norm_chunk:
        return True
        
    # Also check key segments if quote is long (> 60 chars)
    words = norm_gold.split()
    if len(words) >= 8:
        # Check first 8 words and last 8 words
        first_segment = " ".join(words[:8])
        last_segment = " ".join(words[-8:])
        if first_segment in norm_chunk and last_segment in norm_chunk:
            return True
            
    return False


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check top-3 hits against gold evidence and record trace."""
    hit_at_1 = False
    hit_at_3 = False
    hit_ranks = []

    for rank, hit in enumerate(hits, start=1):
        is_hit = check_hit(question, hit)
        hit["is_hit"] = is_hit
        hit["rank"] = rank
        if is_hit:
            hit_ranks.append(rank)
            if rank == 1:
                hit_at_1 = True
            if rank <= 3:
                hit_at_3 = True

    return {
        "question_id": question["id"],
        "split": question["split"],
        "type": question["type"],
        "question": question["question"],
        "expected_answer": question["expected_answer"],
        "gold_page": question["gold_page"],
        "evidence_quote": question["evidence_quote"],
        "filter": question.get("filter"),
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hit_ranks": hit_ranks,
        "top_hits": [
            {
                "rank": h["rank"],
                "chunk_id": h["chunk_id"],
                "page": h["page"],
                "score": round(h["score"], 4),
                "is_hit": h["is_hit"],
                "text": h["text"],
                "metadata": h["metadata"]
            }
            for h in hits[:3]
        ]
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by split (dev / test / all)."""
    summary = {}
    
    for split_name in ["dev", "test", "all"]:
        if split_name == "all":
            subset = traces
        else:
            subset = [t for t in traces if t["split"] == split_name]
            
        total = len(subset)
        if total == 0:
            continue
            
        hit1_count = sum(1 for t in subset if t["hit_at_1"])
        hit3_count = sum(1 for t in subset if t["hit_at_3"])
        
        summary[split_name] = {
            "total_queries": total,
            "hit_at_1_count": hit1_count,
            "hit_at_1_ratio": f"{hit1_count}/{total}",
            "hit_at_1_pct": round((hit1_count / total) * 100, 2),
            "hit_at_3_count": hit3_count,
            "hit_at_3_ratio": f"{hit3_count}/{total}",
            "hit_at_3_pct": round((hit3_count / total) * 100, 2),
        }
        
    return summary
