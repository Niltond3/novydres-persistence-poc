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
    fail(cfg['schema']=='NOVYDRES_MAPWORK_CONFIG_1','config schema')
    w,h=cfg['world_size_units']; scale=cfg['detail_pixels_per_unit']; tile=cfg['tile_size_px']
    fail(w>0 and h>0 and isinstance(scale,int) and scale>0 and scale<=256,'invalid scale')
    fail(isinstance(tile,int) and tile>=128 and tile<=2048 and tile & (tile-1)==0,'invalid tile size')
    fail(tile % scale == 0,'tile size must be aligned to the reference scale')
    fail(cfg['projection']['type']=='illustrated_2d_topdown','projection must remain 2D')
    fail(cfg['projection']['floor_height_units'] is None,'do not invent absolute height')
    fail(len(cfg['layer_order'])==len(set(cfg['layer_order'])),'duplicate layers')
    fail(re.fullmatch('[0-9a-f]{64}',cfg['reference']['sha256']) is not None,'reference SHA')
    fail(cfg['world_size_units']==[cfg['reference']['width'],cfg['reference']['height']],'base dimensions')
    fail(cfg['drive']['folder_id'] and cfg['reference']['drive_file_id'],'missing Drive storage')

def audit_zone(z, cfg, assets=None, strict=False, *, preflight_verified=False):
    validator=Draft202012Validator(load(SCHEMA)); errors=list(validator.iter_errors(z))
    fail(not errors,'schema: '+('; '.join(e.message for e in errors[:4])))
    bounds=z['bounds']; fail(rect(bounds),'zone rectangle invalid')
    fail(inside(bounds,[0,0,*cfg['world_size_units']]),'zone beyond world')
    fail(z['source_commit']!='UNKNOWN','source commit required')
    fail(len({e['id'] for e in z['elements']})==len(z['elements']),'duplicate element ids')
    fail(len({c['id'] for c in z['connectors']})==len(z['connectors']),'duplicate connector ids')
    fail(z['id'] not in z['neighbors'],'self neighbor')
    fail(z['status'] not in ('GENERATING','VISUAL_REVIEW','OWNER_APPROVED','PUBLISHED') or
         z['sketch_approved'] or preflight_verified,
         ' requires sketch approval;  requires verified editorial register')
    fail(z['status'] not in ('OWNER_APPROVED','PUBLISHED') or z.get('owner_approval'),'owner approval missing')
    if z['status']!='PLANNING':
        fail(not any(d['status']=='OPEN' for d in z['decisions']),'open blocking decision')
        if z['status']!='SKETCH_APPROVED':
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
        candidate_polygon_seam=(z['status']=='SKETCH_APPROVED' and z.get('checkpoint',{}).get('border_anchor_mode')=='SKETCH_POLYGON_CANDIDATE')
        if candidate_polygon_seam:
            fail(not strict,f"{c['id']}: candidate polygon seam is not strict-verified")
        else:
            fail(any(abs(c['x']-bounds[i])<1e-9 for i in (0,2)) or any(abs(c['y']-bounds[i])<1e-9 for i in (1,3)),f"{c['id']}: connector not on boundary")
    if strict:
        fail(z['sketch_approved'] or preflight_verified,
             'missing  sketch or verified  decision authority')
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

def _changed_pixels(a,b):
    """1-bit semantic delta: any changed RGBA channel counts."""
    delta=ImageChops.difference(a.convert('RGBA'),b.convert('RGBA')).split()
    changed=delta[0]
    for band in delta[1:]: changed=ImageChops.lighter(changed,band)
    return changed.point(lambda x:255 if x else 0)

def _tile_protection_mask(protected_u02,px,py,tw,th,scale):
    """Expand only one tile of the reference-grid protection mask; never upscale the atlas."""
    u0,v0=px//scale,py//scale
    u1=(px+tw+scale-1)//scale
    v1=(py+th+scale-1)//scale
    part=protected_u02.crop((u0,v0,u1,v1))
    expanded=part.resize((part.width*scale,part.height*scale),Image.Resampling.NEAREST)
    return expanded.crop((px-u0*scale,py-v0*scale,px-u0*scale+tw,py-v0*scale+th))

