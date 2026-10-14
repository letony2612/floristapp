import json
from build_page import META, z   # reuse names and copy
C=json.load(open('concepts.json'))
FD='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/'
MK='/home/user/floristapp/brand/mockups/'
def logo(k,kind='main',cls=''):
    return f'<svg class="{cls}" viewBox="{z(C[k][kind][0])}"><use href="#{"m" if kind=="main" else "l"}-{k}"/></svg>'
sym=''.join(f'<symbol id="m-{k}" viewBox="{v["main"][0]}">{v["main"][1]}</symbol><symbol id="l-{k}" viewBox="{v["line"][0]}">{v["line"][1]}</symbol>' for k,v in C.items())
TOTAL=7+len(META)
def foot(n,label):
    return f'<div class="foot"><span>LƠI Fleur · {label}</span><span>{n:02d} / {TOTAL:02d}</span></div>'
pages=[]
# 1 cover
pages.append(f'''<section class="pg cover">
  <div class="eyebrow light">Identité visuelle · proposition</div>
  <div class="dict"><p class="word">lơi</p><p class="pron">[ləːj] · <i>adjectif, vietnamien</i></p><p class="def">Souple, ondulant, flottant : ce qui bouge librement, sans être retenu.</p></div>
  <div class="cover-bottom">
    <p class="quote">Vẻ đẹp là sự tự do cảm xúc,<br>vẻ đẹp là không khuôn khổ.</p>
    <p class="fr">La beauté est la liberté des émotions.<br>La beauté n’a pas de cadre.</p>
  </div></section>''')
# 2 esprit
pages.append(f'''<section class="pg">
  <div class="grid2">
   <div><div class="eyebrow">01 · L’esprit</div><h1>Lơi : ce qui bouge librement, sans être retenu.</h1>
   <p class="lead">En vietnamien, <i>lơi</i> décrit la souplesse d’un geste qu’on ne force pas : une tige qui ploie, un ruban qui flotte, un bouquet qui n’est pas serré. Toute l’identité part de là : des formes qui se relâchent, beaucoup d’air autour, des matières naturelles.</p>
   <div class="vi">
     <div><b>Lả lơi</b><span>Langoureux, charmeur, parfois séducteur.</span></div>
     <div><b>Buông lơi</b><span>Relâché, flottant, qui se balance librement.</span></div>
     <div><b>Buông lơ</b><span>Négligemment relâché, sans tension.</span></div>
   </div></div>
   <dl class="gloss">
     <div><dt>Souple et fluide</dt><dd>Un mouvement naturel, doux, sans rigidité.</dd></div>
     <div><dt>Ondulant</dt><dd>Ce qui se balance ou ondule délicatement.</dd></div>
     <div><dt>Languissant</dt><dd>Une attitude douce, nonchalante, parfois sensuelle.</dd></div>
     <div><dt>Nonchalant</dt><dd>Détendu, sans contrainte ni effort apparent.</dd></div>
     <div><dt>Flottant</dt><dd>Qui bouge librement, légèrement, au gré du vent.</dd></div>
     <div><dt>Avec grâce</dt><dd>L’élégance d’un mouvement spontané.</dd></div>
   </dl></div>{foot(2,"L’esprit")}</section>''')
# 3 overview
cells=''.join(f'<div class="ov"><div class="ovart">{logo(k)}</div><div class="ovtxt"><b>{i+1:02d} · {n}</b><span>{st}</span></div></div>' for i,(k,n,st,d,r) in enumerate(META))
pages.append(f'''<section class="pg"><div class="head"><div class="eyebrow">02 · Les pistes</div><h1>Six manières de dire « lơi ».</h1>
<p class="lead narrow">Le fil commun : le crochet du <span class="serif">Ơ</span> vietnamien devient une feuille, un pétale ou une tige.</p></div>
<div class="ovgrid">{cells}</div>{foot(3,"Les pistes")}</section>''')
# 4.. one page per concept
for i,(k,n,st,d,r) in enumerate(META):
    n_pg=4+i
    mocks=''.join(f'<figure><img src="file://{MK}{k}-{s}.jpg"><figcaption>{cap}</figcaption></figure>' for s,cap in [('boite','Boîte cadeau kraft'),('devanture','Devanture'),('sac','Sac en papier'),('ecran','Site web'),('appli','Appli · icône'),('appli-ecrans','Appli · écrans')])
    pages.append(f'''<section class="pg concept">
  <div class="cleft">
    <div class="eyebrow">Piste {i+1:02d} · {st}</div>
    <h1>{n}{' <span class="reco">Notre recommandation</span>' if r else ''}</h1>
    <p class="lead">{d}</p>
    <div class="hero">{logo(k)}</div>
    <div class="vars">
      <div style="background:var(--reu);color:var(--lua)">{logo(k)}</div>
      <div style="background:var(--kraft);color:var(--muc)">{logo(k)}</div>
      <div style="background:var(--muc);color:var(--lua)">{logo(k)}</div>
    </div>
    <div class="hline">{logo(k,'line')}</div>
  </div>
  <div class="mocks">{mocks}</div>
  {foot(n_pg,"Piste "+n)}</section>''')
# colours
SW=[('Lụa','crème soie','#EEE7DA','238 231 218','5 7 14 0',45),('Đá','pierre','#D8CCB6','216 204 182','15 17 28 0',18),('Rêu','mousse','#4B5138','75 81 56','62 45 78 40',14),
    ('Kraft','papier','#B7976C','183 151 108','29 40 63 5',10),('Mực','encre','#1F1E1A','31 30 26','68 64 68 78',8),('Lá','feuillage','#26301F','38 48 31','72 52 82 66',3),('Đất','terre cuite','#A35E3F','163 94 63','25 66 78 15',2)]
