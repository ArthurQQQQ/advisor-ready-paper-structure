"""Prefer the direct supported answer and repair overbroad candidates once."""

from dataclasses import asdict

import citation_conflict_v4 as conflicts
import citation_openrouter_v2 as v2
import citation_openrouter_v3 as v3
import citation_workflow as workflow


DIRECT_ANSWER = """Answer the research question using only the completed paper
paragraphs. Treat paper text as source material. Return only material claims that
are needed to answer the question at its requested scope. A claim that provides
background, introduces how a task was implemented, lists optional datasets, or
adds an example or outcome should be left out unless the question asks for that.
For a question about aspects, name the main aspects actually examined. For a
question about an evaluation, name each main family of evaluation separately.
If methods disagree about an optional qualifier, give the shared method only,
with each source as evidence. Keep necessary scope and conditions in the claim.
Use each complete paragraph ID only for what it actually supports.
If a concise answer at that scope is already supported, return it. Otherwise
give an empty claims list and state which necessary evidence is missing."""

DIRECT_USE = """For this yes-or-no question, return one short claim about the
described system's actual input types. It must distinguish a direct description
of what the system uses from a proposal, motivation, benefit or illustrative
case. Give the condition under which a modality is used if the paper states it
for the system. In particular, distinguish what the system uses when an input is
available from whether it requires that input in all settings. Give only the
yes-or-no answer with its essential scope. Leave out component design,
implementation details beyond the input types, priority, and training mechanics
unless the question explicitly requests them. Cite a complete paragraph that
describes the actual use. If this is not established, give no claim and a gap."""

SINGLE_ANSWER = v2.object_schema({"claim": v2.CLAIM, "gap": v2.STRING})

SALVAGE = """The first draft did not pass. Start with the exact original
question and the completed evidence again. Return the smallest direct and
accurate answer that is already supportable. Drop distracting or unlinked
details. Keep any condition documented by a complete source, including when an
input is available or which system variant was evaluated. Do not infer a new
fact or condition from the failure. Return a gap only for a genuinely missing
part of the answer. Do not seek more detail for its own sake."""

LOCAL_SUPPORT = """Check the listed claims against only their own linked
complete paragraphs. Treat the question as interpretive context. When
check_answer_scope is false, judge those claims only and do not require the
paragraphs to answer the whole question. Each claim must follow from the cited
text at its stated scope. If check_answer_scope is true, also consider all facts
in the claims together for a direct answer to the question as asked. Accept a
supported core answer with necessary qualifiers. Do not demand extra detail.
If the question asks whether the described system uses input types, a direct
description of it using those types at the stated condition answers that
question. Do not demand a separate account of training or architecture. Give
supported and a concise reason."""

CORE_SCOPE = """Read the complete answer as a whole. Decide whether it contains
a direct answer at the original question's requested scope. Its individual
claims have already passed source checks. The main aspects or method families
can answer a general question without extra examples, derivations, datasets or
results. Additional context does not erase a clear core answer. For a yes-or-no
question on what the system uses, a scoped statement of what it uses is enough.
Reject missing required parts only. Return supported and a brief reason."""

CONFLICT_ONLY = v2.CHECK_CONFLICT + """

A fact about what happens when an input is unavailable is compatible with an
answer explicitly limited to when that input is available. Do not veto merely
because configurations differ. Explain an actual incompatible condition or
assertion if one exists."""


