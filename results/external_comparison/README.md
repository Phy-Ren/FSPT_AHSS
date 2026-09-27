# External comparison evidence in the public release

The accepted independent results are in `results/space_groups`. The independent
classification freeze is preserved in `results/classification_frozen`.

- All 920 current graded-layer entries match both the original independent
  freeze and the supplied current reference PDF.
- Of 204 populated historical full-stacking rows, 179 agree, 21 differ already
  in graded layers, and four differ with identical graded layers (68, 81, 82,
  101). Another 26 reference rows are blank.
- Nine geometric examples, 687 initial mod-two cohomology dimensions, all 230
  signed H1 groups, and four finite-model labels (two distinct inputs) agree.
- The supplied current PDF has no full-stacking table. The available Weicheng
  materials have no affine-230 full-stacking table. SG219 has no historical
  full-stacking value to compare.

`public_summary.json` retains statistics and hashes. `inputs/manifest.json`
identifies the privately retained reference bytes; those bytes and detailed
reference-row transcriptions are not distributed. The independent finite C2
controls remain in `inputs/finite_c2_controls.json`.

The comparison tools are included for use with separately supplied authorized
reference copies. They are optional and never feed production results. See
[public release scope](../../PUBLIC_RELEASE.md#private-comparison-materials),
[comparison analysis](../../docs/COMPARISON_WEICHENG.md), and
[graded-layer comparison](../../docs/BOSS_LAYER_COMPARISON.md).
