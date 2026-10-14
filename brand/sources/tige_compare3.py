import cairosvg, json
from PIL import Image, ImageDraw, ImageFont
import tige_leaf4 as t4
C=json.load(open('concepts.json'))
FD=t4.FD; INK='#2B2A26'; BG=(227,221,209)
# all three share the same coordinate system, so one viewBox keeps them on the same baseline and scale
V=[('Tige d’origine · crochet du ơ',C['tige']['main'][1]),('Par défaut · feuille posée',t4.V['defaut']),('Feuille décollée',t4.V['decollee'])]
vb=t4.vb; zvb='95 70 95 95'
F=ImageFont.truetype(FD+'bvp-med.ttf',22)
S=Image.new('RGB',(1500,1000),BG); d=ImageDraw.Draw(S)
for i,(lab,b) in enumerate(V):
    cx=i*500+250
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'k{i}.png',output_height=400)
    im=Image.open(f'k{i}.png'); S.paste(im,(cx-im.width//2,50),im)
    cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{zvb}">{b.replace("currentColor",INK)}</svg>'.encode(),write_to=f'kz{i}.png',output_height=330)
    z=Image.open(f'kz{i}.png'); S.paste(z,(cx-z.width//2,560),z)
    tw=d.textlength(lab,font=F); d.text((cx-tw/2,490),lab,font=F,fill=(90,86,78))
    if i: d.line([(i*500,40),(i*500,960)],fill=(208,200,186),width=2)
S.save('/home/user/floristapp/brand/tige-3-versions.png')
