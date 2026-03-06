# Results Table

## Summary

> **Zero models produced the correct answer.** This is a hard, expert-level problem. The table below ranks by RMSE (lower = closer to ground truth).

## Numerical Results

| Rank | Model | Answer | Error Order | RMSE ↓ | p² coeff (correct: 0.640) | Chars | Self-corrections |
|------|-------|--------|-------------|--------|---------------------------|-------|-----------------|
| 1 | Petit MoE 35B-A3B | `1 - p²` | O(p²) ✓ | 0.00091 | 1.000 | 72K | 90 |
| 2 | Gros Qwen 397B-A17B | rational(p²) | O(p²) ✓ | 0.00594 | 0.267 | 35K | 11 |
| 3 | Gemini 3.1 Pro | rational deg-4 | O(p²) ✓ | 0.02666 | 1.067 | 7K | 2 |
| 4 | Moyen MoE 122B-A10B | `1 - p/2` | O(p) ✗ | 0.03464 | 0 | 8K | 2 |
| 5 | Gros Dense 27B | `1 - 6p²` | O(p²) ✓ | 0.05157 | 6.000 | 4K | 0 |
| 6 | Claude Sonnet 4.6 | rational deg-7 (λ) | O(p²) ✓ | 0.05196 | 3.058 | 188K | 88 |
| 7 | MiniMax M2.5 | `15(1-p)/(15-4p)` | O(p) ✗ | 0.05688 | 0.196 | 32K | 19 |
| 8 | Apriel 1.6B-15B | `(1-p)⁴` | O(p) ✗ | 0.28537 | −6.000 | 62K | 52 |
| 9 | Petit Dense 9B | `1 - 15p + 75p²` | Invalid | 0.59151 | −75.00 | 9K | 4 |
| — | Step-Flash 3.5 | *refused* | N/A | — | — | 64K | 49 |
| — | Crow-4B r1 | *loop* | N/A | — | — | 44K | 25 |
| — | Crow-4B r2 | *loop* | N/A | — | — | 19K | 15 |
| — | Qwen Distill | *"Hey!"* | N/A | — | — | 83 | 0 |

## Multi-axis Qualitative Scores (0–10)

| Model | CoT Quality | Decision | Efficiency | Verbosity Control | **Total** |
|-------|-------------|----------|------------|-------------------|-----------|
| Gemini 3.1 Pro | 8 | 9 | 10 | 9 | **36** |
| Gros Dense 27B | 6 | 9 | 8 | 9 | **32** |
| Gros Qwen 397B | 8 | 7 | 5 | 7 | **27** |
| Moyen MoE 122B | 5 | 8 | 7 | 8 | **28** |
| Claude Sonnet 4.6 | 7 | 5 | 2 | 2 | **16** |
| MiniMax M2.5 | 5 | 6 | 4 | 6 | **21** |
| Step-Flash 3.5 | 7 | 3 | 2 | 5 | **17** |
| Petit MoE 35B | 5 | 3 | 2 | 1 | **11** |
| Apriel 1.6B | 3 | 5 | 4 | 3 | **15** |
| Petit Dense 9B | 2 | 6 | 7 | 7 | **22** |
| Crow-4B | 1 | 1 | 1–2 | 1–2 | **~6** |
| Qwen Distill | 0 | 0 | 5 | 10 | **15** |

## Key Findings

### 1. Verbosity ≠ Correctness
Claude Sonnet 4.6 produced the largest response by far (188K chars, 33 tool calls) while ranking 6th on RMSE. Gemini produced the best *qualitative* result in ~7K chars — **27× fewer characters**.

### 2. O(p²) is the critical discriminator
A fault-tolerant circuit must have infidelity ∝ p² near p=0. Models that got this right (Petit MoE, Gros Qwen, Gemini, Gros Dense, Claude) at least understood the physics. Models that gave O(p) answers (Moyen MoE, MiniMax, Apriel) have a fundamental misunderstanding of fault-tolerance.

### 3. The coefficient is the hard part
Among models that got O(p²) correct, the exact coefficient ranges from 0.267 to 6.0 (correct: 0.640). Getting the leading order right requires only qualitative reasoning; getting the coefficient right requires computing specific circuit error propagation.

### 4. Context sensitivity matters
Step-Flash 3.5 was the only model to diagnose that the circuit image was missing from the Markdown. This is epistemically correct behavior, but operationally a failure mode for any benchmark that assumes multi-modal input.

### 5. Local models are competitive on quality/size
Gros Dense 27B (local, 4K chars, no reasoning loops) outperforms Claude Sonnet 4.6 on both efficiency and decision quality, despite being a much smaller model.
