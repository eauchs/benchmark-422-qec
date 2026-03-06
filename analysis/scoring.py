"""
scoring.py — Reproduce all numerical results from the [[4,2,2]] QEC benchmark.

Usage:
    python scoring.py

Requires: sympy, numpy
"""

import sympy as sp
import numpy as np

p = sp.Symbol('p')

# ── Ground truth ─────────────────────────────────────────────────────────────
EXPECTED = 1 - (
    sp.Rational(16, 25)      * p**2
  - sp.Rational(128, 125)    * p**3
  + sp.Rational(2048, 3375)  * p**4
  - sp.Rational(32768, 253125) * p**5
) / (
    1
  - sp.Rational(68, 15)        * p
  + sp.Rational(704, 75)       * p**2
  - sp.Rational(32768, 3375)   * p**3
  + sp.Rational(253952, 50625) * p**4
  - sp.Rational(262144, 253125)* p**5
)

# ── Model answers ─────────────────────────────────────────────────────────────
lam = 1 - sp.Rational(16, 15) * p

ANSWERS = {
    'Claude Sonnet 4.6':   (3*lam**3-lam**2-lam+1)*(3*lam**4+lam**3+2*lam**2+lam+1)/(4*(3*lam**7+1)),
    'Gemini 3.1 Pro':      (50625-175500*p+248400*p**2-161280*p**3+40960*p**4)/(50625-162000*p+259200*p**2-184320*p**3+49152*p**4),
    'MiniMax M2.5':        15*(1-p)/(15-4*p),
    'Apriel 1.6B':         (1-p)**4,
    'Gros Qwen 397B':      15*(1-p)**2/(15*(1-p)**2+4*p**2),
    'Gros Dense 27B':      1-6*p**2,
    'Moyen MoE 122B':      1-p/2,
    'Petit Dense 9B':      1-15*p+75*p**2,
    'Petit MoE 35B':       1-p**2,
}

def rmse(expr, p_vals, expected_vals):
    f = sp.lambdify(p, expr, 'numpy')
    try:
        vals = np.clip(f(p_vals), -10, 10)
        return float(np.sqrt(np.mean((vals - expected_vals)**2)))
    except Exception as e:
        return None

def p2_coeff(expr):
    """Coefficient of p² in the infidelity 1 - F(p)."""
    try:
        infidelity = sp.simplify(1 - expr)
        s = sp.series(infidelity, p, 0, n=3)
        return float(s.coeff(p, 2))
    except:
        return None

if __name__ == '__main__':
    p_vals = np.linspace(0, 0.15, 300)
    exp_f  = sp.lambdify(p, EXPECTED, 'numpy')
    exp_vals = exp_f(p_vals)

    print(f"{'Model':<25} {'RMSE':>10} {'p² coeff':>10} {'O(p²)?':>8}")
    print("-" * 60)

    for name, expr in ANSWERS.items():
        r = rmse(expr, p_vals, exp_vals)
        c = p2_coeff(expr)
        is_p2 = c is not None and abs(c) > 0.001
        rmse_s = f"{r:.5f}" if r is not None else "N/A"
        c_s    = f"{c:.3f}"  if c is not None else "N/A"
        print(f"{name:<25} {rmse_s:>10} {c_s:>10} {'✓' if is_p2 else '✗':>8}")

    print(f"\nCorrect p² coefficient: {float(sp.series(1-EXPECTED, p, 0, n=3).coeff(p,2)):.4f}")
