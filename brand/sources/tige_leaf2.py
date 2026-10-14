import math, cairosvg
from PIL import Image, ImageDraw, ImageFont
from glyphs import text_path
SANS='bvp-light.ttf'; FD='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/'
stem=('M17,200 L17,70 C17,30 40,6 70,8 C86,9 97,19 101,32 L95,35 C91,25 82,21 70,21 C46,21 32,40 32,70 L32,200 Z')
bud='M98,33 C109,41 112,60 101,78 C90,62 89,43 98,33 Z'
d_oi,w_oi,_=text_path(SANS,'oi',200,50,200,tracking=4)
P=lambda d: f'<path d="{d}" fill="currentColor"/>'
W6=50+w_oi
def T(text,size,cx,y,tr):
    d,w,_=text_path(SANS,text,size,0,0,tracking=tr); d,w,_=text_path(SANS,text,size,cx-w/2,y,tracking=tr); return P(d)
ocx=50+63.5; ocy=147; orx=51.1; ory=55; a=math.radians(42); s=0.8
rx,ry=7.5*s,17*s
ex,ey=ocx+orx*math.cos(a), ocy-ory*math.sin(a)      # point on the o's outer edge
def leaf(cx,cy,rot): return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({rot} {cx:.1f} {cy:.1f})" fill="currentColor"/>'
def along(rot,dist):  # move from the edge point along the leaf's long axis
    r=math.radians(rot); return ex+math.sin(r)*dist, ey-math.cos(r)*dist
V={
 'detachee': leaf(ocx+orx*math.cos(a)+17*s, ocy-ory*math.sin(a)-27*s, 38),
 'posee':    leaf(*along(38,ry+1.5),38),
 'pousse':   leaf(*along(46,ry*0.55),46),
}
def body(k): return P(stem)+P(bud)+P(d_oi)+V[k]+T('FLEUR',32,W6/2+8,266,26)
vb=f'4 -2 {W6+8:.0f} 280'
INK='#2B2A26'; BG=(227,221,209)
labels={'detachee':'Détachée','posee':'Posée','pousse':'Qui pousse'}
F=ImageFont.truetype(FD+'bvp-med.ttf',22)
sheet=Image.new('RGB',(1500,620),BG); d=ImageDraw.Draw(sheet)
for i,k in enumerate(V):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body(k).replace("currentColor",INK)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'tl_{k}.png',output_height=420)
    im=Image.open(f'tl_{k}.png'); x=i*500+(500-im.width)//2; sheet.paste(im,(x,60),im)
    tw=d.textlength(labels[k],font=F); d.text((i*500+250-tw/2,535),labels[k],font=F,fill=(90,86,78))
    open(f'/home/user/floristapp/brand/logos/tige-feuille-{k}-encre.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body(k).replace("currentColor","#1F1E1A")}</svg>\n')
sheet.save('/home/user/floristapp/brand/tige-feuille-3-placements.png')
# close-up of the o for each placement
zoom=Image.new('RGB',(1500,420),BG)
for i,k in enumerate(V):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 60 150 150">{body(k).replace("currentColor",INK)}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'tz_{k}.png',output_height=380)
    im=Image.open(f'tz_{k}.png'); zoom.paste(im,(i*500+(500-im.width)//2,20),im)
zoom.save('/home/user/floristapp/brand/tige-feuille-3-placements-zoom.png')
