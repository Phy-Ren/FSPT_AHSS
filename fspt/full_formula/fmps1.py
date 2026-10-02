"""Independent 1+1D fMPS coordinate of Turzillo--You, arXiv:1710.00140.

Fields are gamma=a (degree zero), beta=c (degree one), alpha=v (degree two).
There is no integer layer. The source is d_s alpha=beta cup omega/2.
For a nonsplit extension only gamma=0 is admitted. Nonzero exact omega must
be trivialized explicitly before using the split odd sector; this evaluator
does not silently drop that sector or infer a trivialization locally.

The residual parity gauge alpha~alpha+omega/2 is part of the equivalence,
not an optional correction to this product. The CF degree-zero gauge cylinder
realizes it from the same source. No manuscript-nu dictionary is asserted.
"""
from fractions import Fraction


class FMPS1Backend:
    coordinate='fmps1-turzillo-you-eq44'

    @staticmethod
    def check_integer(fields):
        if any(fields.get('n',())):
            raise ValueError('The d1 fMPS endpoint has no integer decoration')

    @staticmethod
    def gamma(fields):
        values=fields['a']
        gamma=[values[1<<j] for j in range(len(values).bit_length()-1)]
        if not gamma or any(x not in (0,1) for x in gamma):
            raise ValueError('fMPS gamma must be binary')
        if len(set(gamma))!=1:
            raise ValueError('fMPS gamma must be a closed degree-zero field')
        return gamma[0]

    def source(self,dimension,stage,fields):
        if dimension!=1:raise ValueError('fMPS endpoint requires dimension=1')
        self.check_integer(fields)
        if stage=='majorana':return 0
        gamma=self.gamma(fields)
        if stage=='fermion':return gamma*fields['w'][7]
        if stage!='bosonic':raise ValueError('Unknown source stage')
        if gamma and any(fields['w']):
            raise NotImplementedError('Odd fMPS requires pointwise omega=0; explicitly trivialize a nonzero exact extension first')
        return Fraction(fields['c'][3]*fields['w'][14],2)

    def product(self,dimension,stage,left,right,background):
        if dimension!=1:raise ValueError('fMPS endpoint requires dimension=1')
        self.check_integer(left);self.check_integer(right)
        if stage=='majorana':return 0
        a,b=self.gamma(left),self.gamma(right)
        if (a or b) and any(background['w']):
            raise NotImplementedError('Odd fMPS requires pointwise omega=0; explicitly trivialize a nonzero exact extension first')
        if stage=='fermion':return a*b*background['s'][3]
        if stage!='bosonic':raise ValueError('Unknown product stage')
        value=left['c'][3]*right['c'][6]
        if a!=b:
            even=left if a==0 else right
            value+=even['c'][3]*even['c'][6]
        return Fraction(value%2,2)
