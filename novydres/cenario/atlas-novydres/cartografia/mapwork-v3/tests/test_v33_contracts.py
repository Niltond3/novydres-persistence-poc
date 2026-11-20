"""Positive, negative and regression contracts for the V3.3 transition."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v33_contracts as c
import v33_viewer as viewer
import mapwork as core


def _intent(**kwargs):
    payload={
        "schema":"NOVYDRES_MAPWORK_V33_INTENT_1",
        "mode":"CREATE_REGION",
        "original_request":"Vamos construir Sulfok",
        "source_commit":"a"*40,
        "target":{"id":"sulfok","subject_id":"district-sulfok","kind":"region"}
    }
    payload.update(kwargs)
    return payload


def _research():
    return [
        {"category":"TECHNICAL","url":"https://example.org/urbanism",
         "accessed_on":"2026-10-01","observation":"Coastal logistics","relevance":"Cold-port city",
         "adaptation":"Use existing permitted connectors","place":"Port Alpha",
         "source_type":"REAL_WORLD"},
        {"category":"TECHNICAL","url":"https://example.net/rail",
         "accessed_on":"2026-10-02","observation":"Railyard typology","relevance":"Industrial cold climate",
         "adaptation":"Research only; no new rail without consent","place":"Port Beta",
         "source_type":"REAL_WORLD"}
    ]


def _register(status="APPROVED"):
    return {"schema":"NOVYDRES_MAPWORK_V33_DECISIONS_1",
            "region":"sulfok","source_commit":"a"*40,
            "proposals":[{
                "id":"SUL-PROP-014",
                "description":"Transshipment yard",
                "location":"Proposed industrial corridor",
                "origin":"External researched analogy",
                "rationale":"Transfers bulk freight",
                "neighbor_impact":"Requires existing rail connectivity",
                "status":status,
                "authorized_ids":["sulfok-yard-1"],
                "decision":{"by":"OWNER","decision":status,
                            "source_commit":"a"*40,
                            "evidence":"Explicit owner answer in phase 3"}
            }]}


def test_create_and_refine_are_canonical_and_mask_bounded():
    targets={
        "sulfok":{"subject_id":"district-sulfok","kind":"region"},
        "tower":{"subject_id":"district-chelsea","kind":"landmark",
                 "bounds":[1,2,9,10]}
    }
    assert c.validate_intent(_intent(),targets,[0,0,20,20])["target"]=="sulfok"
    changed=_intent(mode="REFINE_AREA",target={
        "id":"tower","subject_id":"district-chelsea","kind":"landmark"
    },intervention={"bounds":[2,3,8,9],"source":"OWNER_APPROVED",
                    "authority_ref":"Owner mask decision 14"})
    assert c.validate_intent(changed,targets,[0,0,20,20])["mode"]=="REFINE_AREA"
    changed["intervention"]["bounds"]=[0,0,8,9]
    with pytest.raises(c.Blocked,match="outside known canonical target"):
        c.validate_intent(changed,targets,[0,0,20,20])
    changed=_intent(target={"id":"Torre Ventura","subject_id":"district-chelsea",
                             "kind":"landmark"})
    with pytest.raises(c.Blocked,match="not uniquely resolved"):
        c.validate_intent(changed,targets,[0,0,20,20])


def test_research_requires_multiple_real_domains_and_keeps_proposals_separate():
    assert c.validate_research(_research())["real_world_domains"]==2
    single=_research()[:1]
    with pytest.raises(c.Blocked,match="at least two domains"):
        c.validate_research(single)
    invented=_research()
    invented[0]["category"]="NEW_ELEMENT"
    with pytest.raises(c.Blocked,match="editorial ID"):
        c.validate_research(invented)


def test_explicit_approval_exact_inventory_rejected_and_conditions():
    reg=_register()
    assert c.validate_proposals(reg,region="sulfok",commit="a"*40)["approved"]==["SUL-PROP-014"]
    assert c.validate_inventory([{"id":"sulfok-yard-1","proposal_id":"SUL-PROP-014"}],reg)["elements"]==1
    with pytest.raises(c.Blocked,match="does not enumerate"):
        c.validate_inventory([{"id":"unlisted","proposal_id":"SUL-PROP-014"}],reg)
    with pytest.raises(c.Blocked,match="lacks explicit"):
        c.validate_inventory([{"id":"bridge-not-approved"}],reg)
    pending=_register("PROPOSED")
    pending["proposals"][0].pop("decision")
    with pytest.raises(c.Blocked,match="pending substantive"):
        c.validate_inventory([],pending)
    conditional=_register("APPROVED_WITH_CONDITIONS")
    conditional["proposals"][0]["decision"]["conditions"]="Preserve rail alignment"
    with pytest.raises(c.Blocked,match="conditions have not been verified"):
        c.validate_proposals(conditional,region="sulfok",commit="a"*40)
    conditional["proposals"][0]["decision"].update(
        conditions_verified=True, verification_evidence="Passed bilateral rail check")
    c.validate_proposals(conditional,region="sulfok",commit="a"*40)


def test_capability_fail_closed_and_native_image_must_materialize(tmp_path):
    caps={"schema":"NOVYDRES_MAPWORK_V33_CAPABILITY_1"}
    assert "native_image_materialization" in c.capability_preflight(caps)["missing"]
    im=Image.new("RGBA",(8,8),(10,20,30,255))
    path=tmp_path/"generated.png"
    im.save(path)
    receipt={
        "schema":"NOVYDRES_MAPWORK_V33_IMAGE_RECEIPT_1",
        "work_unit_id":"WU-TEST", "local_path":str(path),
        "sha256":c.digest(path),"generator_evidence":"native image generation call #1"
    }
    assert c.image_receipt(receipt,expected_size=[8,8],work_unit_id="WU-TEST")["path"]==str(path)
    receipt["sha256"]="0"*64
    with pytest.raises(c.Blocked,match="SHA readback"):
        c.image_receipt(receipt,expected_size=[8,8],work_unit_id="WU-TEST")


def test_authorized_mask_allows_repainting_approved_pixels_but_only_inside(tmp_path):
    before=Image.new("RGBA",(8,8),(20,20,20,255))
    after=before.copy();after.putpixel((3,3),(250,20,20,255))
    editable=Image.new("L",(8,8),0)
    for x in range(2,5):
        for y in range(2,5): editable.putpixel((x,y),255)
    protected=Image.new("L",(8,8),0)
    c.validate_edit_mask(editable,[2,2,5,5],protected)
    assert c.verify_edit_pixels(before,after,editable,protected)["protected_unchanged"]
    after.putpixel((7,7),(20,250,20,255))
    with pytest.raises(c.Blocked,match="unapproved edit-area pixels"):
        c.verify_edit_pixels(before,after,editable,protected)
    protected.putpixel((3,3),255)
    with pytest.raises(c.Blocked,match="overlaps protected"):
        c.validate_edit_mask(editable,[2,2,5,5],protected)


def test_resume_reuses_only_verified_hash_bound_units(tmp_path):
    p=tmp_path/"unit.png";Image.new("RGB",(2,2)).save(p)
    inputs={"canon":"a"*40}
    cp={"schema":"NOVYDRES_MAPWORK_V33_UNITS_1",
        "input_sha256":c.evidence_digest(inputs),
        "units":[{"id":"x","status":"VERIFIED","local_path":str(p),"sha256":c.digest(p)},
                 {"id":"y","status":"PENDING"}]}
    assert c.resume_units(cp,expected_inputs=inputs)==["x"]
    with pytest.raises(c.Blocked,match="input drift"):
        c.resume_units(cp,expected_inputs={"canon":"b"*40})
    p.write_bytes(b"corrupt")
    with pytest.raises(c.Blocked,match="missing or altered"):
        c.resume_units(cp,expected_inputs=inputs)


def test_tile_compositor_permits_scoped_approved_replacement(tmp_path):
    from test_pipeline import make_tile_inputs, element, mark_approved_tiles
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"first",[2,2,6,6],(200,30,30,255))]
    first=tmp_path/"approved"
    core._compose_tiles([zone],cfg,base,assets,first)
    mark_approved_tiles(first)
    zone["elements"]=[element(assets,"replacement",[2,2,6,6],(30,200,30,255))]
    editable=Image.new("L",(32,16),0)
    for y in range(2,6):
        for x in range(2,6): editable.putpixel((x,y),255)
    final=tmp_path/"candidate"
    result=core._compose_tiles([zone],cfg,base,assets,final,
                               approved_before=first,edit_mask_u02=editable)
    assert result["tiles"]
    # The compositor defensively clips the replacement to the owner mask:
    # art supplied for a different area MUST NOT touch an approved old pixel.
    wrong=Image.new("L",(32,16),0);wrong.putpixel((0,0),255)
    core._compose_tiles([zone],cfg,base,assets,tmp_path/"wrong",
                        approved_before=first,edit_mask_u02=wrong)
    with Image.open(first/"tile_0_0.png") as baseline, Image.open(
            tmp_path/"wrong"/"tile_0_0.png") as clipped:
        assert baseline.convert("RGBA").tobytes()==clipped.convert("RGBA").tobytes()


def test_html_uses_lazy_external_tiles_and_integral_overview(tmp_path):
    from test_pipeline import make_tile_inputs, element
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"fresh",[2,2,6,6],(30,200,30,255))]
    after=tmp_path/"tiles"
    core._compose_tiles([zone],cfg,base,assets,after)
    out=tmp_path/"comparison.html"
    summary=viewer.build_comparison(None,after,base,out,cfg)
    html=out.read_text(encoding="utf-8")
    assert summary["after_tiles"]>0 and summary["before_tiles"]==0
    assert "drawImage" in html and "ANTES" in html and "DEPOIS" in html
    assert "base64" not in html and "getImage" in html
    assert (tmp_path/"overview-before.png").is_file()
    assert (tmp_path/"overview-after.png").is_file()


def test_native_batch_must_be_the_actual_composited_png_and_mask(tmp_path):
    import pipeline
    from test_pipeline import make_tile_inputs, element
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    uid="WU-TEST-1"
    e=element(assets,"native",[2,2,6,6],(200,30,30,255))
    e["work_unit_id"]=uid
    zone["elements"]=[e]
    unit={"id":uid,"bbox":[2,2,6,6]}
    receipt={
        "schema":"NOVYDRES_MAPWORK_V33_IMAGE_RECEIPT_1",
        "work_unit_id":uid,"local_path":str(assets/e["asset"]["path"]),
        "sha256":e["asset"]["sha256"],
        "mask_sha256":e["mask"]["sha256"],
        "generator_evidence":"Actual native tool receipt #12345",
        "visual_review":{
            "schema":"NOVYDRES_MAPWORK_V33_UNIT_VISUAL_REVIEW_1",
            "by":"AGENT","model":"GPT-6","status":"PASS",
            "work_unit_id":uid,"image_sha256":e["asset"]["sha256"],
            "mask_sha256":e["mask"]["sha256"],
            "reference_sha256":"a"*64,"spatial_sha256":"b"*64,
            "checks":{key:{"status":"PASS","note":"Checked real visual context"}
                      for key in ("mask_and_footprint","urban_structure",
                                  "connections_and_access","micro_to_macro","macro_to_micro")},
            "neighbors":[],"summary":"Agent visually inspected current unit image"
        }
    }
    batch={"schema":"NOVYDRES_MAPWORK_V33_IMAGE_BATCH_1","images":[receipt]}
    assert pipeline.verify_native_manifest(batch,zone,{"work_units":[unit]},cfg,assets,
                                           reference_sha256="a"*64,spatial_sha256="b"*64)==1
    more={"id":"WU-UNCHANGED","bbox":[11,2,15,6]}
    assert pipeline.verify_native_manifest(
        batch,zone,{"work_units":[unit,more]},cfg,assets,
        active_units={uid},reference_sha256="a"*64,spatial_sha256="b"*64)==1
    with pytest.raises(core.Invalid,match="changed work units"):
        pipeline.verify_native_manifest(
            batch,zone,{"work_units":[unit,more]},cfg,assets,
            reference_sha256="a"*64,spatial_sha256="b"*64)
    batch["images"][0]["visual_review"]["status"]="NOT_CHECKED"
    with pytest.raises(c.Blocked,match="agent visual review"):
        pipeline.verify_native_manifest(batch,zone,{"work_units":[unit]},cfg,assets,
                                        reference_sha256="a"*64,spatial_sha256="b"*64)
    batch["images"][0]["visual_review"]["status"]="PASS"
    batch["images"][0]["mask_sha256"]="0"*64
    with pytest.raises(core.Invalid,match="not bound to composited mask"):
        pipeline.verify_native_manifest(batch,zone,{"work_units":[unit]},cfg,assets,
                                        reference_sha256="a"*64,spatial_sha256="b"*64)
    batch["images"][0]["mask_sha256"]=e["mask"]["sha256"]
    other=assets/"other.png"
    Image.new("RGBA",(32,32),(30,200,30,255)).save(other)
    receipt["sha256"]=core.sha(other)
    receipt["local_path"]=str(other)
    with pytest.raises(core.Invalid,match="provenance is not the composited lot asset"):
        pipeline.verify_native_manifest(batch,zone,{"work_units":[unit]},cfg,assets,
                                        reference_sha256="a"*64,spatial_sha256="b"*64)


def test_offline_comparison_zip_contains_html_tiles_and_overviews(tmp_path):
    import zipfile
    from test_pipeline import make_tile_inputs, element
    cfg,base,assets,zone=make_tile_inputs(tmp_path)
    zone["elements"]=[element(assets,"unit",[2,2,6,6],(30,200,30,255))]
    after=tmp_path/"atlas"
    core._compose_tiles([zone],cfg,base,assets,after)
    output=tmp_path/"comparison.html"
    result=viewer.build_comparison(None,after,base,output,cfg)
    with zipfile.ZipFile(result["bundle"]) as z:
        names=set(z.namelist())
        assert "comparison.html" in names
        assert "overview-after.png" in names
        assert "overview-before.png" in names
        assert "viewer-assets/reference.png" in names
        assert any(n.startswith("viewer-assets/after/") for n in names)
        assert "novydres-comparison.zip" not in names


def test_v33_pipeline_enters_capability_gate_without_fabricated_data(tmp_path):
    import pipeline
    intent=_intent(source_commit="a"*40)
    index={
        "schema":"NOVYDRES_MAPWORK_V33_SCOPE_INDEX_1",
        "source_commit":"a"*40,
        "targets":{"sulfok":{"subject_id":"district-sulfok","kind":"region"}},
        "world_bounds":[0,0,1448,1086]
    }
    ip=tmp_path/"intent.json";sp=tmp_path/"scope.json";cp=tmp_path/"result.json"
    ip.write_text(json.dumps(intent),encoding="utf-8")
    sp.write_text(json.dumps(index),encoding="utf-8")
    assert pipeline.main(["run","--intent",str(ip),"--scope-index",str(sp),
                          "--checkpoint",str(cp)])==0
    result=core.load(cp)
    assert result["phase"]=="CAPABILITY_CHECK"
    assert result["canonical_state_changed"] is False
    assert result["publication_authorized"] is False
    with pytest.raises(SystemExit):
        pipeline.main(["run","--district","kingswell","--execute"])


def test_affected_units_only_include_authorized_edit_pixels():
    import pipeline
    work={"work_units":[{"id":"A","bbox":[0,0,8,8]},
                        {"id":"B","bbox":[8,0,16,8]}]}
    mask=Image.new("L",(16,8),0)
    mask.putpixel((9,2),255)
    assert pipeline.affected_unit_ids(work,mask)=={"B"}
    assert pipeline.affected_unit_ids(work,None)=={"A","B"}
    with pytest.raises(core.Invalid,match="no planned work-unit coverage"):
        pipeline.affected_unit_ids(work,Image.new("L",(16,8),0))
