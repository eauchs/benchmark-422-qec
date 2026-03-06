# Methodology

## Setup

This benchmark evaluates 11 models (+ 2 failed runs) on a single, expert-level physics problem drawn from quantum error correction. The problem is intentionally hard: it requires both domain knowledge ([[4,2,2]] stabilizer codes) and the ability to reason about a circuit that is partially described (the circuit diagram is an image, absent from the Markdown rendering).

## Scoring

### Numerical accuracy (primary)

All models that produced a SymPy-compatible answer were evaluated by computing the **RMSE** between their `F(p)` and the ground-truth `F(p)` over `p ∈ [0, 0.15]` (the physically relevant regime before post-selection probability collapses).

```python
import sympy as sp, numpy as np
p = sp.Symbol('p')
p_vals = np.linspace(0, 0.15, 300)
rmse = np.sqrt(np.mean((model_f(p_vals) - expected_f(p_vals))**2))
```

**Ground truth**: verified against the problem's official expected answer.

### Physical sanity checks

Beyond RMSE, each answer was assessed on three physical criteria:

| Criterion | Description | Correct value |
|-----------|-------------|---------------|
| `F(0) = 1` | No errors → perfect fidelity | 1 |
| `F(15/16) = 1/4` | Fully depolarized → mixed state | 1/4 |
| Error order | Fault-tolerant circuit → O(p²) onset | p² (coefficient 16/25) |

### Qualitative axes

Four qualitative axes were scored 0–10 based on analysis of the raw reasoning:

- **CoT Quality**: accuracy of physical reasoning, correct identification of key concepts (fault-tolerance, stabilizer structure, error propagation)
- **Decision Quality**: does the model converge to a single answer? with appropriate confidence?
- **Efficiency**: bits of quality per character of output
- **Verbosity Control**: signal-to-noise ratio in the response

## Limitations

1. **N=1 problem**: single benchmark problem. Results reflect performance on this specific task class (expert physics + missing context).
2. **Circuit ambiguity**: the circuit image was not rendered in the Markdown. All models that "succeeded" made assumptions about the circuit. The ground truth corresponds to a specific circuit (7 CNOTs: 3 encoding + 4 syndrome).
3. **Local models**: run on Apple Silicon M3 Max (128GB), quantized (Q3_K_XL or Q4). Performance may differ at higher precision.
4. **No prompt optimization**: single-shot, same prompt for all models.

## Models tested

| Model | ID | Provider | Type |
|-------|----|----------|------|
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Anthropic | Cloud |
| Gemini 3.1 Pro | — | Google | Cloud |
| Step-3.5-Flash | — | StepFun | Cloud |
| MiniMax-M2.5 | `MiniMaxAI/MiniMax-M2.5` | Local (llama-server) | Local via Codex CLI |
| Qwen3.5-35B-A3B | `Qwen/Qwen3.5-35B-A3B` | Local | Local |
| Qwen3.5-122B-A10B | `Qwen/Qwen3.5-122B-A10B` | Local | Local |
| Qwen3.5-27B | `Qwen/Qwen3.5-27B` | Local | Local |
| Qwen3.5-397B-A17B | `Qwen/Qwen3.5-397B-A17B` | Local | Local |
| Qwen3.5-9B | `Qwen/Qwen3.5-9B` | Local | Local |
| Apriel-1.6-15B-Thinker | `ServiceNow-AI/Apriel-1.6-15b-Thinker` | Local | Local |
| Crow-4B-Opus-4.6 | `crownelius/Crow-4B-Opus-4.6-Distill-Heretic_Qwen3.5` | Local | Local |
