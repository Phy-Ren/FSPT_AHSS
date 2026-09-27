# Saved p+ip diagnostic evidence

`crystalline_spin_half.json` is derived solely from the accepted 230 independent
results in `../space_groups`. It retains each input SHA-256, source/convention
identifiers, original candidate records, JSON evidence pointers, and marked
torsion-square relation components. No GAP evaluation or reference-answer lookup
was performed. Missing initial classes are recorded as missing, never as zero.

Regenerate with `scripts/analyze_pip_diagnostics.py`; the detailed interpretation
and exact group lists are in `docs/PIP_DIFFERENTIAL_DIAGNOSTICS.md`.
