#!/usr/bin/env python3
"""Novydres Mapwork V3: deterministic geometry, isolated lot assets, tiles, offline comparison.
No image generation, research, remote writes, credentials or automatic canonization here.
The ChatGPT agent owns Drive/GitHub connector actions and approvals.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, math, re, sys
from pathlib import Path
from PIL import Image, ImageChops
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config.json'
SCHEMA = ROOT / 'schemas/zone.schema.json'
STATE = ROOT / 'world-state.json'

class Invalid(Exception): pass

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, data):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def rect(r): return len(r)==4 and all(isinstance(v, (int,float)) and math.isfinite(v) for v in r) and r[0]<r[2] and r[1]<r[3]
def inside(inner, outer): return inner[0]>=outer[0] and inner[1]>=outer[1] and inner[2]<=outer[2] and inner[3]<=outer[3]
def overlaps(a,b): return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
def fail(condition, message):
    if not condition: raise Invalid(message)

def config_check(cfg):
    fail(cfg['schema']=='NOVYDRES_MAPWORK_V3_CONFIG_1','config schema')
    w,h=cfg['world_size_units']; scale=cfg['detail_pixels_per_unit']; tile=cfg['tile_size_px']
    fail(w>0 and h>0 and isinstance(scale,int) and scale>0 and scale<=256,'invalid scale')
    fail(isinstance(tile,int) and tile>=128 and tile<=2048 and tile & (tile-1)==0,'invalid tile size')
    fail(cfg['projection']['type']=='illustrated_2d_topdown','projection must remain 2D')
    fail(cfg['projection']['floor_height_units'] is None,'do not invent absolute height')
    fail(len(cfg['layer_order'])==len(set(cfg['layer_order'])),'duplicate layers')
    fail(re.fullmatch('[0-9a-f]{64}',cfg['reference']['sha256']) is not None,'reference SHA')
    fail(cfg['world_size_units']==[cfg['reference']['width'],cfg['reference']['height']],'base dimensions')
    fail(cfg['drive']['folder_id'] and cfg['reference']['drive_file_id'],'missing Drive storage')

def audit_zone(z, cfg, assets=None, strict=False):
    validator=Draft202012Validator(load(SCHEMA)); errors=list(validator.iter_errors(z))
    fail(not errors,'schema: '+('; '.join(e.message for e in errors[:4])))
    bounds=z['bounds']; fail(rect(bounds),'zone rectangle invalid')
    fail(inside(bounds,[0,0,*cfg['world_size_units']]),'zone beyond world')
    fail(z['source_commit']!='UNKNOWN','source commit required')
    fail(len({e['id'] for e in z['elements']})==len(z['elements']),'duplicate element ids')
    fail(len({c['id'] for c in z['connectors']})==len(z['connectors']),'duplicate connector ids')
    fail(z['id'] not in z['neighbors'],'self neighbor')
    fail(z['status'] not in ('GENERATING','VISUAL_REVIEW','OWNER_APPROVED','PUBLISHED') or z['sketch_approved'],'sketch not approved')
    fail(z['status'] not in ('OWNER_APPROVED','PUBLISHED') or z.get('owner_approval'),'owner approval missing')
    if z['status']!='PLANNING':
        fail(not any(d['status']=='OPEN' for d in z['decisions']),'open blocking decision')
        fail(bool(z['elements']),'nonplanning zone without detailed elements')
        fail(bool(z['connectors']) if z['neighbors'] else True,'nonplanning zone has no neighbor connectors')
    scale=cfg['detail_pixels_per_unit']; max_bleed=cfg['max_bleed_units']
    cores=[]
    for e in z['elements']:
        core,env=e['core'],e['envelope']
        fail(rect(core) and rect(env),f"{e['id']}: invalid box")
        fail(inside(core,env),f"{e['id']}: core outside envelope")
        fail(inside(env,bounds),f"{e['id']}: envelope outside zone; seek border agreement")
        for i in range(4):
            fail(abs(env[i]*scale-round(env[i]*scale))<1e-6,f"{e['id']}: grid alignment")
        fail(max(core[0]-env[0],core[1]-env[1],env[2]-core[2],env[3]-core[3])<=max_bleed+1e-9,f"{e['id']}: bleed too large")
        if e['kind']=='lot':
            for other in cores: fail(not overlaps(core,other),f"{e['id']}: overlapping lot cores")
            cores.append(core)
        if e['kind']=='lot': fail(e['layer']=='lot',f"{e['id']}: lot layer")
        if e['kind']=='special_building':fail(e['layer']=='special',f"{e['id']}: special layer")
        if e['status']=='PENDING':
            fail(not strict,f"{e['id']}: pending asset")
            continue
        fail(e['asset'] is not None and e['mask'] is not None,f"{e['id']}: missing asset/mask")
        for name in ('asset','mask'):
            meta=e[name]
            fail(not Path(meta['path']).is_absolute() and '..' not in Path(meta['path']).parts,f"{e['id']}: unsafe relative path")
        if assets is None:
            fail(not strict,f"{e['id']}: asset directory required")
            continue
        ap=Path(assets)/e['asset']['path']; mp=Path(assets)/e['mask']['path']
        fail(ap.is_file() and mp.is_file(),f"{e['id']}: missing local bytes (fetch by Drive ID)")
        fail(sha(ap)==e['asset']['sha256'] and sha(mp)==e['mask']['sha256'],f"{e['id']}: SHA mismatch")
        with Image.open(ap) as ai, Image.open(mp) as mi:
            exp=tuple(round((env[j+2]-env[j])*scale) for j in (0,1))
            fail(ai.size==exp and mi.size==exp,f"{e['id']}: asset/mask not at common scale")
            a=ai.convert('RGBA').getchannel('A'); m=mi.convert('L')
            fail(a.getbbox() is not None,f"{e['id']}: empty asset")
            fail(not ImageChops.subtract(a,m).getbbox(),f"{e['id']}: painted outside mask")
    for c in z['connectors']:
        fail(c['neighbor'] in z['neighbors'],f"{c['id']}: neighbor not declared")
        fail(bounds[0]<=c['x']<=bounds[2] and bounds[1]<=c['y']<=bounds[3],f"{c['id']}: outside bounds")
        fail(any(abs(c['x']-bounds[i])<1e-9 for i in (0,2)) or any(abs(c['y']-bounds[i])<1e-9 for i in (1,3)),f"{c['id']}: connector not on boundary")
    if strict:
        fail(z['sketch_approved'],'sketch needs owner approval')
        fail(all(e['status']=='VERIFIED' for e in z['elements']),'unverified element')
    return {'zone':z['id'],'elements':len(z['elements']),'connectors':len(z['connectors']),'mode':'strict' if strict else 'structural'}

def connector_match(zones, require_all=False):
    byid={z['id']:z for z in zones}
    for z in zones:
        for neighbor in z['neighbors']:
            if neighbor not in byid:
                fail(not require_all,f"{z['id']}: missing neighbor {neighbor} in strict validation")
                continue
            other=byid[neighbor]
            fail(z['id'] in other['neighbors'],f"{z['id']}/{neighbor}: asymmetric neighbors")
            left={c['id']:c for c in z['connectors'] if c['neighbor']==neighbor}
            right={c['id']:c for c in other['connectors'] if c['neighbor']==z['id']}
            fail(set(left)==set(right),f"{z['id']}/{neighbor}: missing/mismatched connectors")
            for key in left:
                a,b=left[key],right[key]
                for prop in ('kind','x','y','width','profile'):
                    fail(a.get(prop)==b.get(prop),f"{key}: seam mismatch in {prop}")
    return {'verified_adjacent_zone_pairs':sum(1 for z in zones for n in z['neighbors'] if n in byid)//2}

def source_check(base,cfg):
    fail(Path(base).is_file() and sha(base)==cfg['reference']['sha256'],'U02 changed or missing')
    with Image.open(base) as im: fail(list(im.size)==cfg['world_size_units'],'U02 resolution changed')

def tiles_for(zones,cfg):
    s=cfg['detail_pixels_per_unit'];t=cfg['tile_size_px']; w,h=cfg['world_size_units']
    coords=set()
    for z in zones:
        b=z['bounds'];x0,y0,x1,y1=(round(v*s) for v in b)
        for ty in range(y0//t,(y1-1)//t+1):
            for tx in range(x0//t,(x1-1)//t+1): coords.add((tx,ty))
    return sorted(coords,key=lambda p:(p[1],p[0]))

def composite(zones,cfg,base,assets,out):
    source_check(base,cfg)
    for z in zones:audit_zone(z,cfg,assets,strict=True)
    connector_match(zones, require_all=True)
    s=cfg['detail_pixels_per_unit'];t=cfg['tile_size_px'];output=Path(out);output.mkdir(parents=True,exist_ok=True)
    layers={name:i for i,name in enumerate(cfg['layer_order'])}
    elements=[e for z in zones for e in z['elements']]
    elements.sort(key=lambda e:(layers[e['layer']],e['id']))
    coords=tiles_for(zones,cfg)
    with Image.open(base) as src:
        src=src.convert('RGBA'); entries=[]
        for tx,ty in coords:
            px,py=tx*t,ty*t
            tw=min(t,cfg['world_size_units'][0]*s-px);th=min(t,cfg['world_size_units'][1]*s-py)
            im=src.transform((tw,th),Image.Transform.AFFINE,(1/s,0,px/s,0,1/s,py/s),Image.Resampling.BICUBIC)
            for e in elements:
                x0,y0,x1,y1=(round(v*s) for v in e['envelope'])
                a0=max(px,x0);b0=max(py,y0);a1=min(px+tw,x1);b1=min(py+th,y1)
                if a1<=a0 or b1<=b0:continue
                with Image.open(Path(assets)/e['asset']['path']) as original, Image.open(Path(assets)/e['mask']['path']) as mm:
                    box=(a0-x0,b0-y0,a1-x0,b1-y0)
                    crop=original.convert('RGBA').crop(box); mask=mm.convert('L').crop(box)
                    alpha=ImageChops.darker(crop.getchannel('A'),mask);crop.putalpha(alpha)
                    im.alpha_composite(crop,(a0-px,b0-py))
            name=f"tile_{tx}_{ty}.png"; p=output/name; im.save(p,optimize=True)
            entries.append({'x':tx,'y':ty,'filename':name,'sha256':sha(p),'width':tw,'height':th,'drive_file_id':None})
    manifest={'schema':'NOVYDRES_MAPWORK_V3_TILES_1','world_size_units':cfg['world_size_units'],'detail_pixels_per_unit':s,'tile_size_px':t,'zone_ids':[z['id'] for z in zones],'tiles':entries,'stage':'CANDIDATE_NOT_UPLOADED'}
    save(output/'tiles.json',manifest);return manifest

def verify_tiles(manifest,root,cfg):
    fail(manifest['schema']=='NOVYDRES_MAPWORK_V3_TILES_1','tile schema')
    fail(manifest['detail_pixels_per_unit']==cfg['detail_pixels_per_unit'],'tile scale')
    for t in manifest['tiles']:
        p=Path(root)/t['filename'];fail(p.is_file() and sha(p)==t['sha256'],'missing/altered tile '+t['filename'])
    return len(manifest['tiles'])

def image_uri(image):
    import io
    b=io.BytesIO();image.save(b,format='PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

def html_compare(before, after, base, out, cfg):
    source_check(base,cfg)
    with Image.open(base) as im: ref=image_uri(im.convert('RGBA'))
    before_json=load(Path(before)/'tiles.json') if before else None
    after_json=load(Path(after)/'tiles.json')
    verify_tiles(after_json,after,cfg)
    if before_json: verify_tiles(before_json,before,cfg)
    def image_tiles(m,folder):
        if not m:return []
        result=[]
        for entry in m['tiles']:
            with Image.open(Path(folder)/entry['filename']) as im: uri=image_uri(im.convert('RGBA'))
            result.append({'x':entry['x'],'y':entry['y'],'src':uri})
        return result
    prior=image_tiles(before_json,before) if before else []
    # Changed tiles replace matching tiles of the previous release. All coordinates are global.
    merged={(e['x'],e['y']):e for e in prior}
    for e in image_tiles(after_json,after):merged[(e['x'],e['y'])]=e
    data=json.dumps({'base':ref,'before':prior,'after':list(merged.values()),'s':cfg['detail_pixels_per_unit'],'tile':cfg['tile_size_px'],'w':cfg['world_size_units'][0],'h':cfg['world_size_units'][1]},separators=(',',':'))
    template='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Novydres — ANTES / DEPOIS</title><style>body{background:#101820;color:#e8e7e3;font:14px system-ui;margin:10px}header{display:flex;gap:12px;align-items:center;flex-wrap:wrap}button{padding:8px;background:#303b48;color:white;border:1px solid #64778a;border-radius:6px}.views{display:grid;grid-template-columns:1fr 1fr;gap:8px}.frame{overflow:hidden;border:1px solid #64778a;border-radius:8px}canvas{display:block;width:100%;height:70vh;touch-action:none;background:#26333d}small{opacity:.8}@media(max-width:680px){.views{grid-template-columns:1fr}canvas{height:37vh}}</style><header><b>Novydres • mapa integral</b><button onclick="zoom(1.6)">Ampliar +</button><button onclick="zoom(1/1.6)">Reduzir −</button><button onclick="reset()">Ver tudo</button><small>Arraste para mover. Zoom sincronizado nas duas vistas.</small></header><div class="views"><section><h3>ANTES — última versão aprovada</h3><div class="frame"><canvas id="b"></canvas></div></section><section><h3>DEPOIS — candidata</h3><div class="frame"><canvas id="a"></canvas></div></section></div><script>const D=__DATA__;const canv=[document.querySelector('#b'),document.querySelector('#a')];let z=1,dx=0,dy=0,drag=null;let base=new Image();base.src=D.base;const make=(entries)=>entries.map(e=>{let im=new Image();im.src=e.src;return {...e,im}});let before=make(D.before),after=make(D.after);function fit(){return Math.min(canv[0].clientWidth/D.w,canv[0].clientHeight/D.h)}function draw(){canv.forEach((c,i)=>{const dpr=window.devicePixelRatio||1;c.width=Math.round(c.clientWidth*dpr);c.height=Math.round(c.clientHeight*dpr);let ctx=c.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,c.clientWidth,c.clientHeight);let k=fit()*z,ox=(c.clientWidth-D.w*k)/2+dx,oy=(c.clientHeight-D.h*k)/2+dy;ctx.imageSmoothingEnabled=true;if(base.complete)ctx.drawImage(base,ox,oy,D.w*k,D.h*k);const tiles=i===0?before:after;for(const t of tiles)if(t.im.complete)ctx.drawImage(t.im,ox+(t.x*D.tile/D.s)*k,oy+(t.y*D.tile/D.s)*k,t.im.naturalWidth/D.s*k,t.im.naturalHeight/D.s*k)})}function zoom(q){z=Math.max(1,Math.min(D.s*2,z*q));draw()}function reset(){z=1;dx=dy=0;draw()}canv.forEach(c=>{c.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY};c.setPointerCapture(e.pointerId)});c.addEventListener('pointermove',e=>{if(!drag)return;dx+=e.clientX-drag.x;dy+=e.clientY-drag.y;drag={x:e.clientX,y:e.clientY};draw()});c.addEventListener('pointerup',()=>drag=null);c.addEventListener('pointercancel',()=>drag=null);c.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY<0?1.2:1/1.2)},{passive:false})});base.onload=draw;[...before,...after].forEach(t=>t.im.onload=draw);window.addEventListener('resize',draw);draw()</script></html>'''
    p=Path(out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(template.replace('__DATA__',data),encoding='utf-8')
    return {'path':str(p),'before_tiles':len(prior),'after_tiles':len(merged),'bytes':p.stat().st_size}

def next_action(z):
    if z['status']=='PLANNING':
        missing=[d for d in z['decisions'] if d['status']=='OPEN']
        if missing:return {'action':'ASK_OWNER','questions':missing}
        if not z['research']:return {'action':'RESEARCH','note':'Research world analogues; cite sources, do not infer canon.'}
        return {'action':'PRESENT_SKETCH','note':'Whole-region technical sketch and succinct decision packet; wait for explicit approval.'}
    if not z['sketch_approved']:return {'action':'WAIT_SKETCH_APPROVAL'}
    pending=[e['id'] for e in z['elements'] if e['status']!='VERIFIED']
    if pending:return {'action':'GENERATE_NEXT','element_id':pending[0],'remaining':len(pending)}
    if not z.get('owner_approval'):return {'action':'SHOW_BEFORE_AFTER','note':'Render and deliver full comparison before asking for owner approval.'}
    if z['status']!='PUBLISHED':return {'action':'VERIFY_AND_PUBLISH','note':'Owner-approved candidate; Git transaction with CAS, Drive receipts and readback.'}
    return {'action':'COMPLETE','note':'No handoff until all closure gates and readback passed.'}

def validate_spatial_plan(plan, z, cfg):
    """Validate real candidate anchors and gates; planning PASS never implies image readiness."""
    fail(plan.get('schema')=='NOVYDRES_MAPWORK_V3_KINGSWELL_SPATIAL_PLAN_1','spatial plan schema')
    fail(plan.get('status')=='PLANNING_CANDIDATE','spatial plan must remain candidate until full sketch approval')
    owner=plan.get('owner_decision',{})
    fail(owner.get('same_extent') is True and owner.get('owner_subject_id')=='district-chelsea','Kingswell must equal entire Cidade Velha raion')
    fail(z['owner_subject_id']==owner['owner_subject_id'] and z['id']=='kingswell','zone owner and identity mismatch')
    fail(plan.get('base_u02_sha256')==cfg['reference']['sha256'],'spatial plan U02 SHA mismatch')
    fail(plan.get('working_bounds_px')==z['bounds'],'zone bounds and working plan mismatch')
    bridges=plan.get('bridges',[])
    fail(plan.get('bridge_count_mandatory')==3 and len(bridges)==3,'exactly three historical Vasyl bridge candidates required')
    fail(len({b['id'] for b in bridges})==3,'duplicate historical bridge id')
    pois=plan.get('pois',[])
    required={'poi-14','poi-15','poi-16','poi-17','poi-32'}
    fail(len(pois)==len(required) and {p['id'] for p in pois}==required,'missing, duplicate or unexpected Kingswell POI')
    def anchor(point, label):
        fail(isinstance(point,list) and len(point)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) for v in point),label+': invalid coordinate')
        x,y=point
        fail(0<=x<=cfg['world_size_units'][0] and 0<=y<=cfg['world_size_units'][1],label+': coordinate outside U02')
        fail(z['bounds'][0]<=x<=z['bounds'][2] and z['bounds'][1]<=y<=z['bounds'][3],label+': coordinate outside planning bounds')
    for b in bridges:
        anchor(b.get('center_px'),b['id'])
        fail(b.get('confidence')=='CANDIDATE',b['id']+': must not claim canon bridge position')
    for p in pois:
        anchor(p.get('center_px'),p['id'])
        fail(p.get('canonized_location') is False,p['id']+': unapproved POI position canonized')
    fronts=plan.get('external_resource_fronts',[])
    fail(len(fronts)==3 and {x.get('kind') for x in fronts}=={'gold','diamond','natural_gas'},'missing external resource fronts')
    fail(all(x.get('off_map') is True and 'center_px' not in x for x in fronts),'off-frame extraction may not fabricate on-map POIs')
    gas=next(x for x in fronts if x['kind']=='natural_gas')
    fail(gas.get('primary_transport')=='pipeline','natural gas primary transport must be pipeline')
    exits=plan.get('rail_exit_candidates',[])
    fail(bool(exits) and len({x['id'] for x in exits})==len(exits),'missing or duplicate external rail connector candidates')
    for ex in exits:
        point=ex.get('candidate_exit_px')
        fail(isinstance(point,list) and len(point)==2,'external rail connector invalid coordinate')
        x,y=point
        fail(all(isinstance(v,(int,float)) and math.isfinite(v) for v in point),'external rail connector invalid numeric coordinate')
        w,h=cfg['world_size_units']
        fail(0<=x<=w and 0<=y<=h and (x in (0,w) or y in (0,h)),'external rail connector must touch raster boundary')
        fail(ex.get('status')=='CANDIDATE_NEEDS_SNAP_TO_APPROVED_RAIL_BASELINE','rail exit cannot claim verified geometry')
        fail(ex.get('new_station_authorized') is False and ex.get('new_rail_geometry_authorized') is False,'no new station or rail authorized')
    fail(all(b.get('mixed_ped_vehicle') is True for b in bridges),'all three historic bridges remain mixed-use')
    gates=plan.get('gates',{})
    gate_names=('bridge_river_topology_verified','adjacent_zone_edges_verified','poi_u02_sites_verified','full_technical_sketch_approved','image_generation_authorized')
    fail(all(type(gates.get(k)) is bool for k in gate_names),'missing spatial readiness gate')
    if z['status']=='PLANNING':
        fail(z['sketch_approved'] is False and gates['image_generation_authorized'] is False,'planning zone must not authorize images')
    else:
        fail(all(gates[k] for k in gate_names),'nonplanning zone has unresolved spatial/image gates')
        fail(z['sketch_approved'] is True,'technical sketch not approved')
        fail(bool(z['elements']),'approved sketch has no physical elements')
        fail(bool(z['connectors']) if z['neighbors'] else True,'missing neighbor connectors in approved sketch')
    return {'historical_bridges':3,'pois':5,'resource_fronts':3,'readiness':'PLANNING_NOT_READY_FOR_IMAGE' if z['status']=='PLANNING' else 'SPATIAL_GATES_VERIFIED'}

def _point_inside_polygon(point, poly):
    x,y=point
    inside=False
    for i in range(len(poly)):
        x1,y1=poly[i]; x2,y2=poly[(i+1)%len(poly)]
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:
            inside=not inside
    return inside

def _segment_distance(p, a, b):
    ax,ay=a;bx,by=b;px,py=p
    vx,vy=bx-ax,by-ay
    if vx==0 and vy==0:return math.hypot(px-ax,py-ay)
    t=max(0,min(1,((px-ax)*vx+(py-ay)*vy)/(vx*vx+vy*vy)))
    return math.hypot(px-ax-t*vx,py-ay-t*vy)

def _line_distance(p,coords):
    return min(_segment_distance(p,coords[i],coords[i+1]) for i in range(len(coords)-1))

def validate_integral_sketch(g,plan,z,cfg):
    """Validate editable candidate topology; never interpret a planning PASS as owner approval."""
    fail(g.get('schema')=='NOVYDRES_KINGSWELL_U02_INTEGRAL_SKETCH_1','integral sketch schema')
    fail(g.get('state')=='CANDIDATE_FULL_MAP_NOT_OWNER_APPROVED','sketch cannot silently promote status')
    base=g.get('base',{})
    fail(base.get('sha256')==cfg['reference']['sha256'] and base.get('size_px')==cfg['world_size_units'],'sketch U02 identity mismatch')
    fail(base.get('pixels_modified')==0 and base.get('projection')=='top_down_90_degrees','sketch must preserve U02 top-down pixels')
    scope=g.get('scope',{})
    fail(scope.get('same_extent') is True and scope.get('microcore_is_not_a_second_raion') is True,'Kingswell must be entire Cidade Velha raion')
    bounds=z['bounds']; w,h=cfg['world_size_units']
    def points_on_map(points,name,check_bounds=False):
        fail(isinstance(points,list) and len(points)>=3,name+': insufficient vertices')
        for p in points:
            fail(isinstance(p,list) and len(p)==2 and all(isinstance(v,(float,int)) and math.isfinite(v) for v in p),name+': invalid vertex')
            x,y=p
            fail(0<=x<=w and 0<=y<=h,name+': outside U02')
            if check_bounds:fail(bounds[0]<=x<=bounds[2] and bounds[1]<=y<=bounds[3],name+': outside planning bounds')
    poly=g.get('raion_polygon_candidate_px')
    points_on_map(poly,'Kingswell polygon',True)
    for sector in g.get('land_use_sectors',[]):
        points_on_map(sector.get('polygon_px'),sector['id'])
    river=g.get('waterways',{}).get('rio_vasyl_urban_candidate_px')
    fail(isinstance(river,list) and len(river)>=5,'missing substantial Vasyl river candidate')
    points_on_map(river,'Rio Vasyl line')
    bridges=g.get('historical_bridges',[])
    fail(len(bridges)==3 and len({b.get('id') for b in bridges})==3,'sketch must contain exactly three distinct historical bridges')
    plan_b={b['center_px'][0]:b for b in plan['bridges']}
    for bridge in bridges:
        center=bridge.get('center_px')
        fail(isinstance(center,list) and len(center)==2,'invalid bridge coordinate')
        fail(_point_inside_polygon(center,poly),bridge['id']+': bridge outside Kingswell polygon')
        fail(_line_distance(center,river)<=8,bridge['id']+': historical bridge not snapped to candidate Vasyl river')
        fail(bridge.get('priority')=='mixed_ped_vehicle','bridge must preserve mixed pedestrian/vehicle use')
        fail(bridge.get('span_ends_px') and len(bridge['span_ends_px'])==2,'bridge requires two approaches')
        fail(any(b.get('center_px')==center for b in plan['bridges']),bridge['id']+': bridge differs from spatial plan')
    sites=g.get('poi_sites',[])
    fail(len(sites)==5 and {p.get('id') for p in sites}=={'poi-14','poi-15','poi-16','poi-17','poi-32'},'sketch must contain five Kingswell POIs')
    plan_pois={p['id']:p for p in plan['pois']}
    for poi in sites:
        pt=poi.get('candidate_px')
        fail(pt==plan_pois[poi['id']]['center_px'],poi['id']+': POI mismatch with spatial plan')
        fail(_point_inside_polygon(pt,poly),poi['id']+': POI outside Kingswell polygon')
        fail(poi.get('status')=='CANDIDATE_VISUAL_INSPECTION_REQUIRED',poi['id']+': POI cannot claim visual/canon approval')
    conflicts=g.get('crossing_conflicts',[])
    fail(len(conflicts)==3 and len({c.get('id') for c in conflicts})==3,'three observed crossing discrepancies must remain traceable')
    fail(all(c.get('status')=='UNRESOLVED_VISIBLE_CROSSING_NOT_COUNTED' for c in conflicts),'unverified crossing may not be asserted to be another bridge')
    fail(g.get('validation',{}).get('conflicts_unresolved')==3,'unresolved U02 crossings must be recorded as blockers')
    fail(g.get('adjacency',{}).get('sulfok',{}).get('coordination_needed') is True,'do not silently reassign Sulfok geography')
    rail=g.get('transport',{}).get('external_freight_exit',{})
    fail(rail.get('candidate_px')==[100,h],'external freight connector must stay on verified southern raster edge')
    fail(g['transport'].get('no_new_bridges') is True and g['transport'].get('no_new_international_stops') is True,'sketch cannot add bridge/express station')
    if z['status']!='PLANNING':
        fail(g['validation']['conflicts_unresolved']==0 and g['validation']['owner_sketch_approval'] is True,'sketch has unresolved topology or no owner approval')
    return {'sketch_version':g['version'],'bridges':len(bridges),'pois':len(sites),'crossing_conflicts':len(conflicts),'validity':'CANDIDATE_WITH_BLOCKERS' if z['status']=='PLANNING' else 'SKETCH_APPROVED'}

def audit_required_planning_zones(cfg):
    required=cfg.get('required_planning_zones',[])
    fail(bool(required) and len(required)==len(set(required)),'required planning zones must be configured')
    results=[]
    for folder in required:
        fail(re.fullmatch(r'[a-z][a-z0-9-]+',folder) is not None,'unsafe required zone folder')
        path=ROOT/'zones'/folder/'zone.json'
        planpath=ROOT/'zones'/folder/'spatial-plan.json'
        fail(path.is_file(),f'required zone missing: {folder}/zone.json')
        fail(planpath.is_file(),f'required spatial plan missing: {folder}/spatial-plan.json')
        z=load(path);audit_zone(z,cfg,strict=False)
        plan=load(planpath)
        report=validate_spatial_plan(plan,z,cfg)
        if plan.get('gates',{}).get('integral_sketch_prepared'):
            sketchpath=ROOT/'zones'/folder/'esboco-integral-u02-v1.json'
            fail(sketchpath.is_file(),f'required integral sketch missing: {folder}')
            report['sketch']=validate_integral_sketch(load(sketchpath),plan,z,cfg)
        results.append(report)
    return results

def audit_repository(cfg,state):
    config_check(cfg)
    fail(state['schema']=='NOVYDRES_MAPWORK_V3_WORLD_STATE_1','world state schema')
    fail(state['last_approved_global_release'] is None or isinstance(state['last_approved_global_release'],dict),'global release pointer')
    for p in (ROOT/'zones').glob('*/zone.json'):
        z=load(p);audit_zone(z,cfg,strict=False)
    releases=list((ROOT/'releases').glob('*.json'))
    for p in releases:
        r=load(p)
        fail(r.get('schema')=='NOVYDRES_MAPWORK_V3_RELEASE_1',str(p)+': schema')
        fail(r.get('owner_approval',{}).get('decision')=='APPROVED',str(p)+': missing explicit approval')
        fail(bool(r.get('source_global_approved')),str(p)+': missing global base')
        fail(bool(r.get('local_verified_at')),str(p)+': missing local byte verification receipt')
        fail(bool(r.get('tiles')),str(p)+': release has no tiles')
        for t in r['tiles']:
            fail(t.get('drive_file_id') and re.fullmatch('[0-9a-f]{64}',t.get('sha256','')),str(p)+': tile not uploaded/hashed')
    required_zone_reports=audit_required_planning_zones(cfg)
    if state['last_approved_global_release'] is not None:
        pointer=state['last_approved_global_release']
        fail((ROOT/'releases'/pointer['manifest']).is_file(),'approved global release pointer missing')
    return {'repository':'PASS','zones_checked':len(list((ROOT/'zones').glob('*/zone.json'))),'required_zone_reports':required_zone_reports,'image_readiness':'PLANNING_NOT_READY_FOR_IMAGE' if any(x['readiness']=='PLANNING_NOT_READY_FOR_IMAGE' for x in required_zone_reports) else 'SPATIAL_GATES_VERIFIED','releases_checked':len(releases),'last_global_release':state['last_approved_global_release']}

def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('audit')
    p=sub.add_parser('next');p.add_argument('--zone',required=True)
    p=sub.add_parser('validate');p.add_argument('--zones',nargs='+',required=True);p.add_argument('--assets');p.add_argument('--base');p.add_argument('--strict',action='store_true')
    p=sub.add_parser('render');p.add_argument('--zones',nargs='+',required=True);p.add_argument('--assets',required=True);p.add_argument('--base',required=True);p.add_argument('--out',required=True)
    p=sub.add_parser('compare');p.add_argument('--before');p.add_argument('--after',required=True);p.add_argument('--base',required=True);p.add_argument('--out',required=True)
    args=ap.parse_args();cfg=load(CONFIG)
    try:
        config_check(cfg)
        if args.cmd=='audit': result=audit_repository(cfg,load(STATE))
        elif args.cmd=='next':result=next_action(load(args.zone))
        elif args.cmd=='compare':result=html_compare(args.before,args.after,args.base,args.out,cfg)
        else:
            zones=[load(path) for path in args.zones]
            if args.cmd=='validate':
                result={'zones':[audit_zone(z,cfg,args.assets,args.strict) for z in zones], 'seams':connector_match(zones, require_all=args.strict)}
                if args.base:source_check(args.base,cfg)
            else:result=composite(zones,cfg,args.base,args.assets,args.out)
        print(json.dumps({'status':'PASS','result':result},ensure_ascii=False,indent=2))
    except (Invalid,KeyError,ValueError,OSError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)},ensure_ascii=False),file=sys.stderr);sys.exit(2)
if __name__=='__main__':main()
