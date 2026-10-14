import json, os, subprocess, sys
from PIL import Image
B='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/'
FD=B+'fonts/'; OUT='/home/user/floristapp/nappli/mockups/'; TMP=B+'nmock/'
os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
C=json.load(open(os.environ.get('NCONF','nconcepts.json')))
def z(vb): x,y,w,h=vb.split(); return f'0 0 {w} {h}'
def sym(k): return ''.join(f'<symbol id="{n}-{k}" viewBox="{C[k][n][0]}">{C[k][n][1]}</symbol>' for n in ('main','icon'))
def use(k,n,style='',cls=''): return f'<svg class="{cls}" viewBox="{z(C[k][n][0])}" style="{style}"><use href="#{n}-{k}"/></svg>'
CSS=f'''
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-400.ttf");font-weight:400}}
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-500.ttf");font-weight:500}}
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-600.ttf");font-weight:600}}
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-700.ttf");font-weight:700}}
@font-face{{font-family:Allura;src:url("file://{FD}Allura.ttf")}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:919px;height:1149px;overflow:hidden}}
body{{font-family:Inter;color:#000;background:#fff;position:relative;-webkit-font-smoothing:antialiased}}
svg{{display:block;fill:currentColor;overflow:visible}}
.mist{{position:absolute;inset:-10%;filter:blur(60px);
  background:radial-gradient(40% 35% at 25% 30%,#BDEBF0 0,transparent 70%),radial-gradient(45% 40% at 75% 35%,#CFE6FF 0,transparent 70%),
  radial-gradient(40% 35% at 60% 75%,#DCD6FF 0,transparent 70%),radial-gradient(30% 30% at 20% 80%,#FFD9E8 0,transparent 70%),#fff}}
.phone{{position:absolute;background:#0d0d0d;border-radius:58px;padding:11px;box-shadow:inset 0 0 0 1.5px #3a3a3a,0 50px 90px -30px rgba(40,60,120,.45),0 18px 30px -12px rgba(0,0,0,.25)}}
.screen{{width:100%;height:100%;border-radius:47px;overflow:hidden;position:relative;background:#fff}}
.island{{position:absolute;top:13px;left:50%;transform:translateX(-50%);width:104px;height:30px;border-radius:20px;background:#000;z-index:5}}
.status{{height:54px;display:flex;justify-content:space-between;align-items:center;padding:6px 30px 0;font:600 14px Inter;position:relative;z-index:4}}
.homeind{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:128px;height:5px;border-radius:3px;background:#000}}
.tile{{border-radius:22.5%;background:#000;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px -10px rgba(0,0,0,.35)}}
.pillbtn{{display:inline-flex;align-items:center;justify-content:center;background:#000;color:#fff;border-radius:999px;font:500 13px Inter;padding:9px 16px}}
'''
def phone(x,y,w,h,inner,status_dark=True):
    col='#000' if status_dark else '#fff'
    return (f'<div class="phone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="screen">'
            f'<div class="island"></div><div class="status" style="color:{col}"><span>9:41</span><span>●●● ▮</span></div>{inner}<div class="homeind" style="background:{col}"></div></div></div>')
def scene_icone(k):
    apps=['#E9E7FF','#D9F3F6','#FFE3EC','#EDEDED','#DDEBFF','#F3F0E8','#E6F7EE','#FFF1DC','#EDE9FF','#E4F4F8','#FFE9E3']
    cells=''
    for i in range(16):
        if i==5: cells+=f'<div class="app"><div class="tile" style="width:62px;height:62px;padding:13px">{use(k,"icon","width:100%;height:100%")}</div><span>Nappli</span></div>'
        else: cells+=f'<div class="app"><div style="width:62px;height:62px;border-radius:22.5%;background:{apps[i%len(apps)]}"></div><span style="opacity:.0">x</span></div>'
    inner=f'''<div style="position:absolute;inset:0;background:radial-gradient(60% 40% at 30% 20%,#BDEBF0,transparent 70%),radial-gradient(60% 50% at 80% 70%,#DCD6FF,transparent 70%),#F4F7FF"></div>
      <div style="position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:26px 0;padding:24px 18px;justify-items:center">{cells}</div>'''
    return (f'<div class="mist"></div><style>.app{{display:flex;flex-direction:column;align-items:center;gap:6px;font:500 11.5px Inter;color:#1a1a1a}}</style>'
            + phone(300,150,372,806,inner)
            + f'<div class="tile" style="position:absolute;left:96px;top:760px;width:190px;height:190px;padding:40px">{use(k,"icon","width:100%;height:100%")}</div>')
