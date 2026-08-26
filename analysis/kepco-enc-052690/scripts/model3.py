import re, math, random, statistics as st, json
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
random.seed(20260826)
def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d
K=load(_p('long_052690.txt')); cl=[r[4] for r in K]; n=len(cl)
r=[math.log(cl[i]/cl[i-1]) for i in range(1,n)]
r5=r[-1250:]                      # 최근 5년으로 GARCH 적합
mu=st.mean(r5); x=[v-mu for v in r5]; uv=st.pvariance(x)

def nll(p):
    w,a,b=p
    if w<=0 or a<0 or b<0 or a+b>=0.999: return 1e18
    s=uv; L=0.0
    for v in x:
        L+=math.log(s)+v*v/s
        s=w+a*v*v+b*s
        if s<=1e-12: return 1e18
    return 0.5*L
# Nelder-Mead
def nm(f,x0,step=None,it=3000):
    nd=len(x0); step=step or [abs(v)*0.5+1e-8 for v in x0]
    sim=[list(x0)]+[[x0[j]+(step[j] if j==i else 0) for j in range(nd)] for i in range(nd)]
    val=[f(s) for s in sim]
    for _ in range(it):
        o=sorted(range(nd+1), key=lambda i: val[i]); sim=[sim[i] for i in o]; val=[val[i] for i in o]
        if abs(val[-1]-val[0])<1e-10: break
        c=[sum(s[j] for s in sim[:-1])/nd for j in range(nd)]
        rf=[c[j]+1.0*(c[j]-sim[-1][j]) for j in range(nd)]; fr=f(rf)
        if fr<val[0]:
            e=[c[j]+2.0*(c[j]-sim[-1][j]) for j in range(nd)]; fe=f(e)
            sim[-1],val[-1]=(e,fe) if fe<fr else (rf,fr)
        elif fr<val[-2]: sim[-1],val[-1]=rf,fr
        else:
            ct=[c[j]+0.5*(sim[-1][j]-c[j]) for j in range(nd)]; fc=f(ct)
            if fc<val[-1]: sim[-1],val[-1]=ct,fc
            else:
                for i in range(1,nd+1):
                    sim[i]=[sim[0][j]+0.5*(sim[i][j]-sim[0][j]) for j in range(nd)]; val[i]=f(sim[i])
    o=sorted(range(nd+1), key=lambda i: val[i]); return sim[o[0]], val[o[0]]
p,_=nm(nll,[uv*0.05,0.10,0.85])
w,a,b=p
print("=== [3] GARCH(1,1) 적합 (최근 5년, 1,250영업일) ===")
print(f"  omega={w:.3e}  alpha={a:.4f}  beta={b:.4f}  alpha+beta={a+b:.4f} (지속성)")
lrv=w/(1-a-b); print(f"  장기평균 연율변동성 = {math.sqrt(lrv*252)*100:.1f}%")
print(f"  반감기 = {math.log(0.5)/math.log(a+b):.1f}영업일")
# filter to today
s=uv; res=[]
for v in x:
    res.append(v/math.sqrt(s)); s=w+a*v*v+b*s
s_now=s
print(f"  현재(8/26 종가 이후) 조건부 연율변동성 = {math.sqrt(s_now*252)*100:.1f}%")
zs=res[-1250:]
zm=st.mean(zs); zsd=st.pstdev(zs); zs=[(z-zm)/zsd for z in zs]
ku=sum(z**4 for z in zs)/len(zs)-3
print(f"  표준화잔차 초과첨도 {ku:+.2f} (정규분포=0) → 부트스트랩 잔차 사용")
# vol term structure
print("\n  변동성 기간구조 (GARCH 예측, 연율):")
for H,lbl in ((5,'1주'),(20,'1개월'),(60,'3개월'),(125,'6개월'),(250,'1년')):
    sc=s_now; tot=0
    for k in range(H):
        tot+=sc; sc=lrv+(a+b)*(sc-lrv)
    print(f"    {lbl:<4} {math.sqrt(tot/H*252)*100:6.1f}%   (누적 표준편차 {math.sqrt(tot)*100:.1f}%)")
json.dump({'w':w,'a':a,'b':b,'s_now':s_now,'lrv':lrv,'zs':zs}, open(_p('garch.json'),'w'))
