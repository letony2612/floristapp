"""Monoline 'nappli' built from the same rules as the existing n· icon:
stroke weight = 20 % of the n's width, round caps, arches are true half-circles,
the dot is a full circle twice the stroke weight."""
import json
ICON_BODY=('<path d="M5.5 23V14a6.5 6.5 0 0 1 13 0v9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>'
           '<circle cx="23.2" cy="5.6" r="2.6" style="fill:var(--dot,currentColor)"/>')
ICON=('2 -1 29 29',ICON_BODY)
def word(sw=26, gap=50, dot='above', xh=155, nw=130, asc=100, desc=95, bowl=None, dotcol=False, rx=None):
    """Return (viewBox, svg body). Coordinates are stroke centres; baseline y=0."""
    r=nw/2; R=bowl or xh/2; RX=rx or R   # n arch radius, bowl radii
    top=-xh; parts=[]; x=sw/2       # x = current left stroke centre
    def S(d): parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    edge=lambda c: c+sw/2           # right edge of a stroke centred at c
    # n
    S(f'M{x} 0V{top+r}a{r} {r} 0 0 1 {nw} 0V0'); right=edge(x+nw)
    # a : circle + right stem
    cx=right+gap+sw/2+RX; S(f'M{cx-RX} {-R}a{RX} {R} 0 1 0 {2*RX} 0a{RX} {R} 0 1 0 {-2*RX} 0'); S(f'M{cx+RX} {top}V0'); right=edge(cx+RX)
    # p, p : stem + circle
    for _ in range(2):
        sx=right+gap+sw/2; S(f'M{sx} {top}V{desc}'); cx=sx+RX; S(f'M{sx} {-R}a{RX} {R} 0 1 1 {2*RX} 0a{RX} {R} 0 1 1 {-2*RX} 0'); right=edge(cx+RX)
    # l
    lx=right+gap+sw/2; S(f'M{lx} {-xh-asc}V0'); right=edge(lx)
    # i
    ix=right+gap+sw/2; S(f'M{ix} {top}V0'); right=edge(ix)
    dr=sw                            # dot radius = stroke weight (icon: r 2.6, stroke 2.6)
    fill='style="fill:var(--dot,currentColor)"' if dotcol else 'fill="currentColor"'
    if dot=='above': dcx,dcy=ix,top-sw/2-dr-sw*0.9
    else:            dcx,dcy=ix+sw/2+dr*1.15+sw*0.55,top-dr*0.25   # top-right, like the icon
    parts.append(f'<circle cx="{dcx:.1f}" cy="{dcy:.1f}" r="{dr}" {fill}/>'); right=max(right,dcx+dr)
    pad=8; y0=min(-xh-asc-sw/2,dcy-dr)-pad; y1=desc+sw/2+pad
    return (f'{-pad:.0f} {y0:.0f} {right+2*pad:.0f} {y1-y0:.0f}',''.join(parts))
out={
 'fidele': dict(main=word(26,48,'above'), icon=ICON),   # same weight/height ratio as the n· icon
 'leger':  dict(main=word(20,52,'above'), icon=ICON),
 'appuye': dict(main=word(34,44,'above'), icon=ICON),
 'serre':  dict(main=word(30,30,'above'), icon=ICON),
}
json.dump(out,open('nmono.json','w'))
if __name__=='__main__':
    import cairosvg
    from PIL import Image
    S=Image.new('RGB',(1500,900),(255,255,255))
    cur=Image.open('n-pastille-main.png')  # only for size reference below
    for i,(k,v) in enumerate(out.items()):
        vb,body=v['main']
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("var(--dot,currentColor)","#000").replace("currentColor","#000")}</svg>'
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'nm-{k}.png',output_width=560)
        im=Image.open(f'nm-{k}.png'); S.paste(im,((i%2)*750+60,(i//2)*420+60),im)
    ic=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8"/><g transform="translate(2 2)" color="#fff">{ICON_BODY.replace("var(--dot,currentColor)","#fff").replace("currentColor","#fff")}</g></svg>'
    cairosvg.svg2png(bytestring=ic.encode(),write_to='nm-icon.png',output_width=110)
    im=Image.open('nm-icon.png'); S.paste(im,(1380,20),im)
    S.save('nmsheet.png')
