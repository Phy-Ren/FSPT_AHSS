"""Exact U(1)^f CI, localized-charge and phase-sector AHSS formulas.

Only the calibrated sheet-linear convention is exposed. E8State adds the
reviewed neutral closed-sheet operations. Intrinsic higher-response sectors
are outside these local state classes.
"""
from .api import (
    Cochain, Symmetry, State, char, bin0, halves, word,
    integer_obstruction, charge_source, source, integer_product, charge_product, charge_gauge,
    product, gauge, background_change, lower_exchange, associator_3p1,
    integral_cartan, cubic_polarizer, d2, d3, d4,
    obstruction_2p1, obstruction_3p1, obstruction_4p1,
    stacking_2p1, stacking_3p1, stacking_4p1,
)
from .e8 import State as E8State

CONVENTION = {'calibration': 'sheet-linear', 'cubic': '1/6', 'epsilon': 0}
SCOPE = 'CI-generated, localized-charge and group-cohomological phase sector'

__all__ = [name for name in globals() if not name.startswith('_')]
