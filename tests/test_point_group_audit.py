"""Reject finite/affine and representation-label mixups independently of answers."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_point_groups import check_geometry


def mirror():
    matrices = [[[1,0,0],[0,1,0],[0,0,-1]],[[1,0,0],[0,1,0],[0,0,1]]]
    return {'point_group_index':4,'crystalline_spin':'half','pip':{'free_rank':0,'orders':[2]},
        'point_group':{'index':4,'hermannMauguin':'m','schoenflies':'Cs','order':2,'unitary':False,
            'kind':'finite-crystallographic-point-group','representationDimension':3,
            'translationSubgroupPresent':False,'matrices':matrices,'multiplication':[[2,1],[1,2]],
            'identityIndex':2,'signTable':[1,0],'determinantDistribution':{'positive':1,'negative':1},
            'elementSpectra':[[[1,3,1],1],[[2,1,-1],1]],'finiteH0ZsOrders':[],
            'finiteH1ZsOrders':[2],'matrixIsomorphismCheckedAllProducts':True,
            'pcpGeneratorMatrixIndices':[1],'resolutionElementMatrixIndices':[2,1],
            'matrix_set_sha256':hashlib.sha256(json.dumps(sorted(matrices),separators=(',',':')).encode()).hexdigest()}}


class FiniteGeometryAudit(unittest.TestCase):
    def test_mirror_and_identity_order(self):
        check_geometry(mirror())

    def test_reject_affine_translation(self):
        d=mirror();d['point_group']['translationSubgroupPresent']=True
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_affine_result(self):
        d=mirror();d['space_group']=6
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_wrong_multiplication_even_if_group_order_correct(self):
        d=mirror();d['point_group']['multiplication'][0][0]=1
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_sign_with_correct_abstract_c2(self):
        d=mirror();d['point_group']['signTable']=[0,0]
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_matrix_tamper_with_recomputed_digest(self):
        d=mirror();p=d['point_group'];p['matrices'][0]=[[-1,0,0],[0,-1,0],[0,0,-1]]
        p['matrix_set_sha256']=hashlib.sha256(json.dumps(sorted(p['matrices']),separators=(',',':')).encode()).hexdigest()
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_inversion_labeled_mirror_even_with_consistent_spectrum(self):
        d=mirror();p=d['point_group'];p['matrices'][0]=[[-1,0,0],[0,-1,0],[0,0,-1]]
        p['elementSpectra']=[[[1,3,1],1],[[2,-3,-1],1]]
        p['matrix_set_sha256']=hashlib.sha256(json.dumps(sorted(p['matrices']),separators=(',',':')).encode()).hexdigest()
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_spurious_weak_layer(self):
        d=mirror();d['pip']={'free_rank':1,'orders':[0,2]}
        with self.assertRaises(AssertionError): check_geometry(d)

    def test_reject_same_order_wrong_point_name(self):
        d=mirror();d['point_group']['schoenflies']='Ci'
        with self.assertRaises(AssertionError): check_geometry(d)


if __name__ == '__main__': unittest.main()
