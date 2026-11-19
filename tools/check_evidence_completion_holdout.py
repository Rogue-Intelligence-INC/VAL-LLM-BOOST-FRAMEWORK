"""Run a frozen synthetic holdout against a live Valhalla evidence gateway."""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from uuid import uuid4


FIXTURE = Path(__file__).resolve().parents[1] / "tests/fixtures/evidence_completion_holdout_2026-11-19.json"


def call(base, route, key, payload):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = Request(base.rstrip("/") + "/v1/evidence/" + route,
                      data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urlopen(request, timeout=100) as response:
        return json.load(response)


def grade(indices, answer, originals, expected):
    if any(type(index) is not int or not 0 <= index < len(originals) for index in indices):
        raise ValueError("Answer refers to an invalid source line")
    chosen = [originals[index] for index in indices]
    source_ids = [source["id"] for source in chosen]
    if len(set(source_ids)) != len(source_ids):
        raise ValueError("Answer repeats a source")
    hits = [source["id"] for source in chosen if source["id"] in expected and source["value"] in answer]
    return {"correct": set(source_ids) == set(hits) == set(expected), "answered": bool(indices),
            "source_ids": source_ids, "gold_hits": hits}


def verify_citations(body, original, active_document):
    citations = body.get("citations") or []
    if body["decision"] == "abstain":
        if citations or body.get("citation") is not None:
            raise ValueError("Abstention must not cite sources")
        return []
    if body["decision"] != "answer" or not citations:
        raise ValueError("Unrecognized or uncited answer")
    if body.get("citation") != citations[0] or body["answer"] != "\n".join(c["text"] for c in citations):
        raise ValueError("Answer is not composed of its cited original lines")
    indices = []
    for citation in citations:
        line = citation["line"]
        if type(line) is not int or not 1 <= line <= len(original) or citation["text"] != original[line - 1]["text"]:
            raise ValueError("Citation text or line does not match the supplied original")
        if any(citation[field] != active_document[field] for field in ("title", "version", "revision_id")):
            raise ValueError("Citation metadata does not match the active document")
        indices.append(line - 1)
    return indices


def run(gateway, key, output):
    raw_fixture = FIXTURE.read_bytes()
    fixture = json.loads(raw_fixture)
    documents = fixture["documents"]
    for case in fixture["cases"]:
        available = {source["id"]: source for source in documents[case["document"]]}
        for source_id in case["expected"]:
            source = available[source_id]
            if not source["value"] or source["value"] not in source["text"]:
                raise ValueError(f"Unverifiable gold for {case['id']}")

    prefix = "holdout-" + uuid4().hex[:12]
    active = {}
    records = []
    for case in fixture["cases"]:
        document = case["document"]
        original = documents[document]
        session_id = f"{prefix}-{document}"
        if document not in active:
            result = call(gateway, "activate", key, {"session_id": session_id, "title": document,
                                                     "version": fixture["name"],
                                                     "text": "\n".join(source["text"] for source in original)})
            active[document] = result["document"]
        body = call(gateway, "ask", key, {"session_id": session_id, "question": case["question"],
                                         "answer_policy": "evidence_completion"})
        if body.get("question_context_lines") != 0:
            raise ValueError("Query unexpectedly re-sent evidence")
        trace = body["completion"]
        if trace["reason"] in {"local_judge_failed", "invalid_evidence_selection"}:
            raise RuntimeError(f"{case['id']} invalid test response: {trace['reason']}")
        primary = trace["primary"]
        highest = grade(primary.get("sources", []), primary.get("answer", ""), original, case["expected"])
        sources = verify_citations(body, original, active[document])
        completed = grade(sources, body["answer"], original, case["expected"])
        candidate_sources = {original[item["id"]]["id"] for item in trace["candidates"]}
        records.append({**case, "highest": highest, "completion": completed,
                        "missing_candidate_sources": sorted(set(case["expected"]) - candidate_sources),
                        "judge_attempts": trace["judge_attempts"], "response": body})
        print(f"{case['id']} highest={highest['correct']} completion={completed['correct']}", flush=True)

    groups = defaultdict(list)
    for row in records:
        groups[row["category"]].append(row)
    groups["all"] = records
    totals = {group: {"count": len(rows),
                      **{arm: {"correct": sum(row[arm]["correct"] for row in rows),
                               "wrong_answers": sum(row[arm]["answered"] and not row[arm]["correct"] for row in rows),
                               "abstained": sum(not row[arm]["answered"] for row in rows)}
                         for arm in ("highest", "completion")}}
              for group, rows in groups.items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"fixture_sha256": sha256(raw_fixture).hexdigest(), "metrics": totals,
                                  "local_judge_calls": sum(row["judge_attempts"] for row in records),
                                  "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(totals, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gateway", required=True, help="Base URL of a gateway with evidence completion enabled")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.gateway, os.environ.get("VALHALLA_GATEWAY_KEY"), args.output)
