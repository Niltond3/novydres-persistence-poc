"""Negative and end-to-end tests for the unified, fail-closed pipeline."""
import copy
import hashlib
import importlib.util
import json
import sys
import subprocess
from pathlib import Path

import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import mapwork as core
import urban_architecture as urban
import urban_content
import pipeline


def make_tile_inputs(tmp):
    cfg=copy.deepcopy(core.load(ROOT/"config.json"))
    cfg["world_size_units"]=[32,16]
    cfg["reference"]["width"]=32
    cfg["reference"]["height"]=16
    cfg["detail_pixels_per_unit"]=8
    cfg["tile_size_px"]=128
    base=tmp/"u02.png"
    Image.new("RGBA",(32,16),(40,45,50,255)).save(base)
    cfg["reference"]["sha256"]=core.sha(base)
    assets=tmp/"assets";assets.mkdir()
    zone={
        "schema":"NOVYDRES_MAPWORK_V3_ZONE_1","id":"test","owner_subject_id":"district-test",
        "status":"VISUAL_REVIEW","bounds":[0,0,32,16],
        "neighbors":[],"connectors":[],"decisions":[],
        "research":[{"claim":"synthetic","url":"https://example.org","accessed_on":"2026-11-20"}],
        "sketch_approved":True,
        "source_commit":"de9da452fcc8a808b04519ee6e21f218d2a12314",
        "elements":[]
    }
    return cfg,base,assets,zone


def element(assets,name,bounds,color):
    x0,y0,x1,y1=bounds
    dim=((x1-x0)*8,(y1-y0)*8)
    asset=assets/(name+".png")
    mask=assets/(name+".mask.png")
    Image.new("RGBA",dim,color).save(asset)
    Image.new("L",dim,255).save(mask)
    return {
        "id":name,"kind":"lot","layer":"lot",
        "core":bounds,"envelope":bounds,"status":"VERIFIED",
        "asset":{"path":asset.name,"sha256":core.sha(asset),"drive_file_id":"mock-drive-fixture"},
        "mask":{"path":mask.name,"sha256":core.sha(mask),"drive_file_id":"mock-drive-fixture"}
    }


def mark_approved_tiles(root):
    p=root/"tiles.json"
    manifest=core.load(p)
    manifest["stage"]="APPROVED"
    manifest["owner_approval"]={"decision":"APPROVED","evidence":"synthetic owner fixture only"}
    for tile in manifest["tiles"]:
        tile["drive_file_id"]="synthetic-drive-readback-id"
    core.save(p,manifest)


def test_unified_entrypoint_resolves_existing_and_missing_districts():
    p=pipeline.resolve_zone("kingswell")
    assert p.name=="zone.json" and p.parent.name=="cidade-velha"
    assert pipeline.resolve_zone("sulfok") is None
    rc=pipeline.main(["run","--district","sulfok"])
    assert rc==0


def test_real_kingswell_has_a_real_blocker_not_fake_generation_ready():
    args=type("Args",(),{
        "district":"kingswell","zone":None,"spatial":None,"reference":None,"assets":None,
        "before":None,"out":None,"execute":False
    })()
    r=pipeline.run(args)
    assert r["phase"]=="SPATIAL_MODEL"
    assert r["next_action"]=="BUILD_GLOBAL_TRANSPORT_AND_TERRITORY"
    assert r["publication_authorized"] is False
    assert r["canonical_state_changed"] is False


def test_research_always_precedes_open_owner_questions():
    z={"status":"PLANNING","decisions":[{"id":"Q","status":"OPEN"}],
       "research":[],"sketch_approved":False}
    assert core.next_action(z)["action"]=="RESEARCH"
    z["research"]=[{"claim":"historical analogy"}]
    assert core.next_action(z)["action"]=="ASK_OWNER"


