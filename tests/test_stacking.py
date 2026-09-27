import unittest

from fspt.stacking import (
    Generator, InvalidCertificate, Reduction, UnresolvedStacking,
    invariant_factors, measure_stacking, relation_row, PresentedStackingGroup,
)


class CyclicBackend:
    """Exact independent Z/16 oracle retaining integer representatives."""
    def __init__(self, bad_witness=False):
        self.calls = 0
        self.bad_witness = bad_witness

    def zero(self): return 0
    def product(self, x, y):
        self.calls += 1
        return x + y
    def inverse(self, x): return -x
    def verify_flat(self, x): return type(x) is int
    def reduce(self, x, lower):
        # Power relations: 2*8=0, 2*4=8, 2*2=4, 2*1=2.
        coordinates = tuple(int(g.lift == x) for g in lower)
        canonical = sum(c * g.lift for c, g in zip(coordinates, lower))
        return Reduction(coordinates, (x - canonical) // 16 + self.bad_witness)
    def verify_relation(self, x, y, witness): return x - y == 16 * witness


class StackingTests(unittest.TestCase):
    def test_measured_four_layer_extension(self):
        backend = CyclicBackend()
        generators = [Generator(n, i, 2, x) for i, (n, x) in
                      enumerate(zip("DCBA", (8, 4, 2, 1)))]
        result = measure_stacking(generators, backend,
                                  filtration_certificate="four Z2 quotients",
                                  abelian_group_law_certificate="integer addition modulo 16")
        self.assertEqual(result["invariants"], [16])
        self.assertEqual(result["presentation"],
                         [[2, 0, 0, 0], [-1, 2, 0, 0], [0, -1, 2, 0], [0, 0, -1, 2]])
        self.assertLess(backend.calls, 30)  # No 16-by-16 phase table.

    def test_correlated_lower_images(self):
        same = [[2, 0, 0, 0], [0, 2, 0, 0], [-1, 0, 2, 0], [-1, 0, 0, 2]]
        independent = [[2, 0, 0, 0], [0, 2, 0, 0], [-1, 0, 2, 0], [0, -1, 0, 2]]
        self.assertEqual(invariant_factors(same, 4), [2, 2, 4])
        self.assertEqual(invariant_factors(independent, 4), [4, 4])

    def test_integer_carries_and_free_rank(self):
        rows = [[2, 0, 0, 0, 0], [-1, 2, 0, 0, 0], [-7, -1, 2, 0, 0],
                [17, -1, -1, 2, 0]]
        self.assertEqual(invariant_factors(rows, 5), [0, 16])
        self.assertEqual(invariant_factors([], 2), [0, 0])
        self.assertEqual(invariant_factors([], 0), [])

    def test_false_relation_is_rejected(self):
        with self.assertRaises(InvalidCertificate):
            measure_stacking([Generator("D", 0, 2, 8)], CyclicBackend(True),
                             filtration_certificate=True, abelian_group_law_certificate=True)

    def test_unknown_lift_or_law_does_not_split(self):
        with self.assertRaises(UnresolvedStacking):
            measure_stacking([Generator("A", 3, 2, None)], CyclicBackend(),
                             filtration_certificate=True, abelian_group_law_certificate=True)
        with self.assertRaises(UnresolvedStacking):
            measure_stacking([], CyclicBackend(), filtration_certificate=True,
                             abelian_group_law_certificate=None)

    def test_relation_cannot_use_same_or_higher_layer(self):
        generators = [Generator("D", 0, 2, 8), Generator("C", 1, 2, 4)]
        with self.assertRaises(InvalidCertificate):
            relation_row(generators, 1, ["C"], [1])


    def test_saved_joint_presentation_replays_all_four_layer_carries(self):
        result={"status":"computed","invariants":[0,16],"freePipRank":1,
            "fullUpperPhaseWitness":True,"pipGenerator":{"name":"P1"},
            "lower":{"generators":[{"name":n} for n in ("D1","C1","B1")]},
            "fullPresentation":[[2,0,0,0],[-1,2,0,0],[0,-1,2,0],[0,0,-1,2]],
            "fullSmithDiagonal":[1,1,1,16],
            "fullSmithColumnTransform":[[1,0,0,8],[0,1,0,4],[0,0,1,2],[0,0,0,1]]}
        group=PresentedStackingGroup(result)
        self.assertEqual(group.stack({"P1":1},{"P1":1}),group.canonical({"B1":1}))
        self.assertEqual(group.stack({"B1":1},{"B1":1}),group.canonical({"C1":1}))
        self.assertEqual(group.stack({"C1":1},{"C1":1}),group.canonical({"D1":1}))
        self.assertEqual(group.canonical({"P1":-1}), (0,15))
        self.assertEqual(group.order({"P1":1}),16)
        self.assertEqual(group.stack_marked({"P1":1},{"P1":1}),{"B1":1})
        self.assertEqual(group.stack_marked({"P1":-1},{"Pfree1":-3}),
                         {"Pfree1":-3,"D1":1,"C1":1,"B1":1,"P1":1})
        self.assertIsNone(group.order({"Pfree1":1}))
        self.assertEqual(group.stack({"Pfree1":7},{"Pfree1":-10,"P1":17}),(-3,1))
        with self.assertRaises(KeyError):group.canonical({"A1":1})
        with self.assertRaises(TypeError):group.canonical({"P1":0.5})

    def test_abstract_upper_is_not_a_marked_relation(self):
        with self.assertRaises(UnresolvedStacking):
            PresentedStackingGroup({"status":"computed","invariants":[4],
                "lower":{"generators":[]},"pipExtensionCertificate":{}})

    def test_primitive_free_lattice_scope_and_coordinates(self):
        stacking={"status":"computed","invariants":[0,2],"freePipRank":1,
            "lower":{"generators":[{"name":"D1"}],"presentation":[[2]],
                "smithDiagonal":[2],"smithColumnTransform":[[1]]}}
        old=PresentedStackingGroup(stacking)
        self.assertEqual(old.free_generator_scope,"abstract-free-splitting")
        lattice={"status":"computed","rank":1,"fullFreePhaseWitness":True,
            "latticeBasis":[[2]],"latticeIndex":2,"h1BasisOrders":[2,0],
            "generators":[{"name":"Pfree1","h1Coordinates":[1,2]}]}
        result={"stacking":stacking,"pip":{"free_lattice":lattice}}
        group=PresentedStackingGroup(result)
        self.assertEqual(group.free_generator_scope,"explicit-primitive-free-lifts")
        self.assertEqual(group.free_h1_coordinates,((1,2),))
        self.assertEqual(group.stack_marked({"Pfree1":2},{"Pfree1":-1,"D1":3}),
                         {"Pfree1":1,"D1":1})
        lattice["rank"]=2
        with self.assertRaises(InvalidCertificate):PresentedStackingGroup(result)


if __name__ == "__main__":
    unittest.main()
