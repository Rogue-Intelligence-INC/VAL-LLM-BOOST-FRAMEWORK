# Due Diligence Pack — VAL-LLM

Rogue Intelligence INC · 2026-11-14 · English version
Purpose: let investors / customers trace every claim to a reproducible artifact.

## 1. Claim → evidence index

| Claim | Artifact | Location |
|---|---|---|
| 17/21 flat across 0.45M/1.5M/14.95M tokens, 0 fabricated | enhancement_ceiling_lines{30006,100006,1000006}.json | val-llm-fusion-framework/tests/results_extreme |
| Extreme tiers 806/3006/10006: hybrid 12/12 | extreme_targeted_lines*.json, extreme_rerun2.log | same |
| Injection immunity (before/after) | Report §11.7 + quarantine rule in hybrid.py | docs/MISTRAL24_VS_VALHALLA_UNIQUE_POINTS_20261113.md |
| Trimodal 9/9, feature grasp | multimodal_fixed.json, mm_fixed5.log, probe_grasp_cos.py | tests/ |
| BOOST 17→20/21, three versions compared | boost_adapt_lines100006.json, boost_adapt{,2,3,4}.log | tests/results_extreme |
| Fate verdicts with algebraic reasons, live | probe_fate_gateway.py output, fate_telemetry field | valhalla_server/app.py |
| Bake Δw≈0.604, 40 layers, fate_converged | data/decode_heads.json (mistral24-auto-v1) | val-llm-fusion-framework/data |
| multihop_fate/v2 slice 15/25 (internal precedent) | multihop_rag_hybrid_test.json | valhalla-unified-core/reports |
| Multiplier set: 912× window / 331× beyond death point / ~83,000× per-question reach / 17.5× wire | Derived from enhancement_ceiling_lines1000006.json (est_tokens=14,945,110, session_wire_mb=3.42, lines=1,000,026) against the 16,384-token window | same + definitions in this table |
| 470× link compression (incubation, reachability cost disclosed) | Main-project incubation measurement 19,858,861 → 42,199 | Valhalla-main incubation experiments |

Reproduction environment: Windows 11, i9-14900KF, RTX 4090,
Mistral-24B Q4_K_M (llama.cpp, 16K ctx), valhalla_base v1.1.0.

## 2. Architecture at a glance
Corpus → targeted line selection → ValhallaBase session (Fate verdict
emit/abstain with algebraic margin) → evidence hygiene (in-session
sourcing, injection quarantine, bundling) → Mistral-24B decode head
verbalizes; multimodal via co-ingestion + gateway feature grasp;
BOOST operators (spreading / aggregation / intent gate) at the
evidence layer, validated, pending integration into resolve.

## 3. Known limitations (honest list — primary diligence checkpoints)
1. LoCoMo-15: Valhalla 0/15 vs RAG 9/15, Mem0 5/15 — not won; we do
   not claim long-dialogue memory leadership;
2. Multihop: 1/2 after BOOST; residual hop_employer (bridge name with
   ~90 same-name filler lines — entity disambiguation); failure mode
   is abstention, not a wrong guess;
3. Conflicting facts: silently picks the later value (HAL-2);
   conflict surfacing is on the Q1 roadmap;
4. Proactive emission: not implemented under official-protocol review
   on this machine (only the abstention half holds); never marketed;
5. Feature grasp: same-file re-identification measured; cross-instance
   (re-recorded / re-shot) not yet measured;
6. Encoders are product-layer adapters (local CLIP ViT-H / segment-mel,
   384-d contract), not an engine-native aligned space;
7. All tests single-machine, mostly synthetic corpora + official-suite
   subsets; generalization to real customer corpora awaits pilots;
8. Runtime Fate weights are fixed (fate_weight_mode:"fixed"); online
   learning not implemented; offline adaptation is Q3 roadmap.

## 4. IP & open-source boundary
- Public: Rogue-Intelligence-INC/val-llm-fusion-framework and
  VAL-LLM-BOOST-FRAMEWORK (analysis + measured code);
- The valhalla_base engine is the org's own Rust runtime (protocol
  valhalla-base-v1 v1.1.0); the decode head is Mistral-24B weights
  (under its upstream license) + our baked patch;
- Commercial vs open boundary: **[TBD legal — written terms govern
  during diligence]**.

## 5. Diligence Q&A
Q: How is this different from GraphRAG? A: Graphs are one of five
components; unique to us are the Fate grounding verdict (abstention
with algebraic reasons), weight-bake sedimentation, and feature grasp.
Q: Does it survive a base-model swap? A: Fusion is orthogonal to the
head (internal MCQ ladder 0.5B→3B already shows scaling); a second-head
adaptation is a Q3 milestone — no figures promised before measurement.
Q: Why sell memory if LoCoMo loses? A: We sell "never answer recklessly
+ every answer evidenced"; long-dialogue recall is a different race
and we do not claim it.
Q: What exactly does "zero fabrication" cover? A: Codename/number
tokens asserted in answers must exist in the corpus (script-audited
definition). A poisoned source is a different risk class, handled by
evidence hygiene; corpus truthfulness itself is out of scope.

## 6. Materials to be added (before final)
Team bios, financial forecasts, financing terms, pilot customer list,
legal opinions. — None pre-filled; the founding team's final version governs.
