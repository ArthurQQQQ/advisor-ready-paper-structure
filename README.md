# Advisor-Ready Paper Structure

导师会喜欢的论文结构

Turn scattered notes, partial drafts, and experimental results into a defensible paper outline and a concrete agenda for the next advisor meeting. Designed primarily for empirical ML and AI papers.

## What you get

1. **A bounded conclusion** stating what the supplied evidence can support today.
2. **An evidence map** that links paper claims to source files, sections, tables, or figures.
3. **An analysis order** showing which checks could change the conclusion and what each would produce.
4. **An annotated outline** with the job and writing sequence of each section, short gray notes in a second language, and empty slots for planned figures and tables.
5. **A section-by-section review table** showing what to keep, move, add, or verify and how to tell when each task is done.

The writing sequence comes from an advisor-meeting approach. Start Method with the key idea. For each experiment, state the purpose, explain the comparison, describe the observation, interpret it, and connect it to a design choice. Trace the conclusion back to the opening question.

## Try it in Codex

Clone into your user skills directory:

```sh
git clone https://github.com/ArthurQQQQ/advisor-ready-paper-structure.git "${CODEX_HOME:-$HOME/.codex}/skills/advisor-ready-paper-structure"
```

Open Codex and invoke `$advisor-ready-paper-structure` with your files or notes.

> Use $advisor-ready-paper-structure on my draft, experiment notes, and partial tables. Tell me what I can conclude today, which analysis to do first, and what belongs in each section. Give me an English outline with gray Chinese notes at the gaps, blank slots for the missing figures and tables, and a final section-by-section review.

## Worked example

- [Fictional source packet](examples/source-packet.md)
- [Annotated outline and review](examples/plan.html) · download the file and open it in any browser for the styled view

The example starts with a positive pilot result and a broader comparison on mismatched samples. The plan keeps the pilot claim narrow, prioritizes an audit of the sample lists, and leaves the full comparison and ablation cells blank.

## 中文用法

把草稿、组会笔记、实验结果和半成品图表交给技能。它先判断现在能下什么结论，再按章节写清楚每一段要完成的任务，并给出分析顺序。缺什么就在对应位置留空，用灰色小字写明补什么、怎么检查。最后用逐节审阅表汇总每一项修改。

工作提纲和缺口提示单独保存，便于讨论和修订。正式稿中只写有材料支持的内容。
