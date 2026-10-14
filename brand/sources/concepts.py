import math, json
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from glyphs import text_path, font
from logo import horn
C='currentColor'
def P(d,extra=''): return f'<path d="{d}" fill="{C}"{extra}/>'
def G(body,tx=0,ty=0,s=1): return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{body}</g>'
def T(fontname,text,size,x=0,y=0,tr=0,anchor='start'):
    d,w,b=text_path(fontname,text,size,0,0,tracking=tr)
    if anchor=='middle': x-=w/2
    if anchor=='end': x-=w
    d,w,b=text_path(fontname,text,size,x,y,tracking=tr)
    return P(d),w,b
SERIF='fr-soft.ttf'; ITAL='fr-soft-it.ttf'; SANS='bvp-light.ttf'; SANSM='bvp-med.ttf'

# shared: the leaf-horned Ơ from concept 1, as a standalone letter (O at x 0..141, baseline 200)
_size=200;_tr=34
_od,_,_=text_path(SERIF,'O',_size,0,_size)
_st,_lf,_,_=horn(_size,_tr)
_shift=103.2+_tr
LETTER=P(_od)+f'<g transform="translate({-_shift} 0)">'+P(_st)+P(_lf)+'</g>'   # bbox ≈ x 6..176, y 50..202

out={}
# 1 · BUÔNG — serif éditorial, le crochet du Ơ devient une feuille qui pend
d,w,b=text_path(SERIF,'LOI',_size,0,_size,tracking=_tr)
word1=P(d)+P(_st)+P(_lf)
f1,fw,_=T(SANS,'FLEUR',33,w/2,270,28,'middle')
out['buong']=dict(main=('-8 32 384 250',word1+f1),
  line=('-8 32 '+str(int(w+70+250)),None))
f1l,fwl,_=T(SANS,'FLEUR',58,w+60,_size-2,26)
out['buong']['line']=(f'-8 32 {w+64+fwl+16:.0f} 176',word1+f1l)

# 2 · LẢ LƠI — italique manuscrit, minuscules qui ondulent
d2,w2,b2=text_path(ITAL,'lơi',200,0,200,tracking=4)
# loose swash: a long hairline that leaves the i and drifts back under the word
sw=('M150,214 C120,238 40,244 6,232 C40,236 112,232 146,210 Z')
f2,fw2,_=T(ITAL,'fleur',62,w2+6,200,2)
out['laloi']=dict(main=(f'-8 48 {w2+fw2+22:.0f} 206',P(d2)+P(sw)+f2),
                  line=(f'-8 48 {w2+fw2+22:.0f} 206',P(d2)+P(sw)+f2))

# 3 · ARCHE — monogramme dans l'arche de la vitrine
cx=91; aw=112; top=6; bot=262; th=3.4
def arch(aw,top,bot,cx,th):
    o=f'M{cx-aw},{bot} L{cx-aw},{top+aw} A{aw},{aw} 0 0 1 {cx+aw},{top+aw} L{cx+aw},{bot} Z'
    i=aw-th
    n=f'M{cx-i},{bot-th} L{cx-i},{top+aw} A{i},{i} 0 0 1 {cx+i},{top+aw} L{cx+i},{bot-th} Z'
    return f'<path d="{o} {n}" fill="{C}" fill-rule="evenodd"/>'
A=arch(aw,top,bot,cx,th)+G(LETTER,cx-91*0.9,58,0.9)
f3,fw3,_=T(SANS,'LƠI FLEUR',30,cx,318,22,'middle')
VW=max(2*aw,fw3)+16
out['arche']=dict(main=(f'{cx-VW/2:.0f} -2 {VW:.0f} 330',A+f3))
f3l,fw3l,_=T(SANS,'LƠI FLEUR',70,cx+aw+44,165,30)
out['arche']['line']=(f'{cx-aw-8} -2 {2*aw+60+fw3l+16:.0f} 272',A+f3l)

# 4 · NÉT — minimal, sans-serif léger, un seul pétale remplace le crochet
tr4=46
dL,wL,_=text_path(SANS,'L',200,0,200)
dO,wO,_=text_path(SANS,'O',200,wL+tr4,200)
dI,wI,_=text_path(SANS,'I',200,wL+tr4+wO+tr4,200)
ox=wL+tr4; pcx=ox+82+71*math.cos(math.radians(42))+10; pcy=126-76*math.sin(math.radians(42))-16
petal=f'<ellipse cx="{pcx:.1f}" cy="{pcy:.1f}" rx="7.5" ry="17" transform="rotate(38 {pcx:.1f} {pcy:.1f})" fill="{C}"/>'
W4=wL+tr4+wO+tr4+wI
f4,fw4,_=T(SANS,'fleur',40,W4/2,272,30,'middle')
word4=P(dL)+P(dO)+P(dI)+petal
out['net']=dict(main=(f'4 22 {W4+8:.0f} 262',word4+f4))
f4l,fw4l,_=T(SANS,'fleur',70,W4+56,200,24)
out['net']['line']=(f'4 22 {W4+56+fw4l+10:.0f} 192',word4+f4l)

