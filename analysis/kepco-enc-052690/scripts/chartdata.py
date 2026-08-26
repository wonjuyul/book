import re, json, math, random, statistics as st
import os as _os
_D = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
_p = lambda f: _os.path.join(_D, f)
random.seed(11)
def load(fn):
    raw=open(fn,encoding='utf-8').read()
    rows=re.findall(r'\["(\d{8})",\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*(\d+),\s*([\d.]+)\]', raw)
    d=[(a,float(b),float(c),float(e),float(f),int(g),float(h)) for a,b,c,e,f,g,h in rows]
    d.sort(); return d
K=load(_p('long_052690.txt'))
hist=[{"d":r[0],"c":r[4]} for r in K if r[0]>='20250102']
# downsample to ~2/week
hist=[h for i,h in enumerate(hist) if i%2==0 or i==len(hist)-1]
g=json.load(open(_p('garch.json'))); w,a,b,s0,zs=g['w'],g['a'],g['b'],g['s_now'],g['zs']
P0=123400.0; mu=0.195/252; NS=20000; MX=250
paths=[[0.0]*(MX+1) for _ in range(NS)]
for i in range(NS):
    s=s0; lp=0.0
    for t in range(1,MX+1):
        z=random.choice(zs); e=z*math.sqrt(s); lp+=mu-0.5*s+e; s=w+a*e*e+b*s
        paths[i][t]=lp
QS=[0.05,0.25,0.5,0.75,0.95]
fan=[]
days=[0]+[t for t in range(5,MX+1,5)]
for t in days:
    col=sorted(math.exp(p[t])*P0 for p in paths)
    fan.append({"t":t,"q":[round(col[int(q*(NS-1))]) for q in QS]})
json.dump({"hist":hist,"fan":fan,"p0":P0}, open(_p('chart.json'),'w'))
print("hist pts", len(hist), "fan pts", len(fan))
print("fan @250:", fan[-1])
print("fan @20:", [f for f in fan if f['t']==20][0])
print("fan @60:", [f for f in fan if f['t']==60][0])
print("fan @125:", [f for f in fan if f['t']==125][0])
