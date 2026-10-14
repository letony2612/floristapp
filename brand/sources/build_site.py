import json, os, shutil, sys, io, cairosvg
from PIL import Image
from build_page import z
C=json.load(open('concepts.json'))
ROOT='/home/user/floristapp/site'
os.makedirs(ROOT+'/mockups',exist_ok=True)
for f in os.listdir('/home/user/floristapp/brand/mockups'):
    shutil.copy('/home/user/floristapp/brand/mockups/'+f, ROOT+'/mockups/'+f)
MOSS='#4B5138'; CREAM='#EEE7DA'
# favicon: arch monogram, cream on moss
vb,body=C['arche']['main']; x,y,w,h=map(float,vb.split())
# keep only the arch + letter (drop the LƠI FLEUR line under it) by cropping the viewBox to the arch
fav_vb=f'{x} {y} {w} 276'
side=max(w,276)+40
fav=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x-(side-w)/2} {y-(side-276)/2} {side} {side}">'
     f'<rect x="{x-(side-w)/2}" y="{y-(side-276)/2}" width="{side}" height="{side}" rx="{side*.18}" fill="{MOSS}"/>'
     f'<g color="{CREAM}">{body.replace("currentColor",CREAM)}</g></svg>')
# hide the text line by clipping to arch height
fav=fav.replace('<g color',f'<clipPath id="c"><rect x="{x}" y="{y}" width="{w}" height="276"/></clipPath><g clip-path="url(#c)" color')
open(ROOT+'/favicon.svg','w').write(fav)
cairosvg.svg2png(bytestring=fav.encode(),write_to=ROOT+'/apple-touch-icon.png',output_width=180,output_height=180)
# share preview 1200x630: primary logo cream on moss + tagline
vb,body=C['buong']['main']; x,y,w,h=map(float,vb.split())
logo_png=cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="560" height="{int(560*h/w)}">{body.replace("currentColor",CREAM)}</svg>'.encode())
og=Image.new('RGB',(1200,630),MOSS); lg=Image.open(io.BytesIO(logo_png))
og.paste(lg,((1200-lg.width)//2,(630-lg.height)//2-10),lg)
og.save(ROOT+'/apercu.jpg',quality=88)
domain=(sys.argv[1] if len(sys.argv)>1 else '').rstrip('/')
img_url=(domain+'/apercu.jpg') if domain else 'apercu.jpg'
page=open('/home/user/floristapp/brand/charte.html').read()
title_end=page.index('</title>')+len('</title>')
head_extra=f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Proposition d’identité visuelle pour LƠI Fleur : six pistes de logo, mockups, couleurs et typographie.">
<meta property="og:title" content="LƠI Fleur · Identité visuelle">
<meta property="og:description" content="Six pistes de logo à découvrir en situation.">
<meta property="og:type" content="website">
<meta property="og:image" content="{img_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">'''
head=page[:title_end].replace('<meta name="claude:viewport-fit-sides" content="cover">','')
rest=page[title_end:]
# split head-level tags (links + style) from body content at the hidden SVG sprite
cut=rest.index('<svg width="0" height="0"')
doc=(f'<!doctype html>\n<html lang="fr">\n<head>\n{head_extra}\n{head}\n{rest[:cut]}\n'
     f'<style>html{{-webkit-text-size-adjust:100%}}img{{max-width:100%}}</style>\n</head>\n<body>\n{rest[cut:]}\n</body>\n</html>\n')
open(ROOT+'/index.html','w').write(doc)
open(ROOT+'/robots.txt','w').write('User-agent: *\nDisallow: /\n')
print('ok', len(doc), 'og:image =', img_url)
