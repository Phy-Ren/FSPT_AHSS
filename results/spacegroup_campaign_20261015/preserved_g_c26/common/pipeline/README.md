# Prepared G preservation pipeline

Prepared 2026-10-15 UTC. This directory is preparation and a local synthetic validation only. No cluster command below has been executed by this preparation, no process has been signalled, and no real G preservation or acceptance is claimed.

`postprocess_g.py` consumes an existing root-approved stop/observed-ended report. It never creates that process proof, sends signals, queries processes, reruns CI classification, or rewrites an original campaign. Its only mathematical calculation is the already reviewed neutral E8 section through the immutable c26 helper.

## Preconditions and exact scope

Root first establishes that the original G campaign is stopped or observed ended. A live runner must pass the current cleanup policy and the stopper's fresh identity checks; a genuinely ended tree can use the reviewed no-signal attestor without waiting for H. The original failed selections remain failed. In particular, original G226/230 workspace failures are not repaired or promoted.

The revised live cleanup criterion is narrower than waiting for every H tail result: accepted H24, all required G88 original ordinary completions unchanged, all four original G tail cases failed and absent from active jobs, and every remaining active G batch case covered by accepted H24. Root must verify these conditions freshly. Final460 acceptance still requires the four tail replacements. This script does not authorize or evaluate that live cleanup criterion.

`prepared_config.json` pins all 65 files of deployed c26, both original G selections/source hashes, and the required 42 n02 / 46 n03 input/native hashes from the recorded prelaunch availability evidence. Every required input must also match the exact canonical catalogue. Every required case must pass c26's **ordinary completion** inspector; no needed case may be a retry. All valid original selected cases are preserved, including extra controls, and final assembly later selects only the explicit42/46 subsets. The original selection and recovery ledger are never reduced.

At run time, the pipeline verifies the exact helper, original source/runtime, existing report and evidence, original required cases, full CI/E8 byte agreement and collection. It hashes the entire original raw campaign before and after. Its archive contains the whole raw original parent, report evidence, preserved CI, E8, accepted collection and execution logs. The completion state is `accepted-preserved-subset`, not successful completion of the failed original campaign.

## Deployment preparation

The new two-file snapshot archive and `snapshot_metadata.json` are beside this README. Root may deploy it, verify every member, and mark it read-only at the proposed new path:

`/home/user/xyren/AllFSPT_insulator/snapshots/g-preservation-70cc4c24`

The existing helper stays unchanged at:

`/home/user/xyren/AllFSPT_insulator/snapshots/preservation-helper-c26f3de`

The pipeline verifies all its files against the pinned manifest before and after processing. It must run on the original compute node; hostname mismatches reject. Python is the existing runtime Python3.8.

## Root invocation after a valid report

For n02, after root obtains a validated `cancellation.json` at the actual chosen report path:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/xyren/AllFSPT_insulator/runtime/bin/python3 \
  /home/user/xyren/AllFSPT_insulator/snapshots/g-preservation-70cc4c24/postprocess_g.py \
  run --node n02 --report /ABSOLUTE/VALIDATED/N02/REPORT/cancellation.json
```

For n03 use the same exact executable/script, `--node n03`, and its own report. Invoke on the node through the established persistent SSH channel. Only the report path is chosen after root's process verification; the original campaign, source, output paths, required subset and helper are pinned by the config.

Each invocation requires all following paths to be new, using NODE=n02 or n03:

- `/home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-g-NODE-preserved-c26f3de`
- the same prefix plus `-e8`, `-accepted`, `-operation`, `-evidence.tar.gz`, and `-completion.json`.

A failed attempt leaves its evidence available for review and does not overwrite it on retry. No original file is modified. If original finalizers subsequently report incomplete because the original full selection contains failed or deliberately stopped controls, retain that original status; it is not a failure of the independently checked selected G88 records.

## Download and exact local replay

Download the completion JSON, archive, and completion JSON again through the existing persistent `cuhk-cluster3` channel. The second completion download must be byte-identical to the first. Example for n02, using a **new** staging directory already created locally:

```bash
ssh -o ControlMaster=no -o ProxyCommand=false -o BatchMode=yes cuhk-cluster3 \
  'cat /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-g-n02-preserved-c26f3de-completion.json' \
  > completion.json
ssh -o ControlMaster=no -o ProxyCommand=false -o BatchMode=yes cuhk-cluster3 \
  'cat /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-g-n02-preserved-c26f3de-evidence.tar.gz' \
  > evidence.tar.gz
ssh -o ControlMaster=no -o ProxyCommand=false -o BatchMode=yes cuhk-cluster3 \
  'cat /home/user/xyren/AllFSPT_insulator/runs/sgfull-20261015-g-n02-preserved-c26f3de-completion.json' \
  > completion.second.json
cmp completion.json completion.second.json
```

Abort on any SSH/nonzero comparison result. Then run locally, replacing only the two downloaded input paths and choosing a NEW output:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  /home/xingyu/AllFSPT_reviews/g_preservation_prepared_20261015/postprocess_g.py verify \
  --node n02 --completion /ABSOLUTE/NEW/STAGING/completion.json \
  --archive /ABSOLUTE/NEW/STAGING/evidence.tar.gz \
  --output /home/xingyu/insulator-campaign-download/sgfull-20261015-g-n02-preserved-c26f3de-bundle \
  --helper /home/xingyu/AllFSPT_reviews/spacegroup_full_catalogue_20261015/accelerated_gate/preservation-helper-c26f3de \
  --catalog /home/xingyu/FSPT_AHSS_insulator/insulator_catalog/generated
```

The verifier checks archive length/hash, every regular member and safe path before extracting, then revalidates the original required ordinary cases, complete preserved parents and exact CI→E8 bytes. It invokes the exact frozen collector and requires literal equality of `results.json`, `ci_results.json` and `validation.json` with the accepted remote files. Path-dependent collection provenance is retained separately rather than falsely required to be identical. All extracted original bytes are checked unchanged afterward.

The resulting `download_verification.json` and `assembly_entry.json` give the portable proof and exact42/46 selection. Add these entries to a new full460 manifest; do not edit any parent selection or ledger. Validate every full parent before applying these subsets, as the final assembler already does.

## Local evidence

`test_local_pipeline.py` exercised the exact candidate code with rebased paths and an existing genuine native scientific fixture, using the deployed c26 bytes locally. It retained one ordinary completed record out of a three-case original selection and kept two retries, including an incomplete singleton. The E8 section, collector, archive and offline frozen collector replay all passed; original raw bytes were unchanged. Existing outputs, a corrupt downloaded archive and a wrong required-subset completion proof all rejected. It did not use SSH, signal a process or run a CI classifier. `local_test_result.json` records the candidate SHA and fixture directory; raw stdout/stderr are retained.
