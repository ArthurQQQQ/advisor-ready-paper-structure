"""Claim-grounded implementation evidence and paired-source conflict repair."""

from dataclasses import asdict
import re

import citation_conflict_v3 as conflicts
import citation_openrouter_v2 as v2
import citation_workflow as workflow


USE_QUESTION = re.compile(
    r"\b(?:model|system|method|decoder|pipeline|framework)\b"
    r".*\b(?:learn\w*|us(?:e|es|ed|ing)|tak\w*|receiv\w*|train\w*|combin\w*)\b"
    r".*\b(?:both|multiple|jointly)\b", re.IGNORECASE,
)
DIRECT_OPERATION = re.compile(
    r"\b(?:uses?|receiv\w*|tak(?:e|es|ing)|choos\w*|select\w*|determin\w*|"
    r"combin\w*|integrat\w*|incorporat\w*|leverag\w*|fed|feeds?|inputs?|"
    r"learn\w*|process\w*|consum\w*|accept\w*|exclud\w*|omit\w*|without)\b",
    re.IGNORECASE,
)
INTENT_OR_POSSIBILITY = re.compile(
    r"\b(?:propose|plan|intend|aim|hope)\s+to\b|"
    r"\b(?:can|could|may|might|would)\s+(?:help|provide|obtain|improve|"
    r"disambiguate|use|leverage|enable)\b", re.IGNORECASE,
)

METHOD_PROOF = """Decide whether the cited completed paragraphs directly document
the tested/described system actually consuming the input types asked about.
Classify a motivating example, a benefit of using certain inputs, and a plain
statement of intent to leverage them as insufficient. An actual model or decoder
description with concrete inputs is sufficient, including a diagram description or
a described conditional use when the answer preserves that condition. A statement
such as 'we propose a network that takes both [types] as input' can document an
architecture; 'we propose to leverage [type] because an example may help' cannot.
For a yes answer return one contiguous verbatim clause that directly says how the
named model/decoder operates with the input types. For a negative answer locate a
similarly direct exclusion. The quote must name or unambiguously refer to the
model's own operation and be an exact substring of its cited paragraph. The reader
can interpret neighboring words in that same paragraph. Do not merge distant
fragments or quote a proposal rationale. If the cited paragraphs lack this
evidence, supported must be false and both quote fields empty."""

PROOF = v2.object_schema({
    "supported": v2.BOOLEAN,
    "paragraph_id": v2.STRING,
    "quote": v2.STRING,
    "reason": v2.STRING,
})

METHOD_GUIDANCE = """The question asks about the described system's actual inputs.
Do not infer implementation from research motivation, an illustrative case, or
an intention to leverage additional signals. Find a direct description that
establishes the concrete input types or return a gap if it is not visible yet.
If use is conditional, preserve the condition. Omit claims of novelty."""

GENERATE = v2.GENERATE + """

When descriptions use opposed optional characterizations, favor the narrower
method both texts support. Keep a specific characterization only if it is needed
to answer the question. Omit unasked novelty claims or claims of precedence."""


def proof_is_direct(value, cited):
    quote = value["quote"].strip()
    pid = value["paragraph_id"]
    if not value["supported"] or pid not in cited or len(quote.split()) < 5:
        return False
    source = " ".join(cited[pid]["text"].split())
    exact = " ".join(quote.split())
    return (
        exact in source
        and bool(DIRECT_OPERATION.search(exact))
        and not INTENT_OR_POSSIBILITY.search(exact)
    )


