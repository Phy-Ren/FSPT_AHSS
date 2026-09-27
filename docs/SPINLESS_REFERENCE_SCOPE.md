# Available references for the second spin convention

The supplied materials contain **no complete 230-affine-space-group answer
table for crystalline spinless / internal spin-1/2 fermions**. This is an
availability finding, not a claim that collaborators have not computed such
a table elsewhere. No upstream fetch or reference classification program was
run for this inventory.

The complete static inventories, `spinless_reference_inventory.json` and
`spinless_reference_checkout_inventory.json`, are retained only in the private
working copy. They include source excerpts and are excluded from the public
snapshot. The inventory covers all 171 recovered boss-archive files and hashes
191 tracked files in the locally available collaborator checkout, at commit
`c2961a2d6ee9465a7b634a31b6c095e607972966`. That checkout is shallow, so this
does not cover unpublished files or unfetched revisions. The scope findings
below are the public account; the nine geometric overlap controls below provide separate numerical evidence
bound to both accepted archives.

| Material | Available scope | Second-convention comparison |
|---|---|---|
| Boss `space_group_230_layers.pdf` | All 230 **affine** groups, four layers, physical spin-half and effective omega=0; explicitly excludes stacking extensions | Wrong background for the new 230-table comparison |
| Boss recovered `draft_table.json` | Historical first-convention manuscript transcription, 230 layer rows and 204 stacking entries | Historical first-half data, not a second-half independent output |
| Boss ordinary cohomology files | Full affine groups; signed H1 and mod-two / signed integral E2 inputs | Background-independent raw inputs can be checked; they are not permanent layers |
| Weicheng transfer results | Finite C2, multiple dimensions; four dimension-3 nonzero-omega labels representing two inputs | Valid finite controls only: unitary gives the trivial group, antiunitary gives Z16 |
| Weicheng C2h gauge result | Finite C2×C2, omega=w2+w1²; explicit interrupted full calculation | Gauge evidence, no completed full classification |
| Manuscript spinful-internal point-group table | 32 finite point groups | Separate finite inputs; cannot substitute for 230 affine groups |

The four matching finite-C2 labels are `wang-gu-C2-unitary-nonsplit`,
`crystalline-C2-spinless`, `wang-gu-C2-antiunitary-nonsplit`, and
`crystalline-Cs-spinless`. These label two mathematical inputs, not four
independent tests. They must not be compared to affine SG3 or SG6 merely
because those groups have the same point-group quotients.

The boss's `FOUNDATIONS.md` gives full-group predictions for nine oriented
torsion-free groups: 1, 4, 19, 76, 78, 144, 145, 169, 170. It states the
omega=0 convention. The final accepted second-convention results now certify
that the physical extension is trivialized on the **full affine group** in all
nine cases: the saved native gauge satisfies gauge·D1=original omega, and the
orientation character is zero. All four graded layers, full abstract groups
and free-lattice indices agree across the two conventions. Eight of the nine
original native omega vectors are nonzero, so this check uses the actual gauge,
not merely a zero-background label.

The [nine-case certificate](../results/optimization_validation/background_v3/physical_conventions/geometric_overlap_9.json)
has SHA-256 `d845f5d57dbd7afc4d93365551611b20164178ccc8674bbec12d7d3a3717339c`
and binds both sets of result hashes. It licenses reuse of those nine geometric
predictions as shared special cases. Together with the two distinct finite-C2
inputs, this is limited external evidence; it is not a new-convention
230-row independent reference.

## Can the supplied boss code be run for the other spin convention?

Not as a complete second-convention classification pipeline in its supplied
state. The available backend really constructs the full affine group using
`SpaceGroupBBNWZ(3,it)` and HAP, rather than replacing it by its point group.
The available all-group entry `output/space_group_230/backend/hap_all230_e2.g`
computes only mod-two ordinary cohomology. The signed cohomology templates
and Python collectors likewise produce raw E2 inputs, with the determinant
coefficient action.

The archive is truncated (347,645 bytes, SHA-256
`a24ec834cf8b811d7111620143d57901ed61cbd52533ce9b1eca65af9eb9fdef`).
Its README documents `pip/`, `majorana/`, `fermion_boson/`, `o5/`,
`build_report.py` and `validate_final_report.py`; all are absent from the
recovered tree. The README fixes effective omega=0. No available physical
spin selector or omega=w2+s² input was found. Some generated GAP scripts
also retain an absolute original workspace path that would need relocation.
Changing that path or supplying `GAP_BINARY`/`GAP_ROOT` does not restore the
missing higher-differential pipeline.

A complete source archive is needed to determine whether its full engine can
select the other physical background. Reconstructing missing modules and
adding background-dependent obstructions would be new implementation, not
an immediate run of an already available independent reference.
