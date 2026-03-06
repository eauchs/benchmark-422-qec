# Crow-4B-Opus-4.6-Distill-Heretic (Qwen3.5)

**Provider**: Local  
**Correct**: ❌  
**Final answer**: `"Hey! How's it going?" — no attempt`  
**Error order**: N/A  

---

## Metrics

| Metric | Value |
|--------|-------|
| RMSE vs expected (p∈[0, 0.15]) | N/A (no answer) |
| Response size | 83 chars |
| Tool calls | 0 |
| Self-corrections ("wait/actually") | 0 |
| Wall-clock time | N/A |
| p² infidelity coefficient | N/A (correct: `0.640`) |

---

## Thinking & Reasoning Summary

**No reasoning produced.**

The model responded to the quantum error correction benchmark with a casual greeting: *"Hey! How's it going?"*

This suggests the distillation process from the base Qwen3.5 architecture has severely compromised the model's ability to engage with technical prompts, or that the system/chat template was not correctly configured for this task.

---

## Raw Output Excerpt (first 2000 chars, redacted)

```
qwen distill :hey  
Reasoning  
Toggle reasoning content  
Hey\! How's it going?  

```

> Full raw output available in `results/raw_qwen_distill_crow4b.txt`
