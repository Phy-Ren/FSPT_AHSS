"""Comparison-only PDF notation tests; no classification runtime dependency."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from compare_boss import parse_group


def glyph(text, x, y, size=9):
    return dict(text=text, x=x, y=y, font_size=size)


class BossNotationTests(unittest.TestCase):
    def test_subscript_and_large_superscript(self):
        self.assertEqual(parse_group([glyph('Z', 0, 10), glyph('2', 6, 12, 6),
                                      glyph('24', 6, 6, 6)]), [2]*24)
        self.assertEqual(parse_group([glyph('Z', 0, 10), glyph('4', 6, 12, 6)]), [4])

    def test_free_rank_and_direct_sum(self):
        self.assertEqual(parse_group([glyph('Z', 0, 10), glyph('3', 6, 6, 6)]), [0]*3)
        self.assertEqual(parse_group([glyph('Z', 0, 10), glyph('⊕', 9, 10),
                                      glyph('Z', 20, 10), glyph('2', 26, 12, 6)]), [0, 2])

    def test_missing_and_trivial_are_distinct(self):
        self.assertEqual(parse_group([glyph('0', 0, 10)]), [])
        self.assertIsNone(parse_group([glyph('–', 0, 10)]))

    def test_unresolved_glyph_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_group([glyph('Z', 0, 10), glyph('2', 6, 10)])
        with self.assertRaises(ValueError):
            parse_group([glyph('Z', 0, 10), glyph('?', 6, 6, 6)])


if __name__ == '__main__':
    unittest.main(verbosity=2)
