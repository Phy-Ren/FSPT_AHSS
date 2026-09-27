#!/usr/bin/env python3
"""Build classification and abstract stacking tables from frozen result JSON.

Only completed numerical result archives and their source files are inputs.
Each generated CSV and Markdown cell is parsed back and checked against its
original JSON field. The input archives are never modified.
"""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_point_groups import check_geometry, GEOMETRY_KEYS


CONVENTIONS = {
    "half": ("physical-spin-half-det-sign-omega0", "crystalline spin-1/2",
             "internal spinless", "s=w1; omega=0"),
    "spinless": ("physical-spinless-det-sign-Pin-minus", "crystalline spinless",
                 "internal spin-1/2", "s=w1; omega=w2+w1^2"),
}
CELL_KEYS = ("pip", "majorana", "complex_fermion", "bosonic", "stacking")
CELL_LABELS = ("p+ip", "Majorana", "Complex fermion", "Bosonic", "Full stacking group")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compact(value):
    return json.dumps(value, separators=(",", ":"))


def invariants(value, label):
    require(isinstance(value, list), label + ": expected invariant list")
    require(all(type(x) is int and (x == 0 or x >= 2) for x in value),
            label + ": invalid cyclic order")
    require(value == sorted(value), label + ": invariant order is not canonical")
    finite = [x for x in value if x]
    require(all(b % a == 0 for a, b in zip(finite, finite[1:])),
            label + ": cyclic orders do not form invariant factors")
    return list(value)


def cells(data):
    return {
        "pip": invariants(data["pip"]["orders"], "p+ip"),
        "majorana": invariants(data["majorana"], "Majorana"),
        "complex_fermion": invariants(data["complex_fermion"], "complex fermion"),
        "bosonic": invariants(data["bosonic"], "bosonic"),
        "stacking": invariants(data["stacking"]["invariants"], "stacking"),
    }


def group_text(orders):
    terms = []
    for order, count in sorted(Counter(orders).items()):
        term = "Z" if order == 0 else "Z" + str(order)
        if count > 1:
            term += "^" + str(count)
        terms.append(term)
    return " + ".join(terms) if terms else "0"


def parse_group(text):
    text = text.strip("`")
    if text == "0":
        return []
    orders = []
    for term in text.split(" + "):
        match = re.fullmatch(r"Z([2-9][0-9]*|1[0-9]+)?(?:\^([1-9][0-9]*))?", term)
        require(match is not None, "unparseable group cell: " + text)
        orders += [int(match.group(1)) if match.group(1) else 0] * int(match.group(2) or 1)
    return invariants(orders, "rendered group")


