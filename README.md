# The Paper Structure That Your Advisor Would Like to Read | 不烧心的论文结构审阅

**Restructure your paper with logic.**

I put this guide together from my experience doing research with professors at leading universities around the world and writing papers for major machine learning and AI conferences. It helps you educate your readers with a clear, logical paper structure.

Upload your paper as a PDF and get an interactive HTML review you can open offline.

[简体中文](README.zh-CN.md) · [Worked example](examples/plan.html)

## Develop a research idea

Start with one rough idea in Codex.

```text
Use $advisor-ready-paper-structure to help me develop this idea.
Can a retriever stop reading a long document early and still recover the evidence?
```

1. **Develop the five answers.** Revisit the problem, why it matters, what makes it hard, the closest prior attempts, and your general approach. Codex debates the most consequential gap each turn, checks relevant original papers during the discussion, and updates the Research Wall with what changed.
2. **Confirm the topic and comparisons.** When the question and intended claim are clear, confirm the brief. Codex fixes the formal baseline/control plan and records which comparison conditions still need alignment.
3. **Choose the paper structure.** Before writing, Codex identifies whether the main contribution is a method or an analysis, gives its evidence-based reason, then builds the Quick Paper around it. Labeled blanks preserve missing evidence, experiments and conclusions.

Open the Research Wall to follow the key point from each turn, the paper blocks it changes, and the evidence still needed. Ask Codex for a live preview that updates as the conversation progresses. The generated `research-workspace.html` also opens as an offline snapshot. Edit `quick-paper.md` as your draft develops. Download the two example HTML files to the same folder and open them in your browser. [Interactive idea example](examples/research-idea-workbench.html) · [Workspace with checked baselines](examples/research-workspace.html) · [Quick Paper Markdown](examples/quick-paper.md)

The approach starts at a level a reader new to the field can follow. Each close prior paper gets a brief, sourced account of what it establishes and what remains open. The core idea is explained independently of particular models and datasets, with reproducibility details placed in the setup. A method paper builds around the proposed solution and its comparisons. An analysis paper builds around the questions, study design and findings.

[Five-question framing and paper-type criteria](references/research-framing.md)

The [shared writing foundation](references/writing-foundations.md), adapted from the supplied Writing tips, governs the prose across these workflows. It covers the central insight, the five-question introduction followed by findings and contributions, intuition before mathematics, experiment narration, self-contained displays, and clear sentences with stable terminology.

For concept and method diagrams, start with [actual ICLR paper figures](references/figure-styles.md). Inspect the originals and choose an example-based comparison, a computational architecture, or a generation/verification layout. The skill adapts the selected organization to your research and carries it through the paper. Measured results are plotted from source data.

## Research case study

The long-document evidence case includes the live Research Wall workflow, a frozen OpenRouter evidence pipeline, and a fresh QASPER check. The new batch produced seven early-PASS checkpoints, and source review found 14 insufficient answers among 30 PASS responses. The case records the failed API checkpoint and the questions excluded before evaluation.

[Read the case and run the frozen protocol](examples/long-document-early-stop/README.md)

## What to provide

![Inputs for a paper structure review, including the topic, draft, results and baselines, and optional venue, alongside the skill's ML paper template](assets/advisor-ready-input.jpg)

Attach your paper as a PDF, even if the draft is incomplete. If the paper refers to evidence or comparisons outside the PDF, attach the relevant notes, figures, or tables. Include your target venue if it affects how the paper should be structured.

Attach the editable LaTeX or Markdown source if you want the review to apply approved edits to a downloadable revision.

## What you get back

![A single annotated review with recommended section order, an evidence and baseline comparison check, and prioritized edits](assets/advisor-ready-output.jpg)

Start with a short verdict and the numbered argument map in the center. Select a node to see the evidence, gaps, and suggested edits on the left. On the right, the original PDF opens to the corresponding page and highlights the matching passage. When a passage cannot be matched on the PDF page, the panel shows the verified excerpt and explains the fallback.

Red marks a major information gap to address first. Yellow marks a revision or check that needs attention. Green marks a small edit. A node with no marker needs no change.

Approve each suggestion from its node, or use **Approve all** at the top. Approval applies prepared text replacements to a working copy when editable source is available. The ZIP contains the changed LaTeX or Markdown files, a revision record, and the approval manifest.

Click **Open in Codex** after reviewing the approvals. The Codex desktop app opens a new task with your selection. Review the prompt and click **Send** to have the skill prepare the revised source files and check the remaining items against available evidence. If the browser does not open Codex, use **Copy task**, paste it into a Codex chat, and send it.

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

Attach your paper PDF and any editable source, then send this prompt.

```text
Use $advisor-ready-paper-structure to review the attached PDF.
Trace the argument through each section. Show which claims the evidence supports
and where a step in the reasoning, a baseline comparison, or evidence is missing.
Return one offline HTML review with a short verdict and a numbered argument map.
Show one or two specific edits on the left and highlight the matching passage on the original PDF page on the right.
Mark each node by severity and include the controls for individual and batch approval.
Prepare evidence-supported text replacements in my editable source and record checks that require additional material.
```
