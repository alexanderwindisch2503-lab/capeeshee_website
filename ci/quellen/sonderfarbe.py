import pikepdf,re,sys
SPOT='PANTONE 809 C'; ALT=[0.10,0,1,0]   # Neongelb, Ersatzwert CMYK für die Ansicht
YEL=(0.9412,0.9569,0.0)
def cmyk(r,g,b):
    k=1-max(r,g,b)
    if k>=0.999: return (0,0,0,1)
    return tuple(round(x,4) for x in ((1-r-k)/(1-k),(1-g-k)/(1-k),(1-b-k)/(1-k),k))
num=r'(-?\d*\.?\d+)'
pat=re.compile(num+r'\s+'+num+r'\s+'+num+r'\s+(rg|RG)\b')
def conv(data):
    def rep(m):
        r,g,b=map(float,m.groups()[:3]);op=m.group(4)
        if abs(r-YEL[0])<.01 and abs(g-YEL[1])<.01 and b<.01:
            return '/Neon cs 1 scn' if op=='rg' else '/Neon CS 1 SCN'
        c,mm,y,k=cmyk(r,g,b);return f'{c} {mm} {y} {k} '+('k' if op=='rg' else 'K')
    return pat.sub(rep,data)
def run(src,dst):
    pdf=pikepdf.open(src)
    fn=pdf.make_indirect(pikepdf.Dictionary(FunctionType=2,Domain=[0,1],C0=[0,0,0,0],C1=ALT,N=1))
    sep=pdf.make_indirect(pikepdf.Array([pikepdf.Name.Separation,pikepdf.Name('/'+SPOT.replace(' ','#20')),pikepdf.Name.DeviceCMYK,fn]))
    seen=set()
    def walk(obj,res):
        if res is None: res=pikepdf.Dictionary()
        if '/ColorSpace' not in res: res.ColorSpace=pikepdf.Dictionary()
        res.ColorSpace.Neon=sep
        return res
    n=0
    for pg in pdf.pages:
        pg.Resources=walk(pg,pg.get('/Resources'))
        conts=pg.Contents if isinstance(pg.Contents,pikepdf.Array) else [pg.Contents]
        for cs in conts:
            d=cs.read_bytes().decode('latin1');nd=conv(d);n+=d.count('rg')+d.count('RG');cs.write(nd.encode('latin1'))
        for name,x in (pg.Resources.get('/XObject') or {}).items():
            if x.get('/Subtype')=='/Form':
                d=x.read_bytes().decode('latin1');x.write(conv(d).encode('latin1'));x.Resources=walk(x,x.get('/Resources'))
    pdf.save(dst);print(dst,'Farbangaben umgestellt:',n)
for a,b in zip(sys.argv[1::2],sys.argv[2::2]): run(a,b)
