import cv2, numpy as np
from clean import text_mask, rect_mask, grain, inpaint, smooth_fill
IMG='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/images/'
OUT='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/mk/'
def load(i): return cv2.cvtColor(cv2.imread(IMG+f'{i}.webp'),cv2.COLOR_BGR2RGB)
def save(i,im): cv2.imwrite(OUT+f'clean{i}.png',cv2.cvtColor(im,cv2.COLOR_RGB2BGR))
def aniso_fill(img,mask,sx,sy,surf):
    m=(mask==0).astype(np.float32); s=np.zeros_like(m); x0,y0,x1,y1=surf; s[y0:y1,x0:x1]=1; m*=s
    num=cv2.GaussianBlur(img.astype(np.float32)*m[...,None],(0,0),sigmaX=sx,sigmaY=sy)
    den=cv2.GaussianBlur(m,(0,0),sigmaX=sx,sigmaY=sy)[...,None]+1e-6
    out=img.astype(np.float32); mm=(mask>0)[...,None]
    return np.where(mm,num/den,out).astype(np.uint8)
# 5 · ribbed glass door: cream text, vertical ribs -> fill along the ribs
im=load(5)
m=text_mask(im,(530,340,1013,450),'light',14,3)|text_mask(im,(440,580,1013,775),'light',14,4)|text_mask(im,(630,905,910,1005),'light',12,3)
im=aniso_fill(im,m,2.5,26,(306,0,1013,1350)); im=grain(im,m,(560,470,760,560),5); save(5,im)
# 6 · aluminium can: fill along the vertical highlights
im=load(6)
m=rect_mask(im.shape,(445,778,600,845))|rect_mask(im.shape,(362,842,660,1065))|rect_mask(im.shape,(452,1080,595,1160))
can=np.zeros(im.shape[:2],np.uint8); can[:, 366:680]=255
m=m&can
im=aniso_fill(im,m,1.6,60,(366,720,680,1195)); im=grain(im,m,(600,880,660,1000),6); save(6,im)
# 7 · shop window: peach lettering over plants -> colour mask + inpaint
im=load(7)
f=im.astype(np.int32); R,G,Bc=f[...,0],f[...,1],f[...,2]
peach=((R>150)&(R-Bc>45)&(R-G>15)&(R-G<75)&(G>110)).astype(np.uint8)*255
zone=np.zeros_like(peach)
for x0,y0,x1,y1 in [(405,38,655,92),(295,430,670,715),(380,1072,680,1125)]: zone[y0:y1,x0:x1]=255
m=cv2.dilate(peach&zone,np.ones((5,5),np.uint8))
im=cv2.inpaint(im,m,5,cv2.INPAINT_TELEA); save(7,im)
# 8 · round hanging sign: flat terracotta disc
im=load(8)
m=text_mask(im,(580,320,750,392),'light',12,3)|text_mask(im,(540,430,795,610),'light',12,4)|text_mask(im,(570,640,770,720),'light',12,3)
disc=np.zeros(im.shape[:2],np.uint8); cv2.ellipse(disc,(668,518),(232,222),0,0,360,255,-1)
mm=(m&disc)
w=(mm==0)&(disc>0)
num=cv2.GaussianBlur(im.astype(np.float32)*w[...,None],(0,0),18); den=cv2.GaussianBlur(w.astype(np.float32),(0,0),18)[...,None]+1e-6
im=np.where((mm>0)[...,None],num/den,im).astype(np.uint8); im=grain(im,mm,(470,600,560,720),7); save(8,im)
# --- second pass ---
# 6 · can: rebuild the label zone from the cylinder's own column profile (top band -> bottom band)
im=load(6).astype(np.float32)
x0,x1,y0,y1=364,682,776,1162
top=im[738:772,x0:x1].mean(0); bot=im[1164:1180,x0:x1].mean(0)
t=((np.arange(y0,y1)-755)/(1172-755))[:,None,None]
fill=top[None]*(1-t)+bot[None]*t
orig=load(6)
# feather the side edges so the can silhouette stays untouched
a=np.zeros((y1-y0,x1-x0),np.float32); a[:,6:-6]=1; a=cv2.GaussianBlur(a,(0,0),2)
a[:8]*=np.linspace(0,1,8)[:,None]; a[-8:]*=np.linspace(1,0,8)[:,None]
im[y0:y1,x0:x1]=fill*a[...,None]+im[y0:y1,x0:x1]*(1-a[...,None])
im=im.clip(0,255).astype(np.uint8)
m=np.zeros(im.shape[:2],np.uint8); m[y0+8:y1-8,x0+8:x1-8]=255
im=grain(im,m,(600,880,660,1000),6); save(6,im)
# 8 · sign: wipe the whole lettering zone inside the disc
im=load(8)
disc=np.zeros(im.shape[:2],np.uint8); cv2.ellipse(disc,(668,518),(232,222),0,0,360,255,-1)
mm=(rect_mask(im.shape,(570,318,770,395))|rect_mask(im.shape,(530,425,805,615))|rect_mask(im.shape,(560,635,780,722)))&disc
w=(mm==0)&(disc>0)
num=cv2.GaussianBlur(im.astype(np.float32)*w[...,None],(0,0),30); den=cv2.GaussianBlur(w.astype(np.float32),(0,0),30)[...,None]+1e-6
im=np.where((mm>0)[...,None],num/den,im).astype(np.float32)
rng=np.random.default_rng(8); n=cv2.GaussianBlur(rng.normal(0,2.2,im.shape[:2]).astype(np.float32),(0,0),0.7)
mf=cv2.GaussianBlur(mm,(0,0),2)/255.0
im=(im+(n*mf)[...,None]).clip(0,255).astype(np.uint8); save(8,im)
