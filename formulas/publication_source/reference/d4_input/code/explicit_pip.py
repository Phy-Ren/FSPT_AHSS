"""Term-by-term p+ip d4 candidates, in the manuscript's physical coordinates.

All phases are exact integer numerators over 16. The two dimensions retain
independent coefficient tables. The accompanying note proves two-degree cohomological suspension by a
separate universal comparison. Physical d4 normalization is not inferred
from cochain closure or from that comparison.
"""
from pathlib import Path
import json
from functools import lru_cache
from cochains import C,cup,sq,ds,op,background_data,cartan_carry,pure_parity,prism_transgression,mc_phase4
from compact import beta_open,integer_inputs,kappa,ell

@lru_cache(None)
def cartan_words(p):
    return json.loads(Path(__file__).with_name(f'cartan_short_{p}.json').read_text())

def cartan_word(n,omega2,s1):
    """The new single-word ordered Cartan primitive, plus THREE carry terms."""
    p=n.deg;a=n.reduce(2);h=(n-a.lift()).div(2).reduce(2)
    W,v,alpha,hv,P=background_data(omega2,s1)
    z=op(cartan_words(p)['words'][0],alpha,alpha,a,a)
    return z+cup(hv,sq(a,1))+cup(cup(s1,alpha),h)+cup(cup(s1,cup(alpha,s1,1)),a)

def cartan_rephasing(n,omega2,s1):
    """Binary H, with old C + new C = dH pointwise."""
    a=n.reduce(2);_,_,v,_,_=background_data(omega2,s1)
    out=C(n.deg+3)
    for word in cartan_words(n.deg)['homotopy_words']:out=out+op(word,v,v,a,a)
    return out

def cartan_table_shift(n,omega2,s1):
    """Integer carry eta=(lift Cnew-lift Cold-d_s lift H)/2, reduced mod 2."""
    H=cartan_rephasing(n,omega2,s1)
    return (cartan_word(n,omega2,s1).lift()-cartan_carry(n,omega2,s1).lift()-ds(H.lift(),s1)).div(2).reduce(2)

def pure_terms16(n,omega2,s1,*,binary_y=None):
    """Every explicit p+ip-only term, with numerical coefficients restored.

    Set binary_y=C(p+4) to evaluate the seed. Values are NOT separately
    obstruction classes, and summing them must precede a closure test.
    """
    p=n.deg
    if p not in (1,2) or n.mod is not None:raise ValueError('Expected an INTEGER n1 or n2')
    if binary_y is None:binary_y=binary_completion(n,omega2,s1)
    A,K,betaA,_=integer_inputs(n,omega2,s1)
    W,v,_,_,P=background_data(omega2,s1)
    vN=cup(v,n,s=s1,twists=(1,1))
    KN=cup(n,n,p-2,s=s1,twists=(1,1))
    return {
      'y':binary_y.lift().scaled(8),
      'omega2_K':cup(omega2.lift(),K).scaled(4),
      'K_cup_p_K':cup(K,K,p).scaled(4),
      'signed_beta_source_K':cup(betaA,K,p+1).scaled(4*((-1)**p)),
      'minus_K_twisted_Bockstein_source':cup(K,vN,p+1).scaled(-4),
      'minus_Cartan_carry':cartan_word(n,omega2,s1).lift().scaled(-4),
      'background_Pontryagin_n':cup(P,n,s=s1,twists=(0,1)),
      'intrinsic_integer_square':cup(W.lift(),KN,s=s1,twists=(1,0)).scaled(2),
    }

def sum_terms(terms,degree):
    return sum_cochains(terms.values(),degree)

def sum_cochains(cochains,degree):
    out=C(degree,mod=None)
    for term in cochains:out=out+term
    return out

def seed16(n,omega2,s1):
    return sum_terms(pure_terms16(n,omega2,s1,binary_y=C(n.deg+4)),n.deg+4)

def residual(n,omega2,s1):
    """Explicit binary coboundary left by the pure seed; no Y is evaluated."""
    p=n.deg;A,_,_,_=integer_inputs(n,omega2,s1)
    Xi=pure_parity(n,omega2,s1);F=kappa(A,omega2,s1)
    theta=cup(omega2.lift(),A.lift()).scaled(4)+cup(A,ell(omega2,s1),1).lift().scaled(8)
    base=cup(Xi,Xi,p+1)+cup(F,Xi,p+2)+cup(omega2,Xi)
    numerator=ds(seed16(n,omega2,s1)+theta,s1)+base.lift().scaled(8)+mc_phase4(A,C(p+3),omega2,s1).scaled(4)
    return numerator.div(8).reduce(2)

