import json, math, cairosvg
from glyphs import text_path
from PIL import Image
SANS='bvp-light.ttf'
C=json.load(open('concepts.json'))
# Tige, rebuilt: plain "oi" (no horn) + the Nét petal placed where the horn sat
stem=('M17,200 L17,70 C17,30 40,6 70,8 C86,9 97,19 101,32 '
      'L95,35 C91,25 82,21 70,21 C46,21 32,40 32,70 L32,200 Z')
bud='M98,33 C109,41 112,60 101,78 C90,62 89,43 98,33 Z'
d_oi,w_oi,_=text_path(SANS,'oi',200,50,200,tracking=4)
d_hn,_,_=text_path(SANS,'ơi',200,50,200,tracking=4)
# o centre and radii (BVP Light lowercase o: x 12.4–114.6, y 92–202), shifted by the 50 offset
ocx=50+63.5; ocy=147; orx=51; ory=55; a=math.radians(42)
s=0.8                                   # lowercase o is smaller than Nét's capital O
pcx=ocx+orx*math.cos(a)+17*s; pcy=ocy-ory*math.sin(a)-27*s
petal=f'<ellipse cx="{pcx:.1f}" cy="{pcy:.1f}" rx="{7.5*s:.1f}" ry="{17*s:.1f}" transform="rotate(38 {pcx:.1f} {pcy:.1f})" fill="currentColor"/>'
P=lambda d: f'<path d="{d}" fill="currentColor"/>'
W6=50+w_oi
def T(text,size,cx,y,tr):
    d,w,_=text_path(SANS,text,size,0,0,tracking=tr); d,w,_=text_path(SANS,text,size,cx-w/2,y,tracking=tr); return P(d)
main_body=P(stem)+P(bud)+P(d_oi)+petal+T('FLEUR',32,W6/2+8,266,26)
main=(f'4 -2 {W6+8:.0f} 280',main_body)
before=(C['tige']['main'][0],C['tige']['main'][1])
json.dump({'main':main,'line':None},open('tige_leaf.json','w'))
INK='#2B2A26'; BG=(227,221,209)
def png(vb,body,path,h=360):
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor",INK)}</svg>'.encode(),write_to=path,output_height=h)
    return Image.open(path)
out='/home/user/floristapp/brand/logos/'
open(out+'tige-feuille-principal-encre.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{main[0]}">{main_body.replace("currentColor","#1F1E1A")}</svg>\n')
open(out+'tige-feuille-principal-creme.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{main[0]}">{main_body.replace("currentColor","#EEE7DA")}</svg>\n')
# single card, like the screenshot
card=Image.new('RGB',(1200,760),BG); im=png(*main,'tl.png',h=430); card.paste(im,((1200-im.width)//2,(760-im.height)//2),im)
card.save('/home/user/floristapp/brand/tige-feuille.png')
# before / after, close-up on the o
cmp=Image.new('RGB',(1200,560),BG)
for i,(vb,body) in enumerate((before,main)):
    im=png(vb,body,f'c{i}.png',h=420); cmp.paste(im,(i*600+(600-im.width)//2,70),im)
cmp.save('/home/user/floristapp/brand/tige-feuille-avant-apres.png')
print(main[0])
