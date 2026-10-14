import json, io, numpy as np, cv2, cairosvg
from PIL import Image, ImageDraw, ImageFont
B='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/'
FD=B+'fonts/'; MK=B+'mk/'; OUT=B+'out/'
import os; os.makedirs(OUT,exist_ok=True)
CON=json.load(open('concepts.json'))
INK=np.array([31,30,26],np.float32); CREAM=np.array([236,229,214],np.float32); VINYL=np.array([240,238,230],np.float32)
def F(name,px): return ImageFont.truetype(FD+name,int(px))
def logo_alpha(key,kind,width=None,height=None):
    vb,body=CON[key][kind]
    x,y,w,h=map(float,vb.split())
    if width is None: width=int(height*w/h)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{width}" height="{int(width*h/w)}">{body.replace("currentColor","#000")}</svg>'
    png=cairosvg.svg2png(bytestring=svg.encode())
    return Image.open(io.BytesIO(png)).split()[-1]
def fit(key,kind,maxw,maxh):
    x,y,w,h=map(float,CON[key][kind][0].split())
    sc=min(maxw/w,maxh/h); return logo_alpha(key,kind,width=int(w*sc))
class Decal:
    def __init__(s,w,h): s.im=Image.new('L',(w,h),0); s.d=ImageDraw.Draw(s.im); s.w=w; s.h=h
    def paste_c(s,a,cx,cy): s.im.paste(255,(int(cx-a.width/2),int(cy-a.height/2)),a)
    def paste(s,a,x,y): s.im.paste(255,(int(x),int(y)),a)
    def text(s,txt,font,x,y,anchor='mm',track=0):
        if not track: s.d.text((x,y),txt,font=font,fill=255,anchor=anchor); return
        ws=[font.getlength(c) for c in txt]; tot=sum(ws)+track*(len(txt)-1)
        sx={'m':x-tot/2,'l':x,'r':x-tot}[anchor[0]]
        for c,wc in zip(txt,ws): s.d.text((sx,y),c,font=font,fill=255,anchor='l'+anchor[1]); sx+=wc+track
def warp(decal,quad,shape):
    a=np.array(decal.im,np.float32)/255
    src=np.float32([[0,0],[decal.w,0],[decal.w,decal.h],[0,decal.h]])
    M=cv2.getPerspectiveTransform(src,np.float32(quad))
    return cv2.warpPerspective(a,M,(shape[1],shape[0]),flags=cv2.INTER_AREA)
def ink(img,a,op=.9,soft=.5):
    a=cv2.GaussianBlur(a,(0,0),soft)*op
    f=img.astype(np.float32); mul=f*(INK/255.0)*1.15
    return (f*(1-a[...,None])+mul*a[...,None]).clip(0,255).astype(np.uint8)
def light(img,a,col,op=.88,soft=.45,region=None):
    a=cv2.GaussianBlur(a,(0,0),soft)*op
    f=img.astype(np.float32)
    lum=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).astype(np.float32),(0,0),6)
    ref=np.median(lum[a>0.2]) if (a>0.2).any() else lum.mean()
    shade=(lum/ref)**0.5
    c=(col[None,None,:]*shade[...,None]).clip(0,255)
    return (f*(1-a[...,None])+c*a[...,None]).clip(0,255).astype(np.uint8)
def load(i): return cv2.cvtColor(cv2.imread(MK+f'clean{i}.png'),cv2.COLOR_BGR2RGB)
TALL={'arche','an','tige'}
TAG_VI='Vẻ đẹp là sự tự do cảm xúc'
def box(key):
    img=load(1); W,H=816,1356
    d=Decal(W,H)
    if key in TALL: a=fit(key,'main',W*.64,H*.48)
    else: a=fit(key,'main',W*.66,H*.30)
    d.paste_c(a,W/2,H*.40)
    d.text('BOUQUET DE SAISON',F('bvp-med.ttf',27),W/2,H*.86,track=9)
    d.text(TAG_VI,F('fr-soft-it.ttf',38),W/2,H*.91)
    img=ink(img,warp(d,[(366,524),(567,522),(567,858),(366,860)],img.shape),op=.88,soft=.55)
    return img
def bag(key):
    img=load(3); W,H=1216,1064; d=Decal(W,H)
    if key in TALL: a=fit(key,'main',W*.46,H*.62)
    else: a=fit(key,'main',W*.50,H*.34)
    d.paste_c(a,W/2,H*.44)
    d.text('FLEURISTE  ·  '+TAG_VI.upper(),F('bvp-light.ttf',26),W/2,H*.88,track=5)
    return ink(img,warp(d,[(306,548),(609,548),(606,811),(303,814)],img.shape),op=.9,soft=.5)