def test_second_composition_preserves_old_art_in_same_tile(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"old",[2,2,6,6],(220,30,30,255))]
    first=tmp_path/"approved"
    core._compose_tiles([zone],cfg,base,assets,first)
    mark_approved_tiles(first)
    old=Image.open(first/"tile_0_0.png").convert("RGBA").getpixel((3*8,3*8))
    assert old==(220,30,30,255)
    zone["elements"]=[element(assets,"new",[8,2,12,6],(25,205,30,255))]
    second=tmp_path/"candidate"
    core._compose_tiles([zone],cfg,base,assets,second,approved_before=first)
    after=Image.open(second/"tile_0_0.png").convert("RGBA")
    assert after.getpixel((3*8,3*8))==old
    assert after.getpixel((9*8,3*8))==(25,205,30,255)


def test_second_composition_cannot_change_previously_approved_pixel(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"old",[2,2,6,6],(220,30,30,255))]
    first=tmp_path/"approved"
    core._compose_tiles([zone],cfg,base,assets,first)
    mark_approved_tiles(first)
    zone["elements"]=[element(assets,"replacement",[2,2,6,6],(30,220,30,255))]
    with pytest.raises(core.Invalid,match="previously approved content overwritten"):
        core._compose_tiles([zone],cfg,base,assets,tmp_path/"candidate",approved_before=first)


def test_compositor_rejects_protected_road_pixels(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"new",[8,2,12,6],(25,205,30,255))]
    protected=Image.new("L",(32,16),0)
    protected.putpixel((9,3),255)
    with pytest.raises(core.Invalid,match="protected network/territory"):
        core._compose_tiles([zone],cfg,base,assets,tmp_path/"candidate",protected_u02=protected)


def test_collinear_road_overlap_cannot_hide_from_validator():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    p["transport"]["nodes"].append(
        {"id":"EX","point":[16,32],"kind":"portal","level":0})
    p["transport"]["edges"].append({
        "id":"DUPLICATE","class":"service","from":"W","to":"EX",
        "points":[[2,32],[16,32]],"level":0,"width_units":1,
        "separates_blocks":True,"owner":"GLOBAL_NETWORK"
    })
    with pytest.raises(urban.ContractError,match="collinear transport overlap"):
        urban.validate_transport(p["transport"],64,64)


def test_first_zone_may_reserve_peer_seam_against_global_network():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    authority=hashlib.sha256(json.dumps(
        p["transport"],sort_keys=True,separators=(",",":")
    ).encode()).hexdigest()
    p["neighbor_seams"]=[{
        "id":"BORDER-01","from_zone":"test-city","to_zone":"future-city",
        "point":[2,32],"kind":"road","width_units":3,"profile":"urban_at_grade",
        "level":0,"network_edge_id":"AV-01","network_node_id":"W",
        "reservation_status":"APPROVED_SCOPED","authority_sha256":authority
    }]
    r=urban.plan_city(p,cfg)
    assert r["seam_status"]["reserved"]==1
    assert r["gates"]["neighbor_seams"] is True
    assert r["seam_status"]["pending_peer_verification"] is True
    peer={"future-city":{"seams":[{
        "id":"BORDER-01","from_zone":"future-city","to_zone":"test-city",
        "point":[2,32],"kind":"road","width_units":4,"profile":"urban_at_grade",
        "level":0,"network_edge_id":"AV-01","network_node_id":"W"
    }]}}
    with pytest.raises(urban.ContractError,match="existing neighbor seam differs"):
        urban.plan_city(p,cfg,neighbor_manifests=peer)


def test_protected_mask_matches_reference_dimensions():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    im=urban.spatial_protection_mask(p)
    assert im.mode=="L" and im.size==(64,64)
    assert sum(1 for v in im.tobytes() if v)>0


