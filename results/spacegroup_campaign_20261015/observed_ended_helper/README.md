# Reviewed observed-ended campaign helper

Review date: 2026-10-15 UTC. Root and the formula agent approved the exact final script bytes after the actual CLI tests passed. The benchmark agent also reviewed the preceding absence-proof design. This package prepares an immutable deployment archive. It records **no deployment and no real ended-campaign attestation**. The only cluster operations preserved here are prior read-only live-process captures.

The historical filename `attest_natural_exit.py` does not imply a natural or successful termination. The report explicitly records `terminationMode=observed-ended-without-signaling`, `terminationCause=not_inferred`, `signalsSent=false` and `executionExitStatus=not_inferred_from_process_absence`. It never launches, freezes, resumes or terminates a process.

The helper replays exact previously captured runner/GAP ownership and saved launch metadata; pins source, runtime, selection and durable input/driver/native/result evidence; and takes two process censuses around stable final artifact hashes. Captured identities must be absent or zombie, with no active campaign/source worker or captured GAP group left. Running metadata/logs/summary may legitimately finalize between the old capture and the final observation.

The CLI necessarily contains `--root`. It excludes only its own exact PID/UID/startTicks/argv/executable identity, verifies that identity independently in each census, and records the exclusion. Parents, children and other matching commands receive no exemption. The original earlier prototype safely rejected its own CLI; that prototype and all217 external evidence hashes remain unchanged as historical review evidence.

Fourteen local checks pass, including real CLI success, real CLI rejection of an active runner and a scoped worker, changed observer argv, late worker discovery, and an artifact mutation during observation. All three CLI signal traces are empty. The actual CLI report passes the unchanged c26f3de preserver: the valid original per-case exit0 and actual batch exit1 survive byte for byte, while the incomplete singleton remains a retry. No failed result wrapper is rewritten and no successful exit is inferred.

`local_cli_evidence.tar.gz` contains the final raw local fixture, process observations, CLI logs/traces, attestation and preserved output. The copied harness retains its original review-workspace paths; it is recorded evidence rather than an environment-independent integration test. `local_test_result.json` pins the tested attestor bytes. `snapshot_manifest.json` pins the deployment archive's five exact files: the attestor, reviewed process helper and two prior live captures with their manifest. The process helper is imported only for read-only functions. The offline c26 preservation helper is unchanged and is not replaced by this snapshot.

Verify the package without contacting a cluster:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 results/spacegroup_campaign_20261015/observed_ended_helper/verify_package.py
```

After root deployment, run the attestor only on the original campaign node and only after the campaign has ended. A live identity causes immediate refusal. Its `cancellation.json` filename is retained solely for compatibility with the existing preservation schema; it does not claim a cancellation occurred. An ended original campaign with failed superseded cases may be attested/preserved immediately, while final460 acceptance still waits for the full selected replacement coverage. The live-campaign stop policy remains separate.
