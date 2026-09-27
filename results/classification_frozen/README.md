# Original independent classification freeze

`manifest.json` and `sg1.json` through `sg230.json` are exact byte copies
of `runs/classification_frozen`. The copy contains 231 original files and
1,133,830 bytes. Every result hash was checked against the original manifest
both before and after copying; the manifest itself was copied unchanged.

Original manifest SHA-256:

```text
42e42ce70900bf0df2dada35624198474f07e4a98dfe95770d462a69169ec438
```

This is the classification freeze made before external answers were
consulted. Its original timestamp and `external_answers_consulted=false`
field apply to that event. They do not describe the subsequent corrected
formula or performance-regression campaigns. These historical classification
files are not a newly accepted final run and do not supply the final marked
stacking witnesses.

The original first PDF comparison is preserved under
`results/boss_layers/reference_comparison.*`. See
`results/external_comparison/README.md` for commands that compare a later
`FINAL_RUN` with this unchanged freeze and the archived reference inputs.
