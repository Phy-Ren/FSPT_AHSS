"""Integral line-action detectors for 4+1D Spin-c intrinsic responses.

This checks indices on actual closed Spin-c product manifolds. It is not a
standalone proof of the universal transgression or of its signed extension.
"""

from fractions import Fraction
import json
from pathlib import Path


def intrinsic(c_cube, c_p1):
    return (Fraction(c_cube - c_p1, 48), Fraction(c_cube, 2))


def layer(c_square, p1):
    # E8 first, in the gravitational chirality convention of the proof.
    return (-Fraction(p1, 3), Fraction(c_square, 8) - Fraction(p1, 24))


def line_action(e8, iqh):
    # Values of the two intrinsic responses after slanting by the line sphere.
    return (iqh, 24 * iqh - 3 * e8)


def main():
    records = []
    # CP2 has p1=3h^2 and w2=h. Every odd k gives a legitimate determinant kh.
    # On S2 x CP2, tensoring the Spin-c structure by O(t) on S2 changes
    # determinant c=kh into kh+2tu. Thus c^3=6tk^2 and c*p1=6t.
    for k in (-5, -3, -1, 1, 3, 5):
        e8, iqh = layer(k * k, 3)
        assert e8.denominator == iqh.denominator == 1
        for t in (-3, -1, 0, 1, 2):
            actual = intrinsic(6 * t * k * k, 6 * t)
            expected = tuple(t * z for z in line_action(e8, iqh))
            assert actual == expected
            assert all(z.denominator == 1 for z in actual)
            records.append({
                "manifold": "S2 x CP2",
                "determinant": f"{k}h+{2*t}u",
                "line_degree": t,
                "I_J": [int(z) for z in actual],
            })

    # Independent spin base S2 x S2: c=2ax+2by, p1=0, c^2=8ab.
    # With the third S2 line degree t, c^3=48tab, c*p1=0.
    for a, b, t in ((1, 1, 1), (1, -2, 3), (0, 2, 1), (-2, -3, -1)):
        e8, iqh = layer(8 * a * b, 0)
        actual = intrinsic(48 * t * a * b, 0)
        assert actual == tuple(t * z for z in line_action(e8, iqh))
        records.append({
            "manifold": "S2 x S2 x S2",
            "determinant_coefficients": [2*t, 2*a, 2*b],
            "I_J": [int(z) for z in actual],
        })

    # Primitive detectors: CP2 determinants h and 3h have layer coordinates
    # (-1,0),(-1,1). Their determinant is -1, so they detect the full lattice.
    detectors = (layer(1, 3), layer(9, 3))
    determinant = detectors[0][0] * detectors[1][1] - detectors[0][1] * detectors[1][0]
    assert determinant == -1
    assert intrinsic(6, 6) == (0, 3)
    assert intrinsic(54, 6) == (1, 27)

    result = {
        "status": "PASS",
        "checks": len(records),
        "primitive_layer_detector_determinant": int(determinant),
        "line_action_columns_E8_IQH": [[0, 1], [-3, 24]],
        "d3_columns_with_dc_minus_2B": [[0, -1], [3, -24]],
        "scope": "Integral geometric line-action calculation. The universal gerbe transgression proof is separate; no signed or higher differential is asserted by this script.",
        "evaluations": records,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "evaluations"}, indent=2))


if __name__ == "__main__":
    main()
