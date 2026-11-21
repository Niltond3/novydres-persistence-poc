import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("urban_architecture",ROOT/"scripts"/"urban_architecture.py")
urban=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=urban
spec.loader.exec_module(urban)


def fixture():
    p=json.loads((ROOT/"fixtures"/"topology-synthetic.json").read_text(encoding="utf-8"))
    cfg=json.loads((ROOT/"config.json").read_text(encoding="utf-8"))
    return p,cfg


def test_transport_declares_road_rail_tram_and_grade_separation():
    p,cfg=fixture()
    t=urban.validate_transport(p["transport"],64,64)
    assert t["roads"]==4
    assert t["rails"]==1
    assert t["trams"]==2
    assert t["detected_nonnode_crossings"]==1
    assert t["declared_crossings"]==1
    assert t["junctions"]["intersection"]==1


def test_transport_plan_builds_real_quadrants_and_work_units():
    p,cfg=fixture()
    report=urban.plan_city(p,cfg)
    assert report["territory"]["coverage_pct"]==100
    assert report["geometry"]["eligible_coverage_pct"]==100
    assert report["geometry"]["urban_lots"]==4
    assert report["geometry"]["work_units"]>4
    assert report["geometry"]["assigned_pixels"]==report["geometry"]["editable_pixels"]
    assert report["geometry"]["lot_semantics"]=="ROAD_BOUNDED_QUADRANT"
    assert report["generation_ready"] is False


def test_rail_viaduct_does_not_create_false_ground_quadrants():
    p,cfg=fixture()
    a=urban.plan_city(p,cfg)["geometry"]["urban_lots"]
    p["transport"]["edges"]=[e for e in p["transport"]["edges"] if e["id"]!="RL-01"]
    p["transport"]["crossings"]=[]
    assert urban.plan_city(p,cfg)["geometry"]["urban_lots"]==a


def test_tram_does_not_split_extra_lots():
    p,cfg=fixture()
    count=urban.plan_city(p,cfg)["geometry"]["urban_lots"]
    p["transport"]["edges"]=[e for e in p["transport"]["edges"] if e["class"]!="tram"]
    assert urban.plan_city(p,cfg)["geometry"]["urban_lots"]==count


def test_crossing_without_viaduct_contract_is_rejected():
    p,cfg=fixture()
    p["transport"]["crossings"]=[]
    with pytest.raises(urban.ContractError,match="undeclared transport crossing"):
        urban.plan_city(p,cfg)


def test_grade_separation_cannot_claim_same_level():
    p,cfg=fixture()
    p["transport"]["edges"][-1]["level"]=0
    p["transport"]["nodes"][-2]["level"]=0
    p["transport"]["nodes"][-1]["level"]=0
    with pytest.raises(urban.ContractError,match="distinct levels"):
        urban.plan_city(p,cfg)


def test_at_grade_crossing_requires_real_split_at_node():
    p,cfg=fixture()
    p["transport"]["edges"][-1]["level"]=0
    p["transport"]["nodes"][-2]["level"]=0
    p["transport"]["nodes"][-1]["level"]=0
    p["transport"]["crossings"]=[{
        "id":"X-MISWIRED","edge_a":"RD-01","edge_b":"RL-01",
        "kind":"at_grade","point":[32,16],"junction_id":"C"
    }]
    with pytest.raises(urban.ContractError,match="crossing does not align junction"):
        urban.plan_city(p,cfg)


def test_region_requires_total_classification():
    p,cfg=fixture()
    p["territory"][0]["polygon"]=[[2,2],[61,2],[61,30],[2,30]]
    with pytest.raises(urban.ContractError,match="territorial coverage incomplete"):
        urban.plan_city(p,cfg)


def test_overlapping_landuse_classes_are_rejected():
    p,cfg=fixture()
    p["territory"].append({"id":"T-DUP","class":"industrial",
                          "polygon":[[10,10],[20,10],[20,20],[10,20]]})
    with pytest.raises(urban.ContractError,match="overlapping primary landuse"):
        urban.plan_city(p,cfg)


def test_invalid_morphology_stops_before_art():
    p,cfg=fixture()
    p["morphology"]["urban"]["use_mix"]["housing"]=0.7
    with pytest.raises(urban.ContractError,match="sum to one"):
        urban.plan_city(p,cfg)


