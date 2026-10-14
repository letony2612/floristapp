import json, os, subprocess, sys
from PIL import Image
B='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/'
FD=B+'fonts/'; MK='/home/user/floristapp/brand/mockups/'; OUT=B+'app/'
os.makedirs(OUT,exist_ok=True)
C=json.load(open('concepts.json'))
def z(vb):
    x,y,w,h=vb.split(); return f'0 0 {w} {h}'
def sym(k):
    return ''.join(f'<symbol id="{n}-{k}" viewBox="{C[k][n][0]}">{C[k][n][1]}</symbol>' for n in ('main','line','icon'))
def use(k,n,style=''):
    return f'<svg viewBox="{z(C[k][n][0])}" style="{style}"><use href="#{n}-{k}"/></svg>'
CSS=f'''
@font-face{{font-family:FrSoft;src:url("file://{FD}fr-soft.ttf");font-weight:300}}
@font-face{{font-family:FrSoft;src:url("file://{FD}fr-soft-400.ttf");font-weight:400}}
@font-face{{font-family:FrSoft;src:url("file://{FD}fr-soft-it.ttf");font-style:italic}}
@font-face{{font-family:BVP;src:url("file://{FD}bvp-light.ttf");font-weight:300}}
@font-face{{font-family:BVP;src:url("file://{FD}bvp-med.ttf");font-weight:500}}
:root{{--lua:#EEE7DA;--da:#D8CCB6;--kraft:#B7976C;--reu:#4B5138;--la:#26301F;--dat:#A35E3F;--muc:#1F1E1A;--muted:#7A7568;--card:#F6F1E8}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:919px;height:1149px;overflow:hidden}}
body{{background:url("file://{B}gen/BG") center/cover;font-family:BVP;font-weight:300;color:var(--muc);position:relative}}
svg{{display:block;fill:currentColor}}
.phone{{position:absolute;background:#0f0f0e;border-radius:58px;padding:11px;
  box-shadow:inset 0 0 0 1.5px #3a3936, inset 0 0 0 3px #111, -28px 46px 60px rgba(48,30,12,.38), -6px 12px 18px rgba(48,30,12,.25)}}
.screen{{width:100%;height:100%;border-radius:47px;overflow:hidden;position:relative;background:var(--lua)}}
.island{{position:absolute;top:13px;left:50%;transform:translateX(-50%);width:104px;height:30px;border-radius:20px;background:#0b0b0a;z-index:5}}
.status{{height:54px;display:flex;justify-content:space-between;align-items:center;padding:6px 30px 0;font:500 14px BVP;position:relative;z-index:4}}
.status i{{display:flex;gap:5px;align-items:center}}
.status i b{{display:block;width:17px;height:10px;border-radius:2px;border:1.4px solid currentColor;position:relative}}
.status i b::after{{content:"";position:absolute;inset:1.4px;right:4px;background:currentColor;border-radius:1px}}
.status i s{{display:block;width:16px;height:10px;background:linear-gradient(90deg,currentColor 0 3px,transparent 3px 4.3px,currentColor 4.3px 7.3px,transparent 7.3px 8.6px,currentColor 8.6px 11.6px,transparent 11.6px 12.9px,currentColor 12.9px);clip-path:polygon(0 70%,25% 70%,25% 45%,50% 45%,50% 22%,75% 22%,75% 0,100% 0,100% 100%,0 100%)}}
.home-ind{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:128px;height:5px;border-radius:3px;background:currentColor;opacity:.85}}
/* splash */
.splash{{background:var(--reu);color:var(--lua);display:flex;flex-direction:column;height:100%}}
.splash .mid{{flex:1;display:flex;align-items:center;justify-content:center;padding:0 54px}}
.splash .tag{{text-align:center;font:italic 300 15px FrSoft;opacity:.85;padding-bottom:58px;line-height:1.5}}
.icon{{position:absolute;border-radius:26%;background:var(--reu);color:var(--lua);display:flex;align-items:center;justify-content:center;
  box-shadow:-18px 30px 40px rgba(48,30,12,.35), inset 0 1px 0 rgba(255,255,255,.12)}}
.label{{position:absolute;font:500 15px BVP;color:#2b241b;letter-spacing:.02em;text-align:center}}
/* app home */
.hdr{{display:flex;justify-content:space-between;align-items:center;padding:6px 22px 10px}}
.ico{{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.5}}
.hello{{padding:4px 22px 0;font:300 27px/1.15 FrSoft}}
.hello small{{display:block;font:500 10px BVP;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}}
.chips{{display:flex;gap:7px;padding:14px 22px 0;overflow:hidden}}
.chips span{{border:1px solid #CFC3AC;border-radius:999px;padding:6px 12px;font:400 12.5px BVP;white-space:nowrap}}
.chips span.on{{background:var(--muc);color:var(--lua);border-color:var(--muc)}}
.card{{margin:16px 22px 0;background:var(--card);border-radius:18px;overflow:hidden}}
.card .img{{height:190px;background-size:cover;background-position:center}}
.card .t{{padding:12px 14px 14px;display:flex;justify-content:space-between;align-items:flex-end;gap:10px}}
.card h4{{font:400 18px/1.15 FrSoft}}
.card p{{font:300 12px BVP;color:var(--muted);margin-top:3px}}
.price{{font:500 14px BVP;white-space:nowrap}}
.mini{{margin:12px 22px 0;display:flex;gap:12px;align-items:center;background:var(--card);border-radius:16px;padding:8px}}
.mini .img{{width:64px;height:64px;border-radius:11px;background-size:cover;background-position:center;flex:none}}
.mini h4{{font:400 15px FrSoft}} .mini p{{font:300 11.5px BVP;color:var(--muted)}}
.tabs{{position:absolute;left:0;right:0;bottom:0;height:84px;background:rgba(238,231,218,.96);border-top:1px solid #DDD3C0;display:flex;justify-content:space-around;padding-top:10px}}
.tabs div{{display:flex;flex-direction:column;align-items:center;gap:4px;font:400 10px BVP;color:var(--muted)}}
.tabs div.on{{color:var(--muc)}}
/* product */
.pimg{{height:318px;background-size:cover;background-position:center 35%;position:relative}}
.pimg .back{{position:absolute;top:58px;left:18px;width:38px;height:38px;border-radius:50%;background:rgba(238,231,218,.92);display:flex;align-items:center;justify-content:center}}
.pbody{{padding:18px 22px}}
.pbody small{{font:500 10px BVP;letter-spacing:.2em;text-transform:uppercase;color:var(--dat)}}
.pbody h3{{font:300 28px/1.1 FrSoft;margin-top:6px}}
.pbody .d{{font:300 13px/1.55 BVP;color:var(--muted);margin-top:8px}}
.sizes{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}}
.sizes div{{border:1px solid #CFC3AC;border-radius:12px;padding:9px 0;text-align:center;font:400 12px BVP}}
.sizes div b{{display:block;font:400 17px FrSoft;margin-bottom:1px}}
.sizes div.on{{border-color:var(--muc);box-shadow:inset 0 0 0 1px var(--muc)}}
.cta{{position:absolute;left:22px;right:22px;bottom:30px;background:var(--reu);color:var(--lua);border-radius:16px;height:54px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;font:500 14px BVP;letter-spacing:.04em}}
.deliv{{font:300 12px BVP;color:var(--muted);margin-top:14px;display:flex;gap:8px;align-items:center}}
'''
I_BAG='<svg class="ico" viewBox="0 0 24 24"><path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/></svg>'
I_SEARCH='<svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></svg>'
TABS=[('Accueil','<path d="M4 11l8-6 8 6v9H4z"/>'),('Boutique','<path d="M12 21c-4-3-7-6-7-10a7 7 0 0 1 14 0c0 4-3 7-7 10z"/><circle cx="12" cy="11" r="2.5"/>'),
      ('Ateliers','<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>'),('Panier','<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>'),
      ('Profil','<circle cx="12" cy="9" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>')]