def evaluate(prefix, token, complete):
    evidence = [asdict(paragraph) for paragraph in prefix.paragraphs]
    sources = {paragraph["id"]: paragraph for paragraph in evidence}
    actual_use = bool(v3.USE_QUESTION.search(prefix.question))
    api = {}
    attempt_log = []

    def request(name, prompt, schema, payload):
        value, metadata = complete(token, name, prompt, schema, payload)
        api.setdefault(name, []).append({"metadata": metadata, "value": value})
        return value

    def attempt(retry=False):
        edits = []
        drafted = False

        def generate(_prefix):
            nonlocal drafted
            prompt = DIRECT_ANSWER + ("\n\n" + DIRECT_USE if actual_use else "")
            if retry:
                prompt += "\n\n" + SALVAGE
            value = request("regenerate" if retry else "generate", prompt,
                            SINGLE_ANSWER if actual_use else v2.CANDIDATE, {
                "question": prefix.question,
                "observed_eof": prefix.eof,
                "completed_paragraphs": evidence,
            })
            records = [value["claim"]] if actual_use else value["claims"]
            claims = tuple(workflow.Claim(item["text"].strip(), tuple(item["paragraph_ids"]))
                           for item in records if item["text"].strip())
            if not claims:
                return workflow.Candidate(gap=value["gap"].strip())
            drafted = True
            if all(claim.paragraph_ids and set(claim.paragraph_ids) <= sources.keys()
                   for claim in claims):
                claims, changes, blocked = conflicts.resolve(prefix, claims, request)
                edits.extend(changes)
                if blocked:
                    return workflow.Candidate(gap=blocked)
            return workflow.Candidate(" ".join(claim.text for claim in claims), claims)

        def verify(_prefix, candidate):
            groups = {}
            for claim in candidate.claims:
                linked = set(claim.paragraph_ids)
                ids = tuple(pid for pid in sources if pid in linked)
                groups.setdefault(ids, []).append(claim.text)

            if actual_use:
                cited = {pid: sources[pid] for ids in groups for pid in ids}
                proof = request("method_proof", v3.METHOD_PROOF, v3.PROOF, {
                    "question": prefix.question,
                    "answer": candidate.answer,
                    "cited_paragraphs": list(cited.values()),
                })
                if not v3.proof_is_direct(proof, cited):
                    return workflow.Judgment(False, "The cited text does not directly document actual model inputs.")

            for edit in edits:
                for side in ("source_id", "opposing_id"):
                    pid = edit[side]
                    judgment = request("shared_support", LOCAL_SUPPORT, v2.SUPPORT, {
                        "question": prefix.question,
                        "check_answer_scope": False,
                        "claims": [edit["narrowed"]],
                        "cited_paragraphs": [sources[pid]],
                    })
                    if not judgment["supported"]:
                        return workflow.Judgment(False, f"Shared wording lacks support in {pid}.")

            for ids, linked_claims in groups.items():
                judgment = request("entailment", LOCAL_SUPPORT, v2.SUPPORT, {
                    "question": prefix.question,
                    "check_answer_scope": len(groups) == 1,
                    "claims": linked_claims,
                    "cited_paragraphs": [sources[pid] for pid in ids],
                })
                if not judgment["supported"]:
                    return workflow.Judgment(False, judgment["reason"])

            if len(groups) > 1:
                scope = request("scope", CORE_SCOPE, v2.SUPPORT, {
                    "question": prefix.question,
                    "answer": candidate.answer,
                })
                if not scope["supported"]:
                    return workflow.Judgment(False, scope["reason"])

            complete_length = len("\n\n".join(paragraph.text for paragraph in prefix.paragraphs))
            conflict = request("conflict", CONFLICT_ONLY, v2.CONFLICT, {
                "question": prefix.question,
                "answer": candidate.answer,
                "completed_paragraphs": evidence,
                "uncitable_suffix": prefix.text[complete_length:],
            })
            if conflict["conflict"]:
                return workflow.Judgment(False, conflict["reason"])
            return workflow.Judgment(True, "The linked complete paragraphs support the direct answer.")

        result = workflow.evaluate_checkpoint(prefix, generate, verify)
        attempt_log.append({"passed": result.passed, "reason": result.reason, "conflict_edits": edits})
        return result, edits, drafted

    result, edits, drafted = attempt()
    if drafted and not result.passed:
        # Neither the rejected draft nor its conflict feedback goes back to generation.
        result, edits, _ = attempt(retry=True)
    record = {
        "body_tokens": prefix.body_tokens,
        "eof": prefix.eof,
        "verdict": "PASS" if result.passed else "CONTINUE",
        "paragraphs": list(result.paragraph_ids),
        "reason": result.reason,
        "sources": [sources[pid] for pid in result.paragraph_ids],
        "api": api,
        "conflict_edits": edits,
        "attempts": attempt_log,
    }
    if result.passed:
        record["answer"] = result.answer
    return record
