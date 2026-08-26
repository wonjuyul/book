import json, math, random, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
random.seed(7)
g=json.load(open(_p('garch.json'))); w,a,b,s0,lrv,zs=g['w'],g['a'],g['b'],g['s_now'],g['lrv'],g['zs']
P0=123400.0
HS=[(5,'1주'),(20,'1개월'),(60,'3개월'),(125,'6개월'),(250,'1년')]
NS=20000
def run(drift_ann):
    mu=drift_ann/252
    res={h:[] for h,_ in HS}
    mx=HS[-1][0]
    for _ in range(NS):
        s=s0; lp=0.0; 
        path={}
        for t in range(1,mx+1):
            z=random.choice(zs); e=z*math.sqrt(s)
            lp+=mu-0.5*s+e
            s=w+a*e*e+b*s
            path[t]=lp
        for h,_ in HS: res[h].append(math.exp(path[h]))
    return res
def qs(v,ps=(0.05,0.10,0.25,0.50,0.75,0.90,0.95)):
    v=sorted(v); return [v[int(p*(len(v)-1))] for p in ps]
print("=== [5] GARCH-부트스트랩 몬테카를로 (20,000경로, 기준가 123,400원) ===")
for lbl,dr in (("A. 드리프트 0 (중립)",0.0),("B. 드리프트 +15%/년 (강세)",0.15),("C. 드리프트 -15%/년 (약세)",-0.15)):
    R=run(dr)
    print(f"\n  ── {lbl} ──")
    print(f"    {'구간':<6}{'5%':>9}{'10%':>9}{'25%':>9}{'50%(중앙)':>11}{'75%':>9}{'90%':>9}{'95%':>9}{'평균':>9}{'P(상승)':>8}")
    for h,nm in HS:
        q=qs(R[h]); m=st.mean(R[h]); pu=sum(1 for x in R[h] if x>1)/len(R[h])
        print(f"    {nm:<6}"+"".join(f"{P0*x:>9,.0f}" for x in q[:3])+f"{P0*q[3]:>11,.0f}"+"".join(f"{P0*x:>9,.0f}" for x in q[4:])+f"{P0*m:>9,.0f}{pu*100:>7.0f}%")
    if dr==0.0: json.dump({str(h):R[h] for h,_ in HS}, open(_p('mc0.json'),'w'))
