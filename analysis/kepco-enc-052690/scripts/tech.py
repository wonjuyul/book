import json, math, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
import re as _re
_raw = open(_p('long_052690.txt'), encoding='utf-8').read()
d = sorted((a, float(b), float(c), float(e), float(f), int(g), float(h)) for a,b,c,e,f,g,h in
           _re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', _raw))
dates=[r[0] for r in d]; op=[r[1] for r in d]; hi=[r[2] for r in d]; lo=[r[3] for r in d]; cl=[r[4] for r in d]; vol=[r[5] for r in d]; fx=[r[6] for r in d]
n=len(cl)
def sma(x,p,i): return sum(x[i-p+1:i+1])/p if i>=p-1 else None
def ema_series(x,p):
    k=2/(p+1); out=[x[0]]
    for v in x[1:]: out.append(v*k+out[-1]*(1-k))
    return out
# RSI Wilder 14
def rsi(x,p=14):
    g=[0.0]*len(x); l=[0.0]*len(x)
    for i in range(1,len(x)):
        ch=x[i]-x[i-1]; g[i]=max(ch,0); l[i]=max(-ch,0)
    out=[None]*len(x); ag=sum(g[1:p+1])/p; al=sum(l[1:p+1])/p
    out[p]=100-100/(1+ag/al) if al else 100
    for i in range(p+1,len(x)):
        ag=(ag*(p-1)+g[i])/p; al=(al*(p-1)+l[i])/p
        out[i]=100-100/(1+ag/al) if al else 100
    return out
R=rsi(cl)
e12=ema_series(cl,12); e26=ema_series(cl,26)
macd=[a-b for a,b in zip(e12,e26)]; sig=ema_series(macd,9); histm=[a-b for a,b in zip(macd,sig)]
# ATR14
tr=[hi[0]-lo[0]]
for i in range(1,n): tr.append(max(hi[i]-lo[i],abs(hi[i]-cl[i-1]),abs(lo[i]-cl[i-1])))
atr=[None]*n; a=sum(tr[1:15])/14; atr[14]=a
for i in range(15,n): a=(a*13+tr[i])/14; atr[i]=a
i=n-1
mas={p:sma(cl,p,i) for p in (5,20,60,120,200)}
sd20=st.pstdev(cl[i-19:i+1]); bb_mid=mas[20]
print("=== 2026-08-26 기준 기술적 지표 ===")
print(f"종가 {cl[i]:,}  전일 {cl[i-1]:,}  등락 {(cl[i]/cl[i-1]-1)*100:+.2f}%")
for p in (5,20,60,120,200):
    print(f"  MA{p:<3} {mas[p]:>10,.0f}   이격도 {cl[i]/mas[p]*100:6.1f}%")
print(f"  RSI(14) {R[i]:.1f}   (5일전 {R[i-5]:.1f}, 20일전 {R[i-20]:.1f})")
print(f"  MACD {macd[i]:,.0f} / signal {sig[i]:,.0f} / hist {histm[i]:,.0f}  (전일 hist {histm[i-1]:,.0f})")
print(f"  ATR14 {atr[i]:,.0f} ({atr[i]/cl[i]*100:.2f}% of price)")
print(f"  BB(20,2): mid {bb_mid:,.0f} upper {bb_mid+2*sd20:,.0f} lower {bb_mid-2*sd20:,.0f}  %B {(cl[i]-(bb_mid-2*sd20))/(4*sd20)*100:.0f}")
print(f"  거래량 {vol[i]:,} vs 20일평균 {sum(vol[i-19:i+1])/20:,.0f} = {vol[i]/(sum(vol[i-19:i+1])/20):.1f}배")
print(f"  외국인소진율 {fx[i]:.2f}% (1개월전 {fx[i-20]:.2f}%, 3개월전 {fx[i-60]:.2f}%, 연초 {[r[6] for r in d if r[0]>='20260102'][0]:.2f}%)")
# volatility
lr=[math.log(cl[k]/cl[k-1]) for k in range(1,n)]
def ann(x): return st.pstdev(x)*math.sqrt(252)*100
print("\n=== 변동성 ===")
for p,lbl in ((20,'20일'),(60,'60일'),(120,'120일'),(252,'252일')):
    print(f"  {lbl} 실현변동성(연율): {ann(lr[-p:]):.1f}%")
# EWMA lambda .94
var=st.pvariance(lr[-60:])
for x in lr[-60:]: var=0.94*var+0.06*x*x
print(f"  EWMA(0.94) 연율 변동성: {math.sqrt(var*252)*100:.1f}%")
m=st.mean(lr[-252:]); s=st.pstdev(lr[-252:])
sk=sum(((x-m)/s)**3 for x in lr[-252:])/252; ku=sum(((x-m)/s)**4 for x in lr[-252:])/252-3
print(f"  1년 로그수익률 왜도 {sk:+.2f}, 초과첨도 {ku:+.2f}  (일평균 {m*100:+.3f}%)")
json.dump({'lr':lr,'ewma_var':var}, open(_p('stats.json'),'w'))
# monthly closes 2026
print("\n=== 2026 월별 종가 ===")
seen={}
for r in d:
    if r[0]>='20251001': seen[r[0][:6]]=r
for k in sorted(seen): print(f"  {k}: {seen[k][4]:,}")
# key episode
print("\n=== 국면 ===")
def seg(a,b):
    A=[r for r in d if r[0]<=a][-1]; B=[r for r in d if r[0]<=b][-1]
    print(f"  {A[0]} {A[4]:,} → {B[0]} {B[4]:,} : {(B[4]/A[4]-1)*100:+.1f}%")
seg('20250102','20260416'); seg('20260416','20260729'); seg('20260729','20260826'); seg('20260824','20260826')
