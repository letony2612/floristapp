import json, html
C=json.load(open('concepts.json'))
META=[('buong','Buông','Éditorial','Serif douce. Le crochet du Ơ devient une tige qui laisse pendre une feuille : le geste « buông lơi ». La piste la plus polyvalente.',True),
('laloi','Lả lơi','Manuscrit','Italique en minuscules, un trait de plume qui ondule sous le mot. Romantique : cartes, mariages, rubans.',False),
('arche','Arche','Emblème','Le Ơ-feuille posé dans une arche, la forme d’une porte de boutique. Idéal en icône de réseau social, tampon ou étiquette.',False),
('net','Nét','Minimal','Sans-serif léger, très espacé ; un seul pétale remplace le crochet. Moderne et lisible de loin, parfait pour l’enseigne.',False),
('an','Ấn','Cachet','Sceau circulaire portant la devise en vietnamien. Pour fermer le papier de soie, autocollants et packaging.',False),
('tige','Tige','Botanique','Le « l » devient une tige qui s’incline et laisse pendre un bouton au-dessus du mot. La piste la plus illustrative.',False)]
TALL={'arche','an','tige'}
def z(vb):
    x,y,w,h=vb.split(); return f'0 0 {w} {h}'
sym=''.join(f'<symbol id="m-{k}" viewBox="{v["main"][0]}">{v["main"][1]}</symbol><symbol id="l-{k}" viewBox="{v["line"][0]}">{v["line"][1]}</symbol>' for k,v in C.items())
cards=''
for k,n,st,desc,reco in META:
    cards+=(f'<button class="logo-card" type="button" data-k="{k}" aria-pressed="false">'
      f'<div class="art {"tall" if k in TALL else "wide"}"><svg viewBox="{z(C[k]["main"][0])}" role="img" aria-label="Logo {n}"><use href="#m-{k}"/></svg></div>'
      f'<div class="txt"><div class="row"><h3>{n}{"<span class=reco>Notre choix</span>" if reco else ""}</h3><span class="style">{st}</span></div><p>{desc}</p><span class="pick">Voir sur les mockups</span></div></button>')
chips=''.join(f'<button class="chip" type="button" data-k="{k}" aria-pressed="false"><svg viewBox="{z(C[k]["main"][0])}" aria-hidden="true"><use href="#m-{k}"/></svg>{n}</button>' for k,n,*_ in META)
SW=[('Lụa','crème soie','#EEE7DA','238 231 218','5 7 14 0'),('Đá','pierre','#D8CCB6','216 204 182','15 17 28 0'),('Kraft','papier','#B7976C','183 151 108','29 40 63 5'),
    ('Rêu','mousse','#4B5138','75 81 56','62 45 78 40'),('Lá','feuillage','#26301F','38 48 31','72 52 82 66'),('Đất','terre cuite','#A35E3F','163 94 63','25 66 78 15'),('Mực','encre','#1F1E1A','31 30 26','68 64 68 78')]
sw=''.join(f'<div class="sw"><div class="chipc" style="background:{h}"></div><b>{n}</b><i>{d}</i><code>{h}<br>RVB {r}<br>CMJN {c}</code></div>' for n,d,h,r,c in SW)
t=open('page_tpl.html').read()
t=t.replace('%%SYMBOLS%%',sym).replace('%%CARDS%%',cards).replace('%%CHIPS%%',chips).replace('%%SWATCHES%%',sw)
t=t.replace('%%VB_an%%',z(C['an']['main'][0])).replace('%%VB_buong%%',z(C['buong']['main'][0])).replace('%%NAMES%%',json.dumps({k:n for k,n,*_ in META},ensure_ascii=False))
# cover / variants use symbols in a dedicated colour via currentColor
open('/home/user/floristapp/brand/charte.html','w').write(t)
print(len(t))