def evaluate(prefix, token, complete):
    evidence = [asdict(paragraph) for paragraph in prefix.paragraphs]
    sources = {paragraph["id"]: paragraph for paragraph in evidence}
    requires_actual = bool(USE_QUESTION.search(prefix.question))
    api = {}
    repairs = []

    def request(name, prompt, schema, payload):
        value, metadata = complete(token, name, prompt, schema, payload)
        api.setdefault(name, []).append({"metadata": metadata, "value": value})
        return value

    def generate(_prefix):
        prompt = GENERATE + ("\n\n" + METHOD_GUIDANCE if requires_actual else "")
        value = request("generate", prompt, v2.CANDIDATE, {
            "question": prefix.question,
            "observed_eof": prefix.eof,
            "completed_paragraphs": evidence,
        })
        claims = tuple(workflow.Claim(item["text"].strip(), tuple(item["paragraph_ids"]))
                       for item in value["claims"])
        if not claims:
            return workflow.Candidate(gap=value["gap"].strip())
        if all(claim.text and claim.paragraph_ids and set(claim.paragraph_ids) <= sources.keys()
               for claim in claims):
            claims, edits, blocked = conflicts.resolve(prefix, claims, request)
            repairs.extend(edits)
            if blocked:
                return workflow.Candidate(gap=blocked)
        return workflow.Candidate(" ".join(claim.text for claim in claims), claims)

    def verify(_prefix, candidate):
        groups = {}
        for claim in candidate.claims:
            linked = set(claim.paragraph_ids)
            ids = tuple(pid for pid in sources if pid in linked)
            groups.setdefault(ids, []).append(claim.text)

        if requires_actual:
            cited = {pid: sources[pid] for ids in groups for pid in ids}
            proof = request("method_proof", METHOD_PROOF, PROOF, {
                "question": prefix.question,
                "answer": candidate.answer,
                "cited_paragraphs": list(cited.values()),
            })
            if not proof_is_direct(proof, cited):
                reason = proof["reason"] if not proof["supported"] else ""
                return workflow.Judgment(
                    False, reason.strip() or "The cited text does not directly document actual model inputs.",
                )

        for edit in repairs:
            for side in ("source_id", "opposing_id"):
                pid = edit[side]
                judgment = request("shared_support", v2.ENTAILMENT, v2.SUPPORT, {
                    "question": prefix.question,
                    "check_answer_scope": False,
                    "claims": [edit["narrowed"]],
                    "cited_paragraphs": [sources[pid]],
                })
                if not judgment["supported"]:
                    return workflow.Judgment(False, f"Shared wording lacks support in {pid}.")

        for ids, linked_claims in groups.items():
            judgment = request("entailment", v2.ENTAILMENT, v2.SUPPORT, {
                "question": prefix.question,
                "check_answer_scope": len(groups) == 1,
                "claims": linked_claims,
                "cited_paragraphs": [sources[pid] for pid in ids],
            })
            if not judgment["supported"]:
                return workflow.Judgment(False, judgment["reason"])

        if len(groups) > 1:
            scope = request("scope", v2.SCOPE, v2.SUPPORT, {
                "question": prefix.question,
                "answer": candidate.answer,
            })
            if not scope["supported"]:
                return workflow.Judgment(False, scope["reason"])

        complete_length = len("\n\n".join(paragraph.text for paragraph in prefix.paragraphs))
        conflict = request("conflict", v2.CHECK_CONFLICT, v2.CONFLICT, {
            "question": prefix.question,
            "answer": candidate.answer,
            "completed_paragraphs": evidence,
            "uncitable_suffix": prefix.text[complete_length:],
        })
        if conflict["conflict"]:
            return workflow.Judgment(False, conflict["reason"])
        return workflow.Judgment(True, "The linked complete paragraphs support the scoped answer.")

    result = workflow.evaluate_checkpoint(prefix, generate, verify)
    record = {
        "body_tokens": prefix.body_tokens,
        "eof": prefix.eof,
        "verdict": "PASS" if result.passed else "CONTINUE",
        "paragraphs": list(result.paragraph_ids),
        "reason": result.reason,
        "sources": [sources[pid] for pid in result.paragraph_ids],
        "api": api,
        "conflict_edits": repairs,
    }
    if result.passed:
        record["answer"] = result.answer
    return record