def scene_appli(k):
    inner=f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px">
      <div style="width:230px">{use(k,"main","width:100%;height:auto")}</div></div>
      <div style="position:absolute;bottom:60px;left:0;right:0;text-align:center;font:500 13px Inter;color:#9b9b9b">Studio web &amp; mobile</div>'''
    return '<div class="mist"></div>'+phone(273,150,372,806,inner)
def scene_site(k):
    return f'''<div class="mist" style="opacity:.6"></div>
    <div style="position:absolute;left:70px;top:190px;width:779px;height:760px;border-radius:18px;background:#fff;overflow:hidden;box-shadow:0 60px 100px -40px rgba(40,60,140,.45),0 0 0 1px rgba(0,0,0,.06)">
      <div style="height:44px;background:#F6F6F7;display:flex;align-items:center;gap:8px;padding:0 16px;border-bottom:1px solid #ececec">
        <i style="width:12px;height:12px;border-radius:50%;background:#FF5F57"></i><i style="width:12px;height:12px;border-radius:50%;background:#FEBC2E"></i><i style="width:12px;height:12px;border-radius:50%;background:#28C840"></i>
        <div style="margin-left:90px;width:380px;height:26px;border-radius:8px;background:#fff;border:1px solid #ececec;font:500 12px Inter;color:#5c5c5c;display:flex;align-items:center;justify-content:center">nappli.fr</div></div>
      <div style="position:relative;height:716px;overflow:hidden">
        <div class="mist" style="inset:-20% -10% 20% -10%"></div>
        <div style="position:relative;display:flex;justify-content:space-between;align-items:center;padding:22px 30px">
          <div style="width:96px">{use(k,"main","width:100%;height:auto")}</div>
          <div style="display:flex;gap:16px;font:500 12px Inter;color:#5c5c5c"><span style="color:#000">FR</span><span>EN</span><span>VI</span></div></div>
        <div style="position:relative;text-align:center;margin-top:150px">
          <div style="font:600 46px/1.1 Inter;letter-spacing:-.03em">Vous apportez l’idée,<br>on la rend réelle.</div>
          <div style="font:400 18px Inter;color:#5c5c5c;margin-top:18px">Sur le web, et dans votre poche.</div>
          <div class="pillbtn" style="margin-top:30px;font-size:15px;padding:13px 24px">Commencer</div></div>
      </div></div>'''
def scene_reseaux(k):
    posts=['Vous avez l’idée,<br>on s’occupe du reste.','Pas de jargon,<br>juste du concret.','Fait avec soin.','De l’idée<br>au lancement.','Sur le web,<br>et dans votre poche.','100 %<br>en ligne']
    bgs=['linear-gradient(135deg,#BDEBF0,#DCD6FF)','#000','linear-gradient(135deg,#FFD9E8,#DCD6FF)','#fff','linear-gradient(135deg,#CFE6FF,#BDEBF0)','#0c3a44']
    fg=['#000','#fff','#000','#000','#000','#fff']
    grid=''.join(f'<div style="aspect-ratio:1;background:{b};display:flex;align-items:center;justify-content:center;text-align:center;font:600 10.5px/1.25 Inter;color:{c};padding:8px;border:{"1px solid #ececec" if b=="#fff" else "0"}">{t}</div>' for t,b,c in zip(posts,bgs,fg))
    inner=f'''<div style="padding:4px 18px 0">
      <div style="display:flex;justify-content:space-between;align-items:center;font:700 17px Inter"><span>nappli.studio</span><span style="font-size:20px">≡</span></div>
      <div style="display:flex;align-items:center;gap:22px;margin-top:16px">
        <div class="tile" style="width:84px;height:84px;border-radius:50%;padding:20px;flex:none">{use(k,"icon","width:100%;height:100%")}</div>
        <div style="display:flex;gap:18px;text-align:center;font:400 12px Inter"><div><b style="display:block;font:600 16px Inter">48</b>publications</div><div><b style="display:block;font:600 16px Inter">1 204</b>abonnés</div><div><b style="display:block;font:600 16px Inter">180</b>abonnements</div></div></div>
      <div style="margin-top:12px;font:600 13.5px Inter">Nappli · Studio web &amp; mobile</div>
      <div style="font:400 13px/1.45 Inter;color:#333">De l’idée au lancement.<br>Sites, applications iOS et Android.<br><span style="color:#2A44D8">nappli.fr</span></div>
      <div style="display:flex;gap:6px;margin-top:12px"><div style="flex:1;background:#EFEFEF;border-radius:8px;padding:7px;text-align:center;font:600 12.5px Inter">Suivre</div><div style="flex:1;background:#EFEFEF;border-radius:8px;padding:7px;text-align:center;font:600 12.5px Inter">Message</div></div></div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:16px">{grid}</div>'''
    return '<div class="mist"></div>'+phone(273,150,372,806,inner)
