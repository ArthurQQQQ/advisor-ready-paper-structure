# Source packet for the example

This packet is fictional. Its details and numbers serve only to demonstrate the skill.

**Draft question** — On scientific PDFs, does giving a passage reranker page and section information improve which passage it retrieves? Proposed manuscript in English, editorial notes in Simplified Chinese.

## E01 Protocol note

The test compares the same text-only reranker with and without page position and section headings as a combined input. The intended endpoint is exact match of the top-ranked passage to an annotated gold passage. The candidate pool is meant to be shared for each question. The test has no answer generator.

## E02 Paired pilot record

On the same 24 annotated questions from single-column PDFs, with a shared candidate pool for each question, the text-only run retrieved 12 exact matches and the layout-aware run retrieved 15. The record here gives aggregate counts. Per-question outcomes and uncertainty estimates are absent from this packet.

## E03 Mixed-cohort export

A draft spreadsheet compares the earlier text-only pilot on single-column PDFs with a layout-aware export that also includes two-column PDFs. The question IDs and candidate-pool hashes were omitted from the export, so it cannot establish a paired comparison. A lab note says this export looked more favorable than the pilot. No additional outcome values are included here.

## E04 Implementation note

The current layout-aware configuration adds page position and section headings together. Separate runs for the two features are planned. The per-question gold candidate membership is unavailable for the mixed-cohort export.

## Draft claim to check

“Our layout-aware model improves answer accuracy across scientific PDF layouts because it uses section headings to find the right evidence.”
