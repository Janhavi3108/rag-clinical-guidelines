# Day 3 notes: sentence-aware chunking and cleanup

## What changed in ingest.py
1. Removed repeated header/footer lines (short lines on 30%+ of pages, digits normalized).
2. Joined hyphenated line breaks and collapsed newlines into spaces.
3. Chunks now end at sentence boundaries, never mid-word. Very long sentences are split on word boundaries.
4. Overlap carries whole trailing sentences instead of raw characters.
5. Dropped chunks under 100 characters.
6. Skipped pages with no answerable content (table below).
7. Added --size, --overlap, --index, --chunks options for next week's experiments.

## Pages skipped (PDF viewer page numbers)
| File | Pages skipped | Reason |
|---|---|---|
| who_2021_guideline.pdf | 5, 60-80 | Acknowledgements; contributor lists and declarations of interest (names only) |
| icmr_2016_cervix.pdf | 4-11, 54-61 | Forewords, messages, prefaces; reference list |
| mohfw_2016_common_cancers.pdf | 5-21 | Messages, preface, contents. |

Bug found and fixed: `range(60, 79)` stops at 78, so WHO p.79 (declarations of interest) was still indexed. Fixed with `range(60, 80)`. Lesson: check "pages kept ... (skipped N)" against the number of pages meant to be skipped.

## Before vs after
| Metric | Day 2 | Day 3 |
|---|---|---|
| Total chunks | 737 | 539 |
| Average chunk length | 661 | 627 |
| Chunks starting lowercase | 390 | 24 of 604 (before the p.79 fix) |

Lowercase starts dropped but not to zero. 

## Retrieval before vs after (top result)
| Question | Day 2 | Day 3 | Comment |
|---|---|---|---|
| At what age should screening start? | WHO p.46, 0.791 | WHO p.14, 0.811 | Better: p.14 gives the priority age group (30-49) |
| Screening test in India's programme? | MoHFW p.26, 0.701 | MoHFW p.26, 0.731 | Same page, higher score. |
| WHO primary screening test? | WHO p.12, 0.778 | WHO p.12, 0.790 | Recommendation 21 (HPV DNA as primary test) in the top 3 |
| Treatment for stage IB? | ICMR p.21, 0.799 | ICMR p.21, 0.785 | Rank 3 was a reference list (p.56), now p.18 (relevant) |
| Capital of France (unanswerable) | WHO p.70, 0.506 | WHO p.113, 0.447 | Gap to real questions widened. Top result is a reference list |
| Should VIA be replaced by HPV testing? (new) | n/a | WHO p.53, 0.815 | Good: p.45 and p.12 also relevant |
| Recommended screening interval? (new) | n/a | WHO p.37, 0.787 | Weak: p.37 is about follow-up. The 3-5 year recommendation is rank 3 (p.14, 0.757) |

## Observations
- Top-1 scores for answerable questions: 0.73-0.82. Unanswerable: 0.447. A "not found" cutoff near 0.6 looks plausible, but 7 questions can't set it. Tune on the 40-question set and expect some false refusals.
- Scores are not relevance. The interval question scored 0.787 on the wrong page, and the correct chunk was only 0.03 lower. Always read the retrieved text.
- WHO recommends HPV DNA as the primary test, while the 2016 MoHFW framework describes the national programme. The documents differ, which gives good test cases.

## Still wrong / to do
- WHO reference pages still indexed (noise in unanswerable results).
- Tables still extract poorly (MoHFW coverage table).
- Interval question ranks the correct chunk third. Use it to compare chunk sizes and k next week.
