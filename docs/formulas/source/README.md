# Maintaining one formula reference

This directory is the only editable source for the reader formula pages.
The Markdown files one level above, the main guide, and the programmer
translation are generated views. Edit the source, then run:

```sh
python docs/formulas/build_reference.py
python docs/formulas/build_reference.py --check
```

- `equations/` contains the maintained display equations. An equation
  reused verbatim on several pages is stored once. Its descriptive file
  name identifies the page and contribution where it first appears.
- `pages/` contains the exposition and equation references. General
  stacking and self-stacking have distinct page sources, with their
  physical domains stated explicitly. Specializing a general law is a
  mathematical derivation, not a blind replacement of prime symbols.
- `catalog.json` lists the generated destinations. The generated
  `../REFERENCE_MANIFEST.json` records every source dependency, checksum,
  and page that uses a shared equation.
- Long coefficient appendices remain together in their page sources;
  their fixed machine-readable coefficient tables remain under
  `../coefficients/` and `../term_census/`. They are not renamed as new
  mathematical operations.

For a reviewed new page, import it once:

```sh
python docs/formulas/build_reference.py \
  --import-page docs/formulas/NEW_PAGE.md --from-file /path/to/reviewed.md
```

Subsequent routine edits belong in its maintained source. Never update a
reader page and its source independently. `--check` rejects a stale or
hand-edited generated page. Shared equation changes propagate to every
page using that equation; the manifest makes their scope reviewable.

A change to the cochain representative still requires its explicit
paired source/product map, affected gauge maps, formula verification,
and updated counts. This document generator does not prove an identity
or translate arbitrary LaTeX into a numerical evaluator. The numerical
implementation and its coordinate maps are documented in the generated
programmer translation. Frozen source archives and regression evidence
remain frozen; they are not competing current reader definitions.

Before publication, run the applicable exact formula certificates,
regenerate all pages, run `--check`, check links, and inspect actual
GitHub rendering. Publish the source and generated pages in the same
commit. Record which reductions are incorporated in the main formulas
and which are proved identities awaiting a full formula assembly.
