import re, math, statistics as st, json
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d
K=load(_p('long_052690.txt')); cl=[r[4] for r in K]; hi=[r[2] for r in K]; vol=[r[5] for r in K]; n=len(cl); dts=[r[0] for r in K]
def ma(t,p): return sum(cl[t-p+1:t+1])/p
def rsi_at(t,p=14):
    g=l=0.0
    for i in range(t-p+1,t+1):
        ch=cl[i]-cl[i-1]; g+=max(ch,0); l+=max(-ch,0)
    return 100 if l==0 else 100-100/(1+g/l)
def feats(t):
    return [1.0,
            math.log(cl[t]/ma(t,20)),
            math.log(cl[t]/ma(t,120)),
            math.log(cl[t]/max(hi[max(0,t-249):t+1])),
            math.log((sum(vol[t-19:t+1])/20)/(sum(vol[t-59:t+1])/60)),
            (rsi_at(t)-50)/50]
NAMES=['const','log(P/MA20)','log(P/MA120)','log(P/52wHigh)','log(V20/V60)','RSI편차']
def ols(X,y):
    k=len(X[0]); A=[[sum(X[i][a]*X[i][b] for i in range(len(X))) for b in range(k)]+[sum(X[i][a]*y[i] for i in range(len(X)))] for a in range(k)]
    for c in range(k):
        p=max(range(c,k), key=lambda rr: abs(A[rr][c])); A[c],A[p]=A[p],A[c]
        pv=A[c][c]
        for j in range(c,k+1): A[c][j]/=pv
        for rr in range(k):
            if rr!=c and A[rr][c]!=0:
                f=A[rr][c]
                for j in range(c,k+1): A[rr][j]-=f*A[c][j]
    return [A[i][k] for i in range(k)]
print("=== [4] 종목 맞춤 다요인 회귀 (한전기술 2010~2026 자체 데이터로 적합) ===")
today=n-1; ft=feats(today)
print("  현재 팩터값: " + ",  ".join(f"{NAMES[i]} {ft[i]:+.3f}" for i in range(1,6)))
out={}
for h in (5,20,60,120,250):
    X=[];Y=[];D=[]
    for t in range(250,n-h):
        X.append(feats(t)); Y.append(math.log(cl[t+h]/cl[t])); D.append(t)
    bfull=ols(X,Y)
    yh=[sum(b*xx for b,xx in zip(bfull,x)) for x in X]
    ybar=st.mean(Y); ss=sum((a-b)**2 for a,b in zip(Y,yh)); tt=sum((a-ybar)**2 for a in Y)
    r2=1-ss/tt
    # walk-forward OOS: 적합 2010~2021, 검증 2022~
    cut=[i for i,t in enumerate(D) if dts[t]>='20220101'][0]
    bis=ols(X[:cut],Y[:cut])
    yo=[sum(b*xx for b,xx in zip(bis,x)) for x in X[cut:]]
    yv=Y[cut:]
    sso=sum((a-b)**2 for a,b in zip(yv,yo)); tto=sum((a-st.mean(Y[:cut]))**2 for a in yv)
    r2o=1-sso/tto
    ic=(sum((a-st.mean(yo))*(b-st.mean(yv)) for a,b in zip(yo,yv))/len(yo))/(st.pstdev(yo)*st.pstdev(yv))
    pred=sum(b*xx for b,xx in zip(bfull,ft)); rmse=math.sqrt(ss/len(Y))
    out[h]=(pred,rmse,r2,r2o,ic,bfull)
    print(f"\n  ▶ +{h}영업일 예측  |  R²(in) {r2:.3f}  R²(OOS 2022~) {r2o:+.3f}  IC(OOS) {ic:+.2f}")
    print("     계수: " + ",  ".join(f"{NAMES[i]} {bfull[i]:+.3f}" for i in range(1,6)))
    print(f"     ⇒ 예측 로그수익률 {pred*100:+.1f}%  →  단순수익률 {(math.exp(pred)-1)*100:+.1f}%   (잔차 σ {rmse*100:.1f}%)")
json.dump({str(k):(v[0],v[1],v[2],v[3],v[4]) for k,v in out.items()}, open(_p('reg.json'),'w'))
