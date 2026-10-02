"""Optional C++ acceleration; the cochain function equals explicit_y6.Y6."""
from pathlib import Path
from itertools import combinations
import ctypes as ct
import numpy as np
from cochains import C
from explicit_y6 import Y6
from ez_homotopy import ez_homotopy
ROOT=Path(__file__).parent
lib=ct.CDLL(str(ROOT/'residual_engine.so'))
I64=ct.POINTER(ct.c_int64);I32=ct.POINTER(ct.c_int32)
lib.make_engine.argtypes=[ct.c_char_p,ct.c_int,I64,I64,I64];lib.make_engine.restype=ct.c_void_p
lib.engine_sum.argtypes=[ct.c_void_p,I32,ct.c_int];lib.engine_sum.restype=ct.c_int
lib.engine_error.restype=ct.c_char_p
lib.delete_engine.argtypes=[ct.c_void_p]
lib.engine_clear.argtypes=[ct.c_void_p]
lib.engine_evaluations.argtypes=[ct.c_void_p];lib.engine_evaluations.restype=ct.c_uint64
class ResidualEngine:
 def __init__(self,N,w,s,B,program="residual_program.txt"):
  self.B=B;nn=np.zeros((B,B,B),dtype=np.int64);ww=nn.copy();ss=np.zeros((B,B),dtype=np.int64)
  for f in combinations(range(B),3):nn[f]=N(f)%16;ww[f]=w(f)
  for f in combinations(range(B),2):ss[f]=s(f)
  self.ptr=lib.make_engine(str(ROOT/program).encode(),B,nn.ctypes.data_as(I64),ww.ctypes.data_as(I64),ss.ctypes.data_as(I64))
  if not self.ptr:raise RuntimeError(lib.engine_error().decode())
 def evaluate_chain(self,chain):
  data=np.asarray([[((a*self.B)+b)*self.B+c for a,b,c in f] for f in chain],dtype=np.int32)
  if not len(data):return 0
  out=lib.engine_sum(self.ptr,data.ctypes.data_as(I32),len(data))
  if out<0:raise RuntimeError(lib.engine_error().decode())
  return out
 def clear(self):
  if self.ptr:lib.engine_clear(self.ptr)
 def count(self):return lib.engine_evaluations(self.ptr)
 def close(self):
  if self.ptr:lib.delete_engine(self.ptr);self.ptr=None
 def __del__(self):self.close()

def fast_Y6(N,w,s,B,retain_cache=False):
 engine=ResidualEngine(N,w,s,B);aw=Y6(N,w,s,include_h=False);H=ez_homotopy(6)
 def value(face):
  chain=[tuple(tuple(face[c] for c in v) for v in f) for f in H]
  value=engine.evaluate_chain(chain)^aw(face)
  if not retain_cache:engine.clear()
  return value
 out=C(6,fun=value);out.engine=engine;return out
