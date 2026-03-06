# [[4,2,2]] QEC Benchmark

> A single expert-level quantum physics problem, evaluated across **11 models** (cloud + local Apple Silicon).  
> **Result: 0/11 correct.** The patterns of failure are the interesting part.

---

## What's this?

A benchmark run on a problem from quantum error correction: compute the **logical state fidelity** `F(p)` of a fault-tolerant [[4,2,2]] code preparation circuit under two-qubit depolarizing noise, after post-selection.

The answer is a rational function of degree 5 in `p`. The circuit is partially described as an image (missing from Markdown rendering), which creates an additional challenge: can models reconstruct the circuit from context, or do they fail gracefully?

**Why this problem?**
- Requires real domain knowledge (stabilizer codes, fault-tolerance, Pauli propagation)
- Has a clean, verifiable ground truth
- Distinguishes qualitative physical intuition (O(p²) onset) from exact analytical derivation
- Exposes failure modes under missing context

---

## Models Tested

| Model | Provider | Type |
|-------|----------|------|
| Claude Sonnet 4.6 | Anthropic | Cloud |
| Gemini 3.1 Pro | Google | Cloud |
| Step-3.5-Flash | StepFun | Cloud |
| MiniMax-M2.5 | MiniMaxAI | Local (llama-server, Apple Silicon M3 Max) |
| Qwen3.5-397B-A17B | Alibaba | Local |
| Qwen3.5-122B-A10B | Alibaba | Local |
| Qwen3.5-35B-A3B | Alibaba | Local |
| Qwen3.5-27B | Alibaba | Local |
| Qwen3.5-9B | Alibaba | Local |
| Apriel-1.6-15B-Thinker | ServiceNow AI | Local |
| Crow-4B-Opus-4.6-Distill | crownelius | Local |

Local models run on **Apple Silicon M3 Max (128GB)** via `llama-server` with quantization (Q3_K_XL / Q4_0).

---

## Key Results

### Accuracy ranking (RMSE vs ground truth, lower = better)

| Rank | Model | RMSE | Error order | Answer |
|------|-------|------|-------------|--------|
| 1 | Petit MoE 35B-A3B | 0.00091 | O(p²) ✓ | `1 - p²` |
| 2 | Gros Qwen 397B | 0.00594 | O(p²) ✓ | `15(1-p)²/(15(1-p)²+4p²)` |
| 3 | Gemini 3.1 Pro | 0.02666 | O(p²) ✓ | rational deg-4 |
| 4 | Moyen MoE 122B | 0.03464 | O(p) ✗ | `1 - p/2` |
| 5 | Gros Dense 27B | 0.05157 | O(p²) ✓ | `1 - 6p²` |
| 6 | Claude Sonnet 4.6 | 0.05196 | O(p²) ✓ | rational deg-7 (λ) |
| 7 | MiniMax M2.5 | 0.05688 | O(p) ✗ | `15(1-p)/(15-4p)` |
| 8 | Apriel 1.6B | 0.28537 | O(p) ✗ | `(1-p)⁴` |
| 9 | Petit Dense 9B | 0.59151 | invalid | `1 - 15p + 75p²` |
| — | Step-Flash 3.5 | — | — | refused (missing circuit) |
| — | Crow-4B ×2 | — | — | infinite loop |
| — | Qwen Distill | — | — | "Hey! How's it going?" |

### Qualitative ranking (CoT + Decision + Efficiency + Verbosity)

| Rank | Model | Score /40 |
|------|-------|-----------|
| 1 | Gemini 3.1 Pro | 36 |
| 2 | Gros Dense 27B | 32 |
| 3 | Moyen MoE 122B | 28 |
| 4 | Gros Qwen 397B | 27 |
| 5 | Petit Dense 9B | 22 |
| 6 | MiniMax M2.5 | 21 |
| 7 | Step-Flash 3.5 | 17 |
| 8 | Claude Sonnet 4.6 | 16 |

---

## Figures

| Figure | Description |
|--------|-------------|
| [`fig1_rmse.png`](figures/fig1_rmse.png) | RMSE bar chart for all models that gave an answer |
| [`fig2_verbosity_vs_quality.png`](figures/fig2_verbosity_vs_quality.png) | Response size vs quality — bigger ≠ better |
| [`fig3_fidelity_curves.png`](figures/fig3_fidelity_curves.png) | F(p) curves for top models vs ground truth |
| [`fig4_heatmap.png`](figures/fig4_heatmap.png) | Multi-axis qualitative scoring heatmap |

---

## Repository Structure

```
benchmark-422-qec/
├── README.md                    ← you are here
├── prompt/
│   ├── problem_statement.md     ← full problem + circuit description
│   └── expected_answer.md       ← ground truth + verification
├── results/
│   ├── claude_sonnet_4_6.md
│   ├── gemini_3_1_pro.md
│   ├── minimax_m2_5.md
│   ├── qwen3_5_35b_a3b.md
│   ├── qwen3_5_122b_a10b.md
│   ├── qwen3_5_27b.md
│   ├── qwen3_5_397b_a17b.md
│   ├── qwen3_5_9b.md
│   ├── apriel_1_6_15b.md
│   ├── crow4b_run1.md
│   ├── crow4b_run2.md
│   ├── qwen_distill_crow4b.md
│   └── step_flash_3_5.md
├── analysis/
│   ├── methodology.md           ← scoring methodology + limitations
│   ├── results_table.md         ← full results + key findings
│   └── scoring.py               ← reproducible scoring script
└── figures/
    ├── fig1_rmse.png
    ├── fig2_verbosity_vs_quality.png
    ├── fig3_fidelity_curves.png
    └── fig4_heatmap.png
```

---

## Reproduce

```bash
git clone https://github.com/eauchs/benchmark-422-qec
cd benchmark-422-qec
pip install sympy numpy
python analysis/scoring.py
```

---

## Key Takeaways

**1. Verbosity ≠ correctness.**  
Claude Sonnet 4.6 produced 188K characters and 33 tool calls. Gemini produced the best qualitative result in ~7K characters. 27× more tokens did not yield a better answer.

**2. O(p²) is the critical physical discriminator.**  
A fault-tolerant circuit must suppress infidelity to second order. Only 5 of 9 answering models identified this — the others gave O(p) answers reflecting a fundamental misunderstanding of fault-tolerance.

**3. The coefficient is the actual hard problem.**  
Getting `O(p²)` correct requires only qualitative physical reasoning. The exact coefficient (16/25 = 0.64) requires circuit-specific Pauli propagation analysis — a calculation no model performed correctly.

**4. Missing context reveals robustness gaps.**  
Step-Flash 3.5 was the only model to correctly identify the missing circuit diagram and refuse rather than assume. This is rigorous, but operationally a failure mode for automated benchmarks with multimodal inputs.

**5. Small local MoE models can be surprisingly good.**  
Qwen3.5-35B-A3B (3B active params, local) correctly identified O(p²) and achieved the best RMSE — though by numerical coincidence more than physical insight.

---

*Hardware: Apple Silicon M3 Max, 128GB. Local inference via `llama-server` (ggml-org/llama.cpp). Single-shot, no prompt optimization.*