def composite(zones,cfg,base,assets,out,approved_before=None,protected_u02=None,*,contract=None,edit_mask_u02=None):
    """Production entry point: fail closed unless pipeline revalidates all bound inputs.

    Python internals are not a security sandbox. _compose_tiles is an internal
    renderer for unit tests; it must never be exposed as an operational CLI.
    """
    fail(isinstance(contract,dict) and contract.get('schema')==
         'NOVYDRES_MAPWORK_COMPOSITION_CONTRACT_1',
         'pipeline composition contract required')
    import pipeline
    pipeline.verify_composition_contract(
        contract,zones,cfg,base,assets,approved_before,protected_u02)
    return _compose_tiles(zones,cfg,base,assets,out,
                          approved_before=approved_before,protected_u02=protected_u02,
                          edit_mask_u02=edit_mask_u02)


def _compose_tiles(zones,cfg,base,assets,out,approved_before=None,protected_u02=None,edit_mask_u02=None):
    source_check(base,cfg)
    for z in zones:audit_zone(z,cfg,assets,strict=True)
    # Neighbor zones may be reserved but not yet rendered; spatial planner owns the seam gate.
    connector_match(zones, require_all=False)
    if protected_u02 is not None:
        fail(protected_u02.size==tuple(cfg['world_size_units']) and protected_u02.mode=='L',
             'protected U02 mask must be an L image matching immutable reference')
    if edit_mask_u02 is not None:
        fail(edit_mask_u02.mode=='L' and
             edit_mask_u02.size==tuple(cfg['world_size_units']),
             'edit mask must be L image on original U02 geometry')
        if protected_u02 is not None:
            fail(ImageChops.darker(edit_mask_u02,protected_u02).getbbox() is None,
                 'approved edit area intersects protected infrastructure')
    previous={}
    old=None
    if approved_before is not None:
        root=Path(approved_before)
        old=load(root/'tiles.json')
        fail(old.get('stage') in ('APPROVED','PUBLISHED'),
             'previous tiles are not an approved release')
        verify_tiles(old,root,cfg)
        prior_entries=old.get('inherited_tiles',[])+old['tiles']
        fail(all(e.get('drive_file_id') for e in prior_entries),
             'approved inherited tiles need remote Drive ID readback receipts')
        previous={(item['x'],item['y']):item for item in prior_entries}
    s=cfg['detail_pixels_per_unit'];t=cfg['tile_size_px'];output=Path(out);output.mkdir(parents=True,exist_ok=True)
    layers={name:i for i,name in enumerate(cfg['layer_order'])}
    elements=[e for z in zones for e in z['elements']]
    elements.sort(key=lambda e:(layers[e['layer']],e['id']))
    coords=tiles_for(zones,cfg)
    if edit_mask_u02 is not None:
        # Only paint tiles actually intersecting owner-authorized pixels. Every
        # untouched approved tile is inherited byte-for-byte, without re-encode.
        box=edit_mask_u02.getbbox()
        fail(box is not None,'empty edit area cannot produce candidate')
        left,top,right,bottom=(box[0]*s,box[1]*s,box[2]*s,box[3]*s)
        coords=[(tx,ty) for tx,ty in coords
                if tx*t<right and (tx+1)*t>left and
                   ty*t<bottom and (ty+1)*t>top]
        fail(bool(coords),'no work units intersect the authorized edit area')
    with Image.open(base) as src:
        src=src.convert('RGBA'); entries=[]
        for tx,ty in coords:
            px,py=tx*t,ty*t
            tw=min(t,cfg['world_size_units'][0]*s-px);th=min(t,cfg['world_size_units'][1]*s-py)
            baseline=src.transform((tw,th),Image.Transform.AFFINE,
                                   (1/s,0,px/s,0,1/s,py/s),Image.Resampling.BICUBIC)
            previous_tile=previous.get((tx,ty))
            if previous_tile:
                with Image.open(Path(approved_before)/previous_tile['filename']) as old_image:
                    im=old_image.convert('RGBA')
                fail(im.size==(tw,th),'previous approved tile dimensions mismatch')
            else:
                im=baseline.copy()
            before=im.copy()
            edit_window=(_tile_protection_mask(edit_mask_u02,px,py,tw,th,s)
                         if edit_mask_u02 is not None else None)
            for e in elements:
                x0,y0,x1,y1=(round(v*s) for v in e['envelope'])
                a0=max(px,x0);b0=max(py,y0);a1=min(px+tw,x1);b1=min(py+th,y1)
                if a1<=a0 or b1<=b0:continue
                with Image.open(Path(assets)/e['asset']['path']) as original, Image.open(Path(assets)/e['mask']['path']) as mm:
                    box=(a0-x0,b0-y0,a1-x0,b1-y0)
                    crop=original.convert('RGBA').crop(box); mask=mm.convert('L').crop(box)
                    alpha=ImageChops.darker(crop.getchannel('A'),mask)
                    if edit_window is not None:
                        window=edit_window.crop((a0-px,b0-py,a1-px,b1-py))
                        alpha=ImageChops.darker(alpha,window)
                    if alpha.getbbox() is None:
                        continue
                    crop.putalpha(alpha)
                    im.alpha_composite(crop,(a0-px,b0-py))
            delta=_changed_pixels(before,im)
            if protected_u02 is not None:
                protection=_tile_protection_mask(protected_u02,px,py,tw,th,s)
                fail(ImageChops.darker(delta,protection).getbbox() is None,
                     f'protected network/territory pixels changed in tile {tx},{ty}')
            if edit_mask_u02 is not None:
                # Explicitly authorized refinement supersedes prior art INSIDE edit mask;
                # old art, territory and network stay byte-identical everywhere else.
                fail(ImageChops.subtract(delta,edit_window).getbbox() is None,
                     f'changed pixels outside owner-authorized edit area in tile {tx},{ty}')
            elif previous_tile:
                old_changes=_changed_pixels(baseline,before)
                fail(ImageChops.darker(delta,old_changes).getbbox() is None,
                     f'previously approved content overwritten in tile {tx},{ty}')
            name=f"tile_{tx}_{ty}.png"; p=output/name; im.save(p,optimize=True)
            entries.append({'x':tx,'y':ty,'filename':name,'sha256':sha(p),'width':tw,'height':th,'drive_file_id':None})
    modified={(item['x'],item['y']) for item in entries}
    inherited=[item for point,item in sorted(previous.items()) if point not in modified]
    zone_ids=sorted(set((old or {}).get('zone_ids',[]))|{z['id'] for z in zones})
    manifest={'schema':'NOVYDRES_MAPWORK_TILES_1',
              'world_size_units':cfg['world_size_units'],'detail_pixels_per_unit':s,
              'tile_size_px':t,'zone_ids':zone_ids,'tiles':entries,
              'inherited_tiles':inherited,
              'parent_manifest_sha256':sha(Path(approved_before)/'tiles.json') if old else None,
              'stage':'CANDIDATE_NOT_UPLOADED'}
    save(output/'tiles.json',manifest);return manifest

