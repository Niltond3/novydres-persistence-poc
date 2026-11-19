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
    assert result['repository']=='PASS' and result['zones_checked']==0

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
