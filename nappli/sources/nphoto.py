import json, io, subprocess, sys, numpy as np, cv2, cairosvg
from PIL import Image, ImageDraw, ImageFont
from composite import Decal, light, VINYL
import nmock
B='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/'
MK=B+'mk/'; FD=B+'fonts/'; OUT='/home/user/floristapp/nappli/mockups/'
import os
C=json.load(open(os.environ.get('NCONF','nconcepts.json')))
def load(i): return cv2.cvtColor(cv2.imread(MK+f'clean{i}.png'),cv2.COLOR_BGR2RGB)
def alpha(k,kind,width):
    vb,body=C[k][kind]; x,y,w,h=map(float,vb.split())
    body=body.replace('var(--red,#FF3B30)','#000').replace('var(--stamp,#2A44D8)','#000').replace('var(--guide,#8F9BFF)','#000').replace('currentColor','#000')
    png=cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{width}" height="{int(width*h/w)}">{body}</svg>'.encode())
    return Image.open(io.BytesIO(png)).split()[-1]
def porte(k):
    img=load(5); x0,y0,x1,y1=440,320,1000,1020; W,H=(x1-x0)*2,(y1-y0)*2; d=Decal(W,H)
    # letters are cream vinyl; accent pieces keep their colour (added after the warp)
    f=ImageFont.truetype(FD+'Inter-wght-500.ttf',34)
    d.text('STUDIO WEB & MOBILE',f,W/2,880,track=6)
    d.text('Sur rendez-vous · nappli.fr',ImageFont.truetype(FD+'Inter-wght-400.ttf',32),W/2,1240)
    from composite import warp
    out=light(img,warp(d,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],img.shape),VINYL,op=.9,soft=.7)
    vb,body=C[k]['main']; x,y,w,h=map(float,vb.split()); lw=560 if k!='signe' else 600
    col=body.replace('var(--red,#FF3B30)','#FF3B30').replace('var(--stamp,#2A44D8)','#3B55E6').replace('var(--guide,#8F9BFF)','#A9B2FF').replace('currentColor','#F2EFE9')
    lg=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{lw}" height="{int(lw*h/w)}">{col}</svg>'.encode()))).convert('RGBA')
    can=Image.new('RGBA',(W,H),(0,0,0,0)); can.paste(lg,(int(W/2-lg.width/2),int(640-lg.height/2)),lg)
    arr=np.array(can,np.float32)
    M=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),np.float32([(x0,y0),(x1,y0),(x1,y1),(x0,y1)]))
    wp=cv2.warpPerspective(arr,M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
    a=cv2.GaussianBlur(wp[...,3]/255,(0,0),.6)*.92
    lum=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).astype(np.float32),(0,0),6)
    shade=(lum/np.median(lum[a>.2]))**.35
    rgb=(wp[...,:3]*shade[...,None]).clip(0,255)
    out=(out.astype(np.float32)*(1-a[...,None])+rgb*a[...,None]).clip(0,255).astype(np.uint8)
    return out[:1266]   # crop to the 4:5 format of the other mockups
def ordinateur(k):
    # render the site hero at screen resolution, then warp it into the laptop
    W,H=1600,1260
    html=f'''<!doctype html><html><head><meta charset="utf-8"><style>{nmock.CSS}html,body{{width:{W}px;height:{H}px}}</style></head><body>
    <svg width="0" height="0" style="position:absolute">{nmock.sym(k)}</svg><div class="mist" style="inset:-15% -10% 10% -10%"></div>
    <div style="position:relative;display:flex;justify-content:space-between;align-items:center;padding:44px 70px">
      <div style="width:190px">{nmock.use(k,"main","width:100%;height:auto")}</div><div style="display:flex;gap:28px;font:500 24px Inter;color:#5c5c5c"><span style="color:#000">FR</span><span>EN</span><span>VI</span></div></div>
    <div style="position:relative;text-align:center;margin-top:250px"><div style="font:600 92px/1.08 Inter;letter-spacing:-.035em">Vous apportez l’idée,<br>on la rend réelle.</div>
      <div style="font:400 34px Inter;color:#5c5c5c;margin-top:30px">Sur le web, et dans votre poche.</div>
      <div class="pillbtn" style="margin-top:50px;font-size:28px;padding:24px 46px">Commencer</div></div></body></html>'''
    f=B+f'nmock/{k}-screen.html'; open(f,'w').write(html); png=B+f'nmock/{k}-screen.png'
    subprocess.run(['/opt/pw-browsers/chromium-1194/chrome-linux/chrome','--headless','--no-sandbox','--hide-scrollbars','--allow-file-access-from-files',f'--window-size={W},{H+200}','--virtual-time-budget=2000',f'--screenshot={png}','file://'+f],capture_output=True)
    scr=np.array(Image.open(png).convert('RGB').crop((0,0,W,H)),np.float32)
    img=load(4)
    quad=[(510,644),(697,650),(689,806),(495,796)]
    M=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),np.float32(quad))
    wp=cv2.warpPerspective(scr,M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
    m=cv2.warpPerspective(np.ones((H,W),np.float32),M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
    lum=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).astype(np.float32),(0,0),9)
    ref=np.median(lum[m>.9]); shade=(lum/ref).clip(.6,1.2)**.6*0.9
    out=img.astype(np.float32)*(1-m[...,None])+(wp*shade[...,None])*m[...,None]
    return out.clip(0,255).astype(np.uint8)
if __name__=='__main__':
    for k in (sys.argv[1:] or list(C)):
        Image.fromarray(porte(k)).resize((919,1149),Image.LANCZOS).save(OUT+f'{k}-porte.jpg',quality=86,optimize=True,progressive=True)
        Image.fromarray(ordinateur(k)).save(OUT+f'{k}-ordinateur.jpg',quality=86,optimize=True,progressive=True)
    print('ok')
