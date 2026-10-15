# Incomplete H-tail 8g control: historical evidence

The original paired SG226 job exhausted its GAP 8g workspace after 7,750.144
seconds. Both wrappers retain `status: failed`, exit code 1 and no native or
result output. The second, spinless case never obtained a start boundary or
completion marker; its failed wrapper does not represent a separately executed
spinless calculation. The saved error is:

```text
Panic in /home/user/xyren/software/gap-4.13.1/src/gasman.c:1630: cannot extend the workspace any more!!!!
```

The other paired job, SG230, produced two ordinary complete CI records. They
are retained as diagnostics only. This four-case campaign is incomplete; its
finalizer names exactly the two SG226 cases for retry. No E8/collector output
from this parent is accepted, and neither SG230 record is selected here for
the final catalogue. The separately launched standalone parents retain their
own provenance and completion requirements.

`raw.tar.gz` preserves all 33 original files: source/runtime/selection metadata,
the complete case directories and summary, launch records, logs and finalizer
report. It is 77,410 bytes with SHA256
`e177bc43ebd28aafb97abc2be94d1adcfae4938a52e57fc2c6a8141dd6933e90`.
The capture read every artifact twice and confirmed unchanged bytes. It also
checked all 60 actual frozen-H source files and the actual formula library
against their manifests. It changed no remote files and sent no signals.

CI source is commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, manifest SHA256
`80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`.
The native formula library SHA256 is
`0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`.
The verifier binds unchanged launch metadata to the
[original launch archive](../deployment_h_tail/README.md), checks every source
file and input against Git, and verifies exact diagnostic result wrappers.
It does not recompute cochains or certify a physical classification.

```sh
python3 results/spacegroup_campaign_20261015/failed_h_tail_control/verify.py
```

This is an offline evidence check only. A relocated package accepts
`--repository /path/to/checkout`. The retained `capture.py` documents the
read-only acquisition procedure; rerunning it is unnecessary for verification.