def test_urban_design_produces_individual_footprints_with_street_access():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    r=urban.plan_city(p,core.load(ROOT/"config.json"))
    unit=r["work_units"][0]
    design=urban_content.design_unit(p,r,unit["id"])
    assert design["building_count"]==unit["pixels"]
    assert design["parcels_covered_exactly_once"]
    assert design["access_verified"]
    assert all(b["road_access_steps"] is not None for b in design["buildings"])
    for b in design["buildings"]:
        x0,y0,x1,y1=b["parcel"]
        q=b["footprint"]
        assert x0<q[0]<q[2]<x1 and y0<q[1]<q[3]<y1


def test_urban_design_blocks_inaccessible_buildings():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    r=urban.plan_city(p,core.load(ROOT/"config.json"))
    ctx=urban_content.design_context(p)
    ctx["parents"]={}
    ctx["distance"]={}
    design=urban_content.design_unit(p,r,r["work_units"][0]["id"],context=ctx)
    assert design["building_count"]>0
    assert design["access_verified"] is False
    assert len(design["inaccessible_buildings"])==design["building_count"]


def test_underground_metro_does_not_cut_streets_or_erase_surface_buildable_land():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    before=urban.plan_city(p,cfg)
    p["transport"]["nodes"] += [
        {"id":"M1","point":[2,10],"kind":"metro_station","level":-1},
        {"id":"M2","point":[61,50],"kind":"metro_station","level":-1}
    ]
    p["transport"]["edges"].append({
        "id":"METRO-1","class":"metro","from":"M1","to":"M2",
        "points":[[2,10],[61,50]],"level":-1,"width_units":2,
        "separates_blocks":False,"owner":"GLOBAL_NETWORK","structure":"tunnel"
    })
    after=urban.plan_city(p,cfg)
    assert after["transport"]["metro"]==1
    assert after["geometry"]["urban_lots"]==before["geometry"]["urban_lots"]
    assert after["geometry"]["editable_pixels"]==before["geometry"]["editable_pixels"]


def test_underground_pipeline_requires_a_tunnel_and_negative_level():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    p["transport"]["nodes"] += [
        {"id":"U1","point":[2,8],"kind":"utility_hub","level":0},
        {"id":"U2","point":[61,8],"kind":"utility_hub","level":0}
    ]
    p["transport"]["edges"].append({
        "id":"GAS-1","class":"gas_pipe","from":"U1","to":"U2",
        "points":[[2,8],[61,8]],"level":0,"width_units":1,
        "separates_blocks":False,"owner":"GLOBAL_NETWORK"
    })
    with pytest.raises(urban.ContractError,match="underground network requires negative level and tunnel"):
        urban.validate_transport(p["transport"],64,64)


def test_tile_catalogue_inherits_untouched_approved_tiles_across_zones(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"old-west",[2,2,6,6],(220,30,30,255))]
    west=tmp_path/"west"
    core._compose_tiles([zone],cfg,base,assets,west)
    mark_approved_tiles(west)
    zone["id"]="east"
    zone["bounds"]=[16,0,32,16]
    zone["elements"]=[element(assets,"new-east",[18,2,22,6],(25,205,30,255))]
    east=tmp_path/"east"
    manifest=core._compose_tiles([zone],cfg,base,assets,east,approved_before=west)
    assert len(manifest["inherited_tiles"])==1
    assert len(manifest["tiles"])==1
    assert core.verify_tiles(manifest,east,cfg,inherited_root=west)==2
    with pytest.raises(core.Invalid,match="inherited tile"):
        core.verify_tiles(manifest,east,cfg)
    comparison=tmp_path/"compare.html"
    details=core.html_compare(west,east,base,comparison,cfg)
    assert details["before_tiles"]==2
    assert details["after_tiles"]==2


def test_unapproved_prior_tile_manifest_is_rejected(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"old",[2,2,6,6],(220,30,30,255))]
    first=tmp_path/"candidate"
    core._compose_tiles([zone],cfg,base,assets,first)
    with pytest.raises(core.Invalid,match="not an approved release"):
        core._compose_tiles([zone],cfg,base,assets,tmp_path/"new",approved_before=first)


