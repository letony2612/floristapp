import json
from glyphs import text_path
C=json.load(open('nconcepts.json'))
def z(vb): x,y,w,h=vb.split(); return f'0 0 {w} {h}'
META=[('pastille','Pastille','Notification','Le point du i devient la pastille rouge d’une notification : quelque chose arrive. Le prolongement direct de votre n·.'),
('ecran','Écran','Mobile','L’arche du n dessine le haut d’un téléphone, avec sa Dynamic Island. Le mobile se lit dans la première lettre.'),
('esquisse','Esquisse','De l’idée au réel','Le premier p est un tracé, le second est plein : de l’idée au produit, raconté dans le mot lui-même.'),
('reperes','Repères','Précision','Les lignes de construction restent visibles, avec la cote du rayon. Le logo d’un studio qui dessine au pixel près.'),
('signe','Signé','Humain','Inter pour le sérieux, une signature manuscrite pour la personne : « Fait avec soin », un seul interlocuteur.'),
('curseur','Curseur','Code','Le i devient le curseur qui clignote : on écrit, on code, on lance. Il s’anime tout seul sur le site.')]
SHOTS=[('icone','Icône d’app','écran d’accueil iOS'),('appli','Écran d’ouverture','application mobile'),('site','Site web','nappli.fr, en-tête'),('reseaux','Instagram','profil et publications'),
       ('carte','Cartes de visite','recto et verso'),('devis','Devis','document client'),('ordinateur','Sur votre bureau','le site sur un portable'),('porte','Porte du studio','verre cannelé, vitrophanie')]
# blinking caret inside the page only
sym=''
for k,v in C.items():
    for n in ('main','icon'):
        body=v[n][1].replace('class="caret"','class="caret" style="animation:nblink 1.1s steps(1) infinite"').replace('class="caret" style="animation:nblink 1.1s steps(1) infinite" x=','class="caret" x=') if False else v[n][1]
        if k=='curseur': body=body.replace('<rect class="caret"','<rect class="caret" style="fill:var(--stamp,#2A44D8);animation:nblink 1.1s steps(1) infinite"').replace(' style="fill:var(--stamp,#2A44D8)"/>','/>')
        sym+=f'<symbol id="{n}-{k}" viewBox="{v[n][0]}">{body}</symbol>'
# current logo, rebuilt in Inter SemiBold for comparison
d,w,b=text_path('Inter-wght-600.ttf','nappli',200,0,200,tracking=-5)
sym+=f'<symbol id="cur-word" viewBox="-6 40 {w+12:.0f} 206"><path d="{d}"/></symbol>'
cur_icon=open('ncur_icon.svg').read().replace('<svg ','<svg style="width:100%;height:100%;display:block" ')
cards=''.join(f'''<button class="logo-card" type="button" data-k="{k}" aria-pressed="false"><div class="art"><svg class="word" viewBox="{z(C[k]['main'][0])}" role="img" aria-label="Piste {n}"><use href="#main-{k}"/></svg><span class="tile"><svg viewBox="{z(C[k]['icon'][0])}" aria-hidden="true"><use href="#icon-{k}"/></svg></span></div>
<div class="txt"><div class="row"><h3>{i+1:02d} · {n}</h3><span class="style">{st}</span></div><p>{desc}</p><span class="pick">Choisir cette piste</span></div></button>''' for i,(k,n,st,desc) in enumerate(META))
chips=''.join(f'<button class="chip" type="button" data-k="{k}" aria-pressed="false"><span class="t"><svg viewBox="{z(C[k]["icon"][0])}" aria-hidden="true"><use href="#icon-{k}"/></svg></span>{n}</button>' for k,n,*_ in META)
figs=''.join(f'<figure><img id="mk-{s}" src="mockups/pastille-{s}.jpg" width="919" height="1149" alt="{t} : {c}"><figcaption><b>{t}</b><span>{c}</span></figcaption></figure>' for s,t,c in SHOTS)
SW=[('Encre','#000000','logo, titres, boutons'),('Papier','#FFFFFF','fond principal'),('Gris texte','#5C5C5C','texte secondaire'),('Trait','#ECECEC','séparateurs'),
    ('Pastille','#FF3B30','accent · piste Pastille'),('Tampon','#2A44D8','accent · Signé, Curseur'),('Guide','#8F9BFF','accent · Esquisse, Repères'),('Nuit','#0C3A44','fonds sombres, rare')]
sw=''.join(f'<div class="sw"><div class="c" style="background:{h};{"border-bottom:1px solid #ECECEC" if h=="#FFFFFF" else ""}"></div><div class="t"><b>{n}</b><code>{h}</code><i>{u}</i></div></div>' for n,h,u in SW)
t=open('nappli_tpl.html').read()
t=(t.replace('%%SYMBOLS%%',sym).replace('%%CARDS%%',cards).replace('%%CHIPS%%',chips).replace('%%FIGS%%',figs).replace('%%SWATCHES%%',sw)
   .replace('%%CUR_ICON%%',cur_icon).replace('%%VB_CURRENT%%',f'0 0 {w+12:.0f} 206').replace('%%VB0%%',z(C['pastille']['main'][0]))
   .replace('%%NAMES%%',json.dumps({k:n for k,n,*_ in META},ensure_ascii=False)).replace('%%VBS%%',json.dumps({k:z(v['main'][0]) for k,v in C.items()}))
   .replace('%%SHOTS%%',json.dumps([s for s,*_ in SHOTS])))
open('/home/user/floristapp/nappli/charte.html','w').write(t); print(len(t))
