# Local owned-campaign stop validation

Date: 2026-10-15 UTC. This exercise used only synthetic local processes. It sent no SSH commands and no cluster signals.

The tested helper is `/tmp/stop_owned_u1_campaign.py`, SHA256 `3a871509d01b9b268b3b18f5955edcf1ab5a2c80da598bf5fa481358256d5e49`. Its exact tested bytes are preserved as `run-k7teaapx/tested_stop_helper.py`. Reproduce using `python3 test_local_stop.py`; this starts and cleans up a new local synthetic runner, a separate process-group child, its worker, and an unrelated sentinel.

Successful evidence is in `run-k7teaapx/validation.json`. All seven scenarios passed:

- A wrong runner, mismatched child argv, missing child argv, modified snapshot file, and modified formula VM each rejected before any signal call.
- Injected validation failure after freezing the runner sent only STOP and CONT to that same identity. Every synthetic process remained alive and running.
- The confirmed stop affected only the three owned identities. The unrelated sentinel remained running. Every original campaign file retained its exact hash.

The successful report independently verified the original snapshot manifest's file list after the stop. The optional formula VM check covers both a present matching file and a deliberately absent file, and rejects a changed file. The successful D-style fixture had no runtime manifest and records `not_configured` explicitly.

The real archived SG19 input/native output supplied scientific evidence for the first completed case. Offline `preserve_campaign` and `validate_recovered_case` accepted that case, retained its original running metadata, inferred no process exit code, and scheduled the second incomplete case for retry. Its two original driver copies and original logs were preserved unchanged.

`run-k7teaapx/*.signals.jsonl` records every signal call made by the tested helper. `raw_before.json` and `raw_after.json` compare the entire original campaign tree, not just selected report fields. `confirmed_stop/` holds the actual stop report and separately hashed process/source verification evidence. `recovered_subset/` holds the offline preservation output.

The preliminary `run-sbuqsegg/` attempt is retained rather than erased: its positive test exceeded an overly short 20-second harness timeout while scanning/hashing local executable identities. Its negative tests had passed and no unrelated process was signaled. The final helper reuses executable hashes only while path/device/inode/size/mtime/ctime agree, explicitly observes scheduling stops, and the final harness has a 60-second bound.

This is an operational ownership/provenance validation, not a new physical classification or an authorization to stop any cluster job. No repository runtime or frozen campaign output was modified by this exercise.
