import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
FD='/tmp/claude-0/-home-user-floristapp/610656c1-7c28-5e23-9b56-a3d8582b25a7/scratchpad/fonts/'
_cache={}
def font(name):
    if name not in _cache: _cache[name]=TTFont(FD+name)
    return _cache[name]
def text_path(name, text, size, x=0, y=0, tracking=0):
    """Return (svg path d, width, bounds) with baseline at y, y-down coords."""
    f=font(name); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    s=size/upm; pen=SVGPathPen(gs); cx=0; bp=BoundsPen(gs)
    for i,ch in enumerate(text):
        g=cmap[ord(ch)]
        t=(s,0,0,-s,x+cx,y)
        gs[g].draw(TransformPen(pen,t)); gs[g].draw(TransformPen(bp,t))
        cx+=gs[g].width*s+(tracking if i<len(text)-1 else 0)
    return pen.getCommands(), cx, bp.bounds
if __name__=='__main__':
    for ch in 'LOIƠ':
        d,w,b=text_path('fr-soft.ttf',ch,1000)
        print(ch,round(w),[round(v) for v in b])
