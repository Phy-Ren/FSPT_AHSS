"""Reject local signed sections that are not physical uniform responses."""
from fractions import Fraction
import unittest

from insulator import api as ci
from insulator import e8


class UniformResponseDomain(unittest.TestCase):
    @staticmethod
    def background(sign):
        n = len(sign) - 1
        return ci.Symmetry(ci.Cochain(n, 2, {}, sign),
                           ci.char(n, sign).ret(sign),
                           ci.char(n, (0,) * (n + 1)))

    @staticmethod
    def response(sign, multiplicity=1):
        return ci.Cochain(len(sign) - 1, 0,
                          {(i,): multiplicity * (-1) ** (sign[0] ^ s)
                           for i, s in enumerate(sign)}, sign)

    def test_parallel_signed_ci_section_is_not_a_uniform_response(self):
        sign = (0, 1, 0, 1, 1)
        bg = self.background(sign)
        sheet = self.response(sign)
        zero = ci.Cochain(4, 0, {}, sign)
        charge = ci.Cochain(4, 2, {})
        parameter = ci.Cochain(4, 1, {})
        # This is exactly the formerly accepted case: local covariant closure
        # alone does not impose invariance of a uniform group-cochain value.
        self.assertEqual(sheet.d().maxabs(), 0)
        with self.assertRaisesRegex(ValueError, 'uniform CI'):
            ci.State(sheet, charge, ci.Cochain(4, 3, {}, sign)).validate(bg, 2)
        with self.assertRaisesRegex(ValueError, 'uniform CI'):
            ci.integer_obstruction(bg, 2, sheet)
        for validate in (True, False):
            operations = (
                lambda: ci.source(bg, 2, sheet, charge, validate=validate),
                lambda: ci.product(bg, 2, sheet, charge, zero, charge, validate=validate),
                lambda: ci.product(bg, 2, zero, charge, sheet, charge, validate=validate),
                lambda: ci.gauge(bg, 2, sheet, charge, None, parameter, validate=validate),
                lambda: ci.background_change(bg, 2, sheet, charge,
                                              ci.Cochain(4, 2, {}, sign), 'lift', validate=validate),
            )
            for operation in operations:
                with self.subTest(validate=validate, operation=operation):
                    with self.assertRaisesRegex(ValueError, 'uniform CI'):
                        operation()

    def test_parallel_signed_e8_section_is_rejected(self):
        sign = (0, 1, 1, 0, 1)
        bg = self.background(sign)
        neutral = self.response(sign, -2)
        self.assertEqual(neutral.d().maxabs(), 0)
        with self.assertRaisesRegex(ValueError, 'uniform E8'):
            e8.source(bg, 2, neutral, ci.Cochain(4, 0, {}, sign), ci.Cochain(4, 2, {}))

    def test_physical_uniform_domains_remain_valid(self):
        for sign, multiplicity in (((0,) * 5, 3), ((1,) * 5, -2),
                                    ((0, 1, 0, 1, 0), 0)):
            with self.subTest(sign=sign, multiplicity=multiplicity):
                bg = self.background(sign)
                response = self.response(sign, multiplicity)
                state = e8.State(response, response, ci.Cochain(4, 2, {}),
                                 ci.Cochain(4, 3, {}, sign))
                state.validate(bg, 2)
                state.stack(state, bg, 2).validate(bg, 2)
                state.gauge(bg, 2, None, None, ci.Cochain(4, 1, {})).validate(bg, 2)

    def test_validate_false_keeps_uniform_type_constraints(self):
        bg = self.background((0,) * 5)
        half_sheet = self.response((0,) * 5, Fraction(1, 2))
        with self.assertRaisesRegex(ValueError, 'noninteger'):
            ci.source(bg, 2, half_sheet, ci.Cochain(4, 2, {}), validate=False)


if __name__ == '__main__':
    unittest.main()
