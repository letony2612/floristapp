"""Fix the n/appli mismatch: give the n the same squircle curve as the bowls."""
import json, math
from nmono import ICON, ICON_BODY
from nmono2 import sqpath
def sq_arch(x0,x1,base_y,ry,p,n=48):
    # top half of a superellipse spanning x0..x1, sitting on base_y (stroke centre); returns path from left foot to right foot
    cx=(x0+x1)/2; rx=(x1-x0)/2; pts=[]
    for i in range(n+1):
        t=math.pi+math.pi*i/n; c,s=math.cos(t),math.sin(t)
        pts.append(f'{cx+rx*math.copysign(abs(c)**(2/p),c):.2f} {base_y-ry*abs(s)**(2/p):.2f}')
    return pts
def word(sw=34, xh=155, nw=144, asc=125, desc=70, dotr=24, dotgap=.75, p=2.6, rx=72, gaps=(26,34,36,34,30), n_sq=True, n_over=0):
    R=xh/2; RX=rx; top=-xh; parts=[]; x=sw/2; h=sw/2
    def S(d,cap='round'): parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="round"/>')
    if n_sq:
        arch=sq_arch(x,x+nw,-R,R+n_over,p)   # same squircle as the bowls, cut in half
        S(f'M{x} 0L'+'L'.join(arch)+f'L{x+nw} 0')
    else:
        r=nw/2; S(f'M{x} 0V{top+r}a{r} {r} 0 0 1 {nw} 0V0')
    right=x+nw+h
    cx=right+gaps[0]+h+RX; S(sqpath(cx,-R,RX,R,p)); S(f'M{cx+RX} {top-h}V{h}','butt'); right=cx+RX+h
    for g in gaps[1:3]:
        sx=right+g+h; S(f'M{sx} {top-h}V{desc}','butt'); parts.append(f'<circle cx="{sx}" cy="{desc}" r="{h}" fill="currentColor"/>')
        cx=sx+RX; S(sqpath(cx,-R,RX,R,p)); right=cx+RX+h
    lx=right+gaps[3]+h; S(f'M{lx} {-xh-asc}V0'); right=lx+h
    ix=right+gaps[4]+h; S(f'M{ix} {top}V0'); right=ix+h
    dcy=top-h-dotr-sw*dotgap; parts.append(f'<circle cx="{ix:.1f}" cy="{dcy:.1f}" r="{dotr}" fill="currentColor"/>')
    pad=8; y0=min(-xh-asc-h,dcy-dotr)-pad; y1=desc+h+pad
    return (f'{-pad:.0f} {y0:.0f} {right+2*pad:.0f} {y1-y0:.0f}',''.join(parts))
# icon with the same squircle arch (same stems, same dot, same weight)
pts=sq_arch(5.5,18.5,16.75,9.25,2.6)   # spans the original arch height (top at y≈7.5)
ICON_SQ_BODY=(f'<path d="M5.5 23L'+'L'.join(pts)+'L18.5 23" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
              '<circle cx="23.2" cy="5.6" r="2.6" style="fill:var(--dot,currentColor)"/>')
ICON_SQ=('2 -1 29 29',ICON_SQ_BODY)
out={'bplus':dict(main=word(nw=140,gaps=(24,34,36,34,30),n_sq=False),icon=ICON),
     'nsq':  dict(main=word(),icon=ICON),
     'nsq_icon': dict(main=word(),icon=ICON_SQ)}
json.dump(out,open('nmono4.json','w'))
if __name__=='__main__':
    import cairosvg
    from PIL import Image, ImageDraw, ImageFont
    F=ImageFont.truetype('/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/Inter-wght-500.ttf',24)
    S=Image.new('RGB',(1500,1060),(255,255,255)); d=ImageDraw.Draw(S)
    def tile(body,path):
        svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8"/><g transform="translate(2 2)">'+body.replace('var(--dot,currentColor)','#fff').replace('currentColor','#fff')+'</g></svg>'
        cairosvg.svg2png(bytestring=svg.encode(),write_to=path,output_width=150); return Image.open(path)
    labs={'bplus':'B+ · n en demi-cercle (le décalage)','nsq':'1 · n en squircle dans le mot, icône inchangée','nsq_icon':'2 · n en squircle dans le mot et dans l’icône'}
    for i,(k,v) in enumerate(out.items()):
        vb,body=v['main']
        cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#000")}</svg>'.encode(),write_to=f'{k}.png',output_height=230)
        im=Image.open(f'{k}.png'); Y=40+i*340
        d.text((60,Y),labs[k],font=F,fill=(110,110,110) if k=='bplus' else (0,0,0)); S.paste(im,(60,Y+50),im)
        ic=tile(v['icon'][1],f'ic_{k}.png'); S.paste(ic,(60+im.width+70,Y+90),ic)
    S.save('refine3.png')
