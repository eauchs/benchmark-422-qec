# Expected Answer

## Exact Formula

```python
import sympy as sp

p = sp.symbols('p')

F_logical = 1 - (
    sp.Rational(16, 25)   * p**2
  - sp.Rational(128, 125) * p**3
  + sp.Rational(2048, 3375)  * p**4
  - sp.Rational(32768, 253125) * p**5
) / (
    1
  - sp.Rational(68, 15)       * p
  + sp.Rational(704, 75)      * p**2
  - sp.Rational(32768, 3375)  * p**3
  + sp.Rational(253952, 50625)* p**4
  - sp.Rational(262144, 253125)* p**5
)
```

## Key Properties

| Property | Value |
|----------|-------|
| `F(0)` | 1 (perfect fidelity, no errors) |
| `F(15/16)` | 1/4 (fully mixed 2-qubit state) |
| Leading infidelity | O(p²) — confirms fault-tolerant suppression |
| `dF/dp` at p=0 | 0 (quadratic onset) |
| Coefficient of p² in infidelity | 16/25 = 0.64 |

## Physical Interpretation

The circuit is **fault-tolerant**: any single CNOT error either flips the ancilla (→ rejected by post-selection) or produces a detectable syndrome (→ rejected). Only pairs of errors can produce undetected logical faults, giving the O(p²) scaling.

The denominator encodes the post-selection probability — a rational function of p because some error combinations are accepted while others are rejected.
