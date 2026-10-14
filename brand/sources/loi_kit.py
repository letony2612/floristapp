import os, shutil, zipfile, cairosvg
from PIL import Image, ImageDraw, ImageFont
from glyphs import text_path
import tige_leaf3 as t3
K='/home/user/floristapp/brand/logo-final/'; shutil.rmtree(K,ignore_errors=True)
for d in ('svg','png','icones','apercu'): os.makedirs(K+d,exist_ok=True)
SANS='bvp-light.ttf'
P=t3.P
TOP='L32,70 C32,40 46,21 70,21 C82,21 91,25 95,35 L101,32 C97,19 86,9 70,8 C40,6 17,30 17,70 Z'
l_round='M17,172 C17,190 26,200 42,200 L52,200 L52,185 L42,185 C35,185 32,181 32,172 '+TOP
d_hn,w_hn,_=text_path(SANS,'ơi',200,50,200,tracking=4)
W=50+w_hn
word=P(l_round)+P(t3.bud)+P(d_hn)                       # lơi
def T(text,size,x,y,tr,anchor='middle'):
    d,w,_=text_path(SANS,text,size,0,0,tracking=tr)
    if anchor=='middle': x-=w/2
    d,w,_=text_path(SANS,text,size,x,y,tracking=tr); return P(d),w
fleur_c,_=T('FLEUR',32,W/2+8,266,26)
fleur_h,fw=T('FLEUR',56,W+46,200,24,anchor='start')
V={'principal':(f'4 -2 {W+8:.0f} 280',word+fleur_c),
   'horizontal':(f'4 -2 {W+46+fw+12:.0f} 214',word+fleur_h),
   'mot':(f'4 -2 {W+8:.0f} 214',word)}
COL={'encre':'#1F1E1A','creme':'#EEE7DA','mousse':'#4B5138','terre':'#A35E3F'}
def svg(vb,body,c): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body.replace("currentColor",c)}</svg>'
for k,(vb,b) in V.items():
    for cn,c in COL.items():
        open(K+f'svg/loi-fleur-{k}-{cn}.svg','w').write(svg(vb,b,c)+'\n')
        cairosvg.svg2png(bytestring=svg(vb,b,c).encode(),write_to=K+f'png/loi-fleur-{k}-{cn}.png',output_width=2000)
# icons: the lơi mark centred on a coloured square (app, avatar, favicon)
x,y,w,h=map(float,V['mot'][0].split()); side=max(w,h)*1.55; ox=x-(side-w)/2; oy=y-(side-h)/2
def icon(bg,fg,rx=0): return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ox:.1f} {oy:.1f} {side:.1f} {side:.1f}">'
    f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{side:.1f}" height="{side:.1f}" rx="{rx*side:.1f}" fill="{bg}"/>{word.replace("currentColor",fg)}</svg>')
for name,bg,fg in (('mousse',COL['mousse'],COL['creme']),('creme',COL['creme'],COL['encre']),('encre',COL['encre'],COL['creme'])):
    open(K+f'icones/icone-{name}.svg','w').write(icon(bg,fg)+'\n')
    cairosvg.svg2png(bytestring=icon(bg,fg).encode(),write_to=K+f'icones/icone-{name}-1024.png',output_width=1024,output_height=1024)
for s in (512,180,32):
    cairosvg.svg2png(bytestring=icon(COL['mousse'],COL['creme'],0.2).encode(),write_to=K+f'icones/icone-mousse-arrondie-{s}.png',output_width=s,output_height=s)
open(K+'icones/favicon.svg','w').write(icon(COL['mousse'],COL['creme'],0.2)+'\n')
# overview sheet
FD=t3.FD; F=ImageFont.truetype(FD+'bvp-med.ttf',20)
S=Image.new('RGB',(1600,1100),(238,231,218)); d=ImageDraw.Draw(S)
def put(vb,b,c,h,xy,bg=None):
    cairosvg.svg2png(bytestring=svg(vb,b,c).encode(),write_to='tmp.png',output_height=h); im=Image.open('tmp.png')
    S.paste(im,xy,im); return im
put(*V['principal'],COL['encre'],420,(110,80)); d.text((110,540),'Principal',font=F,fill=(90,86,78))
S.paste(Image.new('RGB',(700,470),COL['mousse']),(800,40))
cairosvg.svg2png(bytestring=svg(*V['principal'],COL['creme']).encode(),write_to='tmp2.png',output_height=380); im=Image.open('tmp2.png')
S.paste(im,(800+(700-im.width)//2,85),im); d.text((800,520),'Sur mousse',font=F,fill=(90,86,78))
put(*V['horizontal'],COL['encre'],170,(110,640)); d.text((110,840),'Horizontal',font=F,fill=(90,86,78))
for i,n in enumerate(('mousse','creme','encre')):
    ic=Image.open(K+f'icones/icone-{n}-1024.png').resize((180,180)); S.paste(ic,(110+i*220,880)); d.rectangle((110+i*220,880,290+i*220,1060),outline=(205,196,180))
d.text((800,880),'Icônes : app, avatar, favicon',font=F,fill=(90,86,78))
S.save(K+'apercu/planche.png')
open(K+'LISEZ-MOI.txt','w').write('''LƠI FLEUR · logo final
Version : « Tige », ơ d'origine, l à pied arrondi.

svg/      logo vectoriel (à utiliser en priorité : net à toutes les tailles)
          principal  = lơi + FLEUR dessous
          horizontal = lơi + FLEUR à droite
          mot        = lơi seul
          couleurs   : encre, creme, mousse, terre
png/      les mêmes en PNG transparent, 2000 px de large
icones/   icônes carrées (app, réseaux, favicon)
          icone-*-1024.png : 1024 × 1024, coins droits (iOS les arrondit lui-même)
          icone-mousse-arrondie-*.png : 512, 180, 32 px
          favicon.svg : pour le site
apercu/   planche récapitulative

Couleurs
  Encre       #1F1E1A
  Lụa (crème) #EEE7DA
  Rêu (mousse)#4B5138
  Đất (terre) #A35E3F
  Kraft       #B7976C
  Đá (pierre) #D8CCB6
  Lá          #26301F

Polices (Google Fonts, gratuites, accents vietnamiens complets)
  Be Vietnam Pro : le mot FLEUR, textes, signalétique
  Fraunces (axe Soft 100) : titres, citations

Règles
  Ne pas retaper « lơi » dans une police : utiliser les fichiers.
  Encre sur fond clair, crème sur mousse ou fond sombre.
  Garder autour du logo un espace libre égal à la hauteur du o.
''')
z=zipfile.ZipFile('/home/user/floristapp/brand/LOI-Fleur-logo-final.zip','w',zipfile.ZIP_DEFLATED)
for r,_,fs in os.walk(K):
    for f in fs: z.write(os.path.join(r,f),'LOI-Fleur-logo-final/'+os.path.relpath(os.path.join(r,f),K))
z.close()
print(sum(len(fs) for _,_,fs in os.walk(K)),'fichiers')
