# Singleton ownership preflight for future stopped campaigns

Review date: 2026-10-15 UTC. The promoted [stop helper](../../../scripts/stop_owned_campaign.py) now recognizes a precisely identified ordinary singleton GAP child alongside genuine paired jobs. It checks exact launch argv, own process group, source/host, case ID, input bytes/hash and embedded driver source/input/output. Singleton children are captured as GAP processes but never create a paired recovery batch. The existing freeze/rescan, identity-checked signaling and rollback mechanics are unchanged. Incomplete singleton recovery remains forbidden by the separate recovery helper.

The four focused unittest methods include mixed paired/singleton ownership, thirteen malformed singleton preflights, missing process identity/topology, and explicit false paired metadata. They trap all signaling and prove that malformed inputs reject before freezing, output creation or signal attempts:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_stop_owned_campaign.py -v
```

`local_process_evidence.tar.gz` preserves the separately reviewed real-process LOCAL experiment:20 checks, a synthetic runner with paired and singleton groups plus workers, and an unrelated sentinel. All malformed preflights rejected before any signal; raw campaign hashes remained unchanged and the sentinel stayed alive. Only those test-owned synthetic identities were cleaned up afterward. To reproduce it, extract the archive to a separate scratch directory and run `PYTHONDONTWRITEBYTECODE=1 python3 local_process_evidence/test_singleton_preflight.py`. It never connects to a cluster.

`validation.json` pins the exact promoted helper and test bytes. The promoted helper equals the reviewed isolated candidate byte for byte. `change.patch` compares it with the previously archived production helper. Root and a second agent reviewed the changed branch independently and found no blocker. This package does not record or authorize a live stop, and it does not modify the earlier c26f3de offline preservation snapshot.