def test_legacy_cli_cannot_skip_unified_planning_gates():
    entry=str(ROOT/"scripts"/"mapwork.py")
    result=subprocess.run(
        [sys.executable,entry,"next","--zone",str(ROOT/"zones"/"cidade-velha"/"zone.json")],
        capture_output=True,text=True,check=False
    )
    assert result.returncode==2
    assert "legacy next/render CLI disabled" in result.stderr
    result=subprocess.run(
        [sys.executable,entry,"render","--zones",str(ROOT/"zones"/"cidade-velha"/"zone.json"),
         "--assets","/tmp/nonexistent","--base","/tmp/nonexistent","--out","/tmp/nonexistent",
         "--protected-mask","/tmp/nonexistent"],
        capture_output=True,text=True,check=False
    )
    assert result.returncode==2
    assert "legacy next/render CLI disabled" in result.stderr


def test_existing_neighbor_manifest_without_mate_is_not_a_reservation():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    authority=hashlib.sha256(json.dumps(p["transport"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
    p["neighbor_seams"]=[{"id":"SEAM","from_zone":"test-city","to_zone":"peer",
                          "point":[2,32],"kind":"road","width_units":3,"profile":"urban_at_grade",
                          "level":0,"network_edge_id":"AV-01","network_node_id":"W",
                          "reservation_status":"APPROVED_SCOPED","authority_sha256":authority}]
    with pytest.raises(urban.ContractError,match="existing neighbor seam differs"):
        urban.plan_city(p,cfg,neighbor_manifests={"peer":{"seams":[]}})


def test_poi_must_have_footprint_entrance_and_verified_block():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    report=urban.plan_city(p,cfg)
    p["special_sites"]=[{"id":"POI","block_id":report["blocks"][0]["id"]}]
    with pytest.raises(urban.ContractError,match="required property"):
        urban.plan_city(p,cfg)


def test_too_dense_morphology_blocks_access_corridor():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    p["morphology"]["urban"]["occupation_target"]=1
    with pytest.raises(urban.ContractError,match="less clearance"):
        urban.plan_city(p,cfg)


def test_atomic_art_bindings_refuse_unplanned_or_missing_work_units():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    report=urban.plan_city(p,core.load(ROOT/"config.json"))
    elements=[{"id":"asset-"+u["id"],"kind":"lot","work_unit_id":u["id"],
               "core":u["bbox"],"envelope":u["bbox"],"status":"PENDING"}
              for u in report["work_units"]]
    assert len(pipeline.validate_work_unit_bindings({"elements":elements},report))==len(elements)
    with pytest.raises(core.Invalid,match="lack bound art elements"):
        pipeline.validate_work_unit_bindings({"elements":elements[:-1]},report)
    corrupted=copy.deepcopy(elements)
    corrupted[0]["core"]=[0,0,1,1]
    with pytest.raises(core.Invalid,match="core differs"):
        pipeline.validate_work_unit_bindings({"elements":corrupted},report)
    corrupted=copy.deepcopy(elements)
    corrupted[0]["work_unit_id"]="WU-99999-9999-9999"
    with pytest.raises(core.Invalid,match="absent or invalid"):
        pipeline.validate_work_unit_bindings({"elements":corrupted},report)


def test_legacy_compare_and_validate_cannot_claim_operational_pass():
    entry=str(ROOT/"scripts"/"mapwork.py")
    for command,args in [("validate",["--zones","dummy"]),("compare",["--after","dummy","--base","dummy","--out","dummy"])]:
        result=subprocess.run([sys.executable,entry,command,*args],capture_output=True,text=True)
        assert result.returncode==2
        assert "CLI disabled" in result.stderr


def test_existing_peer_loader_never_silently_reserves_missing_counterpart(tmp_path,monkeypatch):
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    p["fixture_mode"]=False
    p["source_sha256"]=core.load(ROOT/"config.json")["reference"]["sha256"]
    fake=tmp_path/"mapwork"
    path=fake/"zones"/"peer";path.mkdir(parents=True)
    core.save(path/"zone.json",{"id":"peer","status":"SKETCH_APPROVED"})
    other=copy.deepcopy(p)
    other["zone"]["id"]="peer"
    other["neighbor_seams"]=[]
    core.save(path/"global-spatial-v31.json",other)
    monkeypatch.setattr(pipeline,"ROOT",fake)
    authority=hashlib.sha256(json.dumps(p["transport"],sort_keys=True,separators=(",",":")).encode()).hexdigest()
    p["neighbor_seams"]=[{"id":"X","from_zone":"test-city","to_zone":"peer",
                          "point":[2,32],"kind":"road","width_units":3,"profile":"urban_at_grade",
                          "level":0,"network_edge_id":"AV-01","network_node_id":"W",
                          "reservation_status":"APPROVED_SCOPED","authority_sha256":authority}]
    peers=pipeline.load_verified_neighbors(p)
    assert "peer" in peers
    with pytest.raises(urban.ContractError,match="existing neighbor seam differs"):
        urban.plan_city(p,core.load(ROOT/"config.json"),neighbor_manifests=peers)


def test_legacy_pois_cannot_be_omitted_from_new_spatial_plan(tmp_path):
    folder=tmp_path/"zone";folder.mkdir()
    core.save(folder/"spatial-plan.json",{"pois":[{"id":"POI-MUST-SURVIVE"}]})
    with pytest.raises(core.Invalid,match="POIs missing spatial sites"):
        pipeline.check_canonical_pois(folder/"zone.json",{"special_sites":[]})


def test_work_unit_mask_cannot_paint_outside_its_exact_editable_area(tmp_path):
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    report=urban.plan_city(p,cfg)
    u=report["work_units"][0]
    x0,y0,x1,y1=u["bbox"]
    # Full mask over one-pixel bleed must be rejected, even inside a zone.
    env=[x0-1 if x0>=1 else x0,y0-1 if y0>=1 else y0,x1+1,y1+1]
    scale=cfg["detail_pixels_per_unit"]
    assets=tmp_path/"assets";assets.mkdir()
    mask=assets/"outside.png"
    Image.new("L",((env[2]-env[0])*scale,(env[3]-env[1])*scale),255).save(mask)
    element={"id":"E","status":"VERIFIED","mask":{"path":"outside.png"},"envelope":env}
    with pytest.raises(core.Invalid,match="outside its assigned editable cells"):
        pipeline.verify_unit_art_masks(p,report,{u["id"]:element},assets,cfg)


def test_placed_poi_is_occupant_with_street_access_in_atomic_unit():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    context=urban_content.design_context(p)
    cell=next(i for i,v in enumerate(context["editable"]) if v and i in context["distance"])
    x,y=cell%64,cell//64
    block_id=context["blocks"][context["labels"][cell]-1]["id"]
    p["special_sites"]=[{"id":"POI-ACCESS","block_id":block_id,
                         "point":[x+0.5,y+0.5],"entrance":[x+0.5,y+0.5],
                         "footprint":[x+0.2,y+0.2,x+0.8,y+0.8]}]
    report=urban.plan_city(p,cfg)
    unit=next(u for u in report["work_units"]
              if u["block_label"]==context["labels"][cell]
              and u["bbox"][0]<=x<u["bbox"][2] and u["bbox"][1]<=y<u["bbox"][3])
    design=urban_content.design_unit(p,report,unit["id"])
    sites=[building for building in design["buildings"] if building["site_id"]=="POI-ACCESS"]
    assert len(sites)==1 and sites[0]["road_access_steps"] is not None
    assert sites[0]["use"]=="special_site" and design["access_verified"]
