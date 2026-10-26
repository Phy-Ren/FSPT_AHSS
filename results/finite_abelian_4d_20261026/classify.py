#!/usr/bin/env python3
"""Compute the 4+1D stacking group for C_(2m)^f times cyclic spectators."""
import argparse,json
from collections import Counter
from math import prod
try:
    from .nonsplit_closed_formula import nonsplit_closed_formula
    from .nonsplit_layers import nonsplit_layers
except ImportError:
    from nonsplit_closed_formula import nonsplit_closed_formula
    from nonsplit_layers import nonsplit_layers

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fermionic-order',type=int,default=2,
                        help='Order 2m of the distinguished fermionic cyclic factor (default: 2, the split case).')
    parser.add_argument('--spectators',type=int,nargs='*',default=[],help='Orders of the remaining cyclic factors.')
    args=parser.parse_args()
    if args.fermionic_order<2 or args.fermionic_order%2:
        parser.error('--fermionic-order must be a positive even integer')
    if any(n<1 for n in args.spectators):
        parser.error('spectator orders must be positive integers')
    factors=nonsplit_closed_formula(args.fermionic_order//2,args.spectators)
    notation=' x '.join(f'C_{n}'+(f'^{k}' if k>1 else '') for n,k in Counter(factors).items()) or '0'
    print(json.dumps({'fermionic_order':args.fermionic_order,'spectator_orders':args.spectators,
                      'invariant_factors':factors,'stacking_group':notation,'group_order':prod(factors),
                      'final_decoration_layers':nonsplit_layers(args.fermionic_order//2,args.spectators),
                      'scope':'Full mathematical classification; the general result does not assert a physical construction of the terminal p+ip Berry phase.'},indent=2))

if __name__=='__main__':
    main()