def gamma_terms16(nmajorana,omega2,s1):
    """Fixed lift-coordinate continuation of the Majorana phase.

    Its input may be nonclosed. beta_open, not the cocycle Bockstein, is used.
    This operation is not the known closed-input formula evaluated illegally.
    """
    q=nmajorana.deg;p=q-1;b=beta_open(nmajorana)
    return {
      'Majorana_word_transgression':prism_transgression(nmajorana,omega2,s1).lift().scaled(8),
      'Majorana_background_order':cup(nmajorana,ell(omega2,s1)).lift().scaled(8),
      'Majorana_open_Bockstein_square':cup(b,b,p).scaled(4),
      'Majorana_open_Bockstein_derivative':cup(b,b.d(),p+1).scaled(4),
      'Majorana_open_Bockstein_extension':cup(omega2.lift(),b).scaled(4),
    }

def full_terms16(n,nmajorana,nfermion,omega2,s1,*,binary_y=None):
    p=n.deg
    if (p,nmajorana.deg,nfermion.deg) not in ((1,2,3),(2,3,4)):
        raise ValueError('Expected the physical degrees (1,2,3) or (2,3,4)')
    h=(n-n.reduce(2).lift()).div(2).reduce(2);u=nmajorana+cup(s1,h)
    terms={
      'complex_fermion_square':sq(nfermion,2).lift().scaled(8),
      'complex_fermion_extension':cup(omega2,nfermion).lift().scaled(8),
      **gamma_terms16(u,omega2,s1),
      'p_ip_Majorana_mixed':cup(kappa(u,omega2,s1),pure_parity(n,omega2,s1),p+2).lift().scaled(8),
      **pure_terms16(n,omega2,s1,binary_y=binary_y),
    }
    return terms

def binary_completion(n,omega2,s1,*,vertices=None,accelerate=False):
    """Fixed H^*R_new + AW^*y_new, with independently derived low/high tables."""
    from ez_homotopy import ez_homotopy
    from polynomial_tables import total_cochain
    p=n.deg;r=p+4;H=ez_homotopy(r)
    aw=total_cochain(n,omega2,s1,f'Y{r}_word_total.json',r)
    def sign(a,b):return (-1)**(s1(tuple(sorted((a,b)))) if a!=b else 0)
    ng=C(p,fun=lambda f:sign(f[0][0],f[0][1])*n(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:omega2(tuple(v[2] for v in f)));wg.closed=True
    sg=C(1,fun=lambda f:s1(tuple(v[0] for v in f)));sg.closed=True
    if accelerate:
        if p!=2 or vertices is None:raise ValueError('Acceleration requires p=2 and a vertex count')
        from fast_y6 import ResidualEngine
        from polynomial_tables import total_cochain
        engine=ResidualEngine(n,omega2,s1,vertices,program="word_residual_program.txt")
        def val(face):
            chain=[tuple(tuple(face[c] for c in v) for v in simplex) for simplex in H]
            result=engine.evaluate_chain(chain)^aw(face)
            engine.clear();return result
        out=C(r,fun=val);out.engine=engine;return out
    R=residual(ng,wg,sg)
    def val(face):
        ans=aw(face)
        for simplex in H:ans^=R(tuple(tuple(face[c] for c in v) for v in simplex))
        return ans
    return C(r,fun=val)

def O5(n1,n2,n3,omega2,s1):
    return sum_terms(full_terms16(n1,n2,n3,omega2,s1),5)

def O6(n2,n3,n4,omega2,s1,*,vertices=None,accelerate=False):
    y=binary_completion(n2,omega2,s1,vertices=vertices,accelerate=accelerate)
    out=sum_terms(full_terms16(n2,n3,n4,omega2,s1,binary_y=y),6);out.Y6=y;return out

def rephasing16(n,nmajorana,nfermion,omega2,s1):
    """Original independent phase = this revision + d_s(rephasing), mod 16.

    Includes polarization, one-word Cartan change, its binary lift carry,
    and the original 2638-to-960 term total-complex compression.
    """
    from ez_homotopy import ez_homotopy
    from polynomial_tables import compression_rephasing
    p=n.deg;r=p+3
    h=(n-n.reduce(2).lift()).div(2).reduce(2);u=nmajorana+cup(s1,h)
    _,K,_,_=integer_inputs(n,omega2,s1)
    H=cartan_rephasing(n,omega2,s1)
    def sign(a,b):return (-1)**(s1(tuple(sorted((a,b)))) if a!=b else 0)
    ng=C(p,fun=lambda f:sign(f[0][0],f[0][1])*n(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:omega2(tuple(v[2] for v in f)));wg.closed=True
    sg=C(1,fun=lambda f:s1(tuple(v[0] for v in f)));sg.closed=True
    eta=cartan_table_shift(ng,wg,sg);chain=ez_homotopy(r)
    def val(face):
        return sum(eta(tuple(tuple(face[c] for c in v) for v in simplex)) for simplex in chain)%2
    heta=C(r,fun=val)
    return (cup(beta_open(u),K,p+1).scaled(4*((-1)**p))+H.lift().scaled(4)
            +heta.lift().scaled(8)+compression_rephasing(n,omega2,s1).lift().scaled(8))
