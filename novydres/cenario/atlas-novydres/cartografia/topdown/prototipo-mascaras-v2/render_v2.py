#!/usr/bin/env python3
"""POC V2: 7 autonomous illustrated 2.5D building assets; no edits to U02.

Uses a fixed oblique projection per building, parent lot masking, independent
artwork, and pixelwise validation. Requires pillow, numpy, shapely.
Run: python render_v2.py --base /path/T03_U02_aprovada.png
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, random, base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from shapely.geometry import Polygon, MultiPoint

ROOT=Path(__file__).resolve().parent
CFG=json.loads((ROOT/'geometria_v2.json').read_text(encoding='utf-8'))
NODES={n['id']:n for n in CFG['hierarchy']}
BLDGS=[n for n in CFG['hierarchy'] if n['type']=='building']
LOTS=[NODES['lot-a'],NODES['lot-b']]
CROP=CFG['render']['crop_xyxy'];S=CFG['render']['detail_scale']
W=int((CROP[2]-CROP[0])*S);H=int((CROP[3]-CROP[1])*S)
SIL=(8,17,22,255)
PALS={
 'slate': {'roof':(57,75,85,255),'light':(90,114,124,255),'shade':(35,52,65,255),'wall_s':(91,93,90,255),'wall_e':(61,69,72,255),'edge':(149,159,158,255),'window':(217,163,94,255)},
 'terracotta':{'roof':(110,66,63,255),'light':(151,100,86,255),'shade':(68,45,56,255),'wall_s':(105,92,82,255),'wall_e':(68,66,69,255),'edge':(181,153,137,255),'window':(245,185,110,255)},
 'copper':{'roof':(41,108,107,255),'light':(96,163,150,255),'shade':(27,75,81,255),'wall_s':(91,102,94,255),'wall_e':(51,77,77,255),'edge':(153,198,183,255),'window':(241,193,113,255)}
}

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def wp(point):return (round((point[0]-CROP[0])*S),round((point[1]-CROP[1])*S))
def poly(pts):return [wp(p) for p in pts]
def png_bytes(image):
    b=io.BytesIO();image.save(b,format='PNG',compress_level=8);return b.getvalue()
def rgba():return Image.new('RGBA',(W,H),(0,0,0,0))
def F(a,b,t):return (a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t)
def line(d,p,q,c,w=.07):d.line([wp(p),wp(q)],fill=c,width=max(1,round(S*w)))
def polygon_mask(pts):
    m=Image.new('L',(W,H),0);ImageDraw.Draw(m).polygon(poly(pts),fill=255);return m

def project(n):
    x0,y0,x1,y1=n['footprint_px']; factor=n['height_factor']
    # Roof setback is illustrated inside the immutable experimental footprint.
    # This is a 2.5D drawing convention, NOT cadastral 3D or physical height.
    sx,sy=CFG['render']['roof_inset_east_south_px'];sx*=factor;sy*=factor
    tL=(x0+.10,y0+.10);tR=(x1-sx,y0+.10)
    bR=(x1-sx,y1-sy);bL=(x0+.10,y1-sy)
    fL=(x0,y0);fR=(x1,y0);fbR=(x1,y1);fbL=(x0,y1)
    points=[tL,tR,bR,bL,fL,fR,fbR,fbL]
    hull=MultiPoint(points).convex_hull.buffer(.035,cap_style=3,join_style=2)
    return {'top':[tL,tR,bR,bL],'base':[fL,fR,fbR,fbL],
            'south':[bL,bR,fbR,fbL],'east':[tR,bR,fbR,fR],
            'hull':hull,'polygon':list(hull.exterior.coords)[:-1],
            'offset':[round(sx,4),round(sy,4)]}

def draw_windows(d,pts,wall_type,p):
    # Uniform south/east facade fenestration; all openings remain within facade.
    c=p['window'];trace=p['edge'];dark=(19,31,37,255)
    A,B,C,D=pts # four corners (top left, top right, bottom right, bottom left)
    # limit count and placements: window sizes are illustrative, not architectural measurements.
    width=math.dist(A,B)
    count=max(2,min(9,int(width/1.45))) if wall_type=='south' else max(2,min(8,int(width/1.25)))
    for k in range(count):
        t=(k+.5)/count
        tl=F(A,B,t-.22/count);tr=F(A,B,t+.22/count)
        br=F(D,C,t+.22/count);bl=F(D,C,t-.22/count)
        for floor in range(2):
            top=.19+floor*.39
            bot=top+.20
            q=[F(tl,bl,top),F(tr,br,top),F(tr,br,bot),F(tl,bl,bot)]
            d.polygon(poly(q),fill=dark)
            d.line(poly(q+[q[0]]),fill=trace,width=1)
            if (k+floor)%3!=0:
                d.polygon(poly([F(q[0],q[2],.15),F(q[1],q[3],.15),F(q[1],q[3],.80),F(q[0],q[2],.80)]),fill=c)
    line(d,F(A,D,.50),F(B,C,.50),trace,.045)
    line(d,F(A,D,.82),F(B,C,.82),trace,.045)

def roof_facets(d,n,pts,p,style,rng):
    x0,y0,x1,y1=n['footprint_px']; (tl,tr,br,bl)=pts
    w=x1-x0;h=y1-y0
    d.polygon(poly(pts),fill=p['roof'])
    if style in ('gable','mansard','copper'):
        if h>=w:
            ridge0=F(tl,tr,.52); ridge1=F(bl,br,.52)
            left=[tl,ridge0,ridge1,bl];right=[ridge0,tr,br,ridge1]
            d.polygon(poly(left),fill=p['light']);d.polygon(poly(right),fill=p['shade'])
            line(d,ridge0,ridge1,p['edge'],.12)
            if style=='mansard':
                line(d,F(tl,tr,.12),F(bl,br,.12),p['edge'],.08)
                line(d,F(tl,tr,.88),F(bl,br,.88),p['edge'],.08)
            for yy in np.linspace(y0+.55,y1-.55,int(max(4,h*1.3))):
                for a,b in [(tl,bl),(ridge0,ridge1),(tr,br)]:
                    pass
                frac=(yy-y0)/(y1-y0)
                seg0=F(tl,bl,frac);seg1=F(ridge0,ridge1,frac);seg2=F(tr,br,frac)
                line(d,F(seg0,seg1,.16),F(seg0,seg1,.84),(30,44,51,145),.035)
                line(d,F(seg1,seg2,.16),F(seg1,seg2,.84),(155,167,163,115),.035)
        else:
            r0=F(tl,bl,.48);r1=F(tr,br,.48)
            d.polygon(poly([tl,tr,r1,r0]),fill=p['light']);d.polygon(poly([r0,r1,br,bl]),fill=p['shade'])
            line(d,r0,r1,p['edge'],.12)
            for xx in np.linspace(0.2,.8,int(max(4,w*.7))):
                line(d,F(tl,tr,xx),F(r0,r1,xx),(31,45,50,105),.04)
                line(d,F(r0,r1,xx),F(bl,br,xx),(161,164,153,90),.04)
    elif style=='industrial_sawtooth':
        d.polygon(poly([tl,tr,br,bl]),fill=p['shade'])
        count=7
        for i in range(1,count):
            t=i/count;A=F(tl,tr,t);B=F(bl,br,t)
            line(d,A,B,p['edge'],.11)
            lit=F(tl,tr,t-.065);lit2=F(bl,br,t-.065)
            line(d,lit,lit2,(147,181,190,230),.16)
        for i in range(24):
            t=rng.uniform(.08,.92);u=rng.uniform(.09,.91)
            A=F(F(tl,tr,t),F(bl,br,t),u)
            line(d,A,(A[0]+.35,A[1]),(109,141,150,180),.05)
    else:
        d.polygon(poly([tl,tr,br,bl]),fill=p['shade'])
        inset=.10
        inside=[(tl[0]+inset,tl[1]+inset),(tr[0]-inset,tr[1]+inset),(br[0]-inset,br[1]-inset),(bl[0]+inset,bl[1]-inset)]
        d.polygon(poly(inside),fill=p['light'])
        d.line(poly(inside+[inside[0]]),fill=p['edge'],width=2)
        for k in range(3):
            xx=tl[0]+1.1+k*(w-2.3)/3
            yy=tl[1]+2.3+(k%2)*2
            d.rectangle((*wp((xx,yy)),*wp((xx+.55,yy+.9))),fill=(24,45,57,255),outline=p['edge'],width=1)

    # Individual quirks — architectural props are decorative, not canon location/POIs.
    if style=='copper':
        # Decorative dormers and patina on B2 candidate; no new footprint.
        for k in range(3):
            yy=tl[1]+2.2+k*(h-3.6)/3
            xx=tl[0]+1.5
            d.polygon(poly([(xx-.65,yy+.35),(xx,yy-.30),(xx+.68,yy+.35)]),fill=(121,187,166,255))
            d.rectangle((*wp((xx-.33,yy+.35)),*wp((xx+.36,yy+.76))),fill=(27,50,58,255),outline=p['edge'],width=1)
        for i in range(20):
            xx=rng.uniform(tl[0]+.6,tr[0]-.6);yy=rng.uniform(tl[1]+.7,bl[1]-.7)
            line(d,(xx,yy),(xx+.20,yy+.04),(137,201,177,155),.04)
    elif style=='mansard':
        for k in range(3):
            t=(k+.6)/3.6
            xx=tl[0]+1.0+k*(w-1.9)/3.5
            yy=tl[1]+h*.22
            d.polygon(poly([(xx-.34,yy+.25),(xx,yy-.16),(xx+.36,yy+.25)]),fill=p['edge'])
            d.rectangle((*wp((xx-.25,yy+.2)),*wp((xx+.25,yy+.51))),fill=(24,40,47,255))
    elif style=='gable':
        for k in range(2):
            xx=tr[0]-.65-k*.92;yy=tl[1]+1.2+k*.25
            d.rectangle((*wp((xx,yy)),*wp((xx+.31,yy+.48))),fill=(38,45,47,255),outline=p['edge'],width=1)
    elif style=='flat':
        xx=tl[0]+w*.64;yy=tl[1]+h*.55
        d.ellipse((*wp((xx-.65,yy-.48)),*wp((xx+.68,yy+.45))),outline=(183,188,178,255),width=2)
        d.rectangle((*wp((xx-.24,yy-.22)),*wp((xx+.22,yy+.20))),fill=(36,52,57,255))
    # Variety in rooftop fixtures, dirt, chipped snow, without changing external silhouette
    for k in range(12):
        xx=rng.uniform(tl[0]+.45,tr[0]-.45);yy=rng.uniform(tl[1]+.55,bl[1]-.50)
        line(d,(xx,yy),(xx+.12,yy+.02),(184,197,194,90),.03)


def render_building(n,style=None):
    style=style or n['roof_kind']
    g=project(n)
    palette=PALS['copper' if style=='copper' else n['palette']]
    rng=random.Random(sum(map(ord,n['id']))*13 + (919 if style=='copper' else 0))
    canvas=rgba();d=ImageDraw.Draw(canvas,'RGBA')
    # Visible east and south facades, with shared oblique projection.
    d.polygon(poly(g['east']),fill=palette['wall_e']);d.polygon(poly(g['south']),fill=palette['wall_s'])
    for face,side in [('east','east'),('south','south')]:
        p=g[face];draw_windows(d,p,side,palette)
        d.line(poly(p+[p[0]]),fill=palette['edge'],width=1)
    roof_facets(d,n,g['top'],palette,style,rng)
    d.line(poly(g['top']+[g['top'][0]]),fill=palette['edge'],width=1)
    stable=polygon_mask(g['polygon'])
    alpha=np.asarray(canvas.getchannel('A'));clamp=np.asarray(stable)
    canvas.putalpha(Image.fromarray(np.minimum(alpha,clamp).astype('uint8')))
    boxx=stable.getbbox()
    assert boxx and boxx[0]>=0 and boxx[1]>=0 and boxx[2]<=W and boxx[3]<=H
    assert Image.fromarray(np.asarray(canvas.getchannel('A'))).getbbox()
    # Containment at geometric and pixel levels
    lot=Polygon(NODES[n['parent']]['polygon_px'])
    assert lot.covers(g['hull']), f"{n['id']}: projected illustration violates parent lot"
    return canvas.crop(boxx),stable.crop(boxx),boxx,g

def draw_lot(n):
    im=rgba();d=ImageDraw.Draw(im,'RGBA')
    pts=n['polygon_px']
    col=(43,55,65,175) if n['id']=='lot-a' else (48,52,59,172)
    d.polygon(poly(pts),fill=col)
    m=polygon_mask(pts)
    rng=random.Random(120 if n['id']=='lot-a' else 224)
    bounds=Polygon(pts).bounds
    for i in range(190):
        x=rng.uniform(bounds[0],bounds[2]);y=rng.uniform(bounds[1],bounds[3])
        alpha=rng.randint(18,85)
        d.ellipse((*wp((x,y)),*wp((x+.07,y+.07))),fill=(205,216,220,alpha))
    a=np.minimum(np.asarray(im.getchannel('A')),np.asarray(m))
    im.putalpha(Image.fromarray(a.astype('uint8')))
    return im

def paste_tight(composite,asset,row):
    out=rgba();x0,y0,x1,y1=row['bbox_detail_xyxy']
    assert asset.size==(x1-x0,y1-y0)
    out.paste(asset,(x0,y0))
    return Image.alpha_composite(composite,out)

def to_data_uri(im,fmt='WEBP'):
    buf=io.BytesIO();im.save(buf,format=fmt,quality=93,method=6)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()

def build_html(city,stage_lots,stage_edit,z0,z1,z2):
    integral=[to_data_uri(x) for x in [city,stage_lots,stage_edit]]
    detail=[to_data_uri(x) for x in [z0,z1,z2]]
    template='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Novydres • POC V2 • Comparador</title><style>
:root{color-scheme:dark;font-family:system-ui,sans-serif}body{background:#101720;color:#e1e9ee;margin:0;padding:14px}h1{font-size:18px;margin:0 0 8px}.sub{font-size:12px;color:#b2bbc5;margin:0 0 12px}.controls{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}button{background:#283947;color:#e1e9ee;border:1px solid #5a6c7e;border-radius:6px;padding:8px 10px;cursor:pointer}.active{background:#587a80;color:#0b111a}.gallery{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pane{border:1px solid #344655;border-radius:7px;overflow:hidden;background:#0c1218}.pane b{display:block;padding:8px;font-size:12px}.viewport{height:min(67vh,650px);overflow:hidden;position:relative;touch-action:none}.viewport img{display:block;max-width:none;width:100%;height:auto;position:absolute;top:0;left:0;transform-origin:0 0;user-select:none;pointer-events:none}.note{color:#98a9b4;font-size:12px;margin:12px 0}@media(max-width:700px){.gallery{grid-template-columns:1fr}.viewport{height:48vh}}
</style></head><body><h1>POC V2 — máscaras + arquitetura oblíqua 2.5D</h1><p class="sub">Kingswell · U02 íntegra · 7 assets independentes · prédios com fachadas sul/leste</p><div class="controls"><button id="full" class="active">Cidade integral</button><button id="detail">Detalhe 16×</button><button id="lot" class="active">Implantação</button><button id="edit">Microedição B2</button><button id="reset">Repor zoom</button></div><div class="gallery"><div class="pane"><b id="lb1">ANTES — U02 aprovada</b><div class="viewport" id="v1"><img id="i1" alt="mapa original"></div></div><div class="pane"><b id="lb2">DEPOIS — lotes V2</b><div class="viewport" id="v2"><img id="i2" alt="mapa com edifícios"></div></div></div><p class="note">Roda do mouse: zoom. Arraste: navegação. Toque e arraste no celular. Sem geometrias ou rótulos adicionados à imagem.</p><script>
const I=INTEGRAL_DATA;const Z=DETAIL_DATA;let mode='full',variant='lot',scale=1,dx=0,dy=0;const imgs=[document.getElementById('i1'),document.getElementById('i2')];const vp=[document.getElementById('v1'),document.getElementById('v2')];
function reset(){scale=1;dx=0;dy=0;draw()}function draw(){const a=mode==='full'?I:Z;imgs[0].src=a[variant==='lot'?0:1];imgs[1].src=a[variant==='lot'?1:2];document.getElementById('lb1').textContent=variant==='lot'?(mode==='full'?'ANTES — U02 integral':'ANTES — U02 detalhe'):'ANTES — sete edifícios sem editar B2';document.getElementById('lb2').textContent=variant==='lot'?'DEPOIS — sete edifícios oblíquos':'DEPOIS — só B2 alterado (demais idênticos)';imgs.forEach(im=>im.style.transform=`translate(${dx}px,${dy}px) scale(${scale})`);document.querySelectorAll('button').forEach(x=>x.classList.toggle('active',x.id===mode||x.id===variant))}
for(let id of ['full','detail'])document.getElementById(id).onclick=()=>{mode=id;reset()};for(let id of ['lot','edit'])document.getElementById(id).onclick=()=>{variant=id;draw()};document.getElementById('reset').onclick=reset;
vp.forEach(v=>{let pt=null;v.addEventListener('pointerdown',e=>{pt=[e.clientX,e.clientY];v.setPointerCapture(e.pointerId)});v.addEventListener('pointermove',e=>{if(!pt)return;dx+=e.clientX-pt[0];dy+=e.clientY-pt[1];pt=[e.clientX,e.clientY];draw()});v.addEventListener('pointerup',()=>pt=null);v.addEventListener('wheel',e=>{e.preventDefault();scale=Math.max(.5,Math.min(12,scale*(e.deltaY<0?1.2:.8333)));draw()},{passive:false})});draw();
</script></body></html>'''
    return template.replace('INTEGRAL_DATA',json.dumps(integral)).replace('DETAIL_DATA',json.dumps(detail))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',required=True,type=Path);parser.add_argument('--init-assets',action='store_true');parser.add_argument('--edit-b2',action='store_true');args=parser.parse_args()
    if args.init_assets and args.edit_b2:parser.error('Use only one operation')
    source=args.base.read_bytes();assert sha(source)==CFG['base']['sha256'], 'U02 original SHA256 mismatch'
    city=Image.open(io.BytesIO(source)).convert('RGB')
    assert city.size==tuple(CFG['base']['size_px'])
    region=Polygon([(559,660),(1033,660),(1033,1086),(559,1086)])
    hood=Polygon(NODES['neighborhood-ksw-pilot-01']['polygon_px'])
    assert region.covers(hood)
    masks={};rows=[]
    # On micro-edit, never write any non-target assets or their masks.
    protected_paths=[ROOT/n[k] for n in BLDGS for k in ('asset_path','mask_path')]
    protected_before={str(p):sha(p.read_bytes()) for p in protected_paths if p.exists()}
    for n in BLDGS:
        base,stable,boxx,g=render_building(n)
        path=ROOT/n['asset_path'];path.parent.mkdir(parents=True,exist_ok=True)
        mpath=ROOT/n['mask_path'];mpath.parent.mkdir(parents=True,exist_ok=True)
        if args.init_assets:
            path.write_bytes(png_bytes(base));mpath.write_bytes(png_bytes(stable))
        else:
            assert path.is_file() and mpath.is_file(), f'Missing asset {n["id"]}; run --init-assets once'
            assert Image.open(path).size==base.size, f'Asset dimensions changed for {n["id"]}'
            assert png_bytes(Image.open(mpath).convert('L'))==png_bytes(stable), f'Edit mask changed for {n["id"]}'
            alpha=np.asarray(Image.open(path).convert('RGBA').getchannel('A'))
            assert not np.any((alpha>0)&(np.asarray(stable)==0)), f'Asset escapes mask for {n["id"]}'
        masks[n['id']]=stable
        row={'id':n['id'],'parent':n['parent'],'asset':n['asset_path'],'mask':n['mask_path'],
             'bbox_detail_xyxy':list(boxx),'footprint_px':n['footprint_px'],
             'roof_kind':n['roof_kind'],'height_factor':n['height_factor'],
             'projection_offset_px':g['offset'],'asset_sha256':sha(path.read_bytes()),'mask_sha256':sha(mpath.read_bytes()),
             'status':'EXPERIMENTAL_NOT_CANON'}
        rows.append(row)
    b2=next(x for x in rows if x['id']=='b2')
    alt,altmask,altbox,altg=render_building(NODES['b2'],style='copper')
    assert tuple(b2['bbox_detail_xyxy'])==altbox
    assert png_bytes(masks['b2'])==png_bytes(altmask)
    altpath=ROOT/'assets/buildings/b2_cobre.png'
    if args.init_assets or args.edit_b2:altpath.write_bytes(png_bytes(alt))
    else: assert altpath.is_file(), 'Missing B2 edit variant; use --init-assets'
    assert Image.open(altpath).size==alt.size
    assert not np.any((np.asarray(Image.open(altpath).convert('RGBA').getchannel('A'))>0)&(np.asarray(altmask)==0))
    if not args.init_assets:
        assert all(sha(Path(x).read_bytes())==h for x,h in protected_before.items()), 'Non-target asset mutated'
    b2['variant_asset']='assets/buildings/b2_cobre.png';b2['variant_sha256']=sha(altpath.read_bytes())
    # Every building projected mask stays inside parent lot, no mutual mask overlap.
    fullmasks=[]
    for r in rows:
        image=Image.new('L',(W,H),0)
        x0,y0,x1,y1=r['bbox_detail_xyxy']; image.paste(masks[r['id']],(x0,y0))
        fullmasks.append(np.asarray(image)>0)
    overlap=0
    for i in range(len(fullmasks)):
        for j in range(i+1,len(fullmasks)):
            overlap+=int(np.count_nonzero(fullmasks[i]&fullmasks[j]))
    assert overlap==0,f'Building edit masks overlapping: {overlap}'
    rootlot=rgba()
    for lot in LOTS:rootlot=Image.alpha_composite(rootlot,draw_lot(lot))
    def stage(b2candidate=False,override=None):
        composite=rootlot.copy()
        for row in rows:
            path=ROOT/(row['variant_asset'] if b2candidate and row['id']=='b2' else row['asset'])
            asset=Image.open(path).convert('RGBA')
            if override and override[0]==row['id']:asset=override[1]
            composite=paste_tight(composite,asset,row)
        return composite
    lots=stage(False);edited=stage(True)
    # Seven isolated edit tests: individually recolor exactly one opaque roof pixel;
    # no other file written or recomposed from a newly generated building.
    isolation=[]
    for ix,row in enumerate(rows):
        a=np.asarray(Image.open(ROOT/row['asset']).convert('RGBA')).copy()
        yy,xx=np.where(a[:,:,3]>180)
        assert len(xx)>0
        mid=len(xx)//2
        y,x=int(yy[mid]),int(xx[mid])
        original=a[y,x].copy()
        a[y,x,0]=255-int(a[y,x,0])
        if a[y,x,0]==original[0]:a[y,x,0]=(int(a[y,x,0])+60)%255
        modified=Image.fromarray(a,'RGBA')
        altered=stage(False,(row['id'],modified))
        px=np.any(np.asarray(altered)!=np.asarray(lots),axis=2)
        spill=int(np.count_nonzero(px&~fullmasks[ix]))
        count=int(np.count_nonzero(px))
        assert count>0 and spill==0, f'Isolation broken for {row["id"]}'
        isolation.append({'id':row['id'],'pixel_changes':count,'outside_mask_px':spill})
    orig=city.crop(CROP).resize((W,H),Image.Resampling.NEAREST).convert('RGBA')
    detail0=orig.convert('RGB');detail1=Image.alpha_composite(orig,lots).convert('RGB');detail2=Image.alpha_composite(orig,edited).convert('RGB')
    edit_d=np.any(np.asarray(detail1)!=np.asarray(detail2),axis=2)
    lot_d=np.any(np.asarray(detail0)!=np.asarray(detail1),axis=2)
    rootmask=np.zeros((H,W),dtype=bool)
    for lot in LOTS:rootmask|=(np.asarray(polygon_mask(lot['polygon_px']))>0)
    assert not np.any(lot_d&~rootmask),'High-res region lot spill'
    assert not np.any(edit_d&~fullmasks[[r['id'] for r in rows].index('b2')]),'High-res B2 spill'
    # Never modify U02 original: native paste only in mask, and separately allow only B2 in microedit.
    native_lot_mask=Image.new('L',(CROP[2]-CROP[0],CROP[3]-CROP[1]),0)
    nd=ImageDraw.Draw(native_lot_mask)
    for n in LOTS:nd.polygon([(round(x-CROP[0]),round(y-CROP[1])) for x,y in n['polygon_px']],fill=255)
    native_lot=np.asarray(native_lot_mask)>0
    b2_msmall=Image.fromarray((fullmasks[[r['id'] for r in rows].index('b2')]*255).astype('uint8')).resize((CROP[2]-CROP[0],CROP[3]-CROP[1]),Image.Resampling.BOX)
    native_b2=(np.asarray(b2_msmall)>0)
    a0=np.asarray(city).copy();stages=[]
    for detail in [detail1,detail2]:
        small=np.asarray(detail.resize((CROP[2]-CROP[0],CROP[3]-CROP[1]),Image.Resampling.BOX))
        ar=a0.copy(); patch=ar[CROP[1]:CROP[3],CROP[0]:CROP[2]]
        patch[native_lot]=small[native_lot]
        stages.append(ar)
    native1=np.any(stages[0]!=a0,axis=2);native2=np.any(stages[1]!=stages[0],axis=2)
    allow=np.zeros_like(native2);allow[CROP[1]:CROP[3],CROP[0]:CROP[2]]=native_b2
    assert not np.any(native2&~allow),'Native B2 spill'
    city_lots=Image.fromarray(stages[0],'RGB');city_edit=Image.fromarray(stages[1],'RGB')
    city_lots.save(ROOT/'mapa_lotes_v2.png');city_edit.save(ROOT/'mapa_microedicao_v2.png')
    detail0.save(ROOT/'zoom_u02.png');detail1.save(ROOT/'zoom_lotes_v2.png');detail2.save(ROOT/'zoom_microedicao_b2_v2.png')
    # Before-after whole city, headings only external to source images.
    w,h=city.size;compare=Image.new('RGB',(w*2+42,h+62),(10,17,23));d=ImageDraw.Draw(compare)
    d.text((12,18),'ANTES — U02 APROVADA',fill=(235,240,244))
    d.text((w+28,18),'DEPOIS — POC V2 / OBLIQUA',fill=(235,240,244))
    compare.paste(city,(8,50));compare.paste(city_edit,(w+26,50));compare.save(ROOT/'comparacao_integral_v2.png')
    def comparison(filename,left,right,a,b):
        pad=44;panel=Image.new('RGB',(W*2+20,H+pad+10),(11,19,25));draw=ImageDraw.Draw(panel)
        draw.text((10,13),a,fill=(237,240,242));draw.text((W+16,13),b,fill=(237,240,242))
        panel.paste(left,(5,pad));panel.paste(right,(W+15,pad));panel.save(ROOT/filename)
    comparison('comparacao_arquitetura_v2.png',detail0,detail1,'ANTES — U02','DEPOIS — 7 EDIFICIOS OBLÍQUOS')
    comparison('comparacao_microedicao_v2.png',detail1,detail2,'ANTES — 7 EDIFICIOS','DEPOIS — SO B2 ALTERADO')
    html=build_html(city,city_lots,city_edit,detail0,detail1,detail2)
    (ROOT/'comparador_interativo_v2.html').write_text(html,encoding='utf-8')
    manifest={'schema':'NOVYDRES_BUILDING_ASSETS_V2','source_u02_sha256':CFG['base']['sha256'],
              'state':'CANDIDATE_AWAITING_OWNER_VISUAL_REVIEW',
              'projection':CFG['render'],
              'buildings':rows,
              'composition_order':['lot-ground:lot-a','lot-ground:lot-b']+[r['id'] for r in rows],
              'geometry_file':'geometria_v2.json','immutable_origin':'POC_V1 b8b4f4b75b8033c62daa7a494526366cc335f112',
              'pois_untouched':True}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    stats={'schema':'NOVYDRES_V2_VISUAL_POC_TEST','base_sha256_verified':sha(source),
           'world_size_px':[w,h],'detail_size_px':[W,H], 'building_count':len(BLDGS),
           'lot_count':len(LOTS),'independent_building_assets':True,
           'protected_assets_unchanged_in_microedit':(not args.edit_b2 or all(sha(Path(x).read_bytes())==h for x,h in protected_before.items())),
           'projection':'2.5D uniform oblique with south and east facades, plan 90 degrees',
           'building_masks_intersection_px':overlap,
           'isolated_edit_tests':isolation,
           'detail_lot_changes':int(np.count_nonzero(lot_d)),
           'detail_changes_outside_lots':int(np.count_nonzero(lot_d&~rootmask)),
           'detail_b2_changes':int(np.count_nonzero(edit_d)),
           'detail_changes_outside_b2':int(np.count_nonzero(edit_d&~fullmasks[[r['id'] for r in rows].index('b2')])),
           'native_lot_changes':int(np.count_nonzero(native1)),
           'native_b2_changes':int(np.count_nonzero(native2)),
           'native_changes_outside_b2':int(np.count_nonzero(native2&~allow)),
           'source_preserved':sha(args.base.read_bytes())==CFG['base']['sha256'],
           'limitations':['All lot polygons remain experimental and non-cadastral','2.5D projection intentionally illustrates volume, not photogrammetric camera','Native U02 remains 1448x1086; enlarged legacy pixels cannot recover lost detail','No GIS topology revalidation','Human architectural approval required before closing']}
    (ROOT/'validacao_v2.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
