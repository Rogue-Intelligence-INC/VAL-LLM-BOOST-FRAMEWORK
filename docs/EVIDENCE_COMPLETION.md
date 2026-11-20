# Fate evidence completion

The November 20 evaluation covers the later Fate-controlled API feedback workflow, including a paired Gemini pilot, a partial LoCoMo run, and a comparison with the historical policy. See [Fate API feedback evaluation](FATE_API_FEEDBACK_EVALUATION_20261120.md).

The experimental `evidence_completion` policy starts with Fate's highest admissible candidate and a small pool of nearby or coupled candidates. A local semantic judge selects original source lines only when they cover every requested fact. An explicit abstention triggers at most one recheck of the same evidence with stable ordering and prompt-local IDs. An accepted answer consists of the selected original lines with their citations.

## Fresh synthetic holdout · November 19, 2026

The previous 16-request development replay finished at 16/16 with completion and 7/16 with the highest candidate alone. The holdout below uses a different corpus and 12 new questions. The gateway policy, prompt, and thresholds were frozen before the first holdout request and left unchanged throughout the run.

| Case family | Highest candidate only | Evidence completion |
|---|---:|---:|
| Version scope and conflicts | 1/4 | 4/4 |
| Two-source complement | 0/4 | 4/4 |
| Insufficient evidence | 1/4 | 4/4 |
| **Overall** | **2/12** | **12/12** |

The two policies shared the same native Fate response for each request. The highest-candidate control returned six incorrect or incomplete answers and abstained five times. Completion answered all seven requests with sufficient evidence and abstained on the remaining five. Those five included an unresolved conflict between equally authoritative release records in the same revision. All seven completed answers were checked against the exact cited lines and active document metadata.

The run used the real local HTTP gateway with Mistral Small 3.1 24B Instruct Q4_K_M as the local judge, at temperature zero. Five rechecks brought the total to 17 local judge calls. The run used zero external model calls. Every cited holdout line was in the direct Fate candidate set, so this run does not isolate a gain from coupled-container expansion. These results describe a small synthetic fixture and do not establish a production error rate or an external benchmark score.

## Reproduction

Use a running Valhalla gateway that accepts `/v1/evidence/activate` and `/v1/evidence/ask` with `answer_policy` set to `evidence_completion`. The gateway needs a configured local judge. `VALHALLA_COMPLETION_PORT` and `VALHALLA_COMPLETION_MODEL` control its loopback port and model alias. If the gateway requires authentication, set `VALHALLA_GATEWAY_KEY` in the runner's environment.

```powershell
python -B tools/check_evidence_completion_holdout.py --gateway http://127.0.0.1:18780 --output output/evidence-completion-holdout.json
```

The runner creates fresh test sessions, sends just the question at query time, and checks the result against the frozen labels. It requires only the Python standard library. Local model files and gateway runtime are prerequisites.

- [Frozen fixture](../tests/fixtures/evidence_completion_holdout_2026-11-19.json) with SHA-256 `2e206db96f58d562746b43bd977e2f1653d0d8aa82a23da089f2bc9bd6c2cb2e`
- [Holdout runner](../tools/check_evidence_completion_holdout.py)
- Evidence completion policy SHA-256 `6a71609a5cbe1b05d540e0a8067857a1437225391e2faf8f4b753358ac8b37bd`