def verify_tiles(manifest,root,cfg,inherited_root=None):
    fail(manifest['schema']=='NOVYDRES_MAPWORK_TILES_1','tile schema')
    fail(manifest['detail_pixels_per_unit']==cfg['detail_pixels_per_unit'],'tile scale')
    inherited=manifest.get('inherited_tiles',[])
    current=manifest['tiles']
    identifiers=[(x['x'],x['y']) for x in current+inherited]
    fail(len(identifiers)==len(set(identifiers)),'duplicate tile coordinates in release')
    for t in current:
        p=Path(root)/t['filename'];fail(p.is_file() and sha(p)==t['sha256'],'missing/altered tile '+t['filename'])
    for t in inherited:
        p=Path(inherited_root or root)/t['filename']
        fail(p.is_file() and sha(p)==t['sha256'],'missing/altered inherited tile '+t['filename'])
    return len(identifiers)

def image_uri(image):
    import io
    b=io.BytesIO();image.save(b,format='PNG',optimize=True)
    return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()

def html_compare(before, after, base, out, cfg):
    """ portable lazy-tile viewer; HTML does not contain embedded atlas tiles."""
    import viewer
    return viewer.build_comparison(before,after,base,out,cfg)


def next_action(z):
    if z['status']=='PLANNING':
        if not z['research']:return {'action':'RESEARCH','note':'Research world analogues first; cite sources, do not infer canon.'}
        missing=[d for d in z['decisions'] if d['status']=='OPEN']
        if missing:return {'action':'ASK_OWNER','questions':missing}
        return {'action':'PRESENT_SKETCH','note':'Whole-region technical sketch and succinct decision packet; wait for explicit approval.'}
    if not z['sketch_approved']:return {'action':'WAIT_SKETCH_APPROVAL'}
    if z['status']=='SKETCH_APPROVED' and z['id']=='kingswell':
        return {'action':'BUILD_GLOBAL_TRANSPORT_AND_TERRITORY',
                'note':'Macro sketch U02_KW_SKETCH_02 approved. Vectorize global streets, avenues, interchanges, overpasses, rail, tram and water; classify full territory and derive quadrants bounded by at-grade networks before art.'}
    if z['status']=='SKETCH_APPROVED':
        if not z['elements'] or (z['neighbors'] and not z['connectors']):
            return {'action':'PREPARE_DETAIL_GEOMETRY','note':'Sketch approved; derive lot geometry and shared boundary connectors before art.'}
        return {'action':'SUBDIVIDE_ATOMIC_LOTS_AND_VERIFY_MASKS','note':'14 macro-lot windows exist but protected masks, atomic lots and bilateral seams remain unverified; never generate art in SKETCH_APPROVED.'}
    pending=[e['id'] for e in z['elements'] if e['status']!='VERIFIED']
    if pending:return {'action':'GENERATE_NEXT','element_id':pending[0],'remaining':len(pending)}
    if not z.get('owner_approval'):return {'action':'SHOW_BEFORE_AFTER','note':'Render and deliver full comparison before asking for owner approval.'}
    if z['status']!='PUBLISHED':return {'action':'VERIFY_AND_PUBLISH','note':'Owner-approved candidate; Git transaction with CAS, Drive receipts and readback.'}
    return {'action':'COMPLETE','note':'No handoff until all closure gates and readback passed.'}

