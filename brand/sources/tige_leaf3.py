import math, cairosvg, json
from PIL import Image, ImageDraw, ImageFont
from glyphs import text_path
SANS='bvp-light.ttf'; FD='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/'
C=json.load(open('concepts.json'))
# Nét petal, exactly: centre relative to the capital O's box, same size, same 38° tilt
O=dict(x0=11.4,x1=153.0,y0=50,y1=202); ox=123.0+46   # O starts after L (123) + tracking (46)
pcx_n=ox+82+71*math.cos(math.radians(42))+10; pcy_n=126-76*math.sin(math.radians(42))-16
fx=(pcx_n-ox-O['x0'])/(O['x1']-O['x0']); fy=(pcy_n-O['y0'])/(O['y1']-O['y0'])
# lowercase o in Tige (BVP Light, drawn at x offset 50)
o=dict(x0=50+12.4,x1=50+114.6,y0=92,y1=202)
pcx=o['x0']+fx*(o['x1']-o['x0']); pcy=o['y0']+fy*(o['y1']-o['y0'])
stem=('M17,200 L17,70 C17,30 40,6 70,8 C86,9 97,19 101,32 L95,35 C91,25 82,21 70,21 C46,21 32,40 32,70 L32,200 Z')
bud='M98,33 C109,41 112,60 101,78 C90,62 89,43 98,33 Z'
d_oi,w_oi,_=text_path(SANS,'oi',200,50,200,tracking=4); W6=50+w_oi
P=lambda d: f'<path d="{d}" fill="currentColor"/>'
def T(text,size,cx,y,tr):
    d,w,_=text_path(SANS,text,size,0,0,tracking=tr); d,w,_=text_path(SANS,text,size,cx-w/2,y,tracking=tr); return P(d)
def petal(cx,cy,k=1.0): return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{7.5*k:.2f}" ry="{17*k:.2f}" transform="rotate(38 {cx:.1f} {cy:.1f})" fill="currentColor"/>'
body=P(stem)+P(bud)+P(d_oi)+petal(pcx,pcy)+T('FLEUR',32,W6/2+8,266,26)
vb=f'4 -2 {W6+8:.0f} 280'
INK='#2B2A26'; BG=(227,221,209)
open('/home/user/floristapp/brand/logos/tige-feuille-net-encre.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#1F1E1A")}</svg>\n')
open('/home/user/floristapp/brand/logos/tige-feuille-net-creme.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor","#EEE7DA")}</svg>\n')
def png(vb,b,path,h):
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=path,output_height=h); return Image.open(path)
F=ImageFont.truetype(FD+'bvp-med.ttf',22)
S=Image.new('RGB',(1500,600),BG); d=ImageDraw.Draw(S)
# left: Nét's O as reference, middle: the new o at the same scale, right: full logo
net_vb=f'{ox-10} 20 175 195'
a=png(net_vb,C['net']['main'][1],'r1.png',360); S.paste(a,(70,70),a)
b=png(f'{50} 60 135 155',body,'r2.png',360); S.paste(b,(560-30,70),b)
c=png(vb,body,'r3.png',430); S.paste(c,(1010,40),c)
for x,t in ((250,'Nét · la référence'),(700,'Tige · même feuille'),(1250,'Le logo')):
    tw=d.textlength(t,font=F); d.text((x-tw/2,540),t,font=F,fill=(90,86,78))
S.save('/home/user/floristapp/brand/tige-feuille-net.png')
card=Image.new('RGB',(1200,760),BG); im=png(vb,body,'r4.png',430); card.paste(im,((1200-im.width)//2,(760-im.height)//2),im); card.save('/home/user/floristapp/brand/tige-feuille.png')
print(round(pcx,1),round(pcy,1),round(fx,3),round(fy,3))
