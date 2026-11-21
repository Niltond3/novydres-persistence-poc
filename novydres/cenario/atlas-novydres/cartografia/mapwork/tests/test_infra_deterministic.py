"""Negative deterministic topology/coverage tests must not be bypassed by PASS prose."""
import copy
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import infra_checks as infra
import acceptance as acceptance


def scene(tmp_path):
    zone=tmp_path/"zone.png"
    Image.new("L",(16,16),255).save(zone)
    data={"schema":"NOVYDRES_MAPWORK_INFRA_GEOMETRY",
          "stage":"INF-01","source_sha256":"a"*64,"reference_size":[16,16],
          "zone_mask":{"path":zone.name,"sha256":infra.sha(zone)},
          "network":{"nodes":[{"id":"A","point":[1,1],"level":0},
                              {"id":"B","point":[10,1],"level":0}],
                     "edges":[{"id":"road-01","mode":"road","from":"A","to":"B",
                               "points":[[1,1],[10,1]],"level":0,"width_units":1}],
                     "crossings":[]}}
    geo=tmp_path/"geometry.json"
    geo.write_text(json.dumps(data))
    profile=acceptance.criteria_contract()["profile"]
    return data,geo,profile


def audit(geo,profile,prior=None):
    return infra.validate(geo,source_sha="a"*64,dimensions=(16,16),profile=profile,prior=prior)


def test_pass_real_geometry_math_not_text(tmp_path):
    _,geo,p=scene(tmp_path)
    assert audit(geo,p)["status"]=="PASS"


def test_reject_unconnected_crossing_and_false_grade(tmp_path):
    data,geo,p=scene(tmp_path)
    data["network"]["nodes"] += [{"id":"C","point":[5,0],"level":0},
                                    {"id":"D","point":[5,5],"level":0}]
    data["network"]["edges"] += [{"id":"cross-rail","mode":"rail","from":"C","to":"D",
                                      "points":[[5,0],[5,5]],"level":0,"width_units":1}]
    geo.write_text(json.dumps(data))
    with pytest.raises(infra.InfraInvalid, match="untyped crossing"):
        audit(geo,p)
    data["network"]["crossings"]=[{"a":"road-01","b":"cross-rail","kind":"grade_separated"}]
    geo.write_text(json.dumps(data))
    with pytest.raises(infra.InfraInvalid, match="identical levels"):
        audit(geo,p)


def test_reject_missing_cumulative_parent(tmp_path):
    data,geo,p=scene(tmp_path)
    parent=geo
    nextgeo=tmp_path/"inf02.json"
    data["stage"]="INF-02"
    data["previous_stage_sha256"]="b"*64
    nextgeo.write_text(json.dumps(data))
    with pytest.raises(infra.InfraInvalid,match="stale previous"):
        audit(nextgeo,p,prior=parent)


def test_reject_territorial_holes_and_overlap(tmp_path):
    data,geo,p=scene(tmp_path)
    data["stage"]="INF-07"
    layers={}
    for kind in p["territory_classes"]:
        file=tmp_path/(kind+".png")
        Image.new("L",(16,16),255 if kind=="urban" else 0).save(file)
        layers[kind]={"path":file.name,"sha256":infra.sha(file)}
    data["territory"]={"class_masks":layers}
    geo.write_text(json.dumps(data))
    with pytest.raises(infra.InfraInvalid,match="modal"):
        audit(geo,p)
    # Add required rails/tram/metro in disjoint positions
    for kind,y,l in (("rail",5,0),("tram",9,0),("metro",13,-1)):
        a,b=kind+"A",kind+"B"
        data["network"]["nodes"] += [{"id":a,"point":[1,y],"level":l},
                                        {"id":b,"point":[10,y],"level":l}]
        data["network"]["edges"] += [{"id":kind,"mode":kind,"from":a,"to":b,
                                         "points":[[1,y],[10,y]],"level":l,"width_units":1}]
    geo.write_text(json.dumps(data))
    assert audit(geo,p)["territory_pixels"]==256
    with Image.open(tmp_path/"urban.png") as im:
        damaged=im.copy()
    damaged.putpixel((0,0),0)
    damaged.save(tmp_path/"urban.png")
    layers["urban"]["sha256"]=infra.sha(tmp_path/"urban.png")
    geo.write_text(json.dumps(data))
    with pytest.raises(infra.InfraInvalid,match="territory unclassified"):
        audit(geo,p)


def test_text_only_fake_review_cannot_promote(tmp_path):
    from test_infrastructure_acceptance import fixture,write_json,evaluation
    ledger,record,kw=fixture(tmp_path,stages=7)
    attempt=record["stages"]["INF-01"]["attempts"][0]
    attempt.pop("visual_observations")
    write_json(ledger,record)
    result=evaluation(kw)
    assert result["status"]=="FAIL"
    assert "visual inspection receipt missing" in str(result["blockers"])
