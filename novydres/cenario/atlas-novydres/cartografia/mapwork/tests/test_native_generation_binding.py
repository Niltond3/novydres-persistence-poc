"""Mandatory native visual reference and edit-mask handoff; no false transport PASS."""
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import contracts
import native_generation as native
import orchestration
import synthetic_trial
import flow
from native_fixture import fixture
from test_synthetic_trial_isolation import prepared, geometry, OP


def test_reference_bound_request_is_edit_only_and_concrete(tmp_path):
    req,h,inputs,_,_=fixture(tmp_path)
    assert req["scope"]=="SYNTHETIC"
    assert req["mode"]=="EDIT_WITH_REFERENCE"
    assert req["required_input_roles"]==["reference-image","edit-mask"]
    assert "infográficos" in req["prompt"]
    assert native.json_digest(req)==h["request_sha256"]
    assert native.verify_handoff(h,request=req,
        output_sha256=inputs["image"]["sha256"])["status"]=="VERIFIED_INPUT_BINDINGS"


@pytest.mark.parametrize("fault, match", [
    ("missing_reference", "reference-image and edit-mask"),
    ("fake_mask_hash", "edit-mask input differs"),
    ("fake_mask_get", "edit-mask input differs"),
    ("fake_reference_get", "reference-image input differs"),
    ("same_reference_get", "reference-image independent Drive GET missing"),
    ("fake_source_id", "dispatch has no matching visual input attachments"),
    ("missing_generation_id", "dispatch has no matching visual input attachments"),
    ("different_prompt", "dispatch has no matching visual input attachments"),
    ("missing_dispatch", "dispatch has no matching visual input attachments"),
    ("fake_output", "generated image receipt/output mismatch"),
    ("fake_request_hash", "request fingerprint mismatch"),
])
def test_tampered_or_unattached_visual_inputs_fail_closed(tmp_path, fault, match):
    req,h,inputs,_,_=fixture(tmp_path)
    h=copy.deepcopy(h)
    if fault=="missing_reference":
        h["inputs"].pop("reference-image")
    elif fault=="fake_mask_hash":
        h["inputs"]["edit-mask"]["sha256"]="f"*64
    elif fault=="fake_mask_get":
        Path(h["inputs"]["edit-mask"]["readback_path"]).write_bytes(b"tampered")
    elif fault=="fake_reference_get":
        Path(h["inputs"]["reference-image"]["readback_path"]).write_bytes(b"tampered")
    elif fault=="same_reference_get":
        h["inputs"]["reference-image"]["readback_path"]=h["inputs"]["reference-image"]["path"]
    elif fault=="fake_source_id":
        h["dispatch"]["attached_inputs"]["reference-image"]["remote_id"]="another-source"
    elif fault=="missing_generation_id":
        h["dispatch"].pop("generation_id")
    elif fault=="different_prompt":
        h["dispatch"]["prompt_sha256"]="f"*64
    elif fault=="missing_dispatch":
        h.pop("dispatch")
    elif fault=="fake_output":
        h["dispatch"]["result_sha256"]="f"*64
    elif fault=="fake_request_hash":
        h["request_sha256"]="f"*64
    with pytest.raises(ValueError,match=match):
        native.verify_handoff(h,request=req,output_sha256=inputs["image"]["sha256"])


def test_incompatible_png_reference_and_mask_are_rejected(tmp_path):
    req,h,inputs,_,_=fixture(tmp_path)
    other=tmp_path/"different-shape.png"
    Image.new("L",(12,15),255).save(other)
    got=tmp_path/"different-get.png";got.write_bytes(other.read_bytes())
    h["inputs"]["edit-mask"].update(path=str(other),readback_path=str(got),
                                      sha256=native.digest(other.read_bytes()))
    req=copy.deepcopy(req)
    req["mask_sha256"]=native.digest(other.read_bytes())
    req["prompt_sha256"]=native.digest(req["prompt"].encode())
    h["request_sha256"]=native.json_digest(req)
    h["dispatch"]["request_sha256"]=native.json_digest(req)
    with pytest.raises(ValueError,match="mask and reference dimensions differ"):
        native.verify_handoff(h,request=req,output_sha256=inputs["image"]["sha256"])


def test_operation_identity_and_native_output_are_bound(tmp_path):
    req,h,inputs,_,_=fixture(tmp_path,"fixed-operation")
    with pytest.raises(ValueError,match="operation_id mismatch"):
        native.verify_handoff(h,request=req,output_sha256=inputs["image"]["sha256"],
                              expected_operation_id="foreign-operation")
    with pytest.raises(ValueError,match="receipt/output mismatch"):
        native.verify_handoff(h,request=req,output_sha256="0"*64)


