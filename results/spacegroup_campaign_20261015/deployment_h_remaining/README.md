# H replacement launches for 24 remaining G cases

This package records two additional ordinary campaigns. It does not establish successful completion or acceptance, and every original G/H job was left running.

| Node | Start UTC, 2026-10-15 | Runner PID | Finalizer PID | Standalone cases |
| --- | --- | --- | --- | --- |
| n02 |15:17:56.448996|42054|42071|12|
| n03 |15:18:03.871594|40335|40348|12|

Remote tags are `sgfull-20261015-h-remaining-n02` and `sgfull-20261015-h-remaining-n03`. Each node uses at most 12 independent jobs, 12g per case and an individually enforced 14400-second timeout. There is no paired timeout budget. Preflight found 56 logical CPUs per node, loads 4.95/4.03, and available-memory estimates 457.45/462.80 GiB. Each new campaign adds at most 144 GiB in GAP workspace limits plus ordinary process overhead.

The source is the unchanged H snapshot, commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, source SHA256 `80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`. All 60 recorded source files, the snapshot archive, actual native VM, optimized GAP executable and external finalizer were rehashed before spawning. All 24 input bytes match the canonical catalogue. The VM SHA256 is `0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`; GAP is `873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea`. Modes are native primary, Smith cycles, certified closed source and canonical vacuum reduction.

The archived plan records all 201 original G-selected IDs and a complete D/E/F/G/H parent-selection map covering 460 distinct catalogue IDs. It excludes 173 existing native outputs only after complete JSON parsing, saved root-vector/chain/completion checks, independent Smith reduction and primitive-cell filling checks. Their exact hashes are retained. The four SG226/230 cases already assigned to the separate H-tail control are also excluded, leaving 24 candidates. Immediately before launch, all assigned cases were rechecked across known campaigns; none had acquired valid native output. A file's mere existence or an uncertain parse was not used to exclude a case.

These 173 hashes are availability evidence, not accepted results or a stopped-process recovery certificate. The eventual proposed partition is G 173 plus H-new 28, together with D 250 / E 2 / F 2 / primary H 5. This arithmetic covers 460 only after full acceptance and duplicate selection. It does not authorize cancellation, establish recoverability of running G natives, or alter any original selection ledger.

`initial_metadata.tar.gz` preserves 39 original metadata/script files plus an internal byte-hash inventory. Its SHA256 is `9e03964c682218d542f40b03c97a33a8f209ba3dbcb7f73210da2afc5e30ca81`. Paths inside are relative to `/home/user/xyren/AllFSPT_insulator`; capture time is 15:18:29.954009 UTC. All 24 initial run records were running. This is a per-file byte snapshot, not an atomic campaign state. The complete plan and one-shot launcher are inside the archive; they are evidence, not instructions to reuse existing output tags.

Run `python results/spacegroup_campaign_20261015/deployment_h_remaining/verify.py`. It checks package and archive hashes, source and catalogue bytes against the immutable Git commit, exact selected/excluded sets, native-availability certificate metadata, coverage, commands, source/runtime identities and finalizer links. It reads no live process state and makes no completion claim. The verification rechecks recorded evidence; it does not reconstruct absent native files or rerun their cochain calculations.

The isolated completion downloader started locally at 15:22:54 UTC as PID 223851. `downloader/` preserves its exact helper, wrapper, configuration, launch record and initial waiting status. The helper is byte-identical to the previously reviewed [completed-H downloader](../completed_h/download_tool/download_completed.py), SHA256 `15b4501bb0bfbb35c316221cbfdcd77299ff4590ed7d6928abf4b616fa8b7ba3`. Only its in-memory `TAGS` and `HERE` configuration are changed by the separate wrapper. Existing downloader PID 7779 and its source were left unchanged. The active external directory is `/home/xingyu/AllFSPT_reviews/completed_h_replacements_download_20261015`.

It polls these three exact H tags every 60 seconds for at most 10 hours. Only a verified complete remote finalizer permits download to `/home/xingyu/insulator-campaign-download/TAG-finalized`; archive hashes, unchanged finalization, safe members, source identities and exact frozen-G collector replay must pass. It sends no process-control signals and launches no classification. Future downloaded results and acceptance evidence are separate from this immutable launch package.
