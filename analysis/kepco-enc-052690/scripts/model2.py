import re, math, statistics as st, json
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d
K=load(_p('long_052690.txt')); n=len(K)
cl=[r[4] for r in K]; vol=[r[5] for r in K]
def study(name, cond, hs=(5,20,60,120,250)):
    ev=[]
    for t in range(120,n-1):
        if cond(t):
            if ev and t-ev[-1]<10: continue
            ev.append(t)
    agg={h:[r for r in ((cl[t+h]/cl[t]-1) for t in ev if t+h<n)] for h in hs}
    print(f"\n  ▸ {name}  (표본 {len(ev)}건)")
    print(f"    {'구간':<8}{'평균':>9}{'중앙값':>9}{'승률':>8}{'하위10%':>10}{'상위10%':>10}")
    for h in hs:
        a=sorted(agg[h])
        if len(a)<3: print(f"    +{h}일 표본부족({len(a)})"); continue
        p10=a[int(0.1*(len(a)-1))]; p90=a[int(0.9*(len(a)-1))]
        print(f"    +{h}일{'':<3}{st.mean(a)*100:>8.1f}%{st.median(a)*100:>8.1f}%{sum(1 for x in a if x>0)/len(a)*100:>7.0f}%{p10*100:>9.1f}%{p90*100:>9.1f}%")
    return agg
def av(t,p=20): return sum(vol[x] for x in range(t-p,t))/p
def ma(t,p): return sum(cl[t-p+1:t+1])/p
print("=== [2] 한전기술 자기 이력 조건부 이벤트 스터디 (2010~2026, 4,110영업일) ===")
study("2일 +15% 이상 & 거래량 2.5배 이상", lambda t: cl[t]/cl[t-2]-1>=0.15 and vol[t]>=2.5*av(t))
study("20일 이격도 125% 이상 (과열)", lambda t: cl[t]/ma(t,20)>=1.25)
study("20일 이격도 125%↑ & 60일 이격도 115%↑", lambda t: cl[t]/ma(t,20)>=1.25 and cl[t]/ma(t,60)>=1.15)
study("52주 고점 대비 -30%↓ 구간에서의 반등 급등(2일 +15%)", lambda t: cl[t]/cl[t-2]-1>=0.15 and cl[t]/max(r[2] for r in K[max(0,t-250):t+1])<=0.75)
# unconditional baseline
print("\n  ▸ [기준선] 무조건부 전체구간")
for h in (5,20,60,120,250):
    a=sorted(cl[t+h]/cl[t]-1 for t in range(120,n-h))
    print(f"    +{h}일{'':<3}{st.mean(a)*100:>8.1f}%{st.median(a)*100:>8.1f}%{sum(1 for x in a if x>0)/len(a)*100:>7.0f}%{a[int(0.1*(len(a)-1))]*100:>9.1f}%{a[int(0.9*(len(a)-1))]*100:>9.1f}%")