def test_synthetic_pipeline_blocks_without_reference_then_audits_bound_failure(tmp_path):
    args,spec,_=prepared(tmp_path)
    geometry(tmp_path,args)
    assert flow.run(args,None)["next_action"]=="MATERIALIZE_SYNTHETIC_REFERENCE_AND_MASK"
    req,h,inputs,_,review=fixture(tmp_path,OP)
    spec.update(native_reference_sha256=req["reference_sha256"],
                native_mask_sha256=req["mask_sha256"],
                native_edit_goal="Convert crossing into a road overpass, keeping rail and road continuous")
    Path(args.synthetic_trial).write_text(json.dumps(spec))
    state=flow.run(args,None)
    assert state["next_action"]=="GENERATE_AND_AUDIT_CANDIDATE"
    assert state["audit"]["native_edit_request_sha256"]==native.json_digest(req)
    receipt=tmp_path/"receipt.json"
    receipt.write_text(json.dumps({**inputs["image"],"native_generation":True}))
    args.unit_receipt=str(receipt)
    assert flow.run(args,None)["next_action"]=="MATERIALIZE_NATIVE_EDIT_HANDOFF"
    handoff_file=tmp_path/"handoff.json";handoff_file.write_text(json.dumps(h))
    args.native_handoff=str(handoff_file)
    assert flow.run(args,None)["next_action"]=="RECOMPOSE_NATIVE_MASK"
    composed_file=tmp_path/"composed.json"
    composed_file.write_text(json.dumps(inputs["composed-image"]))
    args.native_composed_receipt=str(composed_file)
    assert flow.run(args,None)["next_action"]=="AGENT_INSPECT_IMAGE"
    review_file=tmp_path/"review.json";review_file.write_text(json.dumps(review))
    args.visual_review=str(review_file)
    assert flow.run(args,None)["next_action"]=="RECORD_SYNTHETIC_ATTEMPT"
    review["reference_sha256"]="0"*64
    review_file.write_text(json.dumps(review))
    with pytest.raises(Exception,match="synthetic review must inspect"):
        flow.run(args,None)


def test_canonical_recipe_includes_verifiable_visual_inputs_and_real_prompt(monkeypatch,tmp_path):
    monkeypatch.setattr(contracts,"validate_proposals",lambda *a,**kw:{"pending":[]})
    reference=tmp_path/"master.png";Image.new("RGBA",(16,16),(80,90,100,255)).save(reference)
    mask=tmp_path/"approved-mask.png";Image.new("L",(16,16),255).save(mask)
    design=tmp_path/"unit.json";design.write_text('{"buildings":[],"access_verified":true}')
    intent={"target":{"id":"synthetic-canonical-fixture"},"source_commit":"a"*40}
    recipe=contracts.make_generation_recipe(unit={"id":"WU-TEST","bbox":[0,0,16,16]},
        intent=intent,design_path=design,reference_path=reference,mask_file=mask,
        proposal_register={"proposals":[]},neighbor_digests={},style={"projection":"TOP_DOWN_90"})
    req=recipe["native_edit_request"]
    assert req["mode"]=="EDIT_WITH_REFERENCE"
    assert req["reference_sha256"]==contracts.digest(reference)
    assert req["mask_sha256"]==contracts.digest(mask)
    assert recipe["native_reference_image_path"]==str(reference.resolve())
    bad=tmp_path/"bad.png";Image.new("RGB",(8,8),(22,33,44)).save(bad)
    with pytest.raises((contracts.Blocked,ValueError),match="mask must share pixel dimensions"):
        contracts.make_generation_recipe(unit={"id":"WU-TEST","bbox":[0,0,16,16]},
            intent=intent,design_path=design,reference_path=reference,mask_file=bad,
            proposal_register={"proposals":[]},neighbor_digests={},style={"projection":"TOP_DOWN_90"})


def test_previous_reference_may_repeat_but_generated_image_cannot_be_replayed(tmp_path):
    req,h,inputs,artifacts,review=fixture(tmp_path,"op-1")
    original={"status":"COMPLETED","artifacts":artifacts}
    # Reference and mask are reusable contextual inputs; output and verdict are new attempts.
    newer=copy.deepcopy(artifacts)
    for a in newer:
        if a["kind"]=="image":
            a["remote_id"]="reused-pixels-new-provider-id"
    op={"operation_id":"op-2","action":"GENERATE_AND_AUDIT_CANDIDATE"}
    receipt={"operation_id":"op-2","artifacts":newer}
    with pytest.raises(ValueError,match="completed artifact replayed"):
        orchestration._verify_operation(op,receipt,
            lambda provider,remote:next(a["path"] for a in newer if a["remote_id"]==remote)
                                  if False else next(Path(a["path"]).read_bytes() for a in newer
                                                    if a["remote_id"]==remote),[original])