def source_record(archive):
    source = archive / "source"
    hashes = {str(p.relative_to(source)): sha(p.read_bytes())
              for p in sorted((source / "gap").glob("*.g"))}
    require(bool(hashes), "missing frozen source: " + str(archive))
    source_id = sha(json.dumps(hashes, sort_keys=True).encode())
    manifest_bytes = (archive / "archive.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest["source_id"] == source_id, "frozen source ID mismatch")
    for path, digest in hashes.items():
        entry = manifest["files"]["source/" + path]
        require(entry["sha256"] == digest, "source archive digest mismatch: " + path)
    return hashes, source_id, manifest, sha(manifest_bytes)


def load_campaign(root, name, spins, count):
    archive = root / "results" / name
    hashes, source_id, manifest, manifest_sha = source_record(archive)
    point = name == "point_groups"
    expected = {(spin + "_pg" if point else "sg") + str(n) + ".json"
                for spin in spins for n in range(1, count + 1)}
    pattern = r"(?:half|spinless)_pg[0-9]+\.json" if point else r"sg[0-9]+\.json"
    actual = {p.name for p in archive.iterdir() if re.fullmatch(pattern, p.name)}
    require(actual == expected, "incomplete or extra result inventory: " + name)
    rows = []
    input_records = []
    geometries = {}
    for spin in spins:
        convention, physical, internal, background = CONVENTIONS[spin]
        for n in range(1, count + 1):
            filename = (spin + "_pg" if point else "sg") + str(n) + ".json"
            path = archive / filename
            raw = path.read_bytes()
            digest = sha(raw)
            data = json.loads(raw)
            entry = manifest["files"][filename]
            require(entry["sha256"] == digest and entry["bytes"] == len(raw),
                    "result archive digest mismatch: " + filename)
            require(data["source_id"] == source_id and data["source_sha256"] == hashes,
                    "result source mismatch: " + filename)
            require(data["convention"] == convention, "physical convention mismatch: " + filename)
            for status in (data["status"], data["classification_status"],
                           data["pip"]["status"], data["stacking"]["status"]):
                require(status == "computed", "incomplete calculation: " + filename)
            row = dict(index=n, crystalline_spin=physical, internal_spin=internal,
                       effective_background=background, source_id=source_id,
                       result_path=str(path.relative_to(root)), result_sha256=digest,
                       **cells(data))
            require(row["stacking"].count(0) == sum(row[k].count(0) for k in CELL_KEYS[:-1]),
                    "free-rank mismatch: " + filename)
            # Finite point groups have no free factors, so the filtration
            # independently fixes the total finite cardinality.
            if point:
                finite_order = lambda a: product(a)
                require(finite_order(row["stacking"]) == product(
                    [finite_order(row[k]) for k in CELL_KEYS[:-1]]),
                    "filtration cardinality mismatch: " + filename)
                require(data["point_group_index"] == n, "point-group index mismatch")
                check_geometry(data)
                geometry = {k: data["point_group"][k] for k in GEOMETRY_KEYS}
                if n in geometries:
                    require(geometries[n] == geometry, "two spin conventions use different geometry")
                geometries[n] = geometry
                row.update(hermann_mauguin=data["point_group"]["hermannMauguin"],
                           schoenflies=data["point_group"]["schoenflies"],
                           order=data["point_group"]["order"],
                           matrix_set_sha256=data["point_group"]["matrix_set_sha256"])
            else:
                require(data["space_group"] == n and "point_group_index" not in data,
                        "space-group index mismatch: " + filename)
            rows.append(row)
            input_records.append({k: row[k] for k in ("index", "crystalline_spin", "source_id",
                                                       "result_path", "result_sha256")})
    return rows, {"archive_path": str(archive.relative_to(root)),
                  "archive_sha256": manifest_sha, "source_id": source_id,
                  "source_sha256": hashes, "results": input_records}


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def csv_table(rows, point):
    columns = ["index"]
    if point:
        columns += ["hermann_mauguin", "schoenflies", "order"]
    columns += ["crystalline_spin", "internal_spin", "effective_background"]
    columns += list(CELL_KEYS)
    columns += ["source_id", "result_path", "result_sha256"]
    if point:
        columns += ["matrix_set_sha256"]
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: compact(row[k]) if k in CELL_KEYS else row[k] for k in columns})
    return out.getvalue()


