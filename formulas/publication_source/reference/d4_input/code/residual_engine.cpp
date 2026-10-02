#include <algorithm>
#include <cstdint>
#include <fstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <iostream>
using namespace std;
struct Key{uint64_t lo,hi;bool operator==(const Key&o)const{return lo==o.lo&&hi==o.hi;}};
struct Hash{size_t operator()(const Key&k)const{return k.lo*0x9e3779b97f4a7c15ULL+(k.hi^(k.hi>>29));}};
struct Cut{int sign;vector<vector<int>>faces;};struct Table{int arity;vector<Cut>terms;};
struct Node{int op,deg,mod;vector<int>ch,pa;unordered_map<Key,int64_t,Hash>cache;};
struct Engine{
 int B,root;vector<Node>nodes;vector<Table>tables;vector<int64_t>N,W,S;uint64_t evaluations=0;
 Engine(const char*path,int b,const int64_t*n,const int64_t*w,const int64_t*s):B(b),N(n,n+b*b*b),W(w,w+b*b*b),S(s,s+b*b){
  if((long long)b*b*b>=65536)throw runtime_error("too many original vertices");
  ifstream f(path);if(!f)throw runtime_error("cannot open residual_program.txt");int nn,nt;f>>nn>>nt>>root;
  nodes.resize(nn);tables.resize(nt);
  for(auto&v:nodes){int nc,np;f>>v.op>>v.deg>>v.mod>>nc;v.ch.resize(nc);for(auto&x:v.ch)f>>x;f>>np;v.pa.resize(np);for(auto&x:v.pa)f>>x;}
  for(auto&t:tables){int count;f>>t.arity>>count;t.terms.resize(count);for(auto&c:t.terms){f>>c.sign;c.faces.resize(t.arity);for(auto&face:c.faces){int n;f>>n;face.resize(n);for(auto&x:face)f>>x;}}}
  if(!f)throw runtime_error("malformed residual program");
 }
 int64_t sg(int x,int y){if(x==y)return 0;return S[min(x,y)*B+max(x,y)]&1;}
 int64_t eval(int id,const int*f,int len){
  if(id<0)return 0;auto&n=nodes[id];if(n.op==0)return 0;
  for(int j=1;j<len;j++)if(f[j]==f[j-1])return 0;
  unsigned __int128 kk=0;for(int j=0;j<len;j++)kk|=(unsigned __int128)(unsigned)f[j]<<(16*j);Key key{(uint64_t)kk,(uint64_t)(kk>>64)};
  auto it=n.cache.find(key);if(it!=n.cache.end())return it->second;
  ++evaluations;int64_t v=0;
  auto child=[&](int j){return eval(n.ch[j],f,len);};
  switch(n.op){
   case 1:v=child(0)+child(1);break;
   case 2:v=child(0)-child(1);break;
   case 3:v=n.pa[0]*child(0);break;
   case 4:v=child(0);break;
   case 5:{v=child(0);if(v%n.pa[0])throw runtime_error("non-exact division in residual");v/=n.pa[0];break;}
   case 6:{v=child(0);int k=n.pa[0];v=v>=0?v/k:(v-(k-1))/k;break;}
   case 7:{int ff[12];for(int j=0;j<len;j++){int p=0;for(int k=0;k<len;k++)if(k!=j)ff[p++]=f[k];v+=(j%2?-1:1)*eval(n.ch[0],ff,len-1);}break;}
   case 8:case 9:{
    const auto&t=tables[n.pa[0]];int ff[12];
    for(const auto&cut:t.terms){int64_t term=cut.sign;
     for(int a=0;a<t.arity&&term;a++){
      int l=cut.faces[a].size();for(int z=0;z<l;z++)ff[z]=f[cut.faces[a][z]];
      term*=eval(n.ch[a],ff,l);
     }
     if(term&&n.op==8&&n.ch[2]>=0){
      int sign=0;
      for(int a=0;a<2;a++)if(n.pa[1+a]){int ee[2]={f[0],f[cut.faces[a][0]]};sign^=(int)eval(n.ch[2],ee,2)&1;}
      if(sign)term=-term;
     }
     v+=term;
    }break;}
   case 10:{int a=f[0]/B%B,b=f[1]/B%B,c=f[2]/B%B;if(a!=b&&b!=c&&a!=c)v=(sg(f[0]/(B*B),a)?-1:1)*N[(a*B+b)*B+c];break;}
   case 11:{int a=f[0]%B,b=f[1]%B,c=f[2]%B;if(a!=b&&b!=c&&a!=c)v=W[(a*B+b)*B+c];break;}
   case 12:{int a=f[0]/(B*B),b=f[1]/(B*B);v=sg(a,b);break;}
   default:throw runtime_error("unknown operation");
  }
  if(n.mod){v%=n.mod;if(v<0)v+=n.mod;}
  n.cache.emplace(key,v);return v;
 }
};
static thread_local string error;
extern "C"{
void* make_engine(const char*p,int B,const int64_t*N,const int64_t*W,const int64_t*S){try{error.clear();return new Engine(p,B,N,W,S);}catch(const exception&e){error=e.what();return nullptr;}}
int engine_sum(void*ptr,const int32_t*faces,int count){try{error.clear();auto&e=*(Engine*)ptr;int v=0;for(int i=0;i<count;i++)v^=(int)e.eval(e.root,faces+8*i,8)&1;return v;}catch(const exception&e){error=e.what();return -1;}}
int64_t engine_node(void*p,int id,const int32_t*f,int n){try{error.clear();return ((Engine*)p)->eval(id,f,n);}catch(const exception&e){error=e.what();return INT64_MIN;}}
void engine_clear(void*p){auto&e=*(Engine*)p;for(auto&n:e.nodes){unordered_map<Key,int64_t,Hash> empty;n.cache.swap(empty);}}
uint64_t engine_evaluations(void*p){return ((Engine*)p)->evaluations;}
const char* engine_error(){return error.c_str();}
void delete_engine(void*p){delete (Engine*)p;}
}