def test_missing_global_network_or_ownership_is_rejected():
    p,cfg=fixture()
    p["transport"]["edges"][0]["owner"]="kingswell"
    with pytest.raises(urban.ContractError,match="GLOBAL_NETWORK|globally owned"):
        urban.plan_city(p,cfg)


def test_missing_ramp_grade_change_is_rejected():
    p,cfg=fixture()
    edge=p["transport"]["edges"][0]
    edge["class"]="ramp"
    edge.pop("level")
    edge["level_from"]=0
    edge["level_to"]=0
    edge["separates_blocks"]=False
    with pytest.raises(urban.ContractError,match="ramp must connect two levels"):
        urban.plan_city(p,cfg)


def test_roundabout_must_have_three_branches_and_ring_geometry():
    p,cfg=fixture()
    p["transport"]["nodes"][1]["kind"]="roundabout"
    with pytest.raises(urban.ContractError,match="roundabout requires a physical ring"):
        urban.plan_city(p,cfg)
    p["transport"]["nodes"][1]["ring_geometry"]=[[30,30],[34,30],[34,34],[30,34]]
    assert urban.validate_transport(p["transport"],64,64)["junctions"]["roundabout"]==1


def test_all_work_units_are_bounded_and_not_over_budget():
    p,cfg=fixture()
    report=urban.plan_city(p,cfg)
    assert all(x["max_render_width_px"]<=1024 and x["max_render_height_px"]<=1024
               for x in report["work_units"])
    p["work_policy"]["max_work_units"]=2
    with pytest.raises(urban.ContractError,match="exceeds budget"):
        urban.plan_city(p,cfg)


def test_work_units_must_fit_without_silent_drop():
    labels=[1,1,1,1]
    eligible=bytearray([1,1,1,1])
    tasks,covered=urban.derive_work_units(2,2,labels,eligible,1,64)
    assert len(tasks)==4 and covered==4
    eligible[2]=1;labels[2]=0
    with pytest.raises(urban.ContractError,match="eligible area is not completely assigned"):
        urban.derive_work_units(2,2,labels,eligible,1,64)


def test_gate_cannot_be_promoted_by_owner_art_flag_alone():
    p,cfg=fixture()
    p["owner_art_authorized"]=True
    report=urban.plan_city(p,cfg)
    assert not report["generation_ready"]
    assert report["gates"]["neighbor_seams"] is False
    assert report["gates"]["pixel_masks_verified"] is False


def test_protected_pixels_cannot_be_repainted():
    before=Image.new("RGBA",(4,4),(10,10,10,255))
    after=before.copy()
    after.putpixel((1,1),(50,50,50,255))
    with pytest.raises(urban.ContractError,match="protected pixel changed"):
        urban.verify_no_protected_edits(before,after,[5])
    assert urban.verify_no_protected_edits(before,after,[0,1,2,3])


def test_no_complete_real_geometry_without_real_transport_and_territory():
    p,cfg=fixture()
    p["fixture_mode"]=False
    p["source_sha256"]=cfg["reference"]["sha256"]
    report=urban.plan_city(p,cfg)
    assert report['gates']['source_bytes_verified'] is False
    assert report['generation_ready'] is False
    assert "source_bytes_verified" in report['blocking_gates']


def test_tram_with_own_barrier_is_rejected():
    p,cfg=fixture()
    p["transport"]["edges"][4]["separates_blocks"]=True
    with pytest.raises(urban.ContractError,match="tram tracks do not create"):
        urban.plan_city(p,cfg)


def test_unclassified_pixels_are_not_assigned_any_work_units():
    p,cfg=fixture()
    report=urban.plan_city(p,cfg)
    assert report['territory']['classified_pixels']==report['territory']['total_pixels']
    assert report['geometry']['assigned_pixels']==report['geometry']['editable_pixels']