def markdown_table(rows, title, point):
    lines = ["# " + title, ""]
    if point:
        lines += ["Finite crystallographic point groups in their three-dimensional matrix representations.",
                  "Both crystalline spin conventions are shown; the internal convention is the opposite spin label.", ""]
        columns = ["Index", "HM", "Schoenflies", "Crystalline spin"] + list(CELL_LABELS)
    else:
        first = rows[0]
        lines += [first["crystalline_spin"] + " = " + first["internal_spin"] + ".",
                  "Full infinite affine space groups, including translations, weak phases and atomic fermion parity.", ""]
        columns = ["SG"] + list(CELL_LABELS)
    lines += ["`Z` denotes an infinite cyclic group, `Zn` a cyclic group of order n,",
              "`^r` a repeated direct sum, and `0` the trivial group.", "",
              "| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = [str(row["index"])]
        if point:
            values += [row["hermann_mauguin"], row["schoenflies"], row["crystalline_spin"].split()[-1]]
        values += ["`" + group_text(row[k]) + "`" for k in CELL_KEYS]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"


def verify_tables(csv_text, md_text, rows, root, point):
    parsed = list(csv.DictReader(io.StringIO(csv_text)))
    md_rows = [line.split("|")[1:-1] for line in md_text.splitlines()
               if re.match(r"\| [0-9]+ \|", line)]
    require(len(parsed) == len(md_rows) == len(rows), "generated row count mismatch")
    checked = 0
    for csv_row, md_row, row in zip(parsed, md_rows, rows):
        raw = (root / row["result_path"]).read_bytes()
        require(sha(raw) == row["result_sha256"], "input changed during report generation")
        original = cells(json.loads(raw))
        require(int(csv_row["index"]) == int(md_row[0]) == row["index"], "rendered identity mismatch")
        require(csv_row["crystalline_spin"] == row["crystalline_spin"], "rendered spin mismatch")
        require(csv_row["result_sha256"] == row["result_sha256"], "rendered digest mismatch")
        if point:
            require([s.strip() for s in md_row[1:4]] ==
                    [row["hermann_mauguin"], row["schoenflies"], row["crystalline_spin"].split()[-1]],
                    "rendered point-group name mismatch")
            require(csv_row["hermann_mauguin"] == row["hermann_mauguin"] and
                    csv_row["schoenflies"] == row["schoenflies"], "CSV point-group name mismatch")
        for key, rendered in zip(CELL_KEYS, md_row[-5:]):
            require(json.loads(csv_row[key]) == parse_group(rendered.strip()) == original[key],
                    "rendered group cell differs from original result: " + row["result_path"] + ":" + key)
            checked += 1
    return checked


def summary_table(point_rows):
    rows_by_spin = {spin: {r["index"]: r for r in point_rows if r["crystalline_spin"] == vals[1]}
                    for spin, vals in CONVENTIONS.items()}
    lines = ["# Full stacking groups for the 32 crystallographic point groups", "",
             "Crystalline spin-1/2 corresponds to internal spinless; crystalline spinless corresponds to internal spin-1/2.",
             "The finite groups use their actual three-dimensional spatial representations.", "",
             "| Index | HM | Schoenflies | Crystalline spin-1/2 | Crystalline spinless |",
             "| --- | --- | --- | --- | --- |"]
    for n in range(1, 33):
        half, spinless = rows_by_spin["half"][n], rows_by_spin["spinless"][n]
        lines.append("| %d | %s | %s | `%s` | `%s` |" %
                     (n, half["hermann_mauguin"], half["schoenflies"],
                      group_text(half["stacking"]), group_text(spinless["stacking"])))
    text = "\n".join(lines) + "\n"
    rendered = [line.split("|")[1:-1] for line in lines if re.match(r"\| [0-9]+ \|", line)]
    require(len(rendered) == 32, "summary row count mismatch")
    for n, row in enumerate(rendered, 1):
        require(parse_group(row[3].strip()) == rows_by_spin["half"][n]["stacking"] and
                parse_group(row[4].strip()) == rows_by_spin["spinless"][n]["stacking"],
                "summary group differs from full point-group table")
    return text


def build(root):
    half, half_proof = load_campaign(root, "space_groups", ["half"], 230)
    spinless, spinless_proof = load_campaign(root, "space_groups_spinless", ["spinless"], 230)
    point, point_proof = load_campaign(root, "point_groups", ["half", "spinless"], 32)
    files = {}
    count = 0
    for stem, rows, title, is_point in [
        ("space_groups_spin_half_230", half, "230 space groups: crystalline spin-1/2", False),
        ("space_groups_spinless_230", spinless, "230 space groups: crystalline spinless", False),
        ("point_groups_64", point, "Point-group classification and stacking in both spin conventions", True),
    ]:
        csv_text = csv_table(rows, is_point)
        md_text = markdown_table(rows, title, is_point)
        count += verify_tables(csv_text, md_text, rows, root, is_point)
        files[stem + ".csv"] = csv_text.encode()
        files[stem + ".md"] = md_text.encode()
    require(count == 2620, "expected 524 rows with five group-valued cells each")
    files["point_groups_full_32.md"] = summary_table(point).encode()
    files["README.md"] = ("# Classification and stacking groups\n\n"
        "Complete tables for 230 space groups and 32 crystallographic point groups in each crystalline spin convention. "
        "The four decoration layers and final abstract stacking group are listed separately.\n\n"
        "| Crystalline convention | Equivalent internal convention | Effective background |\n"
        "| --- | --- | --- |\n"
        "| spin-1/2 | spinless | `s=w1, omega=0` |\n"
        "| spinless | spin-1/2 | `s=w1, omega=w2+w1^2` |\n\n"
        "- Space groups, crystalline spin-1/2: [230-row table](space_groups_spin_half_230.md), [CSV](space_groups_spin_half_230.csv).\n"
        "- Space groups, crystalline spinless: [230-row table](space_groups_spinless_230.md), [CSV](space_groups_spinless_230.csv).\n"
        "- Finite point groups, both conventions: [64-row table](point_groups_64.md), [CSV](point_groups_64.csv).\n"
        "- [32-row point-group summary with both full groups](point_groups_full_32.md).\n\n"
        "The space groups include translations, weak phases and atomic fermion parity. "
        "The point groups are finite matrix groups without translations.\n\n"
        "CSV group cells contain invariant-factor arrays: `[]` is trivial, each `0` contributes `Z`, "
        "and each positive entry n contributes `Zn`. Source IDs and result SHA-256 hashes are included per row. "
        "[manifest.json](manifest.json) records all 524 input digests, frozen sources and generated table hashes. "
        "All 2,620 group-valued cells in each of the CSV and Markdown representations are parsed back and "
        "compared with the original result JSON. The 32-row summary is checked separately.\n").encode()
    manifest = {
        "schema": "fspt-public-group-tables-v1",
        "scope": "Four decoration layers and final abstract stacking group",
        "result_rows": 524,
        "verified_distinct_group_cells": count,
        "verified_csv_cells": count,
        "verified_markdown_cells": count,
        "verified_summary_cells": 64,
        "generator": {"path": "scripts/report_public_groups.py", "sha256": sha(Path(__file__).read_bytes())},
        "campaigns": {"space_groups_spin_half": half_proof, "space_groups_spinless": spinless_proof,
                      "point_groups": point_proof},
        "files": {name: {"sha256": sha(raw), "bytes": len(raw)} for name, raw in sorted(files.items())},
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return files, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, help="Default: ROOT/publication/group_tables")
    parser.add_argument("--check", action="store_true", help="Verify existing output without writing")
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root / "publication" / "group_tables").resolve()
    require(output != root, "output overlaps the source root")
    for name in ("space_groups", "space_groups_spinless", "point_groups"):
        archive = root / "results" / name
        require(output != archive and archive not in output.parents,
                "output overlaps an input archive")
    files, manifest = build(root)
    if args.check:
        require(output.is_dir(), "output directory does not exist")
        require({p.name for p in output.iterdir()} == set(files), "output inventory mismatch")
        for name, raw in files.items():
            require((output / name).read_bytes() == raw, "generated output differs: " + name)
    else:
        if output.exists():
            require(not any(output.iterdir()), "output is not empty; use --check or a new directory")
        output.mkdir(parents=True, exist_ok=True)
        for name, raw in files.items():
            (output / name).write_bytes(raw)
    print(json.dumps({"output": str(output), "rows": manifest["result_rows"],
                      "group_cells": manifest["verified_distinct_group_cells"],
                      "summary_cells": manifest["verified_summary_cells"],
                      "files": len(files), "check": args.check}, sort_keys=True))


if __name__ == "__main__":
    main()
