"""Collect fate_grasp candidate series with grasp labels for gate analysis."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Ai\rogue-products\valhalla-server\tests")
sys.path.insert(0, r"C:\Ai\rogue-products\valhalla-server")
from run_extreme_stress import CONFIG, QUESTIONS, gen_corpus, post  # noqa: E402
from run_extreme_targeted import ENGINE, targeted  # noqa: E402

OUT = Path(r"C:\Ai\rogue-products\valhalla-server\tests\results_extreme\fate_series_labeled.json")
NEEDLE = {
    "n_start": "Project Aurora's internal codename is AUR-7.",
    "para1": "Project Aurora's internal codename is AUR-7.",
    "para2": "Project Aurora's internal codename is AUR-7.",
    "inject_q": "Project Aurora's internal codename is AUR-7.",
    "n_mid": "Project Borealis's satellite lead is Dr. Ines Halvorsen.",
    "n_end": "Project Aurora's flight test site is located near Reno, Nevada.",
}
MM_LINES = [
    "Project Aurora is a solar drone program led by Dr. Mara Voss.",
    "Project Borealis is a tidal sensor program led by Dr. Ilya Petrov.",
    "Project Aurora uses battery cells supplied by Helix Cells.",
    "Project Borealis uses pressure sensors supplied by Nordwave.",
    "Project Cygnus is led by Dr. Kenji Sato.",
    "Project Draco has a budget of 9.4 million euros.",
    "Project Lyra completed a review milestone in March.",
]
MM = [("q1", "Who leads Project Aurora?", 0), ("q2", "Who leads Project Borealis?", 1),
      ("q3", "Which company supplies battery cells for Project Aurora?", 2),
      ("q4", "Which company supplies pressure sensors for Project Borealis?", 3),
      ("q5", "Who leads Project Aurora and which company supplies its battery cells?", None),
      ("q8", "Who leads Project Zephyr?", None), ("q9", "Who leads Project Cygnus?", 4)]


def ask(qid, qtext, lines):
    b = post(ENGINE, {"questions": [{"id": qid, "text": qtext, "score_type": "open"}],
                      "config": CONFIG, "context": lines})
    return (b.get("rows") or [{}])[0]


out = []
for qid, q, exp in MM:
    r = ask(qid, q, MM_LINES)
    g = r.get("fate_grasp") or {}
    idx = r.get("retrieval_corpus_idx")
    out.append({"set": "mm", "id": qid, "fog": (r.get("fog_decision") or {}).get("decision"),
                "series": g.get("candidate_scores"), "frag_scores": g.get("fragment_scores"),
                "idx": idx, "needle_idx": exp, "grasp_ok": (idx == exp) if exp is not None else None})
corpus, _ = gen_corpus(806)
for qid, qtext, *_ in QUESTIONS:
    lines = targeted(qtext, corpus)
    r = ask(qid, qtext, lines)
    g = r.get("fate_grasp") or {}
    idx = r.get("retrieval_corpus_idx")
    needle = NEEDLE.get(qid)
    nidx = lines.index(needle) if needle in lines else None
    grasped = lines[idx] if isinstance(idx, int) and 0 <= idx < len(lines) else None
    out.append({"set": "ex", "id": qid, "fog": (r.get("fog_decision") or {}).get("decision"),
                "series": g.get("candidate_scores"), "frag_scores": g.get("fragment_scores"),
                "idx": idx, "needle_idx": nidx,
                "grasp_ok": (grasped == needle) if needle else None})
    print(qid, out[-1]["fog"], out[-1]["grasp_ok"], out[-1]["series"], flush=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {OUT}")