def validate_spatial_plan(plan, z, cfg):
    """Validate real candidate anchors and gates; planning PASS never implies image readiness."""
    fail(plan.get('schema')=='NOVYDRES_MAPWORK_KINGSWELL_SPATIAL_PLAN_1','spatial plan schema')
    fail(plan.get('status') in ('PLANNING_CANDIDATE','SKETCH_OWNER_APPROVED_SPATIAL_PREP_PENDING'),'invalid spatial plan planning/approval state')
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
        fail(plan.get('status')=='PLANNING_CANDIDATE' and z['sketch_approved'] is False and gates['image_generation_authorized'] is False,'planning zone must not authorize images')
        readiness='PLANNING_NOT_READY_FOR_IMAGE'
    elif z['status']=='SKETCH_APPROVED':
        fail(plan.get('status')=='SKETCH_OWNER_APPROVED_SPATIAL_PREP_PENDING','approved sketch must use approved plan')
        fail(z['sketch_approved'] is True and gates['full_technical_sketch_approved'] is True and gates.get('integral_sketch_owner_approved') is True,'missing express sketch approval')
        fail(gates['image_generation_authorized'] is False,'sketch approval alone must not authorize image generation')
        readiness='SKETCH_APPROVED_DETAIL_PREP_REQUIRED'
    else:
        fail(all(gates[k] for k in gate_names),'nonplanning zone has unresolved spatial/image gates')
        fail(z['sketch_approved'] is True,'technical sketch not approved')
        fail(bool(z['elements']),'generation stage has no physical elements')
        fail(bool(z['connectors']) if z['neighbors'] else True,'missing neighbor connectors in generating stage')
        readiness='SPATIAL_GATES_VERIFIED'
    return {'historical_bridges':3,'pois':5,'resource_fronts':3,'readiness':readiness}

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
    if z['status']=='PLANNING':
        fail(g.get('state')=='CANDIDATE_FULL_MAP_NOT_OWNER_APPROVED','planning sketch cannot silently promote status')
    else:
        fail(g.get('state')=='OWNER_APPROVED_SKETCH_NO_CONFLICT_MARKERS','approved sketch must have owner-approved state')
        fail(g.get('owner_approval',{}).get('decision')=='APPROVED' and g.get('owner_approval',{}).get('evidence'),'missing owner evidence for sketch')
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
        fail(poi.get('status')==('CANDIDATE_VISUAL_INSPECTION_REQUIRED' if z['status']=='PLANNING' else 'SKETCH_SITE_APPROVED_NOT_GIS_CANON'),poi['id']+': POI site status mismatches sketch stage')
    conflicts=g.get('crossing_conflicts',[])
    if z['status']=='PLANNING':
        fail(len(conflicts)==3 and len({c.get('id') for c in conflicts})==3,'three observed crossing discrepancies must remain traceable in legacy draft')
        fail(g.get('validation',{}).get('conflicts_unresolved')==3,'draft must retain unresolved marker count')
    else:
        fail(len(conflicts)==0,'approved sketch must not carry conflict markers excluded by owner')
        fail(g.get('validation',{}).get('conflicts_unresolved')==0,'approved sketch must not carry conflict marker count')
    fail(g.get('adjacency',{}).get('sulfok',{}).get('coordination_needed') is True,'do not silently reassign Sulfok geography')
    rail=g.get('transport',{}).get('external_freight_exit',{})
    fail(rail.get('candidate_px')==[100,h],'external freight connector must stay on verified southern raster edge')
    fail(g['transport'].get('no_new_bridges') is True and g['transport'].get('no_new_international_stops') is True,'sketch cannot add bridge/express station')
    if z['status']!='PLANNING':
        fail(g['validation']['conflicts_unresolved']==0 and g['validation']['owner_sketch_approval'] is True,'approved sketch has conflict markers or no owner approval')
    return {'sketch_version':g['version'],'bridges':len(bridges),'pois':len(sites),'crossing_conflicts':len(conflicts),'validity':'CANDIDATE_WITH_BLOCKERS' if z['status']=='PLANNING' else 'OWNER_APPROVED_VISUAL_SKETCH'}


