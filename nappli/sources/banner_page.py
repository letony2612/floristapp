import json, subprocess, os
from PIL import Image
B='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/'
FD=B+'fonts/'; OUT='/home/user/floristapp/nappli/linkedin/page-entreprise/'; os.makedirs(OUT,exist_ok=True)
C=json.load(open('nfinal.json'))['final']
def z(vb): x,y,w,h=vb.split(); return f'0 0 {w} {h}'
SYM=''.join(f'<symbol id="{n}" viewBox="{C[n][0]}">{C[n][1]}</symbol>' for n in ('main','icon'))
W,H=1128,191
CSS=f'''
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-400.ttf");font-weight:400}}
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-500.ttf");font-weight:500}}
@font-face{{font-family:Inter;src:url("file://{FD}Inter-wght-600.ttf");font-weight:600}}
@font-face{{font-family:Allura;src:url("file://{FD}Allura.ttf")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Inter;background:#fff;color:#000;position:relative;-webkit-font-smoothing:antialiased}}
svg{{display:block;fill:currentColor}}
.mist{{position:absolute;inset:-30%;filter:blur(70px);
 background:radial-gradient(30% 45% at 30% 40%,#BDEBF0 0,transparent 70%),radial-gradient(30% 50% at 62% 30%,#CFE6FF 0,transparent 70%),
 radial-gradient(28% 45% at 82% 70%,#DCD6FF 0,transparent 70%),radial-gradient(22% 40% at 12% 80%,#FFD9E8 0,transparent 70%)}}
.word{{width:150px}}
.tile{{width:46px;height:46px;border-radius:11px;background:#000;color:#fff;padding:10px}}
.tile svg{{width:100%;height:100%}}
h1{{font-weight:600;letter-spacing:-.04em;line-height:1.04}}
.sub{{color:#5c5c5c;font-size:13px}}
'''
logo=lambda w=150: f'<div style="width:{w}px"><svg viewBox="{z(C["main"][0])}"><use href="#main"/></svg></div>'
tile=lambda: f'<div class="tile"><svg viewBox="{z(C["icon"][0])}"><use href="#icon"/></svg></div>'
V={}
# 1 · Brume : the site's own headline, nothing else
V['1-brume']=f'''<div class="mist"></div>
<div style="position:absolute;left:300px;right:60px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:10px">
  <h1 style="font-size:34px">Vous apportez l’idée,<br>on la rend réelle.</h1>
  <p class="sub">Sites et applications iOS & Android · nappli.fr</p></div>
<div style="position:absolute;right:60px;top:50%;transform:translateY(-50%)">{logo(104)}</div>'''
# 2 · Parcours : the three steps of the site replace the pills
step=lambda n,t,last=False: f'<div style="display:flex;align-items:center;gap:8px"><span style="width:9px;height:9px;border-radius:50%;background:{"#000" if last else "#fff"};border:1.5px solid #000"></span><span style="font:500 13px Inter">{t}</span></div>'
V['2-parcours']=f'''<div class="mist" style="opacity:.75"></div>
<div style="position:absolute;left:300px;right:60px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:14px">
  <h1 style="font-size:31px">Votre app, de l’idée<br>au lancement.</h1>
  <div style="display:flex;align-items:center;gap:12px">
    {step(1,"L’idée")}<span style="flex:0 0 40px;height:1.5px;background:#000;opacity:.18"></span>
    {step(2,"La création")}<span style="flex:0 0 40px;height:1.5px;background:#000;opacity:.18"></span>
    {step(3,"En ligne",True)}</div></div>
<div style="position:absolute;right:60px;top:50%;transform:translateY(-50%)">{logo(104)}</div>'''
# 3 · Signature : headline + handwritten line, like "Tony, fondateur" on the site
V['3-signature']=f'''<div class="mist"></div>
<div style="position:absolute;left:300px;right:60px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:6px">
  <p style="font:500 11px Inter;color:#5c5c5c">Studio web & mobile</p>
  <h1 style="font-size:30px">Pas de jargon,<br>juste du concret.</h1>
  <p style="font:36px/1 Allura;color:#2A44D8;margin-top:2px">Fait avec soin.</p></div>
<div style="position:absolute;right:60px;top:50%;transform:translateY(-50%)">{logo(104)}</div>'''
# 4 · Nuit : dark version, closest to the current banner, with the personal motto kept small
V['4-nuit']=f'''<div style="position:absolute;inset:0;background:#000"></div>
<div class="mist" style="opacity:.35"></div>
<div style="position:absolute;left:300px;right:60px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:8px;color:#fff">
  <h1 style="font-size:31px">Développer une app<br>n’a jamais été aussi simple.</h1>
  <p class="sub" style="color:#b5b5b5">Sites et applications iOS & Android · nappli.fr</p></div>
<div style="position:absolute;right:60px;top:50%;transform:translateY(-50%);color:#fff">{logo(104)}</div>
<p style="position:absolute;left:300px;top:16px;font:500 10px Inter;color:#8f8f8f">Guided by Faith, built for Innovation.</p>'''
def render(name,body):
    doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{SYM}</svg>{body}</body></html>'
    f=B+f'nmock/banner-{name}.html'; open(f,'w').write(doc); png=OUT+f'banniere-{name}.png'
    subprocess.run(['/opt/pw-browsers/chromium-1194/chrome-linux/chrome','--headless','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files','--force-device-scale-factor=2',f'--window-size={W},{H+200}','--virtual-time-budget=2000',f'--screenshot={png}','file://'+f],capture_output=True)
    Image.open(png).convert('RGB').crop((0,0,W*2,H*2)).save(png,optimize=True)
for k,v in V.items(): render(k,v)
# preview: banner as LinkedIn shows it on a company page, page logo over the bottom-left
from PIL import ImageDraw, ImageFont
F=ImageFont.truetype(FD+'Inter-wght-500.ttf',18)
sheet=Image.new('RGB',(1000,4*260+30),(243,242,239)); d=ImageDraw.Draw(sheet)
icon=Image.open(B+'gen/ic.png').convert('RGBA').resize((104,104))
for i,k in enumerate(V):
    im=Image.open(OUT+f'banniere-{k}.png').resize((920,156),Image.LANCZOS)
    y=20+i*260; card=Image.new('RGB',(920,230),(255,255,255)); card.paste(im,(0,0))
    cd=ImageDraw.Draw(card); cd.rounded_rectangle((20,96,128,204),radius=12,fill=(255,255,255)); card.paste(icon,(22,98),icon)
    sheet.paste(card,(40,y)); d.text((200,y+172),k.split('-',1)[1].capitalize(),font=F,fill=(60,60,60))
sheet.save(OUT+'apercu-page.png')
print(sorted(os.listdir(OUT)))
