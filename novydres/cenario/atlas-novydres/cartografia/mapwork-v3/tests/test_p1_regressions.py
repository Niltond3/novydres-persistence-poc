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


@pytest.mark.xfail(strict=True, reason="P1: direct compositor bypass still works at baseline")
def test_p1_direct_composite_requires_verified_pipeline_contract(tmp_path):
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"unplanned",[2,2,6,6],(240,30,30,255))]
    with pytest.raises(core.Invalid,match="pipeline.*contract"):
        core.composite([zone],cfg,base,assets,tmp_path/"unsafe")


@pytest.mark.xfail(strict=True, reason="P1: approved neighbor without spatial manifest is treated as absent")
def test_p1_existing_approved_neighbor_without_spatial_manifest_fails(tmp_path,monkeypatch):
    monkeypatch.setattr(pipeline,"ROOT",tmp_path)
    folder=tmp_path/"zones"/"neighbor";folder.mkdir(parents=True)
    core.save(folder/"zone.json",{"id":"neighbor","status":"SKETCH_APPROVED"})
    plan={"neighbor_seams":[{"to_zone":"neighbor"}]}
    with pytest.raises(core.Invalid,match="neighbor.*manifest"):
        pipeline.load_verified_neighbors(plan)


@pytest.mark.xfail(strict=True, reason="P1: a POI's entrance is allowed in the building interior")
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
    p["special_sites"]=[{
        "id":"CENTER-DOOR","block_id":report["blocks"][0]["id"],
        "point":[x+.5,y+.5],"entrance":[x+.5,y+.5],
        "footprint":[x+.2,y+.2,x+.8,y+.8]
    }]
    with pytest.raises(urban.ContractError,match="entrance.*boundary"):
        urban.plan_city(p,cfg)


@pytest.mark.xfail(strict=True, reason="P1: last-commit-only push discovery silently skips intermediate requests")
def test_p1_push_with_multiple_distinct_requests_cannot_silently_select_last(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    monkeypatch.setenv("GITHUB_EVENT_BEFORE","a"*40)
    prefix="novydres/cenario/atlas-novydres/cartografia/mapwork-v3/web-requests/"
    def fake_git(args,**kwargs):
        if "rev-parse" in args:
            return "b"*40+"\\n"
        if "diff-tree" in args:
            return prefix+"last.json\\n"
        return prefix+"first.json\\n"+prefix+"last.json\\n"
    monkeypatch.setattr(web_runner.subprocess,"check_output",fake_git)
    with pytest.raises(core.Invalid,match="multiple.*request"):
        web_runner.discover_request_from_push()