def validate_detail_preparation(d, z, plan, sketch, cfg):
    """Fail closed on fictitious production readiness of candidate macro-lot rectangles."""
    fail(d.get('schema')=='NOVYDRES_MAPWORK_KINGSWELL_DETAIL_PREP_1','detail preparation schema')
    fail(d.get('version')=='KW_DETAIL_PREP_V2' and d.get('status')=='GEOMETRY_SEEDED_PENDING_MASK_AND_SEAM_VERIFICATION','detail preparation must be geometry seeded')
    src=d.get('approved_sketch_reference',{})
    fail(src.get('version')==sketch.get('version') and src.get('hash_reference')==cfg['reference']['sha256'] and src.get('owner_approved') is True,'detail preparation sketch reference mismatch')
    fail(src.get('excluded_marker_ids')==['X01','X02','X03'] and len(sketch.get('crossing_conflicts',[]))==0,'owner-excluded conflict overlays cannot return')
    fail(z['status']=='SKETCH_APPROVED' and z['sketch_approved'] is True,'detail preparation requires approved sketch')
    constraints=d.get('constraints',{})
    fail(constraints.get('image_generation_authorized') is False and constraints.get('complete_urban_coverage_verified') is False,'candidate detail plan cannot claim art/coverage readiness')
    fail(constraints.get('roads_water_rail_masks_verified') is False and constraints.get('neighbors_reconciled') is False,'unverified masks or neighbor seams cannot claim pass')
    fail(constraints.get('atomic_window_max_units')==16 and constraints.get('actual_bleed_units')<=cfg['max_bleed_units'],'atomic size or bleed contract mismatch')
    lots=d.get('lots',[])
    required={'KW-L%02d'%i for i in range(1,15)}
    fail(len(lots)==14 and {lot.get('id') for lot in lots}==required,'missing or extra Kingswell macro-lots')
    fail(len(z['elements'])==14 and {e['id'] for e in z['elements']}==required,'zone.elements not synchronized with macro-lot manifest')
    elements={e['id']:e for e in z['elements']}
    groups={g['id']:g['sequence'] for g in d.get('generation_groups',[])}
    fail(set(groups)=={'KW-GEN-%02d'%i for i in range(7)},'required generation groups missing')
    def overlaps(a,b):
        return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
    rects=[]
    poi_positions={p['id']:p['candidate_px'] for p in sketch['poi_sites']}
    seen_pois=[]
    for l in lots:
        name=l['id']; core=l.get('core'); env=l.get('envelope')
        fail(rect(core) and rect(env) and inside(core,env) and inside(env,z['bounds']),name+': invalid core/envelope')
        for other in rects:fail(not overlaps(core,other[1]),name+': overlapping macro-lot cores with '+other[0])
        rects.append((name,core))
        max_bleed=max(core[0]-env[0],core[1]-env[1],env[2]-core[2],env[3]-core[3])
        fail(max_bleed<=cfg['max_bleed_units']+1e-8,name+': bleed exceeds allowed')
        e=elements[name]
        fail(e['core']==core and e['envelope']==env and e['kind']==('special_building' if l['special'] else 'lot'),name+': zone element not synchronized')
        fail(e['status']=='PENDING' and e['asset'] is None and e['mask'] is None,name+': assets cannot be preapproved')
        fail(l['group'] in groups,name+': missing generation group')
        for dep in l.get('depends_on',[]):
            parent=next((x for x in lots if x['id']==dep),None)
            fail(parent is not None and dep!=name,name+': invalid lot dependency')
            fail(groups[parent['group']]<=groups[l['group']],name+': depends on future generation group')
        for item in l.get('contains',[]):
            if item in poi_positions:
                x,y=poi_positions[item]
                fail(core[0]<x<core[2] and core[1]<y<core[3],name+': POI outside lot core')
                seen_pois.append(item)
    fail(set(seen_pois)==set(poi_positions) and len(seen_pois)==5,'five POIs must belong to unique macro-lots')
    # Detect cycles even inside a single allowed generation group.
    byid={l['id']:l for l in lots};active=set();done=set()
    def visit(k):
        fail(k not in active,'cyclic generation dependency')
        if k in done:return
        active.add(k)
        for dep in byid[k].get('depends_on',[]):visit(dep)
        active.remove(k);done.add(k)
    for k in byid:visit(k)
    contracts=d.get('border_contracts',[])
    fail(len(contracts)==4 and len({c['id'] for c in contracts})==4,'four independent boundary reservations required')
    fail(len(z['connectors'])==4 and len({c['id'] for c in z['connectors']})==4,'zone connectors not synchronized with boundary reservations')
    byconn={c['id']:c for c in z['connectors']}
    poly=sketch['raion_polygon_candidate_px']
    for c in contracts:
        x,y=c.get('anchor_px',[None,None])
        fail(c['id'] in byconn and c['target_zone'] in z['neighbors'],'unknown boundary connector or neighbor')
        fail(c.get('edge_state')=='CANDIDATE_NEIGHBOR_NOT_GENERATED' and c.get('requires_neighbor_match') is True,'unverified boundary promoted without neighbor verification')
        actual=byconn[c['id']]
        fail(actual['x']==x and actual['y']==y and actual['width']==c['width_units'] and actual['kind']==c['kind'] and actual['neighbor']==c['target_zone'] and actual['profile']==c['profile'],'connector payload differs from border contract')
        fail(0<=x<=cfg['world_size_units'][0] and 0<=y<=cfg['world_size_units'][1],'connector outside U02')
        fail(min(_segment_distance([x,y],poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly)))<=2,'connector not on proposed raion boundary')
    r=d.get('regional_external_reference',{})
    fail(r.get('owner_zone')=='GLOBAL_RAIL_NOT_KINGSWELL' and r.get('anchor_px')==[100,cfg['world_size_units'][1]],'regional freight connector ownership mismatch')
    fail(r['anchor_px'][0]<z['bounds'][0] and r['id'] not in byconn,'off-zone regional rail must not be assigned to Kingswell')
    fail(r.get('no_new_station') is True and r.get('no_new_track') is True,'regional rail may not create infrastructure')
    internal=d.get('internal_connectors',[])
    fail(len(internal)==35 and len({c['id'] for c in internal})==35,'35 declared internal connectors required')
    intern_ids={c['id'] for c in internal}
    usage={x for l in lots for x in l.get('internal_connectors',[])}
    fail(usage==intern_ids,'internal graph connector missing or orphan')
    valid_refs=required|{c['id'] for c in d.get('external_connectors',[])}
    for c in internal:
        fail(c.get('status')=='PENDING_COORDINATE_CHECK' and c.get('geometry_status')=='GRAPH_ONLY_NEEDS_SNAP_TO_U02','unsnapped internal route promoted')
        fail(bool(c['links']) and all(k in valid_refs for k in c['links']),'broken internal graph reference')
    return {'macro_lots':14,'zone_pending_elements':14,'border_reservations':4,'internal_graph_connectors':35,'unique_pois':5,'atomic_subdivision':'PENDING','mask_status':'PENDING','neighbor_seam_status':'PENDING','image_readiness':'NOT_READY_FOR_ART_GENERATION'}

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
            sketchname=plan.get('integral_sketch_ref','u02-sketch.json')
            fail(re.fullmatch(r'u02-sketch\.json',sketchname) is not None,'unsafe sketch reference')
            sketchpath=ROOT/'zones'/folder/sketchname
            fail(sketchpath.is_file(),f'required integral sketch missing: {folder}')
            sketch=load(sketchpath)
            report['sketch']=validate_integral_sketch(sketch,plan,z,cfg)
            if z.get('elements'):
                detailpath=ROOT/'zones'/folder/'lot-connectors-diagnostic.json'
                fail(detailpath.is_file(),f'required detail preparation missing: {folder}')
                report['detail_preparation']=validate_detail_preparation(load(detailpath),z,plan,sketch,cfg)
        results.append(report)
    return results

