# Day 2 notes: ingestion and retrieval sanity test

## Setup
- Embedding model: BAAI/bge-small-en-v1.5 (normalized embeddings, FAISS inner-product index)
- Chunking: 800 characters, 150 overlap, fixed character cuts
- Query prefix: "Represent this sentence for searching relevant passages: "

## Ingestion results
| File | Pages | Empty / near-empty |
|---|---|---|
| icmr_2016_cervix.pdf | 61 | 1 |
| mohfw_2016_common_cancers.pdf | 44 | 12 |
| who_2021_guideline.pdf | 115 | 1 |

- Total chunks: 737
- Checked the empty pages: they are the cover and blank pages, so no real content is lost.

## Chunk quality problems found (6 random chunks)
1. Chunks start mid-word because cuts are at fixed character counts (e.g. "r9", "cal cone").
2. Words run together or list numbers are mangled (e.g. "marginsneg", "Quality of Life Issues2.").
3. Tables become streams of numbers (MoHFW p.33 coverage table).
4. Low-value chunks are indexed: WHO p.6 acknowledgements, and later annexes with lists of reviewers and declarations of interest.
5. Printed page numbers differ from PDF page numbers (ICMR PDF p.32 is printed p.31). Citations and evaluation questions use PDF page numbers.

## Retrieval sanity test (top-3, k=3)
| Question | Top result | Score | Sensible? |
|---|---|---|---|
| At what age should screening start for women? | WHO p.46 | 0.791 | Yes, WHO pp.46-56 discuss starting ages |
| What screening test does India's national programme use? | MoHFW p.26 | 0.701 | Yes |
| What does WHO recommend as the primary screening test? | WHO p.12 | 0.778 | Yes, recommendations table |
| What is the treatment for stage IB cervical cancer? | ICMR p.21 | 0.799 | Yes, stages IB2/IIA2 |
| What is the capital of France? (unanswerable) | WHO p.70 | 0.506 | Correctly low-scoring, irrelevant text |

## Observations
- Scores for answerable questions were about 0.67-0.80. The unanswerable question scored about 0.48-0.51.
- This suggests a "not found" similarity cutoff somewhere around 0.6, but 5 questions are far too few to set one. Tune on the full evaluation set.
- Some legitimate questions may score low (short or oddly worded), so a cutoff will cost some false refusals.
- The "primary screening test" question returned WHO p.12 and p.13 but the exact recommendation wording is split across chunks. Check this during evaluation.
