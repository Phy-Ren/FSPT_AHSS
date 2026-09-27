"""Optional exact scalar-DAG specialization for the full-background p+ip O5.

No production dispatch is changed. Known low bits and interval bounds are
propagated through integer arithmetic; all division guards left in the graph
remain exact. In even mode the original integer n callback is retained.
"""
from dataclasses import dataclass
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path

from .formulas_pip_compile import Builder

ROOT = Path(__file__).resolve().parents[1]
PRECISION = 32


def v2(value, zero=PRECISION):
    if value == 0:
        return zero
    return (abs(value) & -abs(value)).bit_length()-1


def power2(value):
    return value > 0 and value & (value-1) == 0


@dataclass(frozen=True)
class Fact:
    bits: int = 0
    residue: int = 0
    low: object = None
    high: object = None

    def bounded(self):
        return self.low is not None and self.high is not None


class KnownIntegerBuilder(Builder):
    def __init__(self, mode):
        super().__init__()
        if mode not in ("even", "sign"):
            raise ValueError("specialization must be even or sign")
        self.mode = mode

    @lru_cache(None)
    def fact(self, index):
        op, *args = self.nodes[index]
        if op == "const":
            x = args[0]
            return Fact(PRECISION, x % (1 << PRECISION), x, x)
        if op == "field":
            if args[0] == "s":
                return Fact(0, 0, 0, 1)
            if args[0] == "n" and self.mode == "even":
                return Fact(1, 0)
            return Fact()
        a = self.fact(args[0])
        if op in ("add", "mul"):
            b = self.fact(args[1])
            if op == "add":
                bits = min(a.bits, b.bits)
                residue = (a.residue+b.residue) % (1 << bits)
                low, high = ((a.low+b.low, a.high+b.high)
                             if a.bounded() and b.bounded() else (None, None))
            else:
                bits = min(PRECISION, a.bits+v2(b.residue, b.bits),
                           b.bits+v2(a.residue, a.bits), a.bits+b.bits)
                residue = a.residue*b.residue % (1 << bits)
                if a.bounded() and b.bounded():
                    products = [x*y for x in (a.low, a.high) for y in (b.low, b.high)]
                    low, high = min(products), max(products)
                else:
                    low, high = None, None
            return Fact(bits, residue, low, high)
        k = args[1]
        if op == "mod":
            bits = min(a.bits, v2(k)) if power2(k) else 0
            return Fact(bits, a.residue % (1 << bits), 0, k-1)
        if op == "bit":
            return Fact(0, 0, 0, 1)
        if op in ("floor", "div"):
            shift = v2(k) if power2(k) else PRECISION
            bits = max(0, a.bits-shift)
            residue = (a.residue // k) % (1 << bits)
            low, high = ((a.low//k, a.high//k) if a.bounded() else (None, None))
            return Fact(bits, residue, low, high)
        raise ValueError(op)

    def field(self, name, face):
        if self.mode == "sign" and name == "n":
            name = "s"
        return self.make("field", name, tuple(face))

    def binary(self, op, a, b):
        a, b = self.scalar(a), self.scalar(b)
        # These cancellations are integral identities, independent of closure.
        if op == "add":
            for x, y in ((a, b), (b, a)):
                node = self.nodes[y.index]
                if node[0] == "mul":
                    factors = [self.objects[i] for i in node[1:]]
                    if any(z.index == x.index for z in factors) and any(self.constant(z) == -1 for z in factors):
                        return self.scalar(0)
        elif op == "mul" and a.index == b.index:
            f = self.fact(a.index)
            if f.bounded() and 0 <= f.low <= f.high <= 1:
                return a
        return super().binary(op, a, b)

    def modulo(self, a, modulus):
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError("positive integer modulus required")
        a = self.scalar(a)
        f = self.fact(a.index)
        if power2(modulus) and f.bits >= v2(modulus):
            return self.scalar(f.residue % modulus)
        if f.bounded() and 0 <= f.low <= f.high < modulus:
            return a
        return super().modulo(a, modulus)

    def bit(self, a, position):
        a = self.scalar(a)
        f = self.fact(a.index)
        if f.bits > position:
            return self.scalar((f.residue >> position) & 1)
        if position == 0:
            return self.modulo(a, 2)
        if f.bounded():
            if 0 <= f.low <= f.high < 2**position:
                return self.scalar(0)
            if -1 <= f.low <= f.high <= 0:
                return -a
        return super().bit(a, position)

    def floor(self, a, divisor):
        a = self.scalar(a)
        f = self.fact(a.index)
        if f.bounded() and f.low//divisor == f.high//divisor:
            return self.scalar(f.low//divisor)
        return super().floor(a, divisor)


def specialize(program, mode):
    """Return an exact program on the stated n-domain, with no runtime edits."""
    if program.get("omega_zero") is not False or program["denominator"] != 16:
        raise ValueError("expected the existing complete nonzero-background O5 graph")
    builder, values = KnownIntegerBuilder(mode), []
    for node in program["program"]:
        op, *args = node
        if op == "const":
            value = builder.scalar(args[0])
        elif op == "field":
            value = builder.field(*args)
        elif op in ("add", "mul"):
            value = builder.binary(op, values[args[0]], values[args[1]])
        elif op == "mod":
            value = builder.modulo(values[args[0]], args[1])
        elif op == "bit":
            value = builder.bit(values[args[0]], args[1])
        elif op == "floor":
            value = builder.floor(values[args[0]], args[1])
        elif op == "div":
            value = builder.divide(values[args[0]], args[1])
        else:
            raise ValueError(op)
        values.append(value)
    active, pending = set(), [values[program["output"]].index]
    while pending:
        index = pending.pop()
        if index in active:
            continue
        active.add(index)
        node = builder.nodes[index]
        if node[0] in ("add", "mul"):
            pending.extend(node[1:])
        elif node[0] in ("mod", "bit", "floor", "div"):
            pending.append(node[1])
    mapping = {old: new for new, old in enumerate(sorted(active))}
    nodes = []
    for index in sorted(active):
        node = list(builder.nodes[index])
        if node[0] in ("add", "mul"):
            node[1:3] = [mapping[x] for x in node[1:3]]
        elif node[0] in ("mod", "bit", "floor", "div"):
            node[1] = mapping[node[1]]
        nodes.append(node)
    return dict(program, program=nodes, output=mapping[values[program["output"]].index],
        specialization=dict(mode=mode, precondition="all n edges even; original integer n retained" if mode == "even" else "n equals normalized binary s pointwise",
                            binary_sign=True, method="integer low-bit congruences and interval bounds; no cohomology assumptions"))


def compile_gap(program, digest):
    """Independent names; check every actually evaluated even-n field."""
    from scripts.compile_pip_o5_straight import compile_gap as original_emitter
    mode = program["specialization"]["mode"]
    prefix = "AFSPipO5Background" + ("Even" if mode == "even" else "Sign")
    code = original_emitter(program, digest).replace("AFSPipO5General", prefix)
    code = code.replace("Generated by scripts/compile_pip_o5_straight.py", "Generated by fspt/formulas_background_specialize.py")
    if mode == "even":
        lines = []
        for line in code.splitlines():
            lines.append(line)
            if ":=f.n(" in line:
                variable = line.split(":=", 1)[0]
                lines.append(f'if {variable} mod 2<>0 then Error("Even p+ip specialization received odd n");fi;')
        code = "\n".join(lines)+"\n"
    return "# PRECONDITION: "+program["specialization"]["precondition"]+".\n"+code


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=ROOT/"gap/pip_o5_background.json")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise ValueError("preserve existing experimental output")
    raw = args.input.read_bytes()
    program = json.loads(raw)
    args.output.mkdir(parents=True)
    summary = {}
    for mode in ("even", "sign"):
        result = specialize(program, mode)
        result["source_program_sha256"] = hashlib.sha256(raw).hexdigest()
        path = args.output/f"pip_o5_background_{mode}.json"
        encoded = (json.dumps(result, separators=(",", ":"))+"\n").encode()
        path.write_bytes(encoded)
        (args.output/f"pip_o5_background_{mode}.g").write_text(compile_gap(result, hashlib.sha256(encoded).hexdigest()))
        summary[mode] = dict(nodes=len(result["program"]), original_nodes=len(program["program"]),
                             node_ratio=len(program["program"])/len(result["program"]))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
