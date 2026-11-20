import importlib.util, hashlib, json
from pathlib import Path
import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mapwork',ROOT/'scripts/mapwork.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def fixture(tmp_path):
    cfg=m.load(ROOT/'config.json')
    cfg['world_size_units']=[64,32];cfg['reference']['width']=64;cfg['reference']['height']=32
    cfg['detail_pixels_per_unit']=8;cfg['tile_size_px']=128
    base=tmp_path/'base.png';Image.new('RGBA',(64,32),(40,50,65,255)).save(base)
    cfg['reference']['sha256']=m.sha(base)
    assets=tmp_path/'assets';assets.mkdir()
    zones=[]
    for i,(name,bounds) in enumerate([('west',[0,0,32,32]),('east',[32,0,64,32])]):
        core=[12+i*32,12,18+i*32,18];env=[11+i*32,11,19+i*32,19]
        el='lot-'+name
        a=assets/(el+'.png'); mask=assets/(el+'.mask.png')
        Image.new('RGBA',(64,64),(145+i*40,120,110,255)).save(a)
        Image.new('L',(64,64),255).save(mask)
        zone={'schema':'NOVYDRES_MAPWORK_V3_ZONE_1','id':name,'owner_subject_id':'district-test',
        'status':'VISUAL_REVIEW','bounds':bounds,'neighbors':['east' if name=='west' else 'west'],
        'connectors':[{'id':'main-road','kind':'road','x':32,'y':16,'width':2,'neighbor':'east' if name=='west' else 'west','profile':'at_grade'}],
        'decisions':[],'research':[{'claim':'synthetic fixture','url':'https://example.org/test','accessed_on':'2026-11-19'}],
        'sketch_approved':True,'source_commit':'432609e642c6569da6a64e302dc8272dd4b4a47f',
        'elements':[{'id':el,'kind':'lot','layer':'lot','core':core,'envelope':env,
        'asset':{'path':a.name,'sha256':m.sha(a),'drive_file_id':'mock-drive-asset'},
        'mask':{'path':mask.name,'sha256':m.sha(mask),'drive_file_id':'mock-drive-mask'},'status':'VERIFIED'}]}
        zones.append(zone)
    return cfg,base,assets,zones

def test_repository_contract():
    result=m.audit_repository(m.load(ROOT/'config.json'),m.load(ROOT/'world-state.json'))
    assert result['repository']=='PASS' and result['zones_checked']==1
    assert result['required_zone_reports'][0]['historical_bridges']==3
    assert result['required_zone_reports'][0]['pois']==5
    assert result['image_readiness']=='NOT_READY_FOR_ART_GENERATION'
    assert result['required_zone_reports'][0]['readiness']=='SKETCH_APPROVED_DETAIL_PREP_REQUIRED'

