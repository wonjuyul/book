import json, math, random, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
random.seed(11)
g=json.load(open(_p('garch.json'))); w,a,b,s0,lrv,zs=g['w'],g['a'],g['b'],g['s_now'],g['lrv'],g['zs']
P0=123400.0; SH=38.22e6
# --- 시나리오 확률 트리 ---
print("=== [8] 촉매 확률 트리 (12개월 시계) ===")
cat=[("웨스팅하우스 韓 지분참여 최종 성사 (CFIUS·가격 협상 통과)",0.40),
     ("  └ 성사 시 한전기술 미국 설계·용역 실질 수주로 연결",0.50),
     ("12차 전기본(12월 확정)에 신규 대형원전 2기 이상 반영",0.70),
     ("완도금일 해상풍력 본계약(약 1조원) 체결",0.60),
     ("체코 두코바니 매출 계획대로(2026년 1,000억+) 인식",0.75),
     ("2027년 체코 테멜린 3·4 또는 베트남 닌투언 추가 수주 가시화",0.35)]
for t,p in cat: print(f"  {t:<52} {p*100:>3.0f}%")
P_bull=0.40*0.50*0.70          # 미국 실질수주 + 국내 신규
P_bull=round(P_bull+0.05,2)
P_bear=0.22; P_base=round(1-P_bull-P_bear,2)
print(f"\n  ⇒ 시나리오 확률: Bull {P_bull*100:.0f}% / Base {P_base*100:.0f}% / Bear {P_bear*100:.0f}%")
TP={'Bull':255756,'Base':145997,'Bear':69074}
ev=P_bull*TP['Bull']+P_base*TP['Base']+P_bear*TP['Bear']
print(f"  ⇒ 확률가중 12개월 기대주가 = {ev:,.0f}원 ({(ev/P0-1)*100:+.1f}%)")
mu12=math.log(ev/P0)
print(f"  ⇒ 내재 로그드리프트 = {mu12*100:+.1f}%/년")

# --- 최종 몬테카를로 (드리프트=확률가중, 경로 추적) ---
HS=[(5,'1주'),(20,'1개월'),(60,'3개월'),(125,'6개월'),(250,'12개월')]
NS=30000; mx=250; mu=mu12/252
LV=[('77,100 (7월 저점)',77100),('90,000',90000),('100,000',100000),
    ('135,400 (8/26 장중고가)',135400),('151,816 (61.8% 되돌림)',151816),
    ('198,000 (4월 전고점)',198000)]
term={h:[] for h,_ in HS}; hit={l:[0]*len(HS) for l,_ in LV}
for _ in range(NS):
    s=s0; lp=0.0; mn=0.0; mxp=0.0; snap={}
    for t in range(1,mx+1):
        z=random.choice(zs); e=z*math.sqrt(s); lp+=mu-0.5*s+e; s=w+a*e*e+b*s
        mn=min(mn,lp); mxp=max(mxp,lp)
        if t in (5,20,60,125,250):
            snap[t]=(lp,mn,mxp)
    for h,_ in HS: term[h].append(math.exp(snap[h][0]))
    for li,(lbl,lv) in enumerate(LV):
        for hi_,(h,_) in enumerate(HS):
            lp_,mn_,mx_=snap[h]
            if lv<P0:
                if P0*math.exp(mn_)<=lv: hit[lbl][hi_]+=1
            else:
                if P0*math.exp(mx_)>=lv: hit[lbl][hi_]+=1
def q(v,p): v=sorted(v); return v[int(p*(len(v)-1))]
print("\n=== [9] 최종 통합 예측 분포 (GARCH-부트스트랩 MC 30,000경로 + 시나리오 드리프트) ===")
print(f"  {'구간':<7}{'하위5%':>9}{'하위25%':>9}{'중앙값':>9}{'상위75%':>9}{'상위95%':>9}{'기대값':>9}{'P(상승)':>8}")
for h,nm in HS:
    v=term[h]; print(f"  {nm:<7}"+"".join(f"{P0*q(v,p):>9,.0f}" for p in (0.05,0.25,0.5,0.75,0.95))+f"{P0*st.mean(v):>9,.0f}{sum(1 for x in v if x>1)/len(v)*100:>7.0f}%")
print("\n=== [10] 주요 가격대 '기간 내 1회 이상 도달' 확률 ===")
print(f"  {'레벨':<26}"+"".join(f"{nm:>9}" for _,nm in HS))
for lbl,lv in LV:
    print(f"  {lbl:<26}"+"".join(f"{hit[lbl][i]/NS*100:>8.0f}%" for i in range(len(HS))))
