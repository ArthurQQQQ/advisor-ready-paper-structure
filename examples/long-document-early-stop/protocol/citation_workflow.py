#!/usr/bin/env python3
"""Shared prefix citation gate and offline replay of human development labels."""

import argparse
from dataclasses import dataclass
import hashlib
from itertools import zip_longest
import json
from pathlib import Path
from typing import Callable, Optional


@dataclass(frozen=True)
class Paragraph:
    id: str
    text: str


@dataclass(frozen=True)
class Prefix:
    qid: str
    question: str
    body_tokens: int
    eof: bool
    text: str
    paragraphs: tuple[Paragraph, ...]


@dataclass(frozen=True)
class Claim:
    text: str
    paragraph_ids: tuple[str, ...]


@dataclass(frozen=True)
class Candidate:
    answer: str = ""
    claims: tuple[Claim, ...] = ()
    gap: str = ""


@dataclass(frozen=True)
class Judgment:
    supported: bool
    reason: str


@dataclass(frozen=True)
class Result:
    paragraph_ids: tuple[str, ...]
    answer: Optional[str]
    reason: str

    @property
    def passed(self):
        return self.answer is not None


def evaluate_checkpoint(
    prefix: Prefix,
    generate: Callable[[Prefix], Candidate],
    verify: Callable[[Prefix, Candidate], Judgment],
) -> Result:
    """Generate once, check source eligibility, then get a semantic judgment."""
    candidate = generate(prefix)
    if candidate.gap or not candidate.answer.strip() or not candidate.claims:
        return Result((), None, candidate.gap or "No complete answer was supplied.")
    if any(not claim.text.strip() or not claim.paragraph_ids for claim in candidate.claims):
        return Result((), None, "A material claim has no linked evidence.")
    requested = {pid for claim in candidate.claims for pid in claim.paragraph_ids}
    visible = tuple(paragraph.id for paragraph in prefix.paragraphs)
    unavailable = requested.difference(visible)
    if unavailable:
        reason = "Paragraphs not fully visible: " + ", ".join(sorted(unavailable))
        return Result((), None, reason)
    judgment = verify(prefix, candidate)
    if not judgment.reason.strip():
        raise ValueError("The semantic verifier must provide a reason.")
    if not judgment.supported:
        return Result((), None, judgment.reason)
    return Result(tuple(pid for pid in visible if pid in requested), candidate.answer, judgment.reason)


def iter_prefixes(path: Path, question: dict, document: dict, step: int):
    """Reconstruct each visible prefix from deltas and release full paragraph IDs."""
    spans = iter(document["paragraphs"].items())
    pending = next(spans, None)
    body = bytearray()
    paragraphs = []
    last_tokens = 0
    last_paragraph_end = 0
    eof = False
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            tokens, observed_eof = event["body_tokens"], event["eof"]
            if eof or not isinstance(observed_eof, bool) or type(tokens) is not int:
                raise ValueError(f"Invalid checkpoint at {path.name}:{tokens}")
            width = tokens - last_tokens
            if not 0 < width <= step or (not observed_eof and width != step):
                raise ValueError(f"Checkpoint off the shared grid at {path.name}:{tokens}")
            body.extend(event["text_delta"].encode("utf-8"))
            newly_citable = []
            while pending and pending[1]["end_byte_exclusive"] <= len(body):
                pid, span = pending
                start, end = span["start_byte"], span["end_byte_exclusive"]
                separator = b"\n\n" if paragraphs else b""
                if start != last_paragraph_end + len(separator) or start >= end:
                    raise ValueError(f"Invalid paragraph bounds for {pid}")
                if body[last_paragraph_end:start] != separator:
                    raise ValueError(f"Wrong separator before {pid}")
                paragraphs.append(Paragraph(pid, body[start:end].decode("utf-8")))
                last_paragraph_end = end
                newly_citable.append(pid)
                pending = next(spans, None)
            if newly_citable != event["newly_citable"]:
                raise ValueError(f"Citation release mismatch at {path.name}:{tokens}")
            eof, last_tokens = observed_eof, tokens
            yield Prefix(
                question["qid"], question["question"], tokens, eof,
                body.decode("utf-8"), tuple(paragraphs),
            )
    if not eof or pending or last_tokens != document["body_tokens"] or last_paragraph_end != len(body):
        raise ValueError(f"Incomplete stream: {path.name}")
    if hashlib.sha256(body).hexdigest() != document["body_sha256"]:
        raise ValueError(f"Body hash mismatch: {path.name}")


