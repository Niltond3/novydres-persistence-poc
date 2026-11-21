"""Integrated synthetic regression for planning -> POI -> unit -> art masks.

These tests intentionally cannot certify the real city: no approved U02 bytes
or surveyed metric corridors are available in the CI workspace.
"""
import copy
import math
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import mapwork as core
import pipeline
import urban_architecture as urban
import urban_content as content


def prepared_case(tmp_path):
    plan=core.load(ROOT/"fixtures"/"topology-synthetic.json")
    cfg=core.load(ROOT/"config.json")
    ctx=content.design_context(plan)
    cell=next(i for i in range(ctx["w"]*ctx["h"])
              if ctx["editable"][i] and i in ctx["distance"] and ctx["labels"][i]>0)
    x,y=cell%ctx["w"],cell//ctx["w"]
    initial=urban.plan_city(plan,cfg)
    unit=next(u for u in initial["work_units"]
              if u["block_label"]==ctx["labels"][cell]
              and u["bbox"][0]<=x<u["bbox"][2] and u["bbox"][1]<=y<u["bbox"][3])
    bid=ctx["blocks"][ctx["labels"][cell]-1]["id"]
    plan["special_sites"]=[{"id":"CIVIC-02","block_id":bid,"point":[x+.5,y+.5],
        "footprint":[x+.2,y+.2,x+.8,y+.8],"entrance":[x+.2,y+.5],
        "work_unit_id":unit["id"]}]
    report=urban.plan_city(plan,cfg)
    design=content.design_unit(plan,report,unit["id"])
    building=next(b for b in design["buildings"] if b["site_id"]=="CIVIC-02")
    assert building["entrance"]==[x+.2,y+.5]
    elems=[{"id":"LOT-"+u["id"],"kind":"lot","work_unit_id":u["id"],
            "core":u["bbox"],"envelope":u["bbox"],"status":"PENDING"}
           for u in report["work_units"]]
    scale=cfg["detail_pixels_per_unit"]
    envelope=[x,y,x+1,y+1]
    mask=Image.new("L",(scale,scale),0)
    draw=ImageDraw.Draw(mask)
    f=building["footprint"]
    rect=[math.ceil((f[0]-x)*scale),math.ceil((f[1]-y)*scale),
          math.floor((f[2]-x)*scale)-1,math.floor((f[3]-y)*scale)-1]
    draw.rectangle(rect,fill=255)
    artist=Image.new("RGBA",(scale,scale),(120,120,150,255))
    artist.save(tmp_path/"civic.png")
    mask.save(tmp_path/"civic.mask.png")
    special={"id":"SPECIAL-CIVIC","kind":"special_building",
             "work_unit_id":unit["id"],"building_id":building["id"],
             "core":building["footprint"],"envelope":envelope,"status":"VERIFIED",
             "asset":{"path":"civic.png","sha256":core.sha(tmp_path/"civic.png")},
             "mask":{"path":"civic.mask.png","sha256":core.sha(tmp_path/"civic.mask.png")}}
    elems.append(special)
    return cfg,plan,report,unit,elems,special


def test_integrated_planning_poi_building_mask_and_production_gate(tmp_path):
    cfg,plan,report,unit,elems,special=prepared_case(tmp_path)
    bound=pipeline.validate_work_unit_bindings({"elements":elems},report,plan=plan)
    assert len(bound)==len(report["work_units"])
    assert report["poi_sites"][0]["work_unit_id"]==unit["id"]
    pipeline.verify_unit_art_masks(plan,report,elems,tmp_path,cfg)
    assert report["generation_ready"] is False
    assert report["gates"]["physical_access_certified"] is False

    # An individually valid mask does not authorize the production composer.
    with pytest.raises(core.Invalid,match="pipeline composition contract"):
        core.composite([],cfg,"missing.png",tmp_path,tmp_path/"denied")

    # Whole-parcel art is not allowed for a special building, even on an editable unit.
    Image.new("L",(cfg["detail_pixels_per_unit"],)*2,255).save(tmp_path/"civic.mask.png")
    with pytest.raises(core.Invalid,match="outside its assigned editable cells or footprint"):
        pipeline.verify_unit_art_masks(plan,report,elems,tmp_path,cfg)


def test_integrated_artifact_ownership_cannot_escape_unit_or_building(tmp_path):
    cfg,plan,report,unit,elems,special=prepared_case(tmp_path)
    other=copy.deepcopy(elems)
    other[-1]["work_unit_id"]="WU-99999-9999-9999"
    with pytest.raises(core.Invalid,match="absent or invalid work_unit_id"):
        pipeline.validate_work_unit_bindings({"elements":other},report,plan=plan)
    other=copy.deepcopy(elems)
    other[-1]["building_id"]="UNAUTHORIZED"
    with pytest.raises(core.Invalid,match="approved building footprint"):
        pipeline.validate_work_unit_bindings({"elements":other},report,plan=plan)
    other=copy.deepcopy(elems)
    other[-1]["kind"]="rail"
    with pytest.raises(core.Invalid,match="global infrastructure"):
        pipeline.validate_work_unit_bindings({"elements":other},report,plan=plan)


def test_integrated_visible_layers_cannot_overlap_without_owner_override(tmp_path):
    cfg,plan,report,unit,elems,special=prepared_case(tmp_path)
    finish=copy.deepcopy(special)
    finish["id"]="FINISH-CIVIC"
    finish["kind"]="finish"
    elems.append(finish)
    # A finish asset with a valid assigned building does not waive a second
    # asset's mask ownership or visible pixel overlap.
    pipeline.validate_work_unit_bindings({"elements":elems},report,plan=plan)
    with pytest.raises(core.Invalid,match="unauthorized visible overlap"):
        pipeline.verify_unit_art_masks(plan,report,elems,tmp_path,cfg)
