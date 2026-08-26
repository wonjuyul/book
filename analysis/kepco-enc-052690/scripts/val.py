import math
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
SH=38.22e6; P0=123400.0; MC=SH*P0
print(f"=== [7] 밸류에이션 ===  시가총액 {MC/1e12:.3f}조원 (주가 123,400 × 38,220천주)")
print("\n[7-1] 현재 멀티플")
rows=[("2025A 확정", 2234, 16428),("2026E 컨센서스(FnGuide)", 1514, 16549)]
for lbl,eps,bps in rows:
    print(f"  {lbl:<24} EPS {eps:>6,}원 → PER {P0/eps:>6.1f}배 | BPS {bps:>6,}원 → PBR {P0/bps:>5.2f}배")
ttm_eps=942
print(f"  {'최근 12개월(TTM) 추정':<24} EPS {ttm_eps:>6,}원 → PER {P0/ttm_eps:>6.1f}배   (1H26 순이익 168억 급감 반영)")
print("\n[7-2] 이익 시나리오 빌드업 (자체 추정, 단위 억원)")
sc={
 'Bear':  dict(y26=(5900,650,520), y27=(6200,780,660), y28=(6000,700,600), note="체코 5·6호기만, 신규 대형수주 공백·미국 무산"),
 'Base':  dict(y26=(6000,744,580), y27=(7300,1100,930), y28=(8200,1290,1090), note="체코 정상화+완도금일 본계약+국내 신규 2기 설계"),
 'Bull':  dict(y26=(6183,819,700), y27=(8200,1350,1150), y28=(11000,1980,1650), note="+웨스팅하우스 협업 미국 설계참여+체코/베트남 후속"),
}
for k,v in sc.items():
    print(f"  ▸ {k:<5} {v['note']}")
    for y in ('y26','y27','y28'):
        s,o,ni=v[y]; print(f"      20{y[1:]}  매출 {s:>6,}  영업이익 {o:>5,} (OPM {o/s*100:4.1f}%)  순이익 {ni:>5,}  EPS {ni*1e8/SH:>6,.0f}원")
print("\n[7-3] 12개월 목표주가 (2027E EPS × 적용 PER)")
print(f"  {'시나리오':<7}{'2027E EPS':>11}{'적용PER':>9}{'목표주가':>12}{'현재가대비':>11}")
for k,per in (('Bear',40),('Base',60),('Bull',85)):
    eps=sc[k]['y27'][2]*1e8/SH; tp=eps*per
    print(f"  {k:<7}{eps:>10,.0f}원{per:>8}배{tp:>11,.0f}원{(tp/P0-1)*100:>10.0f}%")
print("\n[7-4] 리버스 DCF — 현재가가 요구하는 이익 성장률")
r=0.095; tg=0.02; base=580e8
def pv(g):
    v=0; f=base
    for t in range(1,11):
        f*= (1+g); v+= f/(1+r)**t
    v += f*(1+tg)/(r-tg)/(1+r)**10
    return v
lo,hi=0.0,0.60
for _ in range(80):
    m=(lo+hi)/2
    if pv(m)<MC: lo=m
    else: hi=m
print(f"  가정: 할인율 9.5%, 영구성장 2.0%, 2026E 순이익(=FCF) 580억, 10년 명시적 예측")
print(f"  ⇒ 현재 시가총액 4.716조가 정당화되려면 10년간 순이익 연평균 {lo*100:.1f}% 성장 필요")
print(f"     (10년 뒤 순이익 {base*(1+lo)**10/1e8:,.0f}억원 = 현재의 {(1+lo)**10:.1f}배)")
for g in (0.10,0.15,0.20,0.25,0.30):
    v=pv(g); print(f"     성장률 {g*100:>4.0f}% 가정 시 적정 시총 {v/1e12:>5.2f}조 → 적정주가 {v/SH:>9,.0f}원 ({(v/SH/P0-1)*100:+6.0f}%)")
print("\n[7-5] 수주잔고 배수")
bl=2.0e12
print(f"  수주잔고 추정 약 {bl/1e12:.1f}조원 (대신증권 8/10 '시총/수주잔고 1.9배' 역산, 당시 주가 100,900원)")
print(f"  현재 시총/수주잔고 = {MC/bl:.2f}배  (국내 원전·전력 피어 3~5배)")
for m in (2.5,3.0,4.0,5.0):
    print(f"    배수 {m:.1f}배 적용 → 시총 {bl*m/1e12:.2f}조 → 주가 {bl*m/SH:>9,.0f}원 ({(bl*m/SH/P0-1)*100:+6.0f}%)")
print("  ※ 완도금일 해상풍력 본계약(1조원 규모) 반영 시 잔고 3.0조 → 배수 1.57배로 하락(밸류 여력 확대)")