def manual_candidate(entry: dict) -> Candidate:
    """The original journal links a whole answer to its cited paragraph group."""
    answer = entry.get("answer", "")
    if not answer:
        return Candidate(gap=entry["reason"])
    return Candidate(answer, (Claim(answer, tuple(entry["paragraphs"])),))


def replay_question(path, question, document, journal, step):
    checks = []
    prefixes = iter_prefixes(path, question, document, step)
    for prefix, entry in zip_longest(prefixes, journal["checks"]):
        if prefix is None or entry is None:
            raise ValueError(f"Stream and journal have different lengths for {question['qid']}")
        if (prefix.body_tokens, prefix.eof) != (entry["body_tokens"], entry["eof"]):
            raise ValueError(f"Journal has the wrong checkpoint for {question['qid']}")
        if entry["verdict"] not in {"PASS", "CONTINUE"}:
            raise ValueError(f"Invalid manual verdict for {question['qid']}")

        def generate(_prefix):
            return manual_candidate(entry)

        def verify(_prefix, _candidate):
            return Judgment(entry["verdict"] == "PASS", entry["reason"])

        result = evaluate_checkpoint(prefix, generate, verify)
        entry_output = {
            "body_tokens": prefix.body_tokens,
            "eof": prefix.eof,
            "verdict": "PASS" if result.passed else "CONTINUE",
            "paragraphs": list(result.paragraph_ids),
            "reason": result.reason,
        }
        if result.passed:
            entry_output["answer"] = result.answer
        visible = {paragraph.id: paragraph.text for paragraph in prefix.paragraphs}
        checks.append({
            **entry_output,
            "sources": [{"id": pid, "text": visible[pid]} for pid in result.paragraph_ids],
        })
    if len(checks) != document["checkpoint_count"]:
        raise ValueError(f"Unexpected number of checkpoints for {question['qid']}")

    first_index = next((i for i, check in enumerate(checks) if check["verdict"] == "PASS"), None)
    if first_index is None:
        first, previous = None, None
    else:
        first = checks[first_index]
        previous = checks[first_index - 1] if first_index else {
            "body_tokens": 0,
            "scheduled_checkpoint": False,
            "reason": "Before reading, no source paragraphs are available.",
        }

    def fields(record):
        return {key: value for key, value in record.items() if key != "sources"} if record else None

    # Recorded summaries are consulted only after the prefixes have been replayed.
    if (fields(first), fields(previous)) != (journal["first_pass"], journal["previous"]):
        raise ValueError(f"First PASS or its predecessor differs for {question['qid']}")
    if [fields(check) for check in checks] != journal["checks"]:
        raise ValueError(f"A checkpoint differs from the manual journal for {question['qid']}")
    return {
        **question,
        "first_pass": first,
        "previous": previous,
        "terminal_outcome": (
            "supported_evidence" if checks[-1]["verdict"] == "PASS" else "insufficient_evidence"
        ),
        "checks": checks,
    }


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def replay(directory):
    audit = load_json(directory / "stream-audit.json")
    journal = load_json(directory / "prefix-review.json")
    questions = load_json(directory / "questions.json")
    if (audit["dataset"]["split"] != "validation" or audit["dataset"] != journal["dataset"] or
            audit["step"] != journal["step"] or audit["step"] != 256):
        raise ValueError("Replay requires the recorded validation split and 256-token grid.")
    documents = {doc["row"]: doc for doc in audit["documents"]}
    annotations = {entry["qid"]: entry for entry in journal["questions"]}
    if (len(annotations) != len(questions) or len(documents) != len(questions) or
            len({q["qid"] for q in questions}) != len(questions) or
            len({q["row"] for q in questions}) != len(questions)):
        raise ValueError("Inputs must give one stream and journal per development question.")
    results = []
    for question in questions:
        row = question["row"]
        if type(row) is not int:
            raise ValueError("Development row must be an integer.")
        doc, entry = documents[row], annotations[question["qid"]]
        if (any(entry[key] != value for key, value in question.items()) or
                doc["paper_id"] != question["paper_id"]):
            raise ValueError(f"Wrong source for validation row {row}")
        results.append(replay_question(
            directory / f"{row}.checkpoints.jsonl", question, doc, entry, audit["step"],
        ))
    return {
        "dataset": audit["dataset"],
        "step": audit["step"],
        "mode": "manual_annotation_replay",
        "match": True,
        "checkpoint_count": sum(len(item["checks"]) for item in results),
        "questions": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Development stream and annotation directory")
    args = parser.parse_args()
    print(json.dumps(replay(args.directory), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