def tabs():
    return '<div class="tabs">'+''.join(f'<div class="{"on" if i==0 else ""}"><svg class="ico" viewBox="0 0 24 24">{p}</svg>{n}</div>' for i,(n,p) in enumerate(TABS))+'</div>'
def status(dark=True):
    col='var(--muc)' if dark else 'var(--lua)'
    return f'<div class="island"></div><div class="status" style="color:{col}"><span>9:41</span><i><s></s><b></b></i></div>'
def img(k,s): return f'file://{MK}{k}-{s}.jpg'
def page_icon(k):
    pw,ph=372,806; px,py=300,150
    ic=168
    html=f'''<div class="phone" style="left:{px}px;top:{py}px;width:{pw}px;height:{ph}px"><div class="screen"><div class="splash">{status(False)}
      <div class="mid">{use(k,'main','width:100%;max-height:300px;color:var(--lua)')}</div>
      <div class="tag">Vẻ đẹp là sự tự do cảm xúc</div><div class="home-ind" style="color:var(--lua)"></div></div></div></div>
    <div class="icon" style="left:118px;top:780px;width:{ic}px;height:{ic}px;padding:{ic*0.2:.0f}px">{use(k,'icon','width:100%;height:100%')}</div>
    <div class="label" style="left:118px;top:{780+ic+14}px;width:{ic}px">Lơi Fleur</div>'''
    return html,'bg1.jpg'
