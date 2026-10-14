import json
from glyphs import text_path
C=json.load(open('nmono.json'))
def z(vb): x,y,w,h=vb.split(); return f'0 0 {w} {h}'
META=[('fidele','Fidèle','Trait du n·','Exactement le rapport épaisseur/hauteur de votre icône : le mot et le n· se superposent sans écart.'),
('leger','Léger','Plus fin','Un trait plus fin et plus d’air entre les lettres. Élégant en grand, plus fragile en très petit.'),
('appuye','Appuyé','Plus présent','Un trait plus épais, proche du poids de votre logo actuel. Tient très bien en petit et sur photo.'),
('serre','Serré','Compact','Le poids d’Appuyé avec moins d’espace entre les lettres : un mot dense, qui se lit d’un bloc.')]
SHOTS=[('icone','Icône d’app','écran d’accueil iOS'),('appli','Écran d’ouverture','application mobile'),('site','Site web','nappli.fr, en-tête'),('reseaux','Instagram','profil et publications'),
       ('carte','Cartes de visite','recto et verso'),('devis','Devis','document client'),('ordinateur','Sur votre bureau','le site sur un portable'),('porte','Porte du studio','verre cannelé, vitrophanie')]
sym=''.join(f'<symbol id="{n}-{k}" viewBox="{v[n][0]}">{v[n][1]}</symbol>' for k,v in C.items() for n in ('main','icon'))
# current logo, rebuilt in Inter SemiBold for comparison
d,w,b=text_path('Inter-wght-600.ttf','nappli',200,0,200,tracking=-5)
sym+=f'<symbol id="cur-word" viewBox="-6 40 {w+12:.0f} 206"><path d="{d}"/></symbol>'
cur_icon=open('ncur_icon.svg').read().replace('<svg ','<svg style="width:100%;height:100%;display:block" ')
# construction diagram: the Fidèle word over its guides, with the icon's n drawn at the same scale
vb,body=C['fidele']['main']; x0,y0,w0,h0=map(float,vb.split())
G='stroke="#8F9BFF" stroke-width="2"'
lines=''.join(f'<line x1="{x0-60}" y1="{y}" x2="{x0+w0+60}" y2="{y}" {G}/>' for y in (0,-155,-255,95))
lab=''.join(f'<text x="{x0+w0+66}" y="{y+6}" font-family="Inter" font-size="18" fill="#8F9BFF">{t}</text>' for y,t in ((0,'ligne de base'),(-155,'hauteur du n'),(-255,'hampe'),(95,'jambage')))
circ=f'<circle cx="78" cy="-90" r="65" fill="none" stroke="#8F9BFF" stroke-width="2" stroke-dasharray="6 8"/>'
build=f'<svg viewBox="{x0-70} {y0-10} {w0+240} {h0+20}" role="img" aria-label="Construction du mot nappli sur ses lignes de repère">{lines}{circ}<g color="#000">{body.replace("var(--dot,currentColor)","#000")}</g>{lab}</svg>'
cards=''.join(f'''<button class="logo-card" type="button" data-k="{k}" aria-pressed="false"><div class="art"><svg class="word" viewBox="{z(C[k]['main'][0])}" role="img" aria-label="Réglage {n}"><use href="#main-{k}"/></svg><span class="tile"><svg viewBox="{z(C[k]['icon'][0])}" aria-hidden="true"><use href="#icon-{k}"/></svg></span></div>
<div class="txt"><div class="row"><h3>{n}</h3><span class="style">{st}</span></div><p>{desc}</p><span class="pick">Choisir ce réglage</span></div></button>''' for i,(k,n,st,desc) in enumerate(META))
chips=''.join(f'<button class="chip" type="button" data-k="{k}" aria-pressed="false"><span class="t"><svg viewBox="{z(C[k]["icon"][0])}" aria-hidden="true"><use href="#icon-{k}"/></svg></span>{n}</button>' for k,n,*_ in META)
figs=''.join(f'<figure><img id="mk-{s}" src="mockups/fidele-{s}.jpg" width="919" height="1149" alt="{t} : {c}"><figcaption><b>{t}</b><span>{c}</span></figcaption></figure>' for s,t,c in SHOTS)
SW=[('Encre','#000000','logo, titres, boutons'),('Papier','#FFFFFF','fond, logo inversé'),('Gris texte','#5C5C5C','texte secondaire'),('Trait','#ECECEC','séparateurs'),
    ('Tampon','#2A44D8','liens, signature'),('Notification','#FF3B30','pastilles de l’interface'),('Guide','#8F9BFF','repères, maquettes'),('Nuit','#0C3A44','fonds sombres, rare')]
sw=''.join(f'<div class="sw"><div class="c" style="background:{h};{"border-bottom:1px solid #ECECEC" if h=="#FFFFFF" else ""}"></div><div class="t"><b>{n}</b><code>{h}</code><i>{u}</i></div></div>' for n,h,u in SW)
t=open('nappli_tpl2.html').read()
t=(t.replace('%%SYMBOLS%%',sym).replace('%%CARDS%%',cards).replace('%%CHIPS%%',chips).replace('%%FIGS%%',figs).replace('%%SWATCHES%%',sw)
   .replace('%%CUR_ICON%%',cur_icon).replace('%%VB_CURRENT%%',f'0 0 {w+12:.0f} 206').replace('%%VB0%%',z(C['fidele']['main'][0])).replace('%%BUILD%%',build)
   .replace('%%NAMES%%',json.dumps({k:n for k,n,*_ in META},ensure_ascii=False)).replace('%%VBS%%',json.dumps({k:z(v['main'][0]) for k,v in C.items()}))
   .replace('%%SHOTS%%',json.dumps([s for s,*_ in SHOTS])))
open('/home/user/floristapp/nappli/charte.html','w').write(t); print(len(t))