def test_e2e_tiles_compare(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    for z in zones:assert m.audit_zone(z,cfg,assets,True)['elements']==1
    assert m.connector_match(zones)['verified_adjacent_zone_pairs']==1
    tile_dir=tmp_path/'tiles';result=m.composite(zones,cfg,base,assets,tile_dir)
    assert result['tiles'] and m.verify_tiles(result,tile_dir,cfg)==len(result['tiles'])
    html=tmp_path/'comparison.html';info=m.html_compare(None,tile_dir,base,html,cfg)
    assert info['after_tiles']==len(result['tiles'])
    text=html.read_text();assert 'ANTES' in text and 'DEPOIS' in text and 'drawImage' in text

def test_seam_mismatch_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    zones[1]['connectors'][0]['width']=2.1
    with pytest.raises(m.Invalid,match='seam mismatch'):m.connector_match(zones)

def test_unapproved_sketch_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    zones[0]['sketch_approved']=False
    with pytest.raises(m.Invalid,match='sketch'):m.audit_zone(zones[0],cfg,assets,True)

def test_scale_mismatch_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    zones[0]['elements'][0]['envelope'][2]+=0.125
    with pytest.raises(m.Invalid,match='common scale'):m.audit_zone(zones[0],cfg,assets,True)

def test_alpha_outside_mask_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    e=zones[0]['elements'][0];mp=assets/e['mask']['path']
    img=Image.open(mp).convert('L');img.putpixel((0,0),0);img.save(mp)
    e['mask']['sha256']=m.sha(mp)
    with pytest.raises(m.Invalid,match='outside mask'):m.audit_zone(zones[0],cfg,assets,True)

def test_hash_tamper_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    p=assets/zones[0]['elements'][0]['asset']['path']
    p.write_bytes(p.read_bytes()+b'X')
    with pytest.raises(m.Invalid,match='SHA mismatch'):m.audit_zone(zones[0],cfg,assets,True)

def test_bleed_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    zones[0]['elements'][0]['core'][0]+=3
    with pytest.raises(m.Invalid,match='bleed too large'):m.audit_zone(zones[0],cfg,assets,True)

def test_checkpoints_and_gates(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    z=zones[0];z['status']='PLANNING';z['decisions']=[{'id':'q1','question':'What density?','status':'OPEN'}]
    assert m.next_action(z)['action']=='ASK_OWNER'
    z['decisions'][0]['status']='APPROVED'
    assert m.next_action(z)['action']=='PRESENT_SKETCH'
    z['status']='GENERATING';z['elements'][0]['status']='PENDING'
    assert m.next_action(z)['action']=='GENERATE_NEXT'
    z['elements'][0]['status']='VERIFIED'
    assert m.next_action(z)['action']=='SHOW_BEFORE_AFTER'
    z['owner_approval']={'decision':'APPROVED','evidence':'explicit user acceptance','approved_on':'2026-11-19'}
    assert m.next_action(z)['action']=='VERIFY_AND_PUBLISH'

def test_source_sha_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    cfg['reference']['sha256']='0'*64
    with pytest.raises(m.Invalid,match='U02 changed'):m.source_check(base,cfg)

def test_duplicate_elements_fails(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    zones[0]['elements'].append(zones[0]['elements'][0].copy())
    with pytest.raises(m.Invalid,match='duplicate element'):m.audit_zone(zones[0],cfg,assets,True)

def test_strict_requires_both_neighbors(tmp_path):
    cfg,base,assets,zones=fixture(tmp_path)
    with pytest.raises(m.Invalid,match='missing neighbor'):
        m.connector_match([zones[0]],require_all=True)

def test_release_rejects_missing_receipts(tmp_path, monkeypatch):
    cfg=m.load(ROOT/'config.json');st=m.load(ROOT/'world-state.json')
    fake=tmp_path/'mapwork';(fake/'zones').mkdir(parents=True);(fake/'releases').mkdir()
    bad={'schema':'NOVYDRES_MAPWORK_V3_RELEASE_1','source_global_approved':'U02',
         'owner_approval':{'decision':'APPROVED'},'local_verified_at':'2026-11-19',
         'tiles':[{'drive_file_id':None,'sha256':'0'*64}]}
    m.save(fake/'releases'/'r.json',bad)
    monkeypatch.setattr(m,'ROOT',fake)
    with pytest.raises(m.Invalid,match='not uploaded'):m.audit_repository(cfg,st)


def planning_inputs():
    cfg=m.load(ROOT/'config.json')
    z=m.load(ROOT/'zones/cidade-velha/zone.json')
    plan=m.load(ROOT/'zones/cidade-velha/spatial-plan.json')
    return cfg,z,plan

def test_kingswell_identity_spatial_gate():
    cfg,z,plan=planning_inputs()
    assert z['sketch_approved'] is True
    assert m.validate_spatial_plan(plan,z,cfg)['readiness']=='SKETCH_APPROVED_DETAIL_PREP_REQUIRED'

def test_bridge_exact_count_and_uniqueness():
    cfg,z,plan=planning_inputs()
    plan['bridges'].append(dict(plan['bridges'][0],id='KW-VASYL-04'))
    with pytest.raises(m.Invalid,match='exactly three'):
        m.validate_spatial_plan(plan,z,cfg)
    _,z,plan=planning_inputs()
    plan['bridges'][1]['id']=plan['bridges'][0]['id']
    with pytest.raises(m.Invalid,match='duplicate historical bridge'):
        m.validate_spatial_plan(plan,z,cfg)

def test_missing_poi_or_site_outside_world_fails():
    cfg,z,plan=planning_inputs()
    plan['pois']=plan['pois'][:-1]
    with pytest.raises(m.Invalid,match='missing, duplicate or unexpected Kingswell POI'):
        m.validate_spatial_plan(plan,z,cfg)
    _,z,plan=planning_inputs()
    plan['bridges'][0]['center_px']=[-1,765]
    with pytest.raises(m.Invalid,match='outside U02'):
        m.validate_spatial_plan(plan,z,cfg)

def test_offframe_resources_and_transport_are_checked():
    cfg,z,plan=planning_inputs()
    plan['external_resource_fronts'][0]['center_px']=[900,700]
    with pytest.raises(m.Invalid,match='off-frame extraction'):
        m.validate_spatial_plan(plan,z,cfg)
    _,z,plan=planning_inputs()
    next(f for f in plan['external_resource_fronts'] if f['kind']=='natural_gas')['primary_transport']='rail'
    with pytest.raises(m.Invalid,match='natural gas primary transport'):
        m.validate_spatial_plan(plan,z,cfg)

def test_no_unapproved_spatial_promotion():
    cfg,z,plan=planning_inputs()
    z['status']='GENERATING'
    with pytest.raises(m.Invalid,match='unresolved spatial'):
        m.validate_spatial_plan(plan,z,cfg)

def test_missing_real_zone_is_not_false_pass(tmp_path,monkeypatch):
    cfg,z,plan=planning_inputs()
    fake=tmp_path/'mapwork';(fake/'zones').mkdir(parents=True);(fake/'releases').mkdir()
    monkeypatch.setattr(m,'ROOT',fake)
    with pytest.raises(m.Invalid,match='required zone missing'):
        m.audit_repository(cfg,m.load(ROOT/'world-state.json'))


def test_canonical_sources_follow_entire_raion_correction():
    cenario=ROOT.parents[2]
    city=json.loads((cenario/'geografia/district-chelsea/cidade-velha-2010.json').read_text())
    raions=json.loads((cenario/'atlas-novydres/raions-oficiais-2010.json').read_text())
    assert city['feature']['is_entire_raion'] is True
    assert city['feature']['spatial_identity']['same_extent'] is True
    assert next(r for r in raions['raions'] if r['subject_id']=='district-chelsea')['same_extent_as_cidade_velha'] is True


def test_rail_exit_is_real_border_candidate_not_new_station():
    cfg,z,plan=planning_inputs()
    assert m.validate_spatial_plan(plan,z,cfg)['historical_bridges']==3
    plan['rail_exit_candidates'][0]['candidate_exit_px']=[100,1000]
    with pytest.raises(m.Invalid,match='raster boundary'):
        m.validate_spatial_plan(plan,z,cfg)
    _,z,plan=planning_inputs()
    plan['rail_exit_candidates'][0]['new_station_authorized']=True
    with pytest.raises(m.Invalid,match='no new station'):
        m.validate_spatial_plan(plan,z,cfg)

def test_all_historical_bridges_must_be_mixed_use():
    cfg,z,plan=planning_inputs()
    plan['bridges'][2]['mixed_ped_vehicle']=False
    with pytest.raises(m.Invalid,match='mixed-use'):
        m.validate_spatial_plan(plan,z,cfg)


def integral_sketch_inputs():
    cfg,z,plan=planning_inputs()
    g=m.load(ROOT/'zones/cidade-velha/esboco-integral-u02-v2.json')
    return cfg,z,plan,g

def test_integral_sketch_matches_spatial_plan():
    cfg,z,plan,g=integral_sketch_inputs()
    result=m.validate_integral_sketch(g,plan,z,cfg)
    assert result['validity']=='OWNER_APPROVED_VISUAL_SKETCH'
    assert result['bridges']==3 and result['pois']==5
    assert result['crossing_conflicts']==0

def test_historical_bridge_cannot_be_off_river():
    cfg,z,plan,g=integral_sketch_inputs()
    g['historical_bridges'][1]['center_px']=[740,900]
    with pytest.raises(m.Invalid,match='not snapped'):
        m.validate_integral_sketch(g,plan,z,cfg)

def test_kingswell_poi_must_be_inside_raion_polygon():
    cfg,z,plan,g=integral_sketch_inputs()
    g['poi_sites'][0]['candidate_px']=[100,200]
    with pytest.raises(m.Invalid,match='POI mismatch|outside Kingswell polygon'):
        m.validate_integral_sketch(g,plan,z,cfg)

def test_owner_removed_crossing_markers_cannot_reappear():
    cfg,z,plan,g=integral_sketch_inputs()
    g['crossing_conflicts']=[{'id':'X01','center_px':[355,742]}]
    with pytest.raises(m.Invalid,match='must not carry conflict markers'):
        m.validate_integral_sketch(g,plan,z,cfg)

def test_approved_sketch_requires_owner_proof():
    cfg,z,plan,g=integral_sketch_inputs()
    g['validation']['owner_sketch_approval']=False
    with pytest.raises(m.Invalid,match='no owner approval'):
        m.validate_integral_sketch(g,plan,z,cfg)

def test_sketch_source_image_preserved():
    cfg,z,plan,g=integral_sketch_inputs()
    g['base']['pixels_modified']=1
    with pytest.raises(m.Invalid,match='preserve U02'):
        m.validate_integral_sketch(g,plan,z,cfg)


def test_next_after_approved_sketch_is_detail_geometry_not_art():
    cfg,z,plan=planning_inputs()
    nxt=m.next_action(z)
    assert nxt['action']=='SUBDIVIDE_ATOMIC_LOTS_AND_VERIFY_MASKS'
    assert m.audit_zone(z,cfg,strict=False)['elements']==14
    assert m.validate_spatial_plan(plan,z,cfg)['readiness']=='SKETCH_APPROVED_DETAIL_PREP_REQUIRED'


def detail_inputs():
    cfg,z,plan,sketch=integral_sketch_inputs()
    d=m.load(ROOT/'zones/cidade-velha/lotes-conectores-v2.json')
    return cfg,z,plan,sketch,d

def test_detail_macrolots_and_seams_are_persisted_but_not_art_ready():
    cfg,z,plan,g,d=detail_inputs()
    r=m.validate_detail_preparation(d,z,plan,g,cfg)
    assert r['macro_lots']==14
    assert r['border_reservations']==4 and r['internal_graph_connectors']==35
    assert r['image_readiness']=='NOT_READY_FOR_ART_GENERATION'
    assert m.next_action(z)['action']=='SUBDIVIDE_ATOMIC_LOTS_AND_VERIFY_MASKS'

def test_macrolot_overlap_is_rejected():
    cfg,z,plan,g,d=detail_inputs()
    d['lots'][1]['core']=d['lots'][0]['core'][:]
    d['lots'][1]['envelope']=d['lots'][0]['envelope'][:]
    e=next(e for e in z['elements'] if e['id']=='KW-L02')
    e['core']=d['lots'][1]['core'][:];e['envelope']=d['lots'][1]['envelope'][:]
    with pytest.raises(m.Invalid,match='overlapping macro-lot cores'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_poi_not_inside_core_is_rejected():
    cfg,z,plan,g,d=detail_inputs()
    d['lots'][0]['contains'].append('poi-14')
    with pytest.raises(m.Invalid,match='POI outside lot core'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_future_group_dependency_is_rejected():
    cfg,z,plan,g,d=detail_inputs()
    d['lots'][0]['depends_on']=['KW-L14']
    with pytest.raises(m.Invalid,match='future generation group'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_cyclic_dependency_is_rejected():
    cfg,z,plan,g,d=detail_inputs()
    d['lots'][0]['depends_on']=['KW-L02']
    with pytest.raises(m.Invalid,match='cyclic generation dependency'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_border_must_stay_on_sketch_perimeter():
    cfg,z,plan,g,d=detail_inputs()
    d['border_contracts'][0]['anchor_px']=[550,850]
    z['connectors'][0]['x']=550;z['connectors'][0]['y']=850
    with pytest.raises(m.Invalid,match='not on proposed raion boundary'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_regional_rail_cannot_be_claimed_by_kingswell():
    cfg,z,plan,g,d=detail_inputs()
    d['regional_external_reference']['owner_zone']='kingswell'
    with pytest.raises(m.Invalid,match='regional freight connector ownership'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_candidate_must_not_claim_mask_verified():
    cfg,z,plan,g,d=detail_inputs()
    d['constraints']['roads_water_rail_masks_verified']=True
    with pytest.raises(m.Invalid,match='unverified masks'):
        m.validate_detail_preparation(d,z,plan,g,cfg)

def test_missing_connector_or_missing_element_fails():
    cfg,z,plan,g,d=detail_inputs()
    z['connectors'].pop()
    with pytest.raises(m.Invalid,match='zone connectors not synchronized'):
        m.validate_detail_preparation(d,z,plan,g,cfg)
    cfg,z,plan,g,d=detail_inputs()
    z['elements'].pop()
    with pytest.raises(m.Invalid,match='zone.elements not synchronized'):
        m.validate_detail_preparation(d,z,plan,g,cfg)