def scene_carte(k):
    card='position:absolute;width:504px;height:300px;border-radius:14px;background:#fff;box-shadow:0 40px 70px -30px rgba(40,60,140,.45),0 2px 6px rgba(0,0,0,.06)'
    front=f'<div style="{card};left:150px;top:230px;transform:rotate(-8deg);display:flex;align-items:center;justify-content:center"><div style="width:250px">{use(k,"main","width:100%;height:auto")}</div></div>'
    back=f'''<div style="{card};left:250px;top:610px;transform:rotate(5deg);padding:38px 40px;display:flex;flex-direction:column;justify-content:space-between">
       <div style="display:flex;justify-content:space-between;align-items:flex-start"><div><div style="font:600 21px Inter;letter-spacing:-.02em">Tony</div><div style="font:400 14px Inter;color:#5c5c5c;margin-top:2px">Fondateur</div></div>
         <div class="tile" style="width:46px;height:46px;padding:10px">{use(k,"icon","width:100%;height:100%")}</div></div>
       <div style="font:400 14px/1.6 Inter;color:#000">contact@nappli.fr<br><span style="color:#5c5c5c">nappli.fr · Studio web &amp; mobile</span></div></div>'''
    return '<div class="mist"></div>'+front+back
def scene_devis(k):
    rows=[('Cadrage et ateliers','1 j','600 €'),('Design des écrans (iOS, Android)','5 j','3 000 €'),('Développement de l’application','12 j','7 200 €'),('Mise en ligne et accompagnement','2 j','1 200 €')]
    tr=''.join(f'<div style="display:grid;grid-template-columns:1fr 50px 80px;padding:11px 0;border-bottom:1px solid #ececec;font:400 12.5px Inter"><span>{a}</span><span style="color:#5c5c5c">{b}</span><span style="text-align:right">{c}</span></div>' for a,b,c in rows)
    return f'''<div class="mist"></div>
    <div style="position:absolute;left:150px;top:120px;width:619px;height:876px;background:#fff;border-radius:6px;box-shadow:0 60px 100px -40px rgba(40,60,140,.45),0 0 0 1px rgba(0,0,0,.05);padding:58px 56px;transform:rotate(-2deg)">
      <div style="display:flex;justify-content:space-between;align-items:flex-start"><div style="width:130px">{use(k,"main","width:100%;height:auto")}</div>
        <div style="text-align:right;font:400 11.5px/1.6 Inter;color:#5c5c5c">Devis n° 2026-014<br>14 octobre 2026</div></div>
      <div style="font:600 30px Inter;letter-spacing:-.03em;margin-top:70px">Devis</div>
      <div style="font:400 13px Inter;color:#5c5c5c;margin-top:6px">Application mobile · iOS et Android</div>
      <div style="margin-top:36px;border-top:1px solid #000">{tr}</div>
      <div style="display:flex;justify-content:space-between;margin-top:22px;font:600 16px Inter"><span>Total HT</span><span>12 000 €</span></div>
      <div style="position:absolute;left:56px;bottom:70px;font:400 11.5px/1.6 Inter;color:#5c5c5c">Un seul interlocuteur, de l’idée au lancement.<br>contact@nappli.fr · nappli.fr</div>
      <div style="position:absolute;right:60px;bottom:66px;font:44px Allura;color:#2A44D8">Tony</div></div>'''
SCENES={'icone':scene_icone,'appli':scene_appli,'site':scene_site,'reseaux':scene_reseaux,'carte':scene_carte,'devis':scene_devis}
def render(k,name):
    doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{sym(k)}</svg>{SCENES[name](k)}</body></html>'
    f=TMP+f'{k}-{name}.html'; open(f,'w').write(doc); png=TMP+f'{k}-{name}.png'
    subprocess.run(['/opt/pw-browsers/chromium-1194/chrome-linux/chrome','--headless','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files','--force-device-scale-factor=2','--window-size=919,1400','--virtual-time-budget=2000',f'--screenshot={png}','file://'+f],capture_output=True)
    Image.open(png).convert('RGB').crop((0,0,1838,2298)).resize((919,1149),Image.LANCZOS).save(OUT+f'{k}-{name}.jpg',quality=86,optimize=True,progressive=True)
if __name__=='__main__':
    ks=[a for a in sys.argv[1:] if a in C] or list(C)
    names=[a for a in sys.argv[1:] if a in SCENES] or list(SCENES)
    for k in ks:
        for n in names: render(k,n)
    print('ok',ks,names)
