#!/usr/bin/env python3
"""Run the complete serial finite-group classification and stacking pipeline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.finite_examples import gap_literal
from fspt.full_run import freeze_runtime, publish_result, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--dimension", type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gap", default=os.environ.get("AFS_GAP") or shutil.which("gap"))
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--audit-generators", help="Comma-separated generator names for focused coherence triples; implies --audit")
    parser.add_argument("--coherence-shards", type=int, default=1,
                        help="Optional number of disjoint coherence audit shards; each recomputes the full presentation.")
    parser.add_argument("--coherence-shard-index", type=int,
                        help="Zero-based shard index; requires --audit and --coherence-shards greater than one.")
    parser.add_argument("--coordinate", choices=("publication", "majorana-ca", "majorana-operator"), default="publication")
    parser.add_argument("--zero-chiral-fiber", action="store_true",
                        help="Compute a finite unitary d2 zero-chiral subgroup and separately report its abstract Z completion")
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--trace-reduction-stages", action="store_true",
                        help="Emit CPU stage markers around exact layer reduction operations")
    parser.add_argument("--tensor-abelian", action="store_true")
    parser.add_argument("--dihedral-resolution", action="store_true",
                        help="Use an independently built standard permutation dihedral resolution")
    parser.add_argument("--canonical-face-cache", action="store_true",
                        help="Opt in to common-left-translation invariant production face memoization")
    parser.add_argument("--certified-zero-lowers", action="store_true",
                        help="Preserve literal zero lower sources under checked pointwise integer-cochain certificates")
    parser.add_argument("--certified-cube-primitive", action="store_true",
                        help="Use the exact finite-unitary h-cubed primitive for n=2h and zero other lower/background fields")
    parser.add_argument("--certified-binary-primitive", action="store_true",
                        help="Use the complete local lookup primitive for binary integral n=omega and zero other lower fields")
    parser.add_argument("--certified-cf-square", action="store_true",
                        help="Use an exactly matched integral-square CF representative and its Cartan primitive")
    parser.add_argument("--certified-character-mc", action="store_true",
                        help="Use the universal flat-lift lookup for a closed character times a binary integral cocycle")
    parser.add_argument("--vacuum-mc-kernel", action="store_true",
                        help="Use the exact compiled d4 publication-coordinate vacuum Majorana cylinder")
    parser.add_argument("--vacuum-cf-kernel", action="store_true",
                        help="Use the exact compiled d4 publication-coordinate vacuum complex-fermion cylinder")
    parser.add_argument("--mc-n0-kernel", action="store_true",
                        help="Use the exact non-vacuum Majorana cylinder with zero integer field")
    parser.add_argument("--cf-n0-kernel", action="store_true",
                        help="Use the exact non-vacuum fermion cylinder with zero integer and Majorana fields")
    parser.add_argument("--vector-request-cache", action="store_true",
                        help="Use a complete typed integer-face key before serializing formula requests")
    parser.add_argument("--pure-cf-source", action="store_true",
                        help="Use the exact composed d3 source when integer and Majorana fields vanish.")
    parser.add_argument("--n0-source", action="store_true",
                        help="Use the exact composed d3 source for a legal tower with zero integer field.")
    parser.add_argument("--closed-cf-source", action="store_true",
                        help="Use the certified direct d3 closed-CF source for marked native cocycle lifts.")
    parser.add_argument("--normalize-binary-extension", action="store_true",
                        help="Record a verified parity-section change to a binary integral extension lift when available")
    parser.add_argument("--cf-primary", choices=("bar", "native", "compare"),
                        help="Evaluate the closed CF primary operation by bar cochains, native cup classes, or both")
    parser.add_argument("--mc-primary", choices=("bar", "native", "compare"),
                        help="Evaluate the closed Majorana primary operation by bar cochains, native cup classes, or both")
    parser.add_argument("--gauge-audit-layers", help="Comma-separated native gauge layers: 3=integer, 2=Majorana, 1=fermion")
    parser.add_argument("--bar-audit-samples", type=int, default=0,
                        help="Seeded pointwise probes per equation, independent of comparison-chain support")
    parser.add_argument("--bar-audit-generators",
                        help="Explicit comma-separated marked generator names; required when --bar-audit-samples is positive.")
    parser.add_argument("--bar-audit-seed", type=int, default=20261001)
    parser.add_argument("--mc-partial-cache-limit", type=int, default=0,
                        help="Retain up to this many exact n=0 partial Majorana states and source projections (0 disables).")
    parser.add_argument("--f2-parity-filter", action="store_true",
                        help="Filter exact even/duplicate coefficients before F2 cochain evaluation.")
    args = parser.parse_args()
    if args.bar_audit_samples < 0:
        parser.error("Bar audit sample count must be nonnegative.")
    if args.bar_audit_samples > 0 and (
            not args.bar_audit_generators or
            any(not name.strip() for name in args.bar_audit_generators.split(","))):
        parser.error("Positive --bar-audit-samples requires explicit nonempty --bar-audit-generators.")
    if args.coherence_shards == 1:
        if args.coherence_shard_index is not None:
            parser.error("A coherence shard index requires at least two shards.")
    elif (not 2 <= args.coherence_shards <= 64 or args.coherence_shard_index is None
          or not 0 <= args.coherence_shard_index < args.coherence_shards
          or not (args.audit or args.audit_generators)):
        parser.error("Coherence sharding requires --audit, 2..64 shards, and a valid zero-based index.")
    if args.f2_parity_filter and args.dimension not in (3, 4):
        parser.error("F2 parity filtering is currently gated only in dimensions three and four.")
    if not 0 <= args.mc_partial_cache_limit <= 1024:
        parser.error("Partial Majorana cache limit must be between 0 and 1024.")
    if (args.pure_cf_source or args.n0_source or args.closed_cf_source) and args.coordinate != "publication":
        parser.error("The pure-CF source kernel is in publication coordinates.")
    # Native primary classes are independently checked against the complete
    # bar formulas in dimensions three and four. Lower endpoints retain their
    # separately calibrated bar laws by default.
    if args.cf_primary is None:
        args.cf_primary = "native" if args.dimension >= 3 else "bar"
    if args.mc_primary is None:
        args.mc_primary = "native" if args.dimension >= 3 else "bar"
    if not args.gap:
        parser.error("Provide --gap or set AFS_GAP.")
    if args.tensor_abelian and args.dihedral_resolution:
        parser.error("Choose only one alternate resolution.")
    if args.output.exists():
        parser.error("Output exists; use a fresh result path to retain provenance.")
    catalog = json.loads(args.catalog.read_text())
    models = catalog["models"] if isinstance(catalog, dict) else catalog
    model = next((m for m in models if m["id"] == args.model), None)
    if model is None:
        parser.error("Unknown finite model in catalog.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.trace:
        if args.trace.exists():
            parser.error("Trace exists; choose a fresh path")
        args.trace.parent.mkdir(parents=True, exist_ok=True)
    source, provenance = freeze_runtime(ROOT)
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="fspt-complete-finite-") as directory:
        work = Path(directory)
        keys = ("id", "group", "order", "productTable", "s1", "omega2", "generatorIndices")
        inp = {key: model[key] for key in keys}
        (work / "models.g").write_text("AFS4_TABLE_MODELS:=" + gap_literal([inp]) + ";;\n")
        settings = {
            "AFS_ROOT": str(source), "AFS4_MODEL_FILE": str(work / "models.g"),
            "AFS4_MODEL_ID": model["id"], "AFS_OUT": str(work / "raw.json"),
            "AFS_FULL_DIMENSION": args.dimension, "AFS_FULL_PYTHON": args.python,
            "AFS_STACK_AUDIT": args.audit or bool(args.audit_generators),
            "AFS_FULL_COORDINATE": args.coordinate,
            "AFS_FULL_TRACE_REDUCTION": args.trace_reduction_stages,
            "AFS_FULL_ZERO_CHIRAL_FIBER": args.zero_chiral_fiber,
            "AFS_FULL_CANONICAL_FACE_CACHE": args.canonical_face_cache,
            "AFS_FULL_CERTIFIED_ZERO_LOWERS": args.certified_zero_lowers,
            "AFS_FULL_CERTIFIED_CUBE_PRIMITIVE": args.certified_cube_primitive,
            "AFS_FULL_CERTIFIED_BINARY_PRIMITIVE": args.certified_binary_primitive,
            "AFS_FULL_CERTIFIED_CF_SQUARE": args.certified_cf_square,
            "AFS_FULL_CERTIFIED_CHARACTER_MC": args.certified_character_mc,
            "AFS_FULL_VACUUM_MC_KERNEL": args.vacuum_mc_kernel,
            "AFS_FULL_VACUUM_CF_KERNEL": args.vacuum_cf_kernel,
            "AFS_FULL_MAJORANA_N0_KERNEL": args.mc_n0_kernel,
            "AFS_FULL_FERMION_N0_KERNEL": args.cf_n0_kernel,
            "AFS_FULL_VECTOR_REQUEST_CACHE": args.vector_request_cache,
            "AFS_FULL_PURE_CF_SOURCE": args.pure_cf_source,
            "AFS_FULL_N0_SOURCE": args.n0_source,
            "AFS_FULL_CLOSED_CF_SOURCE": args.closed_cf_source,
                    "AFS_FULL_MC_PARTIAL_CACHE_LIMIT": args.mc_partial_cache_limit,
                    "AFS_FULL_F2_PARITY_FILTER": args.f2_parity_filter,
            "AFS_FULL_NORMALIZE_BINARY_EXTENSION": args.normalize_binary_extension,
            "AFS_FULL_CF_PRIMARY": args.cf_primary,
            "AFS_FULL_MC_PRIMARY": args.mc_primary,
        }
        if args.trace:
            settings["AFS_FULL_TRACE"] = str(args.trace.resolve())
        if args.audit_generators:
            settings["AFS_FULL_AUDIT_GENERATORS"] = args.audit_generators.split(",")
        if args.coherence_shards > 1:
            settings["AFS_FULL_COHERENCE_SHARDS"] = args.coherence_shards
            settings["AFS_FULL_COHERENCE_SHARD_INDEX"] = args.coherence_shard_index
        if args.bar_audit_samples:
            settings.update(AFS_FULL_BAR_AUDIT_SAMPLES=args.bar_audit_samples,
                            AFS_FULL_BAR_AUDIT_GENERATORS=args.bar_audit_generators.split(","),
                            AFS_FULL_BAR_AUDIT_SEED=args.bar_audit_seed)
        if args.gauge_audit_layers:
            settings["AFS_FULL_GAUGE_AUDIT_LAYERS"] = [int(x) for x in args.gauge_audit_layers.split(",")]
            if any(x not in (1, 2, 3) for x in settings["AFS_FULL_GAUGE_AUDIT_LAYERS"]):
                parser.error("Gauge audit layers must be 1, 2, or 3.")
        driver = "".join(key + ":=" + gap_literal(value) + ";;\n" for key, value in settings.items())
        entry = "run_full_finite_tensor.g" if args.tensor_abelian else "run_full_finite.g"
        if args.dihedral_resolution:
            entry = "run_full_finite_dihedral.g"
        driver += 'Read(Concatenation(AFS_ROOT,"/gap/'+entry+'"));\n'
        (work / "driver.g").write_text(driver)
        process = subprocess.Popen(
            [args.gap, "-q", "-r", "-b", "-T", str(work / "driver.g")],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        complete, error = False, False
        for line in process.stdout:
            print(line, end="", flush=True)
            complete |= "AFS_FULL_FINITE_COMPLETE" in line
            error |= line.startswith(("Error,", "Syntax error:"))
        if process.wait() or not complete or error:
            raise SystemExit("Complete finite calculation failed or lacked its completion marker.")
        result = json.loads((work / "raw.json").read_text())
    result.update(provenance)
    result["pureCFSource3Kernel"] = args.pure_cf_source
    result["n0Source3Kernel"] = args.n0_source
    result.update(started=started, finished=time.time(), wall_seconds=time.time() - started,
                  catalog_sha256=sha256(args.catalog),
                  input_model_sha256=hashlib.sha256(
                      json.dumps(inp, sort_keys=True).encode()).hexdigest())
    publish_result(args.output, result)


if __name__ == "__main__":
    main()
