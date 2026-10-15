# Completed E smoke campaign

Six ordinary complete 3+1D space-group CI records (SG14, SG166 and SG214, each in both separately recorded physical spin conventions) were extended by the selected neutral E8 section and accepted on n08 on 2026-10-15 UTC. This package preserves all raw CI/E8 records and their exact parent links in `sgfull-20261015-e-smoke-evidence-v2.tar.gz`.

The original CI runtime is commit `ce152c6`, source manifest `6817ca7af3c20dbb89139308046456129171d08340014eab83c7c7d6487b86bd`. All 45 source files match that commit. The extension and collector use the independently hash-checked frozen `c07c6e5` implementation. E predates the generated DAG/native VM and `formula_runtime.json`; the first generic finalizer failed before any output mutation because it required that later metadata file. Its failed report is retained. The explicit v2 finalizer verifies the original source and uses ordinary acceptance without manufacturing VM metadata or invoking recovery.

`verify.py` verifies the package, the committed sources, all six independent Smith/filling checks, and exact CI parent bytes. It also reads the four overlapping D cases directly from the adjacent `preserved_d/archives` package. SG14 spin-half, SG166 spin-half, SG166 spinless and SG214 spin-half have identical complete classifications, including presentations, roots, gauges and filling; the only differing field is `resolutionBuildTimings`, whose exact values remain recorded in `finalized_validation.json`. No classification fields were normalized or rewritten.

Run from the repository root:

```bash
python3 results/spacegroup_campaign_20261015/completed_e/verify.py
```

This is acceptance of the implemented four-data sector with its selected E8 section. The physical CI-kernel identification caveat is unchanged. The package is evidence, not a new literature comparison or a replacement for separately organized active result tables.
