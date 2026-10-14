import json, math
from glyphs import text_path
F='Inter-wght-600.ttf'; R='Inter-wght-400.ttf'; S='Allura.ttf'
C='currentColor'
RED='style="fill:var(--red,#FF3B30)"'; STAMP='style="fill:var(--stamp,#2A44D8)"'
GUIDE_S='style="stroke:var(--guide,#8F9BFF)"'; GUIDE_F='style="fill:var(--guide,#8F9BFF)"'
T=-5   # tight tracking, like the site's headings
def P(d,extra=''): return f'<path d="{d}" fill="{C}" {extra}/>'
def word(text,x=0,font=F,size=200,track=T):
    d,w,b=text_path(font,text,size,x,200,tracking=track); return d,w,b
out={}
# advance helpers
_,w_nappl,_=word('nappl'); xi=w_nappl+T
_,w_n,_=word('n'); _,w_na,_=word('na'); _,w_nap,_=word('nap')
d_all,W,_=word('nappli')
VBW=f'-14 34 {W+28:.0f} 226'          # standard wordmark viewBox (ascender to descender)

# 1 · PASTILLE — the i's dot becomes a notification badge
d1,_,_=word('nappl'); di,_,_=word('ı',xi)
cx=xi+26.2
out['pastille']=dict(main=(VBW,P(d1)+P(di)+f'<circle cx="{cx:.1f}" cy="63" r="15.5" {RED}/>'),
  icon=('-14 52 150 150',P(word('n')[0])+f'<circle cx="114" cy="84" r="16" {RED}/>'))

# 2 · ÉCRAN — the n's arch is the top of a phone, with its island
pill=lambda x,y,w,h: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{C}"/>'
# custom n drawn as a phone top: same stem weight as Inter SemiBold
dapp,_,_=word('appli',w_n+T)
n_phone='<path d="M26 200V137.5a35.25 35.25 0 0 1 70.5 0V200" fill="none" stroke="currentColor" stroke-width="25"/>'
out['ecran']=dict(main=(VBW,n_phone+pill(50.25,119,22,9)+P(dapp)),
  icon=('0 0 100 100','<path d="M28 80V45a22 22 0 0 1 44 0v35" fill="none" stroke="currentColor" stroke-width="13" stroke-linecap="round"/>'+pill(41.5,31.5,17,6.5)))

# 3 · ESQUISSE — first p is a sketch, second p is built
dna,_,_=word('na'); dp1,_,_=word('p',w_na+T); dpli,_,_=word('pli',w_nap+T)
out['esquisse']=dict(main=(VBW,P(dna)+f'<path d="{dp1}" fill="none" stroke-width="3.2" stroke-linejoin="round" {GUIDE_S}/>'+P(dpli)),
  icon=('-4 66 266 196',f'<path d="{word("p")[0]}" fill="none" stroke-width="4" stroke-linejoin="round" {GUIDE_S}/>'+P(word('p',132)[0])))

# 4 · REPÈRES — construction lines stay visible
g=lambda y,x0,x1: f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke-width="1.3" {GUIDE_S}/>'
v=lambda x,y0,y1: f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke-width="1.3" {GUIDE_S}/>'
lab,_,_=text_path(R,'r 20',15,W+6,84)
d4,_,_=word('nappli')
guides=g(200,-40,W+40)+g(89.5,-40,W+40)+g(54.5,-40,W+40)+v(13.5,20,240)+f'<circle cx="61" cy="137" r="47.5" fill="none" stroke-width="1.3" stroke-dasharray="3 4" {GUIDE_S}/>'
out['reperes']=dict(main=(f'-46 14 {W+92:.0f} 246',guides+P(d4)+f'<path d="{lab}" {GUIDE_F}/>'),
  icon=('-30 40 182 182',g(200,-30,152)+g(89.5,-30,152)+v(13.5,40,222)+v(108.9,40,222)+f'<circle cx="61" cy="137" r="47.5" fill="none" stroke-width="1.6" stroke-dasharray="3 4" {GUIDE_S}/>'+P(word('n')[0])))

# 5 · SIGNÉ — Inter for the work, a handwritten signature for the person
ds,ws,bs=text_path(S,'studio',118,0,0)
sx=W-ws+64; sy=292
d5,_,_=word('nappli')
sig=f'<g transform="translate({sx:.1f} {sy}) rotate(-7)"><path d="{text_path(S,"studio",118,0,0)[0]}" {STAMP}/></g>'
out['signe']=dict(main=(f'-14 34 {W+86:.0f} 286',P(d5)+sig),
  icon=('-6 64 140 140',P(word('n')[0])+f'<path d="M6 226 C40 214 84 212 128 194 C88 216 44 224 6 230 Z" transform="translate(0 -20)" {STAMP}/>'))

# 6 · CURSEUR — the i is a blinking caret
d6,_,_=word('nappl')
caret=lambda x: f'<rect class="caret" x="{x:.1f}" y="52" width="10" height="190" rx="5" {STAMP}/>'
out['curseur']=dict(main=(VBW,P(d6)+caret(xi+21)),
  icon=('-10 40 180 180',P(word('n')[0])+caret(132)))

json.dump(out,open('nconcepts.json','w'))
if __name__=='__main__':
    import cairosvg
    from PIL import Image
    def fixed(body): return (body.replace('var(--red,#FF3B30)','#FF3B30').replace('var(--stamp,#2A44D8)','#2A44D8').replace('var(--guide,#8F9BFF)','#8F9BFF').replace('currentColor','#000'))
    sheet=Image.new('RGB',(1500,1000),(255,255,255))
    for i,(k,v) in enumerate(out.items()):
        for j,kind in enumerate(('main','icon')):
            vb,body=v[kind]
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{fixed(body)}</svg>'
            open(f'n-{k}-{kind}.svg','w').write(svg)
            cairosvg.svg2png(bytestring=svg.encode(),write_to=f'n-{k}-{kind}.png',output_width=420 if kind=='main' else 120)
            im=Image.open(f'n-{k}-{kind}.png')
            x=(i%3)*500+30+(0 if kind=='main' else 0); y=(i//3)*500+40+(0 if kind=='main' else 260)
            sheet.paste(im,(x,y),im)
    sheet.save('nsheet.png')