# 5 · ẤN — cachet botanique circulaire
def ring_text(fontname,text,size,R,cx,cy,start_deg,tr=0):
    f=font(fontname); gs=f.getGlyphSet(); cm=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    pen=SVGPathPen(gs); a=math.radians(start_deg)
    for ch in text:
        g=cm[ord(ch)]; adv=gs[g].width*s
        mid=a+ (adv/2)/R
        # glyph centred on its advance, upright pointing outwards, read clockwise
        ca,sa=math.cos(mid),math.sin(mid)
        px=cx+R*math.sin(mid); py=cy-R*math.cos(mid)
        # local x along tangent (ca,sa), local y (font up) towards outside (sin,-cos)
        m=(s*ca, s*sa, s*math.sin(mid)*1, -s*math.cos(mid)*1, px-ca*adv/2, py-sa*adv/2)
        # fontTools affine: (xx, xy, yx, yy, dx, dy): x'=xx*x+yx*y+dx ; y'=xy*x+yy*y+dy
        gs[g].draw(TransformPen(pen,m))
        a+=(adv+tr)/R
    return P(pen.getCommands())
R=118
ring=(f'<circle cx="0" cy="0" r="{R}" fill="none" stroke="{C}" stroke-width="3"/>'
      f'<circle cx="0" cy="0" r="{R-44}" fill="none" stroke="{C}" stroke-width="1.4"/>')
txt='LƠI FLEUR · FLEURISTE · VẺ ĐẸP KHÔNG KHUÔN KHỔ · '
_f=font(SANS);_gs=_f.getGlyphSet();_cm=_f.getBestCmap();_sz=15
_tot=sum(_gs[_cm[ord(c)]].width*_sz/_f['head'].unitsPerEm for c in txt)
rt=ring_text(SANS,txt,_sz,R-28,0,0,0,(2*math.pi*(R-28)-_tot)/len(txt))
seal=ring+rt+G(LETTER,-91*0.55,-128*0.55+4,0.55)
out['an']=dict(main=(f'{-R-6} {-R-6} {2*R+12} {2*R+12}',seal))
f5l,fw5l,_=T(SERIF,'LƠI FLEUR',64,R+40,22,10)
# horizontal: seal + serif name; Ơ glyph from font here is fine (secondary)
out['an']['line']=(f'{-R-6} {-R-6} {2*R+40+fw5l+16:.0f} {2*R+12}',seal+f5l)

# 6 · TIGE — le « l » devient une tige qui s'incline et laisse pendre un bouton
stemw=15
stem=('M17,200 L17,70 C17,30 40,6 70,8 C86,9 97,19 101,32 '
      'L95,35 C91,25 82,21 70,21 C46,21 32,40 32,70 L32,200 Z')
bud=('M98,33 C109,41 112,60 101,78 C90,62 89,43 98,33 Z')
d6,w6,b6=text_path(SANS,'ơi',200,50,200,tracking=4)
word6=P(stem)+P(bud)+P(d6)
W6=50+w6
f6,fw6,_=T(SANS,'FLEUR',32,W6/2+8,266,26,'middle')
out['tige']=dict(main=(f'4 -2 {W6+8:.0f} 280',word6+f6))
f6l,fw6l,_=T(SANS,'FLEUR',58,W6+40,200,24)
out['tige']['line']=(f'4 -2 {W6+40+fw6l+10:.0f} 214',word6+f6l)

json.dump(out,open('concepts.json','w'))
def svg(vb,body,color='#1F1E1A'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" style="color:{color}" color="{color}">{body.replace("currentColor",color)}</svg>'
if __name__=='__main__':
    import cairosvg
    rows=[]
    for k,v in out.items():
        for kind in ('main','line'):
            vb,body=v[kind]
            open(f'{k}-{kind}.svg','w').write(svg(vb,body))
            cairosvg.svg2png(bytestring=svg(vb,body).encode(),write_to=f'{k}-{kind}.png',output_width=900 if kind=='line' else 600)
    from PIL import Image
    ims=[Image.open(f'{k}-main.png') for k in out]
    sheet=Image.new('RGB',(1800,1300),(238,231,218))
    for i,im in enumerate(ims):
        im.thumbnail((480,480)); x=(i%3)*600+60; y=(i//3)*650+60
        sheet.paste(im,(x,y),im)
    sheet.save('sheet.png')
