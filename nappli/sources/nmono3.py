"""B+ : version B with flush stem joins, wider n and optical spacing."""
import json
from nmono import ICON
from nmono2 import sqpath, word as wordB
def wordBplus(sw=34, xh=155, nw=140, asc=125, desc=70, dotr=24, dotgap=.75, p=2.6, rx=72,
              gaps=(24,34,36,34,30)):   # n|a, a|p, p|p, p|l, l|i  (edge to edge)
    R=xh/2; RX=rx; top=-xh; parts=[]; x=sw/2; r=nw/2; h=sw/2
    def S(d,cap='round'): parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"/>')
    edge=lambda c: c+h
    S(f'M{x} 0V{top+r}a{r} {r} 0 0 1 {nw} 0V0'); right=edge(x+nw)
    # a : squircle + stem cut flush with the bowl's outer top and bottom
    cx=right+gaps[0]+h+RX; S(sqpath(cx,-R,RX,R,p)); S(f'M{cx+RX} {top-h}V{h}','butt'); right=edge(cx+RX)
    for g in gaps[1:3]:
        sx=right+g+h; S(f'M{sx} {top-h}V{desc}','butt'); parts.append(f'<circle cx="{sx}" cy="{desc}" r="{h}" fill="currentColor"/>')
        cx=sx+RX; S(sqpath(cx,-R,RX,R,p)); right=edge(cx+RX)
    lx=right+gaps[3]+h; S(f'M{lx} {-xh-asc}V0'); right=edge(lx)
    ix=right+gaps[4]+h; S(f'M{ix} {top}V0'); right=edge(ix)
    dcy=top-h-dotr-sw*dotgap; parts.append(f'<circle cx="{ix:.1f}" cy="{dcy:.1f}" r="{dotr}" fill="currentColor"/>')
    pad=8; y0=min(-xh-asc-h,dcy-dotr)-pad; y1=desc+h+pad
    return (f'{-pad:.0f} {y0:.0f} {right+2*pad:.0f} {y1-y0:.0f}',''.join(parts))
out={'b': dict(main=wordB(34,30,asc=125,desc=70,dotr=24,dotgap=.75,p=2.6,rx=72), icon=ICON),
     'bplus': dict(main=wordBplus(), icon=ICON)}
json.dump(out,open('nmono3.json','w'))
if __name__=='__main__':
    import cairosvg
    from PIL import Image, ImageDraw, ImageFont
    F=ImageFont.truetype('/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/Inter-wght-500.ttf',24)
    S=Image.new('RGB',(1500,1180),(255,255,255)); d=ImageDraw.Draw(S)
    ic=Image.open('ic.png')
    for i,(k,lab) in enumerate((('b','B · version actuelle'),('bplus','B+ · jonctions à plat, n élargi, espacement optique'))):
        vb,body=out[k]['main']
        cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#000")}</svg>'.encode(),write_to=f'{k}.png',output_height=230)
        im=Image.open(f'{k}.png'); Y=40+i*330
        d.text((60,Y),lab,font=F,fill=(110,110,110) if k=='b' else (0,0,0)); S.paste(im,(60,Y+50),im); S.paste(ic,(60+im.width+70,Y+90),ic)
    # small sizes: where childishness / mush shows first
    d.text((60,720),'B+ en petit (favicon, en-tête de site, signature mail)',font=F,fill=(0,0,0))
    vb,body=out['bplus']['main']
    xx=60
    for hgt in (90,48,28,18):
        cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#000")}</svg>'.encode(),write_to='s.png',output_height=hgt)
        im=Image.open('s.png'); S.paste(im,(xx,800),im); xx+=im.width+60
    inv=Image.new('RGB',(1380,260),(0,0,0)); 
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#fff")}</svg>'.encode(),write_to='w.png',output_height=150)
    im=Image.open('w.png'); inv.paste(im,(60,55),im)
    icw=Image.open('ic.png').convert('RGBA')
    S.paste(inv,(60,900))
    S.save('refine2.png')
