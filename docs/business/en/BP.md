# Business Plan — VAL-LLM (Fusion + BOOST)

Rogue Intelligence INC · 2026-11-14 · English version (local draft, not final)

## 1. Executive summary
VAL-LLM is a structural enhancement layer for existing LLMs. The Fusion
layer gives a model of any window size an external factual memory of
≥15M tokens that is scale-invariant, zero-fabrication, poison-resistant
and auditably abstinent (all measured). The BOOST layer adds reasoning
operators — multihop, aggregation, verification (measured 17/21 → 20/21).
We do not sell "a smarter model"; we sell a **trustworthy** one: it never
answers recklessly, every answer can cite its evidence, and poisoning
does not flip it.

## 2. Product
- **VAL-LLM Fusion Framework** (public repo val-llm-fusion-framework):
  ValhallaBase structural runtime (the body) + LLM decode head; structure
  decomposed by layer depth and baked into the 24B weights (Tier-A patch,
  Δw≈0.604 @ s=0.08); gateway and direct forms; trimodal co-ingestion
  (text/audio/image) + feature grasp.
- **VAL-LLM BOOST Framework** (org repo VAL-LLM-BOOST-FRAMEWORK):
  spreading retrieval, deterministic aggregation operators, conflict
  surfacing, answer verification, offline adaptation.

## 3. Market
Customers with large corpora, high error cost, and audit requirements:
industrial/energy (procedures, manuals, work orders), legal/compliance
(contracts, case files), financial back office, government knowledge
bases. Common traits: corpora cannot go to public-cloud long-context
APIs, fabrication is unacceptable, errors must be traceable to evidence.

## 4. Competition & differentiation
Long-context models (dead beyond window, no audit), RAG frameworks
(no discipline), memory APIs (no verdicts, no trimodal single body),
GraphRAG (no grounding gate, no weight sedimentation). Six unique
points: see PITCH_DECK S5. Moat = structural runtime (Rust engine +
protocol) + verdict algebra + weight-baking pipeline + measured
evidence base.

## 5. Business model
1. On-prem deployment licensing (annual / per-cluster): engine +
   gateway + head adaptation + upgrades;
2. Model-enhancement engagements (project-based): customer base-model
   decomposition, baking, BOOST integration, customer-corpus
   regression suites;
3. Audit & support (annual): verdict-log analytics, evidence-chain
   review, compliance reporting.
Pricing anchors: **[TBD — to be set against target-industry budgets]**

## 6. Technology roadmap & milestones
- Done: full Fusion measurement (extreme tiers, trimodal, 14.95M
  tokens), BOOST three-operator validation (20/21), two public repos;
- Q1: BOOST into hybrid.resolve, conflict-surfacing channel,
  enumeration exemption;
- Q2: graph traversal, generalized iterative retrieval, engine
  multihop-decoder A/B;
- Q3: offline QA-feedback adaptation (Fate weights / bake v2),
  second decode-head adaptation (base-model independence check).

## 7. Risks & mitigations
- Technical: residual multihop (entity disambiguation) → graph
  traversal / specialized decoders; conflicts not yet surfaced →
  Q1 channel; LoCoMo-class long-dialogue memory not won →
  positioning discipline (sell trust, not dialogue recall) + BOOST
  cross-question write-back;
- Market: base vendors shipping long context / memory → we are the
  verdict layer, orthogonal to vendors, and scale with the head
  (stronger head, stronger us);
- Compliance: open-source vs commercial licensing boundary →
  tiered release of core protocol / production configs **[TBD legal]**.

## 8. Financials & financing
Raise amount, use of funds, forecasts: **[TBD — to be filled by the
founding team; this draft pre-fills no unconfirmed figures]**

## 9. Team
Rogue Intelligence INC. Members and bios: **[TBD]**
Contact: licensing@rogue-intelligence.com
