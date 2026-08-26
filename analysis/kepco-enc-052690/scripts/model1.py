import re, json, math, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)

def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d

K=load(_p('long_052690.txt'))
KS=load(_p('raw_KOSPI.txt'))
DS=load(_p('raw_034020.txt'))
print("052690:",len(K),K[0][0],"~",K[-1][0])

# ---------- 1. 2일 급등 귀속 분석 ----------
def ret(d,i,k=1): return d[i][4]/d[i-k][4]-1
ksm={r[0]:r for r in KS}; dsm={r[0]:r for r in DS}
ki={r[0]:i for i,r in enumerate(K)}
print("\n=== [1] 2026-08-25~26 급등 귀속 ===")
for dt in ('20260825','20260826'):
    i=ki[dt]; j=[x for x,r in enumerate(KS) if r[0]==dt][0]; m=[x for x,r in enumerate(DS) if r[0]==dt][0]
    print(f"  {dt}: 한전기술 {ret(K,i)*100:+6.2f}% | KOSPI {ret(KS,j)*100:+5.2f}% | 두산에너빌리티 {ret(DS,m)*100:+6.2f}%")
i=ki['20260826']
j=[x for x,r in enumerate(KS) if r[0]=='20260826'][0]; m=[x for x,r in enumerate(DS) if r[0]=='20260826'][0]
print(f"  2일누적: 한전기술 {(K[i][4]/K[i-2][4]-1)*100:+6.2f}% | KOSPI {(KS[j][4]/KS[j-2][4]-1)*100:+5.2f}% | 두산 {(DS[m][4]/DS[m-2][4]-1)*100:+6.2f}%")

# beta vs KOSPI (2y daily)
def logs(d,n): return [math.log(d[k][4]/d[k-1][4]) for k in range(len(d)-n,len(d))]
common=[dt for dt in [r[0] for r in K if r[0]>='20240801'] if dt in ksm]
kr=[];mr=[]
prev=None
for dt in common:
    ii=ki[dt]
    kr.append(math.log(K[ii][4]/K[ii-1][4]))
    jj=[x for x,r in enumerate(KS) if r[0]==dt][0]
    mr.append(math.log(KS[jj][4]/KS[jj-1][4]))
cov=sum((a-st.mean(kr))*(b-st.mean(mr)) for a,b in zip(kr,mr))/len(kr)
beta=cov/st.pvariance(mr)
corr=cov/(st.pstdev(kr)*st.pstdev(mr))
print(f"  베타(2년, vs KOSPI) = {beta:.2f}, 상관계수 = {corr:.2f}")
mkt=(KS[j][4]/KS[j-2][4]-1)*beta
tot=K[i][4]/K[i-2][4]-1
print(f"  2일 수익률 분해: 시장요인 {mkt*100:+.1f}%p / 종목·테마 고유요인 {(tot-mkt)*100:+.1f}%p  (고유요인 비중 {(tot-mkt)/tot*100:.0f}%)")

# ---------- 2. 자기 종목 이벤트 스터디 ----------
print("\n=== [2] 자기 종목 이벤트 스터디: '2일 +25% 이상 + 거래량 3배 이상' 국면 이후 경로 ===")
n=len(K); ev=[]
for t in range(60,n-1):
    r2=K[t][4]/K[t-2][4]-1
    av=sum(K[x][5] for x in range(t-20,t))/20
    if r2>=0.25 and K[t][5]>=3*av:
        if ev and t-ev[-1][0]<10: continue
        ev.append((t,K[t][0],r2,K[t][5]/av))
print(f"  표본 {len(ev)}건 (2010~2026)")
hdr=f"  {'날짜':<10}{'2일수익':>8}{'거래량배수':>9}" + "".join(f"{h:>9}" for h in ('+5일','+20일','+60일','+120일'))
print(hdr)
agg={h:[] for h in (5,20,60,120)}
for t,dt,r2,vm in ev:
    row=f"  {dt:<10}{r2*100:>7.1f}%{vm:>8.1f}x"
    for h in (5,20,60,120):
        if t+h<n:
            rr=K[t+h][4]/K[t][4]-1; agg[h].append(rr); row+=f"{rr*100:>8.1f}%"
        else: row+=f"{'-':>9}"
    print(row)
print("  ─"*30)
print(f"  {'평균':<10}{'':>17}"+"".join(f"{st.mean(agg[h])*100:>8.1f}%" for h in (5,20,60,120)))
print(f"  {'중앙값':<9}{'':>17}"+"".join(f"{st.median(agg[h])*100:>8.1f}%" for h in (5,20,60,120)))
print(f"  {'승률':<10}{'':>17}"+"".join(f"{sum(1 for x in agg[h] if x>0)/len(agg[h])*100:>8.0f}%" for h in (5,20,60,120)))
print(f"  {'최저':<10}{'':>17}"+"".join(f"{min(agg[h])*100:>8.1f}%" for h in (5,20,60,120)))
print(f"  {'최고':<10}{'':>17}"+"".join(f"{max(agg[h])*100:>8.1f}%" for h in (5,20,60,120)))
json.dump({'events':[(t,dt) for t,dt,_,_ in ev]}, open(_p('events.json'),'w'))
