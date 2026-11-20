"""V3.2 P1 red tests: freeze verified baseline before closing bypasses.

Baseline: 2b7016976efd360d9e773b1d8a8db4237a284ff6
GitHub Actions run 44784288668, job 136454880161: 98 passed.
Each strict xfail below must be reproduced on the baseline, then converted
to a normal passing test in the implementation commit that closes the defect.
"""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import mapwork as core
import pipeline
import urban_architecture as urban
import web_runner
from test_pipeline import make_tile_inputs, element


def test_p1_direct_composite_requires_verified_pipeline_contract(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"unplanned",[2,2,6,6],(240,30,30,255))]
    with pytest.raises(core.Invalid,match="pipeline.*contract"):
        core.composite([zone],cfg,base,assets,tmp_path/"unsafe")


def test_p1_existing_approved_neighbor_without_spatial_manifest_fails(tmp_path,monkeypatch):
    monkeypatch.setattr(pipeline,"ROOT",tmp_path)
    folder=tmp_path/"zones"/"neighbor";folder.mkdir(parents=True)
    core.save(folder/"zone.json",{"id":"neighbor","status":"SKETCH_APPROVED"})
    plan={"neighbor_seams":[{"to_zone":"neighbor"}]}
    with pytest.raises(core.Invalid,match="neighbor.*manifest"):
        pipeline.load_verified_neighbors(plan)


def test_p1_poi_entrance_at_building_center_is_rejected():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    report=urban.plan_city(p,cfg)
    zone,classes,names,_=urban.classify_territory(p)
    eligible=bytearray(1 if zone[i] and classes[i] in (names["urban"],names["industrial"]) else 0
                       for i in range(64*64))
    divider=urban._line_mask((64,64),p["transport"],lambda e:
                 e["separates_blocks"] and e.get("level",e.get("level_from",0))==0).tobytes()
    labels,_=urban._label_blocks(64,64,eligible,divider,classes)
    protected=urban.spatial_protection_mask(p).tobytes()
    i=next(i for i,v in enumerate(labels) if v==1 and not protected[i])
    x,y=i%64,i//64
    owner=next(u["id"] for u in report["work_units"] if u["block_label"]==labels[i]
               and u["bbox"][0]<=x<u["bbox"][2] and u["bbox"][1]<=y<u["bbox"][3])
    p["special_sites"]=[{
        "id":"CENTER-DOOR","block_id":report["blocks"][0]["id"],
        "point":[x+.5,y+.5],"entrance":[x+.5,y+.5],
        "footprint":[x+.2,y+.2,x+.8,y+.8],"work_unit_id":owner
    }]
    with pytest.raises(urban.ContractError,match="entrance.*boundary"):
        urban.plan_city(p,cfg)