def shop(key):
    img=load(2)
    # valance band: horizontal lockup + services
    W,H=3032,140; d=Decal(W,H)
    a=fit(key,'line',1200,H*.62); d.paste(a,92,(H-a.height)/2)
    d.text('FLEURS DE SAISON  ·  BOUQUETS  ·  ATELIERS',F('bvp-light.ttf',38),W-92,H/2,anchor='rm',track=8)
    img=light(img,warp(d,[(82,541),(840,541),(840,576),(82,576)],img.shape),CREAM,op=.86)
    # awning slope: the brand line, set small like the original
    W,H=1200,320; d=Decal(W,H)
    d.text(TAG_VI,F('fr-soft-it.ttf',58),20,70,anchor='lm')
    d.text('La beauté est la liberté des émotions,',F('fr-soft.ttf',44),20,160,anchor='lm')
    d.text('la beauté n’a pas de cadre.',F('fr-soft.ttf',44),20,222,anchor='lm')
    img=light(img,warp(d,[(112,428),(412,428),(410,508),(110,508)],img.shape),CREAM,op=.8)
    # glass left pane: the mark as white vinyl
    W,H=900,1280; d=Decal(W,H)
    d.text('FLEURISTE',F('bvp-light.ttf',40),W/2,92,track=14)
    if key in TALL: a=fit(key,'main',W*.62,H*.50)
    else: a=fit(key,'main',W*.78,H*.30)
    d.paste_c(a,W/2,H*.40 if key not in TALL else H*.45)
    d.text('@loi.fleur',F('bvp-light.ttf',40),W/2,H-110,track=4)
    img=light(img,warp(d,[(364,642),(589,642),(589,962),(364,962)],img.shape),VINYL,op=.9)
    # glass right pane: what the shop does, hours
    W,H=932,1280; d=Decal(W,H)
    d.text('FLEURISTE',F('bvp-light.ttf',40),W/2,92,track=14)
    fs=F('fr-soft.ttf',84)
    d.text('Fleurs de saison',fs,60,320,anchor='lm'); d.text('& bouquets libres',fs,60,420,anchor='lm')
    d.text('MAR — DIM   ·   9H — 19H',F('bvp-light.ttf',40),W/2,H-110,track=6)
    img=light(img,warp(d,[(597,642),(830,642),(830,962),(597,962)],img.shape),VINYL,op=.9)
    return img
def laptop(key):
    img=load(4); W,H=1600,1260
    scr=Image.new('RGB',(W,H),(238,231,218)); dr=ImageDraw.Draw(scr)
    def put(a,cx,cy,col):
        layer=Image.new('RGB',a.size,col); scr.paste(layer,(int(cx-a.width/2),int(cy-a.height/2)),a)
    ln=fit(key,'line',360,58); put(ln,90+ln.width/2,96,(31,30,26))
    f=F('bvp-light.ttf',34)
    for i,t in enumerate(['Bouquets','Ateliers','Mariages','Contact']):
        dr.text((W-90-(3-i)*200,96),t,font=f,fill=(31,30,26),anchor='rm')
    dr.rectangle((0,170,W,H),fill=(75,81,56))
    a=fit(key,'main',W*.42 if key not in TALL else W*.30,H*.40); put(a,W/2,H*.47,(236,229,214))
    dr.text((W/2,H*.78),TAG_VI,font=F('fr-soft-it.ttf',50),fill=(236,229,214),anchor='mm')
    bx=(W/2-190,H*.85,W/2+190,H*.85+84); dr.rectangle(bx,outline=(236,229,214),width=3)
    dr.text((W/2,H*.85+42),'COMMANDER UN BOUQUET',font=F('bvp-med.ttf',28),fill=(236,229,214),anchor='mm')
    s=np.array(scr,np.float32)
    quad=[(510,644),(697,650),(689,806),(495,796)]
    src=np.float32([[0,0],[W,0],[W,H],[0,H]]); M=cv2.getPerspectiveTransform(src,np.float32(quad))
    warped=cv2.warpPerspective(s,M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
    m=cv2.warpPerspective(np.ones((H,W),np.float32),M,(img.shape[1],img.shape[0]),flags=cv2.INTER_AREA)
    lum=cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).astype(np.float32),(0,0),9)
    ref=np.median(lum[m>.9]); shade=(lum/ref).clip(.6,1.2)**.6*0.93
    out=img.astype(np.float32)*(1-m[...,None])+(warped*shade[...,None])*m[...,None]
    return out.clip(0,255).astype(np.uint8)
FN={'boite':box,'devanture':shop,'sac':bag,'ecran':laptop}
if __name__=='__main__':
    import sys
    keys=sys.argv[1:] or list(CON)
    for k in keys:
        for name,fn in FN.items():
            im=fn(k); Image.fromarray(im).save(OUT+f'{k}-{name}.jpg',quality=86)
    print('done',keys)
