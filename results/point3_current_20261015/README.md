# Current 3+1D point-group calculations

All 64 physical-spin backgrounds were classified with immutable source
`c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`, including complete charge and
sheet primitives, gauges, and integer stacking presentations. The CI records
come from the [optimized point-group audit](../point3_optimized_20261015/README.md).
All 64 presentations agree exactly with the previously accepted computations;
the active tables display only this latest collection.

The neutral E8 section was then computed with the explicit 3+1D postprocessor.
`collection.json` records accepted coverage and hashes. Each E8 record embeds
the exact CI result it consumed, and the collector independently checks Smith
invariants, filling, E8 root relations, and source/input identities. This is
the existing selected neutral section, with the physical CI-kernel
identification caveat retained in every classification.

`e8_raw.tar.gz` preserves all 64 postprocessor records, inputs, source hashes,
and witnesses. `e8_archive.json` records its SHA256. The CI raw archive remains
in the linked optimized point-group audit; it is not duplicated here.

The accepted collection was produced by:

```sh
python scripts/collect_expansion.py \
  --ci-root /path/to/point3_optimized_g_20261015/run \
  --e8-root /path/to/point3_optimized_g_20261015/e8 \
  --output /path/to/new-accepted-point3-collection
```