def page_screens(k):
    pw,ph=356,772
    home=f'''<div class="screen">{status()}
      <div class="hdr">{use(k,'line','height:30px;width:auto;max-width:200px')}<div style="display:flex;gap:14px">{I_SEARCH}{I_BAG}</div></div>
      <div class="hello"><small>Mardi 14 octobre</small>Les fleurs<br>de la semaine</div>
      <div class="chips"><span class="on">Tout</span><span>Bouquets</span><span>Feuillages</span><span>Coffrets</span><span>Mariages</span></div>
      <div class="card"><div class="img" style="background-image:url('{img(k,'boite')}');background-position:center 8%;background-size:150%"></div>
        <div class="t"><div><h4>Feuillages de saison</h4><p>Monstera, strelitzia, palmier</p></div><span class="price">dès 25 €</span></div></div>
      <div class="mini"><div class="img" style="background-image:url('{img(k,'devanture')}');background-position:50% 72%"></div>
        <div><h4>Atelier du samedi</h4><p>Composer un bouquet libre · 10 h</p></div></div>
      {tabs()}<div class="home-ind"></div></div>'''
    prod=f'''<div class="screen">{status()}
      <div class="pimg" style="background-image:url('{img(k,'boite')}');background-position:52% 62%;background-size:175%"><div class="back"><svg class="ico" viewBox="0 0 24 24" style="width:18px"><path d="M15 5l-7 7 7 7"/></svg></div></div>
      <div class="pbody"><small>Coffret cadeau</small><h3>Le coffret lơi</h3>
        <p class="d">Une boîte en kraft garnie le matin même de fleurs de saison, posées sans attache serrée pour garder leur mouvement.</p>
        <div class="sizes"><div><b>S</b>35 €</div><div class="on"><b>M</b>45 €</div><div><b>L</b>60 €</div></div>
        <p class="deliv">{I_BAG.replace('class="ico"','class="ico" style="width:16px;height:16px"')} Livraison le jour même avant 14 h</p></div>
      <div class="cta"><span>AJOUTER AU PANIER</span><span>45 €</span></div><div class="home-ind"></div></div>'''
    html=(f'<div class="phone" style="left:92px;top:200px;width:{pw}px;height:{ph}px">{home}</div>'
          f'<div class="phone" style="left:478px;top:150px;width:{pw}px;height:{ph}px">{prod}</div>')
    return html,'bg2.jpg'
def render(k,kind):
    body,bg=(page_icon if kind=='appli' else page_screens)(k)
    doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("BG",bg)}</style></head><body><svg width="0" height="0" style="position:absolute">{sym(k)}</svg>{body}</body></html>'
    f=OUT+f'{k}-{kind}.html'; open(f,'w').write(doc)
    png=OUT+f'{k}-{kind}.png'
    subprocess.run(['/opt/pw-browsers/chromium-1194/chrome-linux/chrome','--headless','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files',
        '--force-device-scale-factor=2','--window-size=919,1400','--virtual-time-budget=2000',f'--screenshot={png}','file://'+f],capture_output=True)
    Image.open(png).convert('RGB').crop((0,0,1838,2298)).resize((919,1149),Image.LANCZOS).save(MK+f'{k}-{kind}.jpg',quality=84,optimize=True,progressive=True)
if __name__=='__main__':
    ks=sys.argv[1:] or list(C)
    for k in ks:
        for kind in ('appli','appli-ecrans'): render(k,kind)
    print('ok',ks)
