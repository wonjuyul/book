import re, math, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d
K=load(_p('long_052690.txt')); n=len(K); P0=123400.0
HI, LO = 198000.0, 77100.0
print("=== [6-1] 되돌림/기술적 레벨 (2026-04-16 고점 198,000 → 07-29 저점 77,100, 낙폭 120,900) ===")
for f,l in ((0.236,'23.6%'),(0.382,'38.2%'),(0.5,'50.0%'),(0.618,'61.8%'),(0.786,'78.6%'),(1.0,'100%')):
    v=LO+f*(HI-LO); tag=" ← 현재가 근접" if abs(v-P0)/P0<0.03 else ""
    print(f"  피보나치 {l:<6} {v:>9,.0f}원  (현재가 대비 {(v/P0-1)*100:+6.1f}%){tag}")
print("\n=== [6-2] 매물대 분석 (최근 250영업일, 5,000원 구간) ===")
W=K[-250:]; tv=sum(r[5] for r in W)
buck={}
for r in W:
    tp=(r[2]+r[3]+r[4])/3; b=int(tp//5000)*5000
    buck[b]=buck.get(b,0)+r[5]
top=sorted(buck.items(), key=lambda x:-x[1])[:10]
above=sum(v for b,v in buck.items() if b>P0); below=sum(v for b,v in buck.items() if b<=P0)
print(f"  현재가 위 누적 거래량 비중 {above/tv*100:.0f}%  /  아래 {below/tv*100:.0f}%")
print("  상위 밀집 매물대:")
for b,v in sorted(top, key=lambda x:-x[0]):
    pos = "저항" if b>P0 else "지지"
    print(f"    {b:>8,}~{b+5000:>8,}원  거래량비중 {v/tv*100:5.1f}%   [{pos}]")
print("\n=== [6-3] ATR 기반 단기 밴드 ===")
cl=[r[4] for r in K]; hi=[r[2] for r in K]; lo=[r[3] for r in K]
tr=[max(hi[i]-lo[i],abs(hi[i]-cl[i-1]),abs(lo[i]-cl[i-1])) for i in range(1,n)]
atr=sum(tr[-14:])/14
print(f"  ATR(14) = {atr:,.0f}원 ({atr/P0*100:.1f}%)")
for k in (1,2,3):
    print(f"    ±{k}ATR : {P0-k*atr:>9,.0f} ~ {P0+k*atr:>9,.0f}")
print("\n=== [6-4] 이동평균 ===")
for p in (5,20,60,120,200):
    m=sum(cl[-p:])/p
    print(f"  MA{p:<4}{m:>10,.0f}원   현재가 {'상회' if P0>m else '하회'} ({(P0/m-1)*100:+.1f}%)")
