#!/usr/bin/env python3
"""Novydres mask hierarchy proof: actual U02, two lots, seven editable buildings.

Run: python render.py --base /path/to/T03_U02_aprovada.png
All output pixels outside permitted masks remain identical to the U02 source.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import hashlib, json, base64, io, math, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from shapely.geometry import Polygon, box

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / 'geometria.json').read_text(encoding='utf8'))
S = CFG['render']['detail_scale']
CROP = CFG['render']['crop_xyxy']
W, H = (CROP[2]-CROP[0])*S, (CROP[3]-CROP[1])*S
NODE = {n['id']:n for n in CFG['hierarchy']}
BIDS = [n['id'] for n in CFG['hierarchy'] if n['type']=='building']
LOTIDS = ['lot-a','lot-b']
COLOR = {
    'slate': {'outer':(21,36,49,255),'side':(42,56,63,255),'lit':(75,93,101,255),'dark':(28,45,56,255),'ridge':(161,180,181,255),'window':(181,137,85,255)},
    'terracotta': {'outer':(29,34,38,255),'side':(62,52,50,255),'lit':(115,91,80,255),'dark':(57,53,60,255),'ridge':(178,153,132,255),'window':(195,145,83,255)},
    'copper': {'outer':(20,38,38,255),'side':(26,66,67,255),'lit':(76,133,126,255),'dark':(31,84,81,255),'ridge':(142,199,182,255),'window':(216,166,100,255)}
}

def wp(p):return (round((p[0]-CROP[0])*S),round((p[1]-CROP[1])*S))
def polyp(pts):return [wp(p) for p in pts]
def solid_polygon_mask(points):
    m=Image.new('L',(W,H)); ImageDraw.Draw(m).polygon(polyp(points),fill=255);return m

def mask_for_building(n):
    x0,y0,x1,y1=n['footprint_px'];
    # Fixed stable edit envelope includes roof parapet and a thin east/south facade/shadow.
    r=[(x0-.4,y0-.4),(x1+.70,y0-.4),(x1+.70,y1+.75),(x0-.4,y1+.75)]
    return solid_polygon_mask(r),r

def lot_ground(n):
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer,'RGBA')
    pts=n['polygon_px'];boxv=Polygon(pts).bounds
    d.polygon(polyp(pts),fill=(29,43,51,99) if n['id']=='lot-a' else (39,48,51,110))
    # In-yard aging + snow patches, contained to each lot after clipping.
    rng=random.Random(104 if n['id']=='lot-a' else 208)
    minx,miny,maxx,maxy=boxv
    for i in range(210):
        x=rng.uniform(minx,maxx);y=rng.uniform(miny,maxy)
        col=(114,137,140,rng.randint(15,44)) if i%5 else (190,200,197,rng.randint(30,72))
        rx=rng.choice([1,2,3,5])/S;ry=rng.choice([2,3,4])/S
        xa,ya=wp((x,y));xb,yb=wp((x+rx,y+ry));d.ellipse((xa,ya,xb,yb),fill=col)
    # Narrow interior passage/dirt boundary, no city streets touched.
    xa,ya=wp((minx+0.7,maxy-0.5));xb,yb=wp((maxx-.7,maxy-0.5));d.line((xa,ya,xb,yb),fill=(166,181,179,75),width=max(1,S//14))
    alpha=layer.getchannel('A');lotm=solid_polygon_mask(pts)
    alpha=Image.fromarray(np.minimum(np.asarray(alpha),np.asarray(lotm)).astype('uint8'))
    layer.putalpha(alpha)
    return layer

def line(d,p,q,c,w=0.08):d.line((wp(p),wp(q)),fill=c,width=max(1,round(S*w)))
def roof(n,variant=None):
    im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
    x0,y0,x1,y1=n['footprint_px']; w=x1-x0;h=y1-y0
    pal=COLOR['copper' if variant=='copper' else n['palette']]
    variant_roof=variant or n['roof_kind']
    rng=random.Random(sum(ord(c) for c in n['id'])*33 + (1000 if variant=='copper' else 0))
    # Sharp under-roof shadow and visible wall edge, still orthographic world grid.
    d.polygon(polyp([(x0+.28,y0+.55),(x1+.60,y0+.55),(x1+.60,y1+.6),(x0+.28,y1+.6)]), fill=(4,12,19,194))
    d.polygon(polyp([(x0+.2,y1-.15),(x1+.25,y1-.15),(x1+.25,y1+.35),(x0+.2,y1+.35)]),fill=pal['side'])
    d.polygon(polyp([(x1-.15,y0+.35),(x1+.30,y0+.35),(x1+.30,y1+.35),(x1-.15,y1-.15)]),fill=pal['outer'])
    # Basic rooftop mass is tightly bound to the local footprint.
    d.rectangle((*wp((x0,y0)),*wp((x1,y1))),fill=pal['dark'])
    if variant_roof in ('gable','mansard') or variant_roof=='copper':
        # Roof facets convey volume without rotating the city map.
        if h>=w:
            mid=(x0+x1)/2
            d.polygon(polyp([(x0,y0),(mid,y0+.25),(mid,y1-.25),(x0,y1)]),fill=pal['lit'])
            d.polygon(polyp([(mid,y0+.25),(x1,y0),(x1,y1),(mid,y1-.25)]),fill=pal['dark'])
            line(d,(mid,y0+.25),(mid,y1-.25),pal['ridge'],.09)
            if variant_roof=='mansard':
                line(d,(x0+1.15,y0+.45),(x0+1.15,y1-.45),(174,181,178,150),.06)
                line(d,(x1-1.10,y0+.45),(x1-1.10,y1-.45),(17,25,30,225),.08)
            for i in range(1,int(h)):
                yy=y0+i
                line(d,(x0+.35,yy),(mid-.28,yy+.18),(26,37,45,110),.035)
                line(d,(mid+.27,yy+.10),(x1-.3,yy),(118,135,135,90),.035)
        else:
            mid=(y0+y1)/2
            d.polygon(polyp([(x0,y0),(x1,y0),(x1-.3,mid),(x0+.3,mid)]),fill=pal['lit'])
            d.polygon(polyp([(x0+.3,mid),(x1-.3,mid),(x1,y1),(x0,y1)]),fill=pal['dark'])
            line(d,(x0+.3,mid),(x1-.3,mid),pal['ridge'],.10)
            for i in range(1,int(w)):
                xx=x0+i
                line(d,(xx,y0+.2),(xx+.14,mid-.2),(38,44,47,100),.04)
                line(d,(xx+.13,mid+.2),(xx,y1-.2),(123,137,139,80),.035)
    elif variant_roof=='industrial_sawtooth':
        # Small historic light-industry sawtooth roof adjoining tenements.
        d.rectangle((*wp((x0,y0)),*wp((x1,y1))),fill=pal['dark'])
        for xx in np.linspace(x0+.35,x1-.35,7):
            line(d,(xx,y0+.35),(xx,y1-.35),(151,171,170,182),.075)
            line(d,(xx+.23,y0+.35),(xx+.23,y1-.35),(15,25,35,240),.12)
        for i in range(10):
            xx=rng.uniform(x0+.5,x1-.5);yy=rng.uniform(y0+.4,y1-.5)
            line(d,(xx,yy),(xx+0.55,yy),(123,156,165,132),.10)
    else:
        d.rectangle((*wp((x0+.45,y0+.45)),*wp((x1-.45,y1-.45))),fill=pal['lit'],outline=pal['ridge'],width=max(1,S//9))
        for i in range(3):
            sx=x0+1.0+i*(w-2.1)/3
            d.rectangle((*wp((sx,y0+1.2)),*wp((sx+.6,y0+2.25))),fill=(23,38,48,255),outline=(163,187,188,225),width=1)
        # roof drain path & parapet
        line(d,(x0+.55,y1-.65),(x1-.55,y1-.65),(25,35,45,200),.10)
    # Old roof details: chimneys, hatches, slate hatching and warm service windows.
    for i in range(2 if w>8 else 1):
        cx=x0+min(w-1.2, 1.5+i*(w-2.1)/2)
        cy=y0+1.1 +(i%2)*.55
        d.rectangle((*wp((cx-.19,cy-.21)),*wp((cx+.27,cy+.38))),fill=(22,31,35,255),outline=(180,174,160,220),width=1)
    for xx in np.arange(x0+.75,x1-.4,1.85):
        # Continuous small windows on the exposed south wall.
        ax,ay=wp((xx,y1+.02));bx,by=wp((min(xx+.55,x1-.15),y1+.30))
        d.rectangle((ax,ay,bx,by),fill=pal['window'])
    for xx in [x0+.55,x1-.5]:
        line(d,(xx,y0+.24),(xx,y1-.2),pal['ridge'],.055)
    line(d,(x0,y0),(x1,y0),(168,190,190,200),.07)
    line(d,(x0,y0),(x0,y1),(180,185,179,160),.07)
    if variant=='copper':
        # Target edit: ornate oxidized-copper pitched roof with explicit dormers.
        for yy in np.linspace(y0+2.0,y1-1.5,3):
            cx=x0+2.1
            d.polygon(polyp([(cx-.72,yy+.34),(cx,yy-.56),(cx+.77,yy+.35)]),fill=(125,179,168,255),outline=(20,59,62,255),width=1)
            d.rectangle((*wp((cx-.4,yy+.25)),*wp((cx+.42,yy+.86))),fill=(32,49,56,255),outline=(182,212,200,255),width=max(1,S//16))
        for xx,yy in [(x1-1.45,y0+1.8),(x1-2.1,y1-1.7)]:
            d.rectangle((*wp((xx,yy)),*wp((xx+.34,yy+.74))),fill=(27,51,54,255),outline=(159,189,177,255),width=max(1,S//16))
        # A clear turquoise-copper ridge and patina flecks.
        for k in range(18):
            xx=rng.uniform(x0+.65,x1-.6);yy=rng.uniform(y0+.6,y1-.6)
            line(d,(xx,yy),(xx+.25,yy-.02),(119,173,159,rng.randint(110,210)),.045)
    m,_=mask_for_building(n)
    alpha=np.minimum(np.array(im.getchannel('A')),np.asarray(m)).astype('uint8')
    im.putalpha(Image.fromarray(alpha))
    return im

def overlay_lots():
    layer=Image.new('RGBA',(W,H))
    for name in LOTIDS:layer=Image.alpha_composite(layer,lot_ground(NODE[name]))
    return layer

def composite_lot_and_buildings(bg,mods=None):
    out=bg.copy()
    for name in BIDS:
        b=NODE[name];out=Image.alpha_composite(out,roof(b,variant=(mods or {}).get(name)))
    return out

def mask_parent(id):return solid_polygon_mask(NODE[id]['polygon_px'])

def sha(b):return hashlib.sha256(b).hexdigest()
def pngbytes(im):
    buf=io.BytesIO();im.save(buf,format='PNG',compress_level=6);return buf.getvalue()
def image_data(im,fmt='WEBP',quality=95):
    b=io.BytesIO();im.save(b,format=fmt,quality=quality,method=6);return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',type=Path,required=True);args=parser.parse_args()
    source=args.base.read_bytes();assert sha(source)==CFG['base']['sha256'], 'U02 SHA256 mismatch'
    city=Image.open(io.BytesIO(source)).convert('RGB')
    assert city.size==tuple(CFG['base']['size_px'])
    # Geometry/ownership; no tram/road changes are permitted in prototype.
    for bname in BIDS:
        n=NODE[bname];lot=Polygon(NODE[n['parent']]['polygon_px'])
        mask_poly=Polygon(mask_for_building(n)[1]);assert lot.contains(mask_poly),f'Building {bname} exceeds lot'
    assert not Polygon(NODE['lot-a']['polygon_px']).intersects(Polygon(NODE['lot-b']['polygon_px']))
    reg=box(559,660,1033,1086)
    assert reg.contains(Polygon(NODE['neighborhood-ksw-pilot-01']['polygon_px']))
    a_mask=np.asarray(mask_parent('lot-a'))>0;b_mask=np.asarray(mask_parent('lot-b'))>0
    original_patch=city.crop(tuple(CROP)).resize((W,H),Image.Resampling.NEAREST).convert('RGBA')
    ground=overlay_lots()
    layer1=composite_lot_and_buildings(ground)
    layer2=composite_lot_and_buildings(ground,{'b2':'copper'})
    mask_b2=np.asarray(mask_for_building(NODE['b2'])[0])>0
    # Render U02 baseline and both candidate stages at high zoom.
    view1=Image.alpha_composite(original_patch,layer1).convert('RGB')
    view2=Image.alpha_composite(original_patch,layer2).convert('RGB')
    data0=np.asarray(original_patch.convert('RGB'))
    data1=np.asarray(view1); data2=np.asarray(view2)
    changed1=np.any(data0!=data1,axis=2)
    changed2=np.any(data1!=data2,axis=2)
    assert (changed1 & ~(a_mask|b_mask)).sum()==0, 'Modified beyond lots'
    assert (changed2 & ~mask_b2).sum()==0, 'Single-building modification spilled'
    assert changed1.sum()>0 and changed2.sum()>0
    # Binary child edit mask (high-res), lot masks and staged presentation.
    Image.fromarray((mask_b2*255).astype('uint8')).save(HERE/'mask_predio_b2.png')
    Image.fromarray(((a_mask|b_mask)*255).astype('uint8')).save(HERE/'mascaras_lotes.png')
    for title,im in [('zoom_u02_original',original_patch.convert('RGB')),('zoom_lotes',view1),('zoom_predio_b2_editado',view2)]:
        im.save(HERE/(title+'.png'))
    # Save transparent layered overlays to maintain sharp roofs at arbitrary map zoom.
    layer1.save(HERE/'overlay_lotes.png');layer2.save(HERE/'overlay_microedicao.png')
    # Native 1448x1086 composition, strict native polygon mask preserving original outside.
    outputs=[]; native_maps=[]
    city_arr=np.asarray(city).copy()
    for highres in [view1,view2]:
        loc=highres.resize((CROP[2]-CROP[0],CROP[3]-CROP[1]),Image.Resampling.BOX)
        arr=city_arr.copy(); small=np.asarray(loc)
        mask_low=Image.new('L',(CROP[2]-CROP[0],CROP[3]-CROP[1]));draw=ImageDraw.Draw(mask_low)
        for lotid in LOTIDS:
            draw.polygon([(round(x-CROP[0]),round(y-CROP[1])) for x,y in NODE[lotid]['polygon_px']],fill=255)
        native_mask=np.array(mask_low)>0
        yy=slice(CROP[1],CROP[3]);xx=slice(CROP[0],CROP[2])
        patch=arr[yy,xx]
        patch[native_mask]=small[native_mask]
        outputs.append(Image.fromarray(arr,'RGB'))
        native_maps.append(arr)
    outputs[0].save(HERE/'mapa_candidato_lotes.png')
    outputs[1].save(HERE/'mapa_candidato_microedicao.png')
    changed_native1=np.any(city_arr!=native_maps[0],axis=2)
    changed_native2=np.any(native_maps[0]!=native_maps[1],axis=2)
    root_native_mask=np.zeros((city.height,city.width),dtype=bool)
    root_native_mask[CROP[1]:CROP[3],CROP[0]:CROP[2]]=native_mask
    assert not (changed_native1 & ~root_native_mask).any()
    # micro-edit native diff is restricted to the target roof's stable edit mask, not just the parent lots.
    msmall=Image.new('L',(CROP[2]-CROP[0],CROP[3]-CROP[1]));p=mask_for_building(NODE['b2'])[1]
    ImageDraw.Draw(msmall).polygon([(round(x-CROP[0]),round(y-CROP[1])) for x,y in p],fill=255)
    sm=np.asarray(msmall)>0
    allowed=np.zeros((city.height,city.width),dtype=bool)
    allowed[CROP[1]:CROP[3],CROP[0]:CROP[2]]=sm
    # A downsampled antialias boundary can spill one original pixel, prevent by strict native paste.
    spill=changed_native2 & ~allowed
    if spill.any():
        native_maps[1][spill]=native_maps[0][spill]
        outputs[1]=Image.fromarray(native_maps[1],'RGB')
        outputs[1].save(HERE/'mapa_candidato_microedicao.png')
        changed_native2=np.any(native_maps[0]!=native_maps[1],axis=2)
    assert (changed_native2 & ~allowed).sum()==0
    # Before-after full city comparison; markers/titles only OUTSIDE map, never rasterized within city.
    from PIL import ImageFont
    fw,fh=city.size
    comparison=Image.new('RGB',(fw*2+48,fh+62),(11,19,25))
    comparison.paste(city,(12,52)); comparison.paste(outputs[1],(fw+36,52))
    dt=ImageDraw.Draw(comparison);dt.text((17,15),'ANTES — U02 original',fill=(226,236,239))
    dt.text((fw+39,15),'DEPOIS — prototipo hierarquico (microedicao B2)',fill=(226,236,239))
    comparison.save(HERE/'comparacao_integral.png')
    # Larger meaningful comparison, preserving crop bounds identical.
    banner=52
    focus=Image.new('RGB',(W*2+24,H+banner+12),(12,20,27)); focus.paste(original_patch.convert('RGB'),(8,banner));focus.paste(view2,(W+16,banner))
    f=ImageDraw.Draw(focus);f.text((12,17),'ANTES — U02',fill=(225,234,237));f.text((W+18,17),'DEPOIS — SETE EDIFICIOS / DOIS LOTES',fill=(225,234,237))
    focus.save(HERE/'comparacao_bairro_zoom.png')
    # Interactive compare; native U02 exact, two vector-grade overlays have 16x local pixel density.
    u02data=image_data(city,quality=97)
    layer1data=image_data(layer1,quality=98)
    layer2data=image_data(layer2,quality=98)
    info={
       'schema':'NOVYDRES_PROTOTYPE_MASK_VALIDATION_V1',
       'base_sha256':CFG['base']['sha256'],
       'city_size_px':[fw,fh],
       'detail_scale':S,
       'region':'Kingswell',
       'neighborhood':'neighborhood-ksw-pilot-01',
       'lot_count':2,'buildings_count':7,'microedit_target':'b2',
       'changed_pixels_16x_lots':int(changed1.sum()),
       'changed_pixels_16x_microedit':int(changed2.sum()),
       'changed_pixels_native_lots':int(changed_native1.sum()),
       'changed_pixels_native_microedit':int(changed_native2.sum()),
       'highres_microedit_outside_b2':int((changed2&~mask_b2).sum()),
       'highres_lot_edit_outside_lots':int((changed1&~(a_mask|b_mask)).sum()),
       'native_lot_edit_outside_lots':int((changed_native1&~root_native_mask).sum()),
       'native_microedit_outside_b2':int((changed_native2&~allowed).sum()),
       'geometry_child_within_parent':True,
       'source_unchanged':sha(args.base.read_bytes())==CFG['base']['sha256'],
       'structural_validation':'pixelwise outside protected masks; exact rail/water layer geometry not revalidated',
       'limitations':['Experimental 2.5D roofs, not generative architectural illustration','No approved cadastral lot geometry','Original U02 only has 1448x1086 details; high-res new building layers cannot recover lost original detail','No physical GIS validation and no real-world absolute dimensions','HTML browser/mobile device visual QA pending']
    }
    (HERE/'validacao.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    html=f'''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1, maximum-scale=1"><title>Novydres | Hierarquia de máscaras — protótipo</title><style>
    :root{{color-scheme:dark;font:14px system-ui,Segoe UI,Arial,sans-serif}}*{{box-sizing:border-box}}body{{background:#0b141b;color:#dce8ee;margin:0;padding:12px}}h1{{font-size:18px;margin:0 0 6px}}p{{color:#adbeca;line-height:1.35;margin:8px 0}}.bar{{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0;align-items:center}}button,select{{background:#1c3542;border:1px solid #496674;color:#e7f4f4;border-radius:7px;padding:9px 11px;font:inherit}}button.active{{background:#376173}}button:focus{{outline:2px solid #a8c9d1}}.compare{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.panel{{min-width:0}}.panel h2{{font-size:13px;margin:3px 0 7px;color:#d0dae2;font-weight:600}}.view{{height:min(66vh,620px);background:#03101a;overflow:hidden;position:relative;cursor:grab;touch-action:none;border:1px solid #3e5664;border-radius:6px}}.view:active{{cursor:grabbing}}.content{{position:absolute;top:0;left:0;width:100%;height:100%;transform-origin:0 0;will-change:transform}}.map{{position:absolute;left:0;top:0;width:1448px;height:1086px;max-width:none;pointer-events:none}}.layer{{position:absolute;left:{CROP[0]}px;top:{CROP[1]}px;width:{CROP[2]-CROP[0]}px;height:{CROP[3]-CROP[1]}px;max-width:none;pointer-events:none}}.caption{{font-size:12px;color:#9db1bf;margin-top:8px}}.legend{{margin-top:10px;font-size:12px;line-height:1.45;color:#afc2ce}}@media(max-width:720px){{.view{{height:38vh}}.compare{{gap:6px}}h1{{font-size:16px}}button{{padding:8px}}}}
    </style></head><body><h1>Novydres — protótipo de máscaras hierárquicas</h1><p>U02 preservada. Kingswell: um bairro, dois lotes, sete edifícios. Compare a imagem original com o estágio escolhido. As imagens usam as mesmas coordenadas e enquadramento.</p><div class="bar"><button id="full">Ver cidade inteira</button><button id="focus" class="active">Ampliar quarteirão</button><button id="zin">Zoom +</button><button id="zout">Zoom −</button><label for="stage">Camada direita:</label><select id="stage"><option value="1">Etapa 1: lotes detalhados</option><option value="2" selected>Etapa 2: edifício B2 modificado</option><option value="0">U02 original (controle)</option></select></div><div class="compare"><section class="panel"><h2>ANTES — U02 original</h2><div class="view" id="left"><div class="content"><img class="map" src="{u02data}"></div></div></section><section class="panel"><h2>DEPOIS — protótipo</h2><div class="view" id="right"><div class="content"><img class="map" src="{u02data}"><img class="layer" id="detail" src="{layer2data}"></div></div></section></div><div class="legend">Arraste para navegar. Use a roda do mouse ou os botões de zoom. Teste a alteração de apenas um prédio alternando “Etapa 1” e “Etapa 2”. Nenhum rótulo é desenhado sobre o mapa. As cores e lotes são candidatos, não cânone.</div><script>
    const pane=[...document.querySelectorAll('.view')], maps=pane.map(p=>p.querySelector('.content'));const ov=document.getElementById('detail'),stage=document.getElementById('stage');const layers=['','{layer1data}','{layer2data}'];let zoom=1,x=0,y=0,drag=null;function dim(){{return {{w:pane[0].clientWidth,h:pane[0].clientHeight}}}}function draw(){{for(let i=0;i<2;i++)maps[i].style.transform=`translate(${{x}}px,${{y}}px) scale(${{zoom}})`}}function full(){{const d=dim();zoom=Math.min(d.w/1448,d.h/1086);x=(d.w-1448*zoom)/2;y=(d.h-1086*zoom)/2;draw()}}function focus(){{const d=dim();zoom=Math.min(d.w/90,d.h/68);x=d.w/2-777*zoom;y=d.h/2-804*zoom;draw()}}function scale(k){{const d=dim(), cx=d.w/2,cy=d.h/2;const wx=(cx-x)/zoom, wy=(cy-y)/zoom;zoom=Math.max(.05,Math.min(35,zoom*k));x=cx-wx*zoom;y=cy-wy*zoom;draw()}}pane.forEach(p=>{{p.addEventListener('pointerdown',e=>{{drag={{id:e.pointerId,px:e.clientX,py:e.clientY}};p.setPointerCapture(e.pointerId)}});p.addEventListener('pointermove',e=>{{if(!drag||drag.id!==e.pointerId)return;x+=e.clientX-drag.px;y+=e.clientY-drag.py;drag.px=e.clientX;drag.py=e.clientY;draw()}});p.addEventListener('pointerup',()=>drag=null);p.addEventListener('pointercancel',()=>drag=null);p.addEventListener('wheel',e=>{{e.preventDefault();scale(e.deltaY<0?1.2:1/1.2)}},{{passive:false}})}});document.getElementById('full').onclick=full;document.getElementById('focus').onclick=focus;document.getElementById('zin').onclick=()=>scale(1.35);document.getElementById('zout').onclick=()=>scale(1/1.35);stage.onchange=()=>{{ov.style.display=stage.value==='0'?'none':'block';if(stage.value!=='0')ov.src=layers[Number(stage.value)]}};window.addEventListener('resize',draw);focus();
    </script></body></html>'''
    (HERE/'comparador_interativo.html').write_text(html,encoding='utf-8')
    (HERE/'RELATORIO.md').write_text(f'''# Novydres — protótipo de máscaras hierárquicas (candidato)

**Escopo:** Kingswell (região), `neighborhood-ksw-pilot-01`, lotes A e B, 7 edifícios (A1–A3, B1–B4). Não há obra sobre os 34 POIs.

**Fonte:** T03/U02 aprovada, SHA256 `{CFG['base']['sha256']}`, 1448×1086, conferido sem modificação.

## Prova efetiva

- Imagem completa U02 original comparada com etapa 2 (`comparacao_integral.png`).
- Zoom 16× do mesmo retângulo (`comparacao_bairro_zoom.png`), camadas de arquitetura com escala local 16×, sem girar o mapa.
- `overlay_lotes.png` contém sete edifícios sobre dois lotes; `overlay_microedicao.png` difere apenas no edifício B2.
- Pixels alterados no detalhe 16× na etapa de lotes: **{info['changed_pixels_16x_lots']}**, com **zero fora das máscaras dos lotes**.
- Pixels alterados no detalhe 16× na microedição B2: **{info['changed_pixels_16x_microedit']}**, com **zero fora da máscara B2**.
- Pixels alterados na cidade original 1448×1086 pela implantação dos lotes: **{info['changed_pixels_native_lots']}**, com **zero fora dos lotes**.
- Pixels alterados na cidade original 1448×1086 somente pela microedição B2: **{info['changed_pixels_native_microedit']}**, com **zero fora da máscara B2**.
- Todos os edifícios cabem integralmente nos pais; as máscaras dos dois lotes não se sobrepõem.

## Limitações honestas

Este protótipo **valida hierarquia, persistência de geometria, composição e isolamento de edição**, não qualidade arquitetônica final. As coberturas vetoriais ilustram volume em projeção de planta, mas não atingem a arte definitiva desejada. A U02 continua tendo 1448×1086 px; o detalhamento criado em 16× não recupera detalhes do raster de origem. Lotes são experimentais, não contornos cadastrais aprovados. Sem análise GIS completa. Nenhuma aprovação implícita de U03; nenhum cânone ou POI alterado.

**Estado: CANDIDATA, AGUARDANDO AVALIAÇÃO.**
''',encoding='utf8')
    print(json.dumps(info,indent=2,ensure_ascii=False))

if __name__=='__main__':main()