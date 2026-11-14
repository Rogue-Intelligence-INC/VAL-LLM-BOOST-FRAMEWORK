# Pitch Deck — VAL-LLM (Fusion + BOOST)

Rogue Intelligence INC · 2026-11-14 · English version
All figures are from on-machine measured artifacts; see DD.md for the evidence index.

## S1 Cover
**A structural skeleton that keeps any LLM from fabricating.**
Valhalla structural runtime + an LLM decode head: beyond-window memory,
zero fabrication, auditable abstention — plus an emerging reasoning
layer (BOOST). We don't train bigger models; we make existing models
**trustworthily stronger**.

## S2 Problem
Three walls for enterprise LLM deployment:
- **Window wall**: private corpora run to millions of tokens; they don't
  fit in context, and forcing them in is expensive;
- **Fabrication wall**: RAG feeds raw text back to the model, which still
  invents facts — and a single injected SYSTEM NOTE line can hijack answers;
- **Audit wall**: "I don't know" comes from prompting; it cannot be
  evidenced or traced.

## S3 Solution (two layers)
- **Fusion layer (measured)**: ValhallaBase structural runtime as the body,
  the LLM only as decode head; structure decomposed by layer depth and
  baked into the 24B weights (Tier-A patch).
- **BOOST layer (in development)**: spreading retrieval + deterministic
  aggregation + verification discipline — upgrading "memory" into
  "reasoning memory" (measured 17/21 → 20/21).

## S4 Measured headline metrics (same machine, questions, decode head)
| Metric | VAL-LLM | Baseline |
|---|---|---|
| QA over a 14.95M-token corpus | 17/21, 0 fabricated | 16K-window model dies at 45K tokens (0/13) |
| Prompt-injection (one poisoned line) | Immune | Full-context hijacked; plain RAG poisoned |
| Abstention on absent facts | 4/4, with auditable algebraic reasons | Plain RAG 3/4 |
| Trimodal (text/audio/image, one session) | 9/9 incl. feature grasp | Caption-RAG cannot accept features at all |
| BOOST reasoning layer | 20/21 (multihop 0→1/2, aggregation 0→2/2) | Baseline 17/21 |

## S4b The multiplier view (every ratio shows its numerator and denominator)

| Ratio | Definition | Status |
|---|---|---|
| **912×** | Measured working corpus 14,945,110 tokens ÷ decode head's native 16,384-token window | Measured — thousand-fold-class context |
| **331×** | Same ÷ the full-context arm's death point at 45,093 tokens (where it scored 0/13) | Measured — 331× beyond where the baseline flatlines |
| **~83,000×** | Lines touched per question: 1,000,026-line corpus vs ≤12 evidence lines | Measured — each question reads ~1/100,000 of the corpus |
| **1,240×** | Corpus growth 806 → 1,000,026 lines while session lines stay 27→28, wire 1.34→3.42MB | Measured — cost decoupled from corpus size |
| **17.5×** | Session wire 3.42MB vs ~59.8MB raw corpus text | Measured — the on-wire form of memory |
| **470×** | Incubation links 19,858,861 → 42,199 (main-project measurement; long-range reachability tradeoff disclosed) | Internal measurement — structural compression |
| **8×** | fate_link group-8 fragments 40 → 5 | Measured (Report §11.9) |

Potential (not measured, mechanism only): the protocol contains no
corpus-size term — the next tier, 10M lines, is ~9,120× the window;
the bottleneck is client-side selection indexing, not the engine.
External wording may say "912× measured, thousand-fold class" —
never present the potential tier as measured.

## S5 Why us (unique points ★)
1. Trimodal co-ingestion under a single Fate verdict — competitors store
   captions, not adjudicated multimodal facts;
2. Feature grasp: re-identifying ingested media by raw audio/image
   features — structurally impossible for caption-RAG;
3. Beyond-window working set: flat accuracy to ~15M tokens, session cost
   decoupled from corpus size (~3.4MB constant);
4. Zero fabrication + auditable abstention: abstention is a verdict
   artifact with algebraic reasons, not a prompted behavior;
5. Source-poisoning immunity: defense sits before decoding — the
   structural blind spot of feed-it-all-back RAG;
6. Structure baked into weights: memory becomes a model asset
   (Δw patch), not an external index.

## S6 Competitive landscape
- Long-context models: unbeatable in-window, dead beyond it, costly, no audit;
- RAG frameworks: recall without discipline (fabrication/poisoning/abstention
  all left to prompts);
- Memory APIs (Mem0/Zep/Letta): storage layer, no structural verdicts,
  no trimodal single body;
- GraphRAG class: strong graph traversal, no grounding gate, no weight baking.
Our position: the **structural verdict layer** in front of any decode head —
orthogonal to model vendors, never competing with them.

## S7 Honest boundaries (disclosed up front)
LoCoMo-15 not won (0/15 vs RAG 9/15); one residual multihop question
(entity disambiguation); conflicting facts not yet surfaced (mechanism
located); proactive emission not implemented and never marketed.
A team that prints its boundaries in the deck is a team you can trust
with "zero fabrication".

## S8 Business model
- On-prem enterprise licensing (annual / per-cluster): regulated
  industries, industrial, legal;
- Model-enhancement engagements: structural decomposition + baking +
  BOOST integration for customer base models;
- Audit & support services: verdict logs, evidence chains, compliance review.

## S9 Roadmap
- Q1: BOOST into hybrid.resolve (enumeration exemption + operator
  pass-through), conflict surfacing;
- Q2: Graph traversal + generalized iterative retrieval, engine
  multihop-decoder A/B;
- Q3: Offline QA-feedback adaptation (Fate weights / bake v2),
  multi-customer corpus regression suites.

## S10 Team & financing
Team: Rogue Intelligence INC (licensing@rogue-intelligence.com).
Raise amount / valuation / milestones: **[TBD — to be filled by the
founding team; no figures pre-filled]**

## Speaker notes
- Linger on S4: every number is reproducible on site (repos + scripts + logs);
- If asked about LoCoMo: concede it — we win "never answer recklessly",
  not long-dialogue recall;
- If asked vs GraphRAG: they do graphs; we do verdicts + graphs + weight sedimentation.
