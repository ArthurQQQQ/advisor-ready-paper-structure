# A frozen evidence workflow on new QASPER questions

This case follows an idea through topic debate, sourced baselines, a Quick Paper, checkpoint experiments, and a frozen check on new documents. The working question is whether sequential evidence retrieval can stop early under a 5% evidence-insufficiency constraint.

The shared evidence generator and citation verifier reached matching PASS/CONTINUE decisions on three development questions after several revisions. Those same questions had guided the revisions. The frozen workflow was then checked on new documents.

## Frozen protocol

The snapshot uses `google/gemini-2.5-flash-lite` through OpenRouter and Google AI Studio, temperature 0, seed 42, and a 1,536-token output cap. The model receives the question, the observed main-body prefix, completed citation paragraphs, and the observed EOF. Incomplete text participates only in the conflict check.

The protocol extracts actual model-operation evidence, retains source-backed input conditions, checks claims against their linked completed paragraphs, and narrows conflicting descriptions to wording both sources support. The case study records exhausted API failures separately. The runner stops on an API error and preserves completed checkpoints for retry.

The snapshot includes the effective aspects-schema recovery used in the development run. Its twelve code dependencies were hashed before the new source documents were read. The manifest hash was verified after execution.

[Freeze manifest](protocol/freeze-manifest.json) · [Execution entry](protocol/run-frozen-citations.py)

## New-question check

Three documents supplied six candidate questions. Three original questions from two papers met the main-body-only and unambiguous-question rules. The other questions were excluded for architecture or metric ambiguity, or a table-dependent enumeration.

The initial indices were 240, 320, and 400. The pinned validation split has 281 documents. Before reading replacement documents, the out-of-range indices were mapped modulo 281 to 39 and 119. The effective selection was 240, 39, 119. This amendment is recorded in the results.

Review references were prepared by independent Codex agents from the original sources and successive prefixes, then sealed before they reviewed the experimental model outputs.

| Question | First model PASS | First supportable prefix | First sufficient returned answer |
| --- | ---: | ---: | ---: |
| Training-data annotation | 1,280 | 1,280 | 1,536 |
| EEG discriminative information | 1,024 | 2,816 | 2,816 |
| Five binary classification tasks | 768 | 2,048 | 2,048 |

All positions use the same absolute 256-token grid plus each document's actual EOF.

Of 45 attempted checkpoints, 44 returned decisions and one exhausted three unchanged generation attempts. There were seven early-PASS checkpoints and zero reference-PASS/model-CONTINUE checkpoints among completed responses. Source review found 14 insufficient answers among the 30 model PASS responses.

The errors included attributing previous studies to the current paper, confusing training annotation with runtime annotation budgets, omitting preprocessing conditions, and adding an unsupported task comparison. A PASS at a reference-supportable prefix could still return the wrong evidence or an incomplete answer.

The nine reserved formal-evaluation questions remain held out. The stopping-risk calibration and formal policy comparison are still pending.

[Source-free per-checkpoint results](results.json) · [Training-annotation paper](https://arxiv.org/abs/1608.08188) · [EEG paper](https://arxiv.org/abs/1904.04358) · [QASPER revision](https://huggingface.co/datasets/allenai/qasper/tree/fdc9d8214fbab5dd782958601db4d678e6934a54)

## Run with prepared streams

Provide `OPENROUTER_API_KEY` in the execution environment, then run from the repository root.

```sh
python3 examples/long-document-early-stop/protocol/run-frozen-citations.py \
  /path/to/prepared-streams /path/to/new-output
```

The runner uses the Python standard library. Prepare these UTF-8 files in the input directory.

| File | Required content |
| --- | --- |
| `questions.json` | An array of questions with `row`, `question_order`, `qid`, `paper_id`, and `question`. |
| `stream-audit.json` | The pinned QASPER validation dataset metadata, `step: 256`, and `documents`. Each document has `row`, `paper_id`, `body_tokens`, `body_sha256`, `checkpoint_count`, and ordered `paragraphs` keyed by original paragraph ID with `start_byte` and `end_byte_exclusive`. |
| `<row>.checkpoints.jsonl` | One ordered event per checkpoint with `body_tokens`, `text_delta`, `eof`, and `newly_citable` IDs. Exactly one observed EOF ends each stream. |

The stream convention uses `tiktoken==0.8.0` with `cl100k_base`. Strip outer whitespace from retained main-body paragraphs, preserve original paragraph IDs, join paragraphs with two newlines, then tokenize the whole body once. Use UTF-8-safe deltas at 256-token intervals and the actual EOF. Keep abstracts, floats, captions, appendices, references, and acknowledgments outside the main-body stream.

The runner verifies its snapshot and the prepared streams, saves each completed checkpoint for resuming with the same inputs, and writes `model-run.json` after a complete run. The public result summary preserves the failed checkpoint as an API failure. The raw dataset and full model responses are external inputs to this source-free example.

[简体中文](README.zh-CN.md)
