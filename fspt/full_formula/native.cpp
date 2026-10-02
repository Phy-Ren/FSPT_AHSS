// Exact scalar-DAG execution. Overflow requests the Python big-integer path.
// Every quotient and floor operation retains the publication semantics.
#include <cstdint>
#include <limits>
#include <vector>

static int64_t mod_positive(int64_t a,int64_t b) {
    int64_t r=a%b;
    return r<0?r+b:r;
}
extern "C" int fspt_formula_eval(const int64_t* nodes,int64_t count,
                                 const int64_t* fields,int64_t field_count,
                                 const int64_t* outputs,int64_t output_count,
                                 int64_t* result,int64_t* bad_node) {
    std::vector<int64_t> values(static_cast<std::size_t>(count));
    for(int64_t i=0;i<count;++i) {
        int64_t op=nodes[3*i],a=nodes[3*i+1],b=nodes[3*i+2],v=0;
        *bad_node=i;
        switch(op) {
        case 0:v=a;break;
        case 1:if(a<0||a>=field_count)return -4;v=fields[a];break;
        case 2:if(__builtin_add_overflow(values[a],values[b],&v))return -2;break;
        case 3:if(__builtin_mul_overflow(values[a],values[b],&v))return -2;break;
        case 4:if(b<=0)return -4;v=mod_positive(values[a],b);break;
        case 5:if(b<=0||values[a]%b)return -3;v=values[a]/b;break;
        case 6:{if(b<=0)return -4;int64_t x=values[a];v=x/b-(x%b<0);break;}
        case 7:{if(b<0||b>=62)return -4;int64_t q=int64_t(1)<<b,x=values[a];
                v=mod_positive(x/q-(x%q<0),2);break;}
        default:return -4;
        }
        values[i]=v;
    }
    for(int64_t j=0;j<output_count;++j)result[j]=values[outputs[j]];
    return 0;
}
