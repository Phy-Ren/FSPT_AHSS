# Isolated GAP 4.13.1 optimization audit

Date: 2026-10-15. The original installation and running jobs were preserved.
The candidate is an out-of-tree build at
`/home/user/xyren/software/gap-4.13.1-o2-20261015`, compiled on n08 with at
most eight make jobs. The original source root remains
`/home/user/xyren/software/gap-4.13.1`.

## Finding

The original `config.status`, `GNUmakefile`, `cnf/GAP-CFLAGS`, and
`sysinfo.gap` agree: CFLAGS was explicitly set to
`-Wno-error=incompatible-pointer-types`, suppressing configure's usual
optimization defaults. The C kernel therefore had no `-O` setting.
Debug mode was disabled; the ELF's debug-information label did not mean
that GAP was running in its debug mode. C++ already used `-g -O2`.

The candidate uses the same conda GCC 15.2.0 compiler and source, with:

- `--disable-maintainer-mode`, preventing regeneration of shared source files;
- `CFLAGS=-O2 -Wno-error=incompatible-pointer-types`;
- `CXXFLAGS=-g -O2`;
- the original shared GAP library and package tree, without package rebuilds.

`gap-o2` executes the isolated binary with an explicit `-l` pointing to
the original library/package root. The candidate builds its own bundled
zlib in its own directory. GMP and the other resolved system libraries
remain those of the original installation. No saved workspace is used.

## Controlled startup probe on n08

Both cluster probes used `-q -b -m 256m -K 1g`, the same package loading,
and the exact sum of integers 1 through 10,000,000. Times below are GAP
CPU seconds, except the final row. The package lists are identical: 33
packages auto-loaded before HAP.

| Stage | Original | Isolated O2 | Speed ratio |
| --- | ---: | ---: | ---: |
| Initial GAP startup | 10.247 | 2.130 | 4.81 |
| Explicit HAP loading | 5.734 | 1.399 | 4.10 |
| 10 million integer additions | 3.577 | 0.283 | 12.64 |
| Entire probe, wall seconds | 20.338 | 4.636 | 4.39 |

Versions: GAP 4.13.1, HAP 1.62, Cryst 4.1.27, CrystCat 1.1.10,
Polycyclic 2.16. The arithmetic sum was exactly 50000005000000.

For context, local GAP 4.12.1 on the Ryzen 9 9950X3D measured
0.334/0.348/0.110 CPU seconds for the same three stages. The cluster
n08 CPU is a Xeon E5-2680 v4 at 2.40 GHz. Local startup auto-loaded only
seven packages. The local/cluster comparison is not a controlled
single-variable experiment; the same-node original/O2 comparison is.

## Provenance and scope

- Executable SHA256:
  `873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea`.
- Source/build-input manifest SHA256:
  `18941be8159a09b7b6e8bcad49c08362fa3db652b36869847f84bfc444d46b01`.
- `source_inputs.json` pins 206 source/build files.
- `original_before.json` and `original_after.json` verify unchanged selected
  original binary/configuration files.
- `review_manifest.json` pins the downloaded build logs and metadata.
- `startup_benchmark_original.json` explicitly identifies the preserved
  numeric baseline as transcribed from the actual pre-build tool output;
  `startup_benchmark_o2.json` is the direct saved process output.

These startup measurements are microbenchmarks, not full classification
timings. The same frozen snapshot-C SG19 paired classification is recorded
separately in the [performance audit](../README.md); its exact root and
presentation comparison and the focused backend/cache/affine tests are
the scientific compatibility checks. The build and startup evidence here
does not replace those checks.

The first candidate does not use `-A`, a workspace image, altered package
loading, new formulas, or a different classifier. Reducing automatic
package loading or saving a clean package workspace could be investigated
later, but either would need its own exact regression. O2 already removes
a large measured overhead without those additional changes.
