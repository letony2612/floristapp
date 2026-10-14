import math, cairosvg
from PIL import Image, ImageDraw, ImageFont
import tige_leaf3 as t3
FD=t3.FD; INK='#2B2A26'; BG=(227,221,209)
rot=math.radians(38)
def body_at(gap):
    # move the petal outward along its own long axis by `gap` units
    cx=t3.pcx+math.sin(rot)*gap; cy=t3.pcy-math.cos(rot)*gap
    return t3.P(t3.stem)+t3.P(t3.bud)+t3.P(t3.d_oi)+t3.petal(cx,cy)+t3.T('FLEUR',32,t3.W6/2+8,266,26)
V={'defaut':body_at(0),'decollee':body_at(9)}
vb=t3.vb
for k,b in V.items():
    for cn,c in (('encre','#1F1E1A'),('creme','#EEE7DA')):
        open(f'/home/user/floristapp/brand/logos/tige-{k}-{cn}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor",c)}</svg>\n')
F=ImageFont.truetype(FD+'bvp-med.ttf',22)
S=Image.new('RGB',(1400,1000),BG); d=ImageDraw.Draw(S)
labels={'defaut':'Par défaut · feuille posée','decollee':'Feuille décollée'}
for i,(k,b) in enumerate(V.items()):
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'v_{k}.png',output_height=430)
    im=Image.open(f'v_{k}.png'); S.paste(im,(i*700+(700-im.width)//2,50),im)
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="95 70 95 95">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'z_{k}.png',output_height=330)
    z=Image.open(f'z_{k}.png'); S.paste(z,(i*700+(700-z.width)//2,560),z)
    tw=d.textlength(labels[k],font=F); d.text((i*700+350-tw/2,510),labels[k],font=F,fill=(90,86,78))
S.save('/home/user/floristapp/brand/tige-defaut-et-decollee.png')