def test_p1_push_with_multiple_distinct_requests_cannot_silently_select_last(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    monkeypatch.setenv("GITHUB_EVENT_BEFORE","a"*40)
    prefix="novydres/cenario/atlas-novydres/cartografia/mapwork-v3/web-requests/"
    def fake_git(*args):
        if args[:2]==("rev-parse","HEAD"):return "b"*40
        if args[0]=="merge-base":return "a"*40
        if args[0]=="rev-list":return "c"*40+"\\n"+"b"*40
        if args[0]=="diff-tree":
            return prefix+("first.json" if args[-1]=="c"*40 else "last.json")
        raise AssertionError(args)
    monkeypatch.setattr(web_runner,"_git",fake_git)
    with pytest.raises(core.Invalid,match="multiple.*request"):
        web_runner.discover_request_from_push()


def test_p1_push_intermediate_single_request_is_discovered(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    monkeypatch.setenv("GITHUB_EVENT_BEFORE","a"*40)
    prefix="novydres/cenario/atlas-novydres/cartografia/mapwork-v3/web-requests/"
    def fake_git(*args):
        if args[:2]==("rev-parse","HEAD"):return "b"*40
        if args[0]=="merge-base":return "a"*40
        if args[0]=="rev-list":return "c"*40+"\\n"+"b"*40
        if args[0]=="diff-tree":
            return prefix+"intermediate.json" if args[-1]=="c"*40 else ""
        raise AssertionError(args)
    monkeypatch.setattr(web_runner,"_git",fake_git)
    assert web_runner.discover_request_from_push()=="web-requests/intermediate.json"



def test_p1_fake_composition_contract_rejected(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"fake",[2,2,6,6],(240,20,20,255))]
    with pytest.raises(core.Invalid,match="contract"):
        core.composite([zone],cfg,base,assets,tmp_path/"denied",
                       contract={"schema":"NOVYDRES_MAPWORK_V32_COMPOSITION_CONTRACT_1"})


def test_p1_seam_must_touch_real_edge_with_matching_width_level_profile():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    authority=hashlib.sha256(json.dumps(p["transport"],sort_keys=True,
                             separators=(",",":")).encode()).hexdigest()
    seam={"id":"BORDER","from_zone":"test-city","to_zone":"future",
          "point":[2,32],"kind":"road","width_units":3,"profile":"urban_at_grade",
          "level":0,"network_edge_id":"AV-01","network_node_id":"W",
          "reservation_status":"APPROVED_SCOPED","authority_sha256":authority}
    p["neighbor_seams"]=[seam]
    assert urban.plan_city(p,cfg)["gates"]["neighbor_seams"]
    seam["point"]=[2,22]
    with pytest.raises(urban.ContractError,match="transport edge"):
        urban.plan_city(p,cfg)
    seam["point"]=[2,32];seam["level"]=1
    with pytest.raises(urban.ContractError,match="level"):
        urban.plan_city(p,cfg)
    seam["level"]=0;seam["profile"]="wrong"
    with pytest.raises(urban.ContractError,match="profile"):
        urban.plan_city(p,cfg)


def test_p1_existing_peer_must_share_boundary_not_only_connector_id():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    seam={"id":"BORDER","from_zone":"test-city","to_zone":"future",
          "point":[2,32],"kind":"road","width_units":3,"profile":"urban_at_grade",
          "level":0,"network_edge_id":"AV-01","network_node_id":"W"}
    p["neighbor_seams"]=[seam]
    mate={**seam,"from_zone":"future","to_zone":"test-city"}
    peer={"future":{"seams":[mate],"zone_polygon":[[5,2],[6,2],[6,61],[5,61]],
                    "transport":p["transport"]}}
    with pytest.raises(urban.ContractError,match="shared zone boundary"):
        urban.plan_city(p,cfg,neighbor_manifests=peer)
    peer["future"]["zone_polygon"]=[[0,2],[2,2],[2,61],[0,61]]
    assert urban.plan_city(p,cfg,neighbor_manifests=peer)["seam_status"]["matched"]==1
    peer["future"]["seams"].append({**mate,"id":"EXTRA"})
    with pytest.raises(urban.ContractError,match="asymmetric"):
        urban.plan_city(p,cfg,neighbor_manifests=peer)


def test_p1_physical_corridor_geometry_width_and_ground_egress():
    road={"class":"street","level":0,"width_units":1.0,
          "points":[[1.5,0],[1.5,2]]}
    args=dict(entrance=[.8,.5],footprint=[.2,.2,.8,.8],
              mode="pedestrian",scale=10,minimum_width_m=1.2,
              ground_roads=[road])
    good={"mode":"pedestrian","width_m":1.5,
          "points":[[.8,.5],[1.5,.5]]}
    assert urban.validate_physical_route(good,**args)
    with pytest.raises(urban.ContractError,match="insufficient"):
        urban.validate_physical_route({**good,"width_m":.8},**args)
    with pytest.raises(urban.ContractError,match="another building"):
        urban.validate_physical_route(good,obstacles=[[.95,.3,1.1,.7]],**args)
    with pytest.raises(urban.ContractError,match="ground-level"):
        urban.validate_physical_route(good,**{**args,"ground_roads":[{**road,"level":-1}]})
    with pytest.raises(urban.ContractError,match="entrance"):
        urban.validate_physical_route(good,**{**args,"entrance":[.5,.5]})


def test_p1_physical_scale_never_inferred_from_reference_pixels():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    r=urban.plan_city(p,cfg)
    assert r["gates"]["physical_access_certified"] is False
    assert r["access"]["surveyed_scale_available"] is False
    bad={"verification":"SURVEYED_APPROVED","metres_per_unit":1.0,
         "source_sha256":cfg["reference"]["sha256"],
         "owner_approved":False,"evidence":"not reviewed by owner",
         "minimum_width_m":{"pedestrian":1.2,"vehicle":3.0}}
    p["physical_reference"]=bad
    with pytest.raises(urban.ContractError,match="V3.1 schema|explicit owner evidence"):
        urban.plan_city(p,cfg)


def test_p1_global_infrastructure_cannot_paint_as_unit_asset():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    report=urban.plan_city(p,core.load(ROOT/"config.json"))
    elems=[{"id":"L"+u["id"],"kind":"lot","work_unit_id":u["id"],
            "core":u["bbox"],"status":"PENDING"} for u in report["work_units"]]
    first=report["work_units"][0]
    elems.append({"id":"UNOWNED-ROAD","kind":"road","work_unit_id":first["id"],
                  "core":first["bbox"],"status":"PENDING"})
    with pytest.raises(core.Invalid,match="global infrastructure"):
        pipeline.validate_work_unit_bindings({"elements":elems},report,plan=p)


def test_p1_special_building_cannot_claim_arbitrary_footprint():
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    report=urban.plan_city(p,core.load(ROOT/"config.json"))
    elems=[{"id":"L"+u["id"],"kind":"lot","work_unit_id":u["id"],
            "core":u["bbox"],"status":"PENDING"} for u in report["work_units"]]
    u=report["work_units"][0]
    elems.append({"id":"SPECIAL","kind":"special_building","work_unit_id":u["id"],
                  "building_id":"FAKE-BUILDING","core":u["bbox"],"status":"PENDING"})
    with pytest.raises(core.Invalid,match="approved building footprint"):
        pipeline.validate_work_unit_bindings({"elements":elems},report,plan=p)


def test_p1_special_asset_mask_cannot_paint_whole_adjacent_unit(tmp_path):
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    report=urban.plan_city(p,cfg)
    unit=report["work_units"][0]
    from PIL import Image
    scale=cfg["detail_pixels_per_unit"]
    bounds=unit["bbox"]
    im=Image.new("L",((bounds[2]-bounds[0])*scale,
                     (bounds[3]-bounds[1])*scale),255)
    im.save(tmp_path/"wide.png")
    e={"id":"SPECIAL-WIDE","kind":"special_building","work_unit_id":unit["id"],
       "status":"VERIFIED","envelope":bounds,
       "core":[bounds[0]+.25,bounds[1]+.25,bounds[0]+.75,bounds[1]+.75],
       "mask":{"path":"wide.png"}}
    with pytest.raises(core.Invalid,match="outside its assigned editable cells or footprint"):
        pipeline.verify_unit_art_masks(p,report,[e],tmp_path,cfg)


def test_p1_visible_mask_overlap_requires_explicit_owner_authority(tmp_path):
    from PIL import Image
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    cfg["detail_pixels_per_unit"]=8
    Image.new("RGBA",(8,8),(255,0,0,255)).save(tmp_path/"a.png")
    Image.new("RGBA",(8,8),(0,255,0,255)).save(tmp_path/"b.png")
    Image.new("L",(8,8),255).save(tmp_path/"mask.png")
    members=[{"id":id,"work_unit_id":"WU-00001-0000-0000","status":"VERIFIED",
              "asset":{"path":f"{id}.png"},"mask":{"path":"mask.png"},
              "envelope":[0,0,1,1]} for id in ("a","b")]
    with pytest.raises(core.Invalid,match="unauthorized visible overlap"):
        pipeline.verify_art_overlaps(p,members,tmp_path,cfg)
    p["owner_art_authorized"]=True
    p["owner_art_approval"]={"decision":"APPROVED",
        "authorized_overlaps":[{"elements":["a","b"],
                                "evidence":"human owner explicitly reviewed both layers"}]}
    pipeline.verify_art_overlaps(p,members,tmp_path,cfg)