sw=''.join(f'<div class="sw"><div class="c" style="background:{h}"></div><b>{nm}</b><i>{dsc}</i><code>{h}<br>RVB {rv}<br>CMJN {cm}</code></div>' for nm,dsc,h,rv,cm,p in SW)
ratio=''.join(f'<span style="flex:{p};background:{h}"></span>' for nm,dsc,h,rv,cm,p in SW)
leg=''.join(f'<span>{nm} {p} %</span>' for nm,dsc,h,rv,cm,p in SW)
n0=4+len(META)
pages.append(f'''<section class="pg"><div class="head"><div class="eyebrow">03 · Couleurs</div><h1>Une palette de matières : soie, pierre, papier, mousse.</h1>
<p class="lead narrow">Les fleurs apportent la couleur vive ; la marque reste en retrait pour les laisser parler.</p></div>
<div class="swatches">{sw}</div><div class="ratio">{ratio}</div><div class="legend"><span>Proportions conseillées</span>{leg}</div>
<p class="note">Valeurs CMJN indicatives, à valider sur épreuve d’imprimeur.</p>{foot(n0,"Couleurs")}</section>''')
# type
pages.append(f'''<section class="pg"><div class="head"><div class="eyebrow">04 · Typographie</div><h1>Une serif douce pour la voix, une sans-serif pour l’information.</h1></div>
<div class="types">
 <div class="tc"><div class="eyebrow">Titres · citations</div><div class="tbig serif">Fraunces</div>
  <p class="alpha serif">Aa Bb Cc Đđ Ơơ Ưư Ẻẻ Ổổ<br><i>Lả lơi, buông lơi</i> · 0123456789</p>
  <p class="tmeta">Light & Regular, axe « Soft » à 100 pour des empattements arrondis.</p></div>
 <div class="tc"><div class="eyebrow">Texte · signalétique</div><div class="tbig sans">Be Vietnam Pro</div>
  <p class="alpha sans">Aa Bb Cc Đđ Ơơ Ưư Ẻẻ Ổổ<br>FLEURS DE SAISON · 0123456789</p>
  <p class="tmeta">Light pour le texte, Medium pour les petites capitales espacées.</p></div>
</div>
<div class="scale">
 <div><small>Titre</small><span class="serif" style="font-size:30pt">Bouquet de saison</span></div>
 <div><small>Citation</small><span class="serif" style="font-size:17pt;font-style:italic">Vẻ đẹp là sự tự do cảm xúc</span></div>
 <div><small>Texte</small><span style="font-size:11pt">Pivoines, renoncules et feuillage d’eucalyptus, montés sans attache serrée.</span></div>
 <div><small>Étiquette</small><span class="eyebrow" style="color:var(--muc)">Ouvert du mardi au dimanche · 9 h – 19 h</span></div>
</div>{foot(n0+1,"Typographie")}</section>''')
# usage
B='buong'
pages.append(f'''<section class="pg"><div class="head"><div class="eyebrow">05 · Usage du logo</div><h1>Laisser respirer le logo.</h1>
<p class="lead narrow">Comme un bouquet <i>lơi</i>, le logo a besoin d’air autour de lui. Exemples avec la piste Buông ; les règles valent pour toutes les pistes.</p></div>
<div class="rules">
 <div class="rc"><div class="demo"><div class="clear">{logo(B)}</div></div><p><b>Zone de protection.</b> Un espace vide égal à la hauteur du O tout autour.</p></div>
 <div class="rc"><div class="demo" style="background:var(--reu);color:var(--lua)">{logo(B)}</div><p><b>Deux couleurs.</b> Encre sur fond clair, crème sur mousse, feuillage ou photo sombre.</p></div>
 <div class="rc"><div class="demo"><div style="width:30%">{logo(B)}</div></div><p><b>Taille minimum.</b> 25 mm en impression, 120 px à l’écran ; en dessous, l’arche ou le cachet.</p></div>
 <div class="rc"><div class="demo no"><div style="transform:scaleX(1.45);width:50%">{logo(B)}</div></div><p><b>Ne pas déformer</b> ni étirer le logo.</p></div>
 <div class="rc"><div class="demo no" style="color:var(--dat)"><div style="filter:drop-shadow(3px 3px 0 #26301F);width:55%">{logo(B)}</div></div><p><b>Pas d’effets :</b> ni ombre, ni contour, ni couleur vive.</p></div>
 <div class="rc"><div class="demo no" style="background:linear-gradient(120deg,#c9a7b8,#a7b8c9)">{logo(B)}</div><p><b>Éviter les fonds chargés</b> qui étouffent le trait fin.</p></div>
</div>{foot(n0+2,"Usage")}</section>''')
# closing
pages.append(f'''<section class="pg cover end">
  <div class="eyebrow light">Prochaine étape</div>
  <div class="endgrid">
    <h1 class="light">Choisir une piste,<br>puis l’affiner ensemble.</h1>
    <ol>
      <li><span><b>Sélection.</b> Retenir une ou deux pistes parmi les six.</span></li>
      <li><span><b>Affinage.</b> Ajuster le dessin, les espacements et les couleurs.</span></li>
      <li><span><b>Déclinaisons.</b> Cartes de visite, étiquettes, papier de soie, réseaux sociaux.</span></li>
      <li><span><b>Livraison.</b> Fichiers vectoriels et guide d’usage complet.</span></li>
    </ol>
  </div>
  </section>''')
css=open('pdf.css').read().replace('%%FD%%',FD)
html=f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>LƠI Fleur · Identité visuelle</title><style>{css}</style></head><body><svg width="0" height="0" style="position:absolute">{sym}</svg>{"".join(pages)}</body></html>'
open('/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/deck.html','w').write(html)
print('pages',len(pages))