def test_special_site_is_represented_as_content_not_new_city_lot():
    p,cfg=fixture()
    orig=urban.plan_city(p,cfg)
    block=orig["blocks"][0]["id"]
    zone,classes,names,_=urban.classify_territory(p)
    eligible=bytearray(1 if zone[i] and classes[i] in (names["urban"],names["industrial"]) else 0
                       for i in range(64*64))
    dividers=urban._line_mask((64,64),p["transport"],lambda e:
                e["separates_blocks"] and e.get("level",e.get("level_from",0))==0).tobytes()
    labels,_=urban._label_blocks(64,64,eligible,dividers,classes)
    protect=urban.spatial_protection_mask(p).tobytes()
    cell=next(i for i,v in enumerate(labels) if v==1 and not protect[i])
    x,y=cell%64,cell//64
    owner=next(u["id"] for u in orig["work_units"] if u["block_label"]==labels[cell]
               and u["bbox"][0]<=x<u["bbox"][2] and u["bbox"][1]<=y<u["bbox"][3])
    p["special_sites"]=[{"id":"CIVIC-01","block_id":block,
                         "point":[x+0.5,y+0.5],"entrance":[x+0.2,y+0.5],
                         "footprint":[x+0.2,y+0.2,x+0.8,y+0.8],
                         "work_unit_id":owner}]
    report=urban.plan_city(p,cfg)
    assert report["geometry"]["urban_lots"]==orig["geometry"]["urban_lots"]
    assert report["block_programs"][0]["poi_sites"]==["CIVIC-01"]


def test_hole_support_for_water_inside_urban_territory():
    p,cfg=fixture()
    hole=[[20,6],[26,6],[26,12],[20,12]]
    p["territory"][0]["holes"]=[hole]
    p["territory"].append({"id":"T-WATER","class":"water","polygon":hole})
    report=urban.plan_city(p,cfg)
    assert report["territory"]["coverage_pct"]==100
    assert report["territory"]["by_landuse"]["water"]>0


def test_interchange_requires_ramps_not_just_a_named_intersection():
    p,cfg=fixture()
    p["transport"]["nodes"][1]["kind"]="interchange"
    with pytest.raises(urban.ContractError,match="grade-changing ramp"):
        urban.plan_city(p,cfg)


def test_at_grade_mixed_rail_road_requires_declared_crossing():
    p,cfg=fixture()
    p["transport"]["nodes"].append({"id":"L","point":[2,2],"kind":"portal","level":0})
    p["transport"]["edges"].append({
        "id":"R-ATGRADE","class":"rail_siding","from":"L","to":"C",
        "points":[[2,2],[32,32]],"level":0,"width_units":1,
        "separates_blocks":True,"owner":"GLOBAL_NETWORK"
    })
    with pytest.raises(urban.ContractError,match="rail crossing"):
        urban.plan_city(p,cfg)


def test_incremental_batches_are_bounded_and_lossless():
    p,cfg=fixture()
    r=urban.plan_city(p,cfg)
    q=r["generation_queue"]
    assert q["batch_size"]==4
    ids=[v for batch in q["batches"] for v in batch["work_unit_ids"]]
    assert len(ids)==r["geometry"]["work_units"]
    assert len(set(ids))==len(ids)
    assert all(len(batch["work_unit_ids"])<=4 for batch in q["batches"])
    assert all(batch["status"]=="PENDING_UNAUTHORIZED" for batch in q["batches"])
    assert not q["generation_authorized"]


def test_invalid_batch_size_cannot_authorize_any_art():
    p,cfg=fixture()
    p["work_policy"]["batch_size"]=201
    with pytest.raises(urban.ContractError,match="batch size"):
        urban.plan_city(p,cfg)


def test_poi_invalid_site_has_no_art_gate():
    p,cfg=fixture()
    report=urban.plan_city(p,cfg)
    p["special_sites"]=[{"id":"MISSING-ENTRANCE","block_id":report["blocks"][0]["id"],
                         "point":[10.5,10.5],"footprint":[10.2,10.2,10.8,10.8]}]
    with pytest.raises(urban.ContractError,match="entrance"):
        urban.plan_city(p,cfg)


def test_explicit_clearance_and_access_mode_required_before_art():
    p,cfg=fixture()
    del p["morphology"]["urban"]["access_mode"]
    with pytest.raises(urban.ContractError,match="access mode required"):
        urban.plan_city(p,cfg)
    p,cfg=fixture()
    del p["morphology"]["urban"]["access_clearance_units"]
    with pytest.raises(urban.ContractError,match="explicit at-grade"):
        urban.plan_city(p,cfg)
