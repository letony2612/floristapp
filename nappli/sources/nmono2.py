"""Grown-up refinements of the 'Appuyé' monoline wordmark."""
import json, math
from nmono import ICON
def sqpath(cx,cy,rx,ry,p=2.0,n=96):
    # superellipse ("squircle", like iOS icon corners); p=2 is a circle
    pts=[]
    for i in range(n):
        t=2*math.pi*i/n; c,s=math.cos(t),math.sin(t)
        x=cx+rx*math.copysign(abs(c)**(2/p),c); y=cy+ry*math.copysign(abs(s)**(2/p),s); pts.append(f'{x:.2f} {y:.2f}')
    return 'M'+'L'.join(pts)+'Z'
def word(sw=34, gap=44, xh=155, nw=130, asc=100, desc=95, dotr=None, p=2.0, rx=None, dotgap=0.9):
    r=nw/2; R=xh/2; RX=rx or R; top=-xh; parts=[]; x=sw/2
    def S(d): parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    edge=lambda c: c+sw/2
    S(f'M{x} 0V{top+r}a{r} {r} 0 0 1 {nw} 0V0'); right=edge(x+nw)
    cx=right+gap+sw/2+RX; S(sqpath(cx,-R,RX,R,p)); S(f'M{cx+RX} {top}V0'); right=edge(cx+RX)
    for _ in range(2):
        sx=right+gap+sw/2; S(f'M{sx} {top}V{desc}'); cx=sx+RX; S(sqpath(cx,-R,RX,R,p)); right=edge(cx+RX)
    lx=right+gap+sw/2; S(f'M{lx} {-xh-asc}V0'); right=edge(lx)
    ix=right+gap+sw/2; S(f'M{ix} {top}V0'); right=edge(ix)
    dr=dotr or sw; dcy=top-sw/2-dr-sw*dotgap
    parts.append(f'<circle cx="{ix:.1f}" cy="{dcy:.1f}" r="{dr}" fill="currentColor"/>')
    pad=8; y0=min(-xh-asc-sw/2,dcy-dr)-pad; y1=desc+sw/2+pad
    return (f'{-pad:.0f} {y0:.0f} {right+2*pad:.0f} {y1-y0:.0f}',''.join(parts))
out={
 'appuye': dict(main=word(34,44), icon=ICON),                                              # current
 'a1':     dict(main=word(34,30,asc=125,desc=70,dotr=24,dotgap=.75), icon=ICON),            # tighter, smaller dot, taller l, shorter p
 'a2':     dict(main=word(34,30,asc=125,desc=70,dotr=24,dotgap=.75,p=2.6,rx=72), icon=ICON),# + squircle bowls (iOS curve)
 'a3':     dict(main=word(30,28,asc=130,desc=70,dotr=20,dotgap=.75,p=2.6,rx=70), icon=ICON),# + a touch lighter
}
json.dump(out,open('nmono2.json','w'))
if __name__=='__main__':
    import cairosvg
    from PIL import Image, ImageDraw, ImageFont
    F=ImageFont.truetype('/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/Inter-wght-500.ttf',22)
    labels={'appuye':'Actuel · Appuyé','a1':'A · serré, point plus petit, proportions plus élancées','a2':'B · A + panses « squircle » (courbe des icônes iOS)','a3':'C · B + trait un peu plus fin'}
    S=Image.new('RGB',(1500,1260),(255,255,255)); d=ImageDraw.Draw(S)
    icon_svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8"/><g transform="translate(2 2)">'+ICON[1].replace('var(--dot,currentColor)','#fff').replace('currentColor','#fff')+'</g></svg>'
    cairosvg.svg2png(bytestring=icon_svg.encode(),write_to='ic.png',output_width=150)
    ic=Image.open('ic.png')
    for i,(k,v) in enumerate(out.items()):
        vb,body=v['main']; x,y,w,h=map(float,vb.split())
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#000")}</svg>'
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'r-{k}.png',output_height=200)
        im=Image.open(f'r-{k}.png'); Y=40+i*305
        d.text((60,Y),labels[k],font=F,fill=(110,110,110) if k=='appuye' else (0,0,0))
        S.paste(im,(60,Y+50),im); S.paste(ic,(60+im.width+80,Y+75),ic)
    S.save('refine.png')
