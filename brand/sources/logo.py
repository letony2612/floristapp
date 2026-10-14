from glyphs import text_path
INK='#1F1E1A'
def wordmark(size=200, track=34):
    # LOI drawn from Fraunces Soft Light; the Ơ horn is replaced by a drooping leaf.
    d,w,b=text_path('fr-soft.ttf','LOI',size,0,size,tracking=track)
    return d,w,b
def horn(size=200, track=34):
    s=size/200
    # O spans approx: L adv 103 + track
    ox=103.2*s+track
    cx=ox+70.5*s; cy=size-69.8*s; rx=64.3*s; ry=72*s
    import math
    a=math.radians(38)
    sx=cx+rx*math.cos(a); sy=cy-ry*math.sin(a)
    # stem: rises out of the bowl, bends over, lets a leaf hang loose
    tx=sx+30*s; ty=sy-40*s
    # tapered filled stem: wide where it leaves the bowl, fine at the tip
    w0=4.6*s; w1=1.6*s
    stem=(f'M{sx-6*s-w0:.1f},{sy+6*s:.1f} C{sx+4*s-w0:.1f},{sy-16*s:.1f} {sx+16*s-w1:.1f},{sy-34*s-w1:.1f} {tx-w1*0.4:.1f},{ty-w1:.1f} '
          f'L{tx+w1*0.4:.1f},{ty+w1:.1f} C{sx+18*s+w1:.1f},{sy-30*s+w1:.1f} {sx+8*s+w0:.1f},{sy-14*s:.1f} {sx-6*s+w0:.1f},{sy+8*s:.1f} Z')
    # leaf hangs from tip, slightly swaying
    lx,ly=tx,ty
    leaf=(f'M{lx:.1f},{ly:.1f} C{lx+14*s:.1f},{ly+6*s:.1f} {lx+17*s:.1f},{ly+26*s:.1f} {lx+9*s:.1f},{ly+44*s:.1f} '
          f'C{lx-1*s:.1f},{ly+30*s:.1f} {lx-4*s:.1f},{ly+12*s:.1f} {lx:.1f},{ly:.1f} Z')
    vein=f'M{lx+1*s:.1f},{ly+3*s:.1f} C{lx+7*s:.1f},{ly+16*s:.1f} {lx+9*s:.1f},{ly+28*s:.1f} {lx+9*s:.1f},{ly+40*s:.1f}'
    return stem,leaf,vein,s
def svg_primary(color=INK, fleur=True, pad=24):
    size=200; track=34
    d,w,b=wordmark(size,track)
    stem,leaf,vein,s=horn(size,track)
    parts=[f'<path d="{d}" fill="{color}"/>',
           f'<path d="{stem}" fill="{color}"/>',
           f'<path d="{leaf}" fill="{color}"/>']
    H=size+20
    if fleur:
        fd,fw,fb=text_path('bvp-light.ttf','FLEUR',30,0,0,tracking=24)
        fx=(w-fw)/2; fy=size+70
        fd,fw,fb=text_path('bvp-light.ttf','FLEUR',30,fx,fy,tracking=24)
        parts.append(f'<path d="{fd}" fill="{color}"/>')
        H=fy+10
    vb=f'{-pad} {-pad+20} {w+2*pad:.0f} {H+2*pad-20:.0f}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="LƠI Fleur">'+''.join(parts)+'</svg>'
if __name__=='__main__':
    open('primary.svg','w').write(svg_primary())
    open('test.html','w').write('<body style="margin:0;background:#EEE7DA"><img src="primary.svg" style="width:900px;margin:40px">')