def audit_repository(cfg,state):
    config_check(cfg)
    fail(state['schema']=='NOVYDRES_MAPWORK_WORLD_STATE_1','world state schema')
    fail(state['last_approved_global_release'] is None or isinstance(state['last_approved_global_release'],dict),'global release pointer')
    for p in (ROOT/'zones').glob('*/zone.json'):
        z=load(p);audit_zone(z,cfg,strict=False)
    releases=list((ROOT/'releases').glob('*.json'))
    for p in releases:
        r=load(p)
        fail(r.get('schema')=='NOVYDRES_MAPWORK_RELEASE_1',str(p)+': schema')
        fail(r.get('owner_approval',{}).get('decision')=='APPROVED',str(p)+': missing explicit approval')
        fail(bool(r.get('source_global_approved')),str(p)+': missing global base')
        fail(bool(r.get('local_verified_at')),str(p)+': missing local byte verification receipt')
        fail(bool(r.get('tiles')),str(p)+': release has no tiles')
        for t in r['tiles']:
            fail(t.get('drive_file_id') and re.fullmatch('[0-9a-f]{64}',t.get('sha256','')),str(p)+': tile not uploaded/hashed')
    required_zone_reports=audit_required_planning_zones(cfg)
    #  architecture is checked on every CI audit, but synthetic fixtures
    # can NEVER certify the real Kingswell zone or authorize rendering.
    import importlib.util
    arch_path=ROOT/'scripts'/'urban_architecture.py'
    require_arch=arch_path.is_file()
    fail(require_arch,' urban architecture planner missing')
    module_spec=importlib.util.spec_from_file_location('novydres_urban_architecture',arch_path)
    architecture=importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(architecture)
    fixture=load(ROOT/'fixtures'/'topology-synthetic.json')
    arch_report=architecture.plan_city(fixture,cfg)
    fail(arch_report['fixture'] is True and arch_report['generation_ready'] is False,
         'synthetic architecture fixture must never authorize generation')
    fail(arch_report['territory']['coverage_pct']==100 and
         arch_report['geometry']['eligible_coverage_pct']==100 and
         arch_report['geometry']['urban_lots']>=4,
         'architecture  synthetic coverage invalid')
    real_legacy=architecture.audit_sketch_coverage(
        load(ROOT/'zones'/'cidade-velha'/'u02-sketch.json'),
        load(ROOT/'zones'/'cidade-velha'/'lot-connectors-diagnostic.json'),
        *cfg['world_size_units']
    )
    fail(real_legacy['window_coverage_pct']<100,
         'legacy Kingswell windows unexpectedly cover entire territory; update architecture checkpoint')
    if state['last_approved_global_release'] is not None:
        pointer=state['last_approved_global_release']
        fail((ROOT/'releases'/pointer['manifest']).is_file(),'approved global release pointer missing')
    return {'repository':'PASS','zones_checked':len(list((ROOT/'zones').glob('*/zone.json'))),'required_zone_reports':required_zone_reports,'image_readiness':'SPATIAL_GATES_VERIFIED' if all(x['readiness']=='SPATIAL_GATES_VERIFIED' for x in required_zone_reports) else 'NOT_READY_FOR_ART_GENERATION','architecture':{'synthetic_contracts':'PASS','transport':arch_report['transport'],'quadrants':arch_report['geometry']['urban_lots'],'fixture_not_a_real_zone':True,'preliminary_sketch':real_legacy,'real_zone_generation_ready':False},'releases_checked':len(releases),'last_global_release':state['last_approved_global_release']}
