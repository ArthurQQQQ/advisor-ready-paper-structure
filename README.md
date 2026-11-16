# The Paper Structure That Your Advisor Would Like to Read | 不烧心的论文结构审阅

**Restructure your paper with logic.**

Advisor-Ready Paper Structure gives you a short verdict and a clickable outline that shows how each section moves the argument forward.

[简体中文](README.zh-CN.md) · [Worked example](examples/plan.html)

I built this Codex skill from paper discussions with senior advisors who had different styles across several Top 30 CS departments. One recommendation kept coming up. State the research problem in the opening paragraph, then explain why it matters.

## What to provide

![Inputs for a paper structure review, including the topic, draft, results and baselines, and optional venue, alongside the skill's ML paper template](assets/advisor-ready-input.jpg)

Provide your topic or research question and a draft or outline, even if it is incomplete. Attach any experiment notes, results, figures, or tables you have, including the baselines and how you evaluated them. Add the target venue if it affects the structure.

The skill brings an ML paper structure template drawn from those advisor discussions. It adapts the template to your topic and checks how each section supports the paper's argument.

## What you get back

![A single annotated review with recommended section order, an evidence and baseline comparison check, and prioritized edits](assets/advisor-ready-output.jpg)

The review opens with its conclusion and up to three edits to make first. The clickable paper map shows the proposed section order and how each section hands off to the next. Open a section to see the evidence, baseline checks, what to keep or move, and how to verify the edit.

## Review the argument section by section

| Section | What the reader should be able to follow |
|---|---|
| **Introduction** | The research problem, why it matters, the gap in prior work, and the idea the paper puts forward. |
| **Method** | How the key idea determines the inputs, operations, and outputs, with the rationale for consequential choices. |
| **Experiments and results** | What each baseline tests, whether the comparison conditions and metric are clear, and which claim the result supports. |
| **Conclusion** | The answer to the opening question, the conditions it holds under, and what remains open. |

In the worked example, the introduction can open with “Can page position and section headings help a reranker retrieve the correct evidence passage from a scientific PDF?”

## Worked example

In the fictional example, a layout-aware reranker improves top-ranked passage matches from 12 to 15 on the same 24 questions from single-column PDFs (`E02`). A larger export includes two-column PDFs and omits question IDs and candidate-pool hashes (`E03`). The review keeps the pilot result in the paper and marks the cross-layout comparison as pending. The first check (`G01`) is to recover the matching question IDs, gold annotations, and candidate pools.

Open a node for its gray editor notes and any pending figure or table.

[Example source packet](examples/source-packet.md) · [Interactive review](examples/plan.html) (download the HTML and open it in a browser)

## Run in Codex

Clone into your Codex skills directory, then open a new chat.

```sh
git clone https://github.com/ArthurQQQQ/advisor-ready-paper-structure.git "${CODEX_HOME:-$HOME/.codex}/skills/advisor-ready-paper-structure"
```

Share the topic, draft or outline, and any results or baseline details you want the review to use.

```text
Use $advisor-ready-paper-structure to review this paper.
Adapt the ML paper template to my topic and trace the argument through each section.
Check which claims the evidence supports and whether the baseline comparisons are complete.
Start with your verdict and the edits to make first. Show the revised outline as a clickable paper map with details inside each section.
```
