# The Paper Structure That Your Advisor Would Like to Read | 不烧心的论文结构审阅

**Restructure your paper with logic.**

I put this guide together from my experience doing research with professors at leading universities around the world and writing papers for major machine learning and AI conferences. It helps you educate your readers with a clear, logical paper structure.

Upload your paper as a PDF and get an interactive HTML review you can open offline.

[简体中文](README.zh-CN.md) · [Worked example](examples/plan.html)

## What to provide

![Inputs for a paper structure review, including the topic, draft, results and baselines, and optional venue, alongside the skill's ML paper template](assets/advisor-ready-input.jpg)

Attach your paper as a PDF, even if the draft is incomplete. If the paper refers to evidence or comparisons outside the PDF, attach the relevant notes, figures, or tables. Include your target venue if it affects how the paper should be structured.

## What you get back

![A single annotated review with recommended section order, an evidence and baseline comparison check, and prioritized edits](assets/advisor-ready-output.jpg)

Start with a short verdict and the numbered argument map in the center. Select a node to highlight the corresponding manuscript passage on the left and see what it supports, what is missing, and how to revise it on the right.

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

[Example source packet](examples/source-packet.md) · [Interactive review](examples/plan.html) (download the HTML and open it in a browser)

## Run in Codex

Clone into your Codex skills directory, then open a new chat.

```sh
git clone https://github.com/ArthurQQQQ/advisor-ready-paper-structure.git "${CODEX_HOME:-$HOME/.codex}/skills/advisor-ready-paper-structure"
```

Attach your paper PDF and send this prompt.

```text
Use $advisor-ready-paper-structure to review the attached PDF.
Trace the argument through each section. Show which claims the evidence supports
and where a step in the reasoning, a baseline comparison, or evidence is missing.
Return one offline HTML review with a short verdict and a numbered argument map.
Link each node to the corresponding source excerpt and one or two specific edits.
```
