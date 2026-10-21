import json, math, sys
src = sys.argv[1]; out = sys.argv[2]
d = json.load(open(src))
def dp(pts, eps):
    if len(pts) < 3: return pts
    # iterative Douglas-Peucker
    keep = [False]*len(pts); keep[0]=keep[-1]=True
    stack=[(0,len(pts)-1)]
    while stack:
        a,b=stack.pop()
        ax,ay=pts[a]; bx,by=pts[b]; dx,dy=bx-ax,by-ay; L=math.hypot(dx,dy)
        best=-1; bi=-1
        for i in range(a+1,b):
            px,py=pts[i]
            dist = abs(dy*px-dx*py+bx*ay-by*ax)/L if L>0 else math.hypot(px-ax,py-ay)
            if dist>best: best=dist; bi=i
        if best>eps: keep[bi]=True; stack+=[(a,bi),(bi,b)]
    return [p for p,k in zip(pts,keep) if k]
def area(r):
    s=0
    for i in range(len(r)-1): s+=r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1]
    return s/2
def fix(ring, exterior, eps, prec):
    r = dp(ring, eps) if eps>0 else ring
    r = [[round(x,prec),round(y,prec)] for x,y in r]
    o=[]
    for p in r:
        if not o or p!=o[-1]: o.append(p)
    if o[0]!=o[-1]: o.append(o[0])
    if len(o)<4: return None
    a=area(o)
    if (exterior and a>0) or ((not exterior) and a<0): o=o[::-1]
    return o
feats=[]
for f in d['features']:
    p=f['properties']; g=f['geometry']
    polys = g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    xs=[c[0] for poly in polys for c in poly[0]]; ys=[c[1] for poly in polys for c in poly[0]]
    out_polys=[]
    for poly in polys:
        rx=[c[0] for c in poly[0]]; ry=[c[1] for c in poly[0]]
        span=max(max(rx)-min(rx),max(ry)-min(ry))
        if span>3: eps,prec=0,3
        elif span>0.5: eps,prec=0,3
        else: eps,prec=0,3
        rings=[]
        for i,ring in enumerate(poly):
            fr=fix(ring,True,eps,prec) if i==0 else fix(ring,False,0,3)
            if fr: rings.append(fr)
            elif i==0: break
        if rings: out_polys.append(rings)
    if not out_polys: print('DROPPED',p['NAME']); continue
    feats.append([p['ADM0_A3'],p['NAME'],p['SUBREGION'],p['REGION_UN'],p['TYPE'],out_polys])
s=json.dumps(feats,separators=(',',':'),ensure_ascii=False)
open(out,'w').write(s); print(len(feats), len(s))
