# Polarization of the binary Majorana stacking carry

For arbitrary binary degree-three cochains, the cochain cup identity gives

{{equation:general-mixed-quarter-polarization--polarization-of-the-binary-majorana-stacking-carry--1}}

Neither input is assumed closed. To verify the formula, expand the two
differentials with the higher-cup Leibniz identity. The terms
$`dx\cup_2y`$ occur twice and cancel, while
$`d(dx\cup_3y)=dx\cup_3dy+dx\cup_2y+y\cup_2dx`$.

In the general 4+1D mixed quarter numerator, use this equality for the
three pairs
$`(x,y)=(\bar\lambda_3^\gamma,\bar\lambda_3^{\gamma\psi})`$,
$`(\bar\lambda_3^\gamma,\bar\lambda_3^\psi)`$, and
$`(\bar\lambda_3^{\gamma\psi},\bar\lambda_3^\psi)`$.
Its last twelve terms become the following nine:

{{equation:general-mixed-quarter-polarization--polarization-of-the-binary-majorana-stacking-carry--2}}

This finite sum has **nine explicitly specified cup terms**. The complete
mixed binary numerator therefore has **39 terms instead of 42**, with the
same lower carries retained. Its whole canonical lift is unchanged.
The differentials in the displayed identity have not been dropped; this
is pointwise equality, not an output-gauge replacement. The bosonic
obstruction, stacking representative, and physical contribution labels
are unchanged.

The [coefficient check](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/LOWER_AND_GENERAL_POLARIZATION_CHECK.json)
uses all thirty independent input-face bits on the five-simplex.
