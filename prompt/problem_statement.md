# [[4,2,2]] Quantum Error Detection — Benchmark Problem

## Problem Setup

In quantum error correction, you encode quantum states into logical states made of many qubits in order to improve their resilience to errors. In quantum error detection, you do the same but can only detect the presence of errors and not correct them.

In this problem, we consider a single **[[4,2,2]] quantum error detection code**, which encodes two logical qubits into four physical qubits, and investigate how robust logical quantum operations in this code are to quantum errors.

### Code Definition

- Physical qubits: labelled **0, 1, 2, 3**
- Logical qubits: labelled **A** and **B**
- Stabilizers: `XXXX` and `ZZZZ`
- Logical operators: `X_L^A = XXII`, `Z_L^A = ZZII`, `X_L^B = IIXX`, `Z_L^B = IIZZ` (up to stabilizer multiplication)

### Error Model

Each CNOT gate in the circuit has a **two-qubit depolarizing error channel** following it, producing one of the 15 non-identity two-qubit Paulis with equal probability `p/15`. The parameter `p` denotes the probability of an error in a single two-qubit gate.

---

## Main Problem

Prepare a logical two-qubit **|Φ+⟩** state in the [[4,2,2]] code using a fault-tolerant circuit with an ancilla qubit (qubit 4).

### Circuit (time order)

1. H on qubit 0 *(noiseless)*
2. CNOT(0,1), CNOT(0,2), CNOT(0,3) — encoding gates, each noisy
3. H on ancilla qubit 4 *(noiseless)*
4. CNOT(0,4), CNOT(1,4), CNOT(2,4), CNOT(3,4) — XXXX syndrome check, each noisy
5. H on qubit 4 *(noiseless)*, then measure qubit 4

**Post-selection**: ancilla = |0⟩ **AND** code space (+1 eigenspace of both XXXX and ZZZZ stabilizers).

> Note: the equation is written in matrix multiplication order; quantum operations occur in reverse order (right-to-left).  
> If the ancilla measurement is **+1** (|0⟩), state preparation **succeeds**. If **-1** (|1⟩), it **fails**.

---

## Question

**What is the logical state fidelity of the final 2-qubit logical state as a function of two-qubit gate error rate `p`, assuming post-selection on all detectable errors and on ancilla measuring |0⟩?**

---

## Answer Template

```python
import sympy as sp

p = sp.symbols('p')

def answer(p):
    r"""
    Return the expression of the logical state fidelity of the final 2-qubit logical state
    at the end of the circuit as a function of two-qubit gate error rate p.

    Inputs
    ----------
    p: sympy.Symbol, two-qubit gate error rate

    Outputs
    ----------
    F_logical: sympy.Expr, logical state fidelity of the final 2-qubit logical state
    """

    # ------------------ FILL IN YOUR RESULTS BELOW ------------------
    F_logical = ...  # a SymPy expression of p
    # ---------------------------------------------------------------

    return F_logical
```
