import math, cairosvg
from PIL import Image, ImageDraw, ImageFont
import tige_leaf3 as t3
FD=t3.FD; INK='#2B2A26'; BG=(227,221,209)
rot=math.radians(38)
leaf=t3.petal(t3.pcx,t3.pcy)                # default: Nét leaf resting on the o
rest=t3.P(t3.bud)+t3.P(t3.d_oi)+leaf+t3.T('FLEUR',32,t3.W6/2+8,266,26)
stem_full=t3.stem
# stem stopped above the baseline so the foot can turn out of it
stem_short=t3.stem.replace('M17,200 L17,70','M17,172 L17,70').replace('L32,70 L32,200 Z','L32,70 L32,172 Z')
# one closed outline per l (stem + arch + foot) so there is no seam at the join
TOP='L32,70 C32,40 46,21 70,21 C82,21 91,25 95,35 L101,32 C97,19 86,9 70,8 C40,6 17,30 17,70 Z'
l_flat=t3.P('M17,200 L52,200 L52,185 L32,185 '+TOP)
l_round=t3.P('M17,172 C17,190 26,200 42,200 L52,200 L52,185 L42,185 C35,185 32,181 32,172 '+TOP)
V=[('Sans pied',t3.P(stem_full)+rest),('Pied droit',l_flat+rest),('Pied arrondi',l_round+rest)]
vb=t3.vb; zvb='0 110 120 105'
for name,b in zip(('sans-pied','pied-droit','pied-arrondi'),[v[1] for v in V]):
    open(f'/home/user/floristapp/brand/logos/tige-{name}-encre.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor","#1F1E1A")}</svg>\n')
F=ImageFont.truetype(FD+'bvp-med.ttf',22)
S=Image.new('RGB',(1500,960),BG); d=ImageDraw.Draw(S)
for i,(lab,b) in enumerate(V):
    cx=i*500+250
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'f{i}.png',output_height=400)
    im=Image.open(f'f{i}.png'); S.paste(im,(cx-im.width//2,50),im)
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{zvb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'fz{i}.png',output_height=300)
    z=Image.open(f'fz{i}.png'); S.paste(z,(cx-z.width//2,580),z)
    tw=d.textlength(lab,font=F); d.text((cx-tw/2,490),lab,font=F,fill=(90,86,78))
    if i: d.line([(i*500,40),(i*500,920)],fill=(208,200,186),width=2)
S.save('/home/user/floristapp/brand/tige-pied-du-l.png')
