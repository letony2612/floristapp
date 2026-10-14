import sys, numpy as np, cv2
from PIL import Image
from composite import Decal, fit, light, ink, F, warp, TALL, CON, MK, VINYL, CREAM
OUT='/home/user/floristapp/brand/mockups/'
SIGN='Made by Nappli'
def load(i): return cv2.cvtColor(cv2.imread(MK+f'clean{i}.png'),cv2.COLOR_BGR2RGB)
def place_logo(d,key,cx,cy,maxw_wide,maxh_wide,maxw_tall,maxh_tall):
    a=fit(key,'main',maxw_tall,maxh_tall) if key in TALL else fit(key,'main',maxw_wide,maxh_wide)
    d.paste_c(a,cx,cy)
def porte(key):
    img=load(5); x0,y0,x1,y1=440,320,1000,1020; W,H=(x1-x0)*2,(y1-y0)*2; d=Decal(W,H)
    d.text('FLEURISTE',F('bvp-light.ttf',34),W/2,110,track=12)
    d.text('VẺ ĐẸP KHÔNG KHUÔN KHỔ',F('bvp-light.ttf',30),W/2,170,track=8)
    place_logo(d,key,W/2,730,780,440,560,620)
    d.text(SIGN,F('fr-soft.ttf',50),W/2,1250)
    return light(img,warp(d,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],img.shape),VINYL,op=.9,soft=.7)
def canette(key):
    img=load(6); cx,R=523,159; y0,y1=770,1170
    W,H=900,(y1-y0)*2; d=Decal(W,H)
    d.text(SIGN,F('fr-soft.ttf',33),W/2,72)
    place_logo(d,key,W/2,385,440,300,330,430)
    d.text('fleurs de saison',F('fr-soft-it.ttf',36),W/2,712)
    a=np.array(d.im,np.float32)/255
    ys,xs=np.mgrid[0:img.shape[0],0:img.shape[1]].astype(np.float32)
    s=np.clip((xs-cx)/R,-.999,.999); th=np.arcsin(s)
    mapx=(W/2+th*R*2).astype(np.float32); mapy=((ys-y0)*2).astype(np.float32)
    out=cv2.remap(a,mapx,mapy,cv2.INTER_LINEAR,borderValue=0)
    out[:, :cx-R+4]=0; out[:, cx+R-4:]=0; out[:y0]=0; out[y1:]=0
    out*=np.clip(np.cos(th)*1.6,0,1)   # ink fades into the curve
    return ink(img,out,op=.92,soft=.5)
def vitrine(key):
    img=load(7); x0,y0,x1,y1=280,30,780,1140; W,H=(x1-x0)*2,(y1-y0)*2; d=Decal(W,H)
    d.text(SIGN,F('fr-soft.ttf',60),W/2,72)
    place_logo(d,key,W/2,1090,700,420,520,640)
    d.text('Fleurs · Plantes · Ateliers',F('fr-soft.ttf',56),W/2,2140)
    return light(img,warp(d,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],img.shape),VINYL,op=.92,soft=.6)
def enseigne(key):
    img=load(8); x0,y0,x1,y1=428,290,908,746; W=H=960; d=Decal(W,H)
    d.text(SIGN,F('fr-soft.ttf',52),W/2,110 if key=='an' else 150)
    if key=='an': a=fit(key,'main',570,570); d.paste_c(a,W/2,H/2+8)
    else: place_logo(d,key,W/2,H*.5,600,300,420,440)
    d.text('Fleuriste',F('fr-soft-it.ttf',50),W/2,H*.87 if key=='an' else H*.84)
    return light(img,warp(d,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],img.shape),CREAM,op=.93,soft=.6)
FN={'porte':porte,'canette':canette,'vitrine':vitrine,'enseigne':enseigne}
if __name__=='__main__':
    ks=sys.argv[1:] or list(CON)
    for k in ks:
        for n,fn in FN.items():
            Image.fromarray(fn(k)).save(OUT+f'{k}-{n}.jpg',quality=84,optimize=True,progressive=True)
    print('ok',ks)
