# Fate API feedback evaluation

November 20, 2026 · Valhalla research prototype

Valhalla can checkpoint responses from an external model as Fate signals, replay those signals after a restart, and use the resulting candidate scores to change which approved passages enter a later model request. A hosted Qwen replay showed the passage set changing. The fresh Gemini pilot showed signal recovery and score changes with stable answers. Neither run established an improvement in final-answer accuracy from enabling feedback.

## Historical evidence

| Workflow | Evaluation | Observed result |
|---|---|---|
| Highest candidate versus local evidence completion | Frozen synthetic holdout, 12 requests | 2/12 versus 12/12 overall. The completion policy answered 7 supported requests and abstained on 5. |
| Highest admissible source versus local evidence completion | Full LoCoMo, 1,986 questions, paired within the historical run | Mean score rose from 0.0581 to 0.1863. On answerable questions the score rose from 0.0535 to 0.0688. On the adversarial category it rose from 7.4% to 59.2%. |
| Valhalla-controlled hosted Qwen feedback | One synthetic task, 5 paired rounds | On 3/5 rounds, feedback expanded the API request from one to two already-approved passages. Both arms answered all five rounds correctly. The verification reused identical hosted responses where available. |

The older completion workflow used a local semantic judge. Its largest measured gain came from handling adversarial questions. The later feedback workflow uses Fate to approve evidence and control the final release, with the external model acting inside the loop. In the Qwen case, the final output already included both original facts in both arms, so expanding the model request showed context selection changing without showing a gain in final answers. See the [frozen completion holdout and its runner](EVIDENCE_COMPLETION.md).

## Fresh Gemini pilot

The experiment used Gemini 3.5 Flash-Lite at temperature zero and the live evidence gateway. Two new synthetic scenarios covered eight rounds, including complementary source passages, an injected incorrect model draft, a process restart, document revision changes, and one request missing a required passage. The same exact provider requests shared cached responses. The pilot used 16 distinct generations and 16 token-count requests.

| Arm | Correct answer | Correct abstention | False abstention | Model input tokens across rounds |
|---|---:|---:|---:|---:|
| Gemini with all active passages | 7 | 1 | 0 | 3,397 |
| Gemini with BM25 under the Valhalla model evidence budget | 0 | 1 | 7 | 1,754 |
| Valhalla + Gemini, feedback off | 7 | 1 | 0 | 1,514 |
| Valhalla + Gemini, feedback on | 7 | 1 | 0 | 1,514 |

Both Valhalla arms released only original evidence. The enabled arm captured the injected draft as a signal, recovered it after the restart, and changed the ranking scores of the original candidates. The selected passages remained stable. When the active revision changed, the answer switched to the new values and the old signal was absent from the new revision's replay. When a required passage was removed, the gateway abstained before calling Gemini.

The Valhalla arms used about 55% fewer model input tokens than the full-passage baseline on these rounds. The token comparison describes model requests only. The BM25 budget is a matched allowance for passages in those requests. Valhalla's local verifier also accesses the corpus and can release a second verified passage even when Gemini receives only one.

## Partial LoCoMo evaluation

The Gemini run stopped at 163 of 1,986 questions, using contiguous prefixes from six conversations of the [official LoCoMo dataset](https://github.com/snap-research/locomo) and its answer-scoring functions. The checkpoint contains 62 multi-hop, 81 temporal, 18 open-domain, and 2 single-hop questions. It covers zero adversarial questions.

- Both feedback arms returned identical final answers and chose identical passages for the model. The enabled arm captured 40 responses, replayed history on 106 questions, and produced different candidate scores on 89 questions. Each of the 129 questions that called Gemini had only one approved passage in the model request.
- Both arms averaged 0.0375 token F1 on the released answers and abstained on 34 answerable questions. Gemini's intermediate drafts averaged 0.0586 using Valhalla-selected passages. On 89 questions, Gemini abstained while Valhalla released an original passage.
- Of 162 questions with annotated evidence, 30 had at least one annotated passage in the released answer. Mean annotated-evidence recall was 14.3%. One temporal question asked for the date of a specific visit. The final answer quoted a different conversation about a related group and supplied no evidence for the requested date.
- Rescoring historical outputs for the same 163 question IDs with the same answer scorer gives 0.0523 for the old completion policy and 0.0243 for its highest-source control. The old and new runs use different evidence policies and temporal prompts, so the matched-question result is descriptive.

The complete historical run and the Gemini checkpoint use different protocols and category mixes. The 0.0375 checkpoint score describes these 163 questions. The evidence annotations and error review show that selecting an authentic passage is possible even when it fails to support the exact entity, relation, or time the user asks about.

## Assessment

The prototype has demonstrated **version-bound evidence delivery, multi-passage answers to explicit facets, abstention in tested missing-evidence cases, and recoverable external-model feedback that can alter later model context**. Its strongest fit for further testing is versioned documentation with explicit facts and auditable citations. General conversational memory quality, reliable detection of insufficient evidence at scale, and sustained feedback-driven improvement remain unproven. Production readiness and performance parity with commercial memory products require broader comparative evaluation.

The next test should score factual sufficiency for each requested facet before measuring feedback gains. It should pair an initially incomplete request with a later request where the correct additional passage is available, then count newly recovered evidence, final-answer improvements, and drift under wrong feedback and version changes. Include real multi-hop and adversarial questions alongside synthetic diagnostics.

[Aggregate results and synthetic round observations](../tests/results/gemini_fate_feedback_2026-11-20.json)
