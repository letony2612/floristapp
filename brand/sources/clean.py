import cv2, numpy as np
IMG='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/images/'
OUT='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/mk/'
def load(i): return cv2.cvtColor(cv2.imread(IMG+f'{i}.webp'),cv2.COLOR_BGR2RGB) if cv2.imread(IMG+f'{i}.webp') is not None else None
def text_mask(img, box, mode, thr, dil=3):
    x0,y0,x1,y1=box
    g=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY).astype(np.float32)
    bg=cv2.medianBlur(g.astype(np.uint8),31).astype(np.float32)
    diff=(bg-g) if mode=='dark' else (g-bg)
    m=np.zeros(g.shape,np.uint8)
    sub=(diff[y0:y1,x0:x1]>thr).astype(np.uint8)*255
    m[y0:y1,x0:x1]=sub
    if dil: m=cv2.dilate(m,np.ones((dil*2+1,dil*2+1),np.uint8))
    return m
def rect_mask(shape, box):
    m=np.zeros(shape[:2],np.uint8); x0,y0,x1,y1=box; m[y0:y1,x0:x1]=255; return m
def grain(img, mask, ref_box, seed=0):
    # re-add surface texture lost by inpainting, sampled from a clean patch
    x0,y0,x1,y1=ref_box
    patch=img[y0:y1,x0:x1].astype(np.float32)
    hp=patch-cv2.GaussianBlur(patch,(0,0),3)
    h,w=img.shape[:2]; rng=np.random.default_rng(seed)
    tile=np.zeros((h,w,3),np.float32)
    ph,pw=hp.shape[:2]
    for yy in range(0,h,ph):
        for xx in range(0,w,pw):
            p=hp[::(1 if rng.random()<.5 else -1),::(1 if rng.random()<.5 else -1)]
            tile[yy:yy+ph,xx:xx+pw]=p[:min(ph,h-yy),:min(pw,w-xx)]
    out=img.astype(np.float32)
    mm=(cv2.GaussianBlur(mask,(0,0),1.5)/255.0)[...,None]
    out=out+tile*mm
    return np.clip(out,0,255).astype(np.uint8)
def inpaint(img,mask,r=6):
    return cv2.inpaint(img,mask,r,cv2.INPAINT_TELEA)
def smooth_fill(img, mask, sigma=12, surf=None):
    # normalized-convolution fill: good for flat surfaces with gentle light gradients
    m=(mask==0).astype(np.float32)
    if surf is not None:
        x0,y0,x1,y1=surf; s=np.zeros_like(m); s[y0:y1,x0:x1]=1; m*=s
        mask=mask.copy(); keep=np.zeros_like(mask); keep[y0:y1,x0:x1]=1; mask*=keep
    num=cv2.GaussianBlur(img.astype(np.float32)*m[...,None],(0,0),sigma)
    den=cv2.GaussianBlur(m,(0,0),sigma)[...,None]+1e-6
    fill=num/den
    out=img.copy().astype(np.float32)
    mm=(mask>0)[...,None]
    out=np.where(mm,fill,out)
    return out.astype(np.uint8)
res={}
# 1 · box
im=load(1)
m=text_mask(im,(372,532,560,668),'dark',14,3)|text_mask(im,(375,757,465,845),'dark',14,4)
im=smooth_fill(im,m,10,(368,528,566,857)); im=grain(im,m,(420,690,540,750),1)
ms=rect_mask(im.shape,(573,758,599,834)); im=smooth_fill(im,ms,7,(571,700,601,850)); im=grain(im,ms,(420,690,540,750),4); res[1]=im
# 2 · storefront
im=load(2)
m=text_mask(im,(100,428,405,500),'light',10,3)|text_mask(im,(98,543,280,574),'light',12,3)
im=smooth_fill(im,m,9); im=grain(im,m,(450,440,600,500),2)
g=np.zeros(im.shape[:2],np.uint8)
x0,y0,x1,y1=372,846,500,944; dx=226
patch=im[y0:y1,x0+dx:x1+dx].copy()
a=np.zeros((y1-y0,x1-x0),np.float32); a[4:-4,4:-4]=1; a=cv2.GaussianBlur(a,(0,0),2)[...,None]
im[y0:y1,x0:x1]=(patch*a+im[y0:y1,x0:x1]*(1-a)).astype(np.uint8)
for b in [(372,660,484,686),(596,660,707,686),(375,712,550,773),(599,712,772,773),(372,940,500,968),(599,942,728,970)]:
    g|=text_mask(im,b,'light',16,2)
im=cv2.inpaint(im,g,4,cv2.INPAINT_NS); res[2]=im
# 3 · bag
im=load(3)
m=rect_mask(im.shape,(312,551,512,697))|rect_mask(im.shape,(312,712,410,808))
im=smooth_fill(im,m,45,(307,549,607,810)); im=grain(im,m,(450,720,580,790),3); res[3]=im
# 4 · laptop: screen is replaced later, keep as is
res[4]=load(4)
for i,im in res.items(): cv2.imwrite(OUT+f'clean{i}.png',cv2.cvtColor(im,cv2.COLOR_RGB2BGR))
