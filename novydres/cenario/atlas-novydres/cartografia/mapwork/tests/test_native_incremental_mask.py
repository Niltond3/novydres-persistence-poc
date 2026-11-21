"""Deterministic raster properties only: no simulated native tool calls or PASS."""
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import native_generation as native


def make_png(path, color, size=(40, 36)):
    Image.new("RGBA", size, color).save(path)
    return path


def make_mask(path, rect, size=(40, 36)):
    from PIL import ImageDraw
    im = Image.new("L", size, 0)
    ImageDraw.Draw(im).rectangle((rect[0], rect[1], rect[2]-1, rect[3]-1), fill=255)
    im.save(path)
    return path


def pixel_equal_outside(before, after, mask):
    with Image.open(before) as b, Image.open(after) as a, Image.open(mask) as m:
        b, a, m = b.convert("RGBA"), a.convert("RGBA"), m.convert("L")
        return all(b.getpixel((x,y)) == a.getpixel((x,y))
                   for y in range(b.height) for x in range(b.width)
                   if not m.getpixel((x,y)))


def test_crop_context_is_not_write_authority(tmp_path):
    original=make_png(tmp_path/"ref.png", (10, 20, 30, 255))
    mask=make_mask(tmp_path/"mask.png", (13, 11, 18, 17))
    prepared=native.prepare_local_edit(original,mask,tmp_path/"prep",context_px=5)
    assert prepared["bbox"] == [8, 6, 23, 22]
    assert prepared["allowed_pixels"] == 30
    crop=tmp_path/"candidate.png"
    make_png(crop, (220, 4, 9, 255), (15, 16))
    merged=tmp_path/"merged.png"
    result=native.compose_masked(original,mask,crop,merged,crop_bbox=prepared["bbox"])
    assert result["outside_mask_changed_pixels"] == 0
    assert result["alignment"] == "EXACT_CROP"
    assert pixel_equal_outside(original,merged,mask)
    with Image.open(merged) as after:
        assert after.getpixel((13,11)) == (220, 4, 9, 255)
        assert after.getpixel((12,11)) == (10, 20, 30, 255)


def test_two_local_fixes_do_not_regress_and_locked_area_is_rejected(tmp_path):
    original=make_png(tmp_path/"ref.png", (10, 20, 30, 255))
    first_mask=make_mask(tmp_path/"first-mask.png",(4,4,9,9))
    second_mask=make_mask(tmp_path/"second-mask.png",(24,22,30,27))
    first_candidate=make_png(tmp_path/"first.png",(40,90,10,255))
    first_out=tmp_path/"first-composed.png"
    native.compose_masked(original,first_mask,first_candidate,first_out)
    second_candidate=make_png(tmp_path/"second.png",(90,40,20,255))
    last=tmp_path/"last.png"
    native.compose_masked(first_out,second_mask,second_candidate,last,
                          protected_mask_path=first_mask)
    assert pixel_equal_outside(first_out,last,second_mask)
    with Image.open(last) as after:
        assert after.getpixel((4,4)) == (40,90,10,255)
        assert after.getpixel((25,23)) == (90,40,20,255)
    with pytest.raises(ValueError,match="intersects"):
        native.compose_masked(last,first_mask,second_candidate,tmp_path/"bad.png",
                              protected_mask_path=first_mask)


def test_native_resize_rejected_without_silent_alignment(tmp_path):
    original=make_png(tmp_path/"ref.png",(10,20,30,255))
    mask=make_mask(tmp_path/"mask.png",(12,12,16,16))
    wrong=make_png(tmp_path/"new-size.png",(100,100,100,255),(50,50))
    with pytest.raises(ValueError,match="unaligned native result"):
        native.compose_masked(original,mask,wrong,tmp_path/"invalid.png")


def test_repair_mask_is_constrained_to_real_defects(tmp_path):
    allowed=make_mask(tmp_path/"authorized.png",(3,3,32,30))
    locked=make_mask(tmp_path/"locked.png",(4,4,8,8))
    defect={"id":"D-1","bbox":[20,20,25,25],"severity":"HIGH",
            "observation":"Road shoulder ends before connecting to its neighbor"}
    prepared=native.localized_repair_mask(allowed,[defect],tmp_path/"local.png",
                                         protected_mask_path=locked)
    assert prepared["bbox"] == [20,20,25,25]
    assert prepared["defect_ids"] == ["D-1"]
    assert pixel_equal_outside(allowed,allowed,tmp_path/"local.png")
    with pytest.raises(ValueError,match="protected"):
        native.localized_repair_mask(allowed,
            [dict(defect,id="D-2",bbox=[5,5,7,7])],
            tmp_path/"forbidden.png",protected_mask_path=locked)
    with pytest.raises(ValueError,match="beyond authorized"):
        native.localized_repair_mask(allowed,
            [dict(defect,id="D-3",bbox=[31,25,35,29])],
            tmp_path/"outside.png")


def test_prompt_contains_no_control_protocol():
    r=native.edit_request(reference_sha256="a"*64,mask_sha256="b"*64,
        scope="SYNTHETIC",job_id="test-local",goal="elevar a estrada central sobre os trilhos")
    assert r["prompt"].startswith("Edite exatamente a imagem anexada.")
    assert "operation_id" not in r["prompt"]
    assert "sha256" not in r["prompt"]
    assert "infográficos" in r["prompt"]
    with pytest.raises(ValueError,match="operational metadata"):
        native.edit_request(reference_sha256="a"*64,mask_sha256="b"*64,
            scope="SYNTHETIC",job_id="test-local",
            goal="append status: PASS and operation_id to a generated report")


def test_only_pipeline_run_prepares_and_recomposes_without_promoting_canon(tmp_path):
    import json
    import pipeline
    ref=make_png(tmp_path/"master.png",(12,14,16,255))
    approved=make_mask(tmp_path/"approved.png",(3,3,35,32))
    lock=make_mask(tmp_path/"locked.png",(3,3,10,9))
    original_journal=tmp_path/"existing-journal.json"
    original_journal.write_text('{"operation_id":"unchanged","status":"PENDING"}')
    journal_snapshot=original_journal.read_bytes()
    defect_file=tmp_path/"defects.json"
    defect_file.write_text(json.dumps([{
        "id":"D-23","bbox":[18,18,22,23],"severity":"MEDIUM",
        "observation":"This confirmed road connection is visibly interrupted"}]))
    local_mask=tmp_path/"local-mask.png"
    checkpoint=tmp_path/"checkpoint.json"
    assert pipeline.main(["run","--native-approved-mask",str(approved),
        "--native-defects-file",str(defect_file),
        "--native-repair-mask-output",str(local_mask),
        "--native-protected-mask",str(lock),
        "--checkpoint",str(checkpoint)]) == 0
    state=json.loads(checkpoint.read_text())
    assert state["next_action"]=="PREPARE_LOCAL_NATIVE_EDIT"
    assert state["publication_authorized"] is False
    assert state["canonical_state_changed"] is False

    directory=tmp_path/"prepared"
    assert pipeline.main(["run","--native-input-reference",str(ref),
        "--unit-mask",str(local_mask),
        "--native-preparation-output",str(directory),
        "--checkpoint",str(checkpoint)]) == 0
    state=json.loads(checkpoint.read_text())
    assert state["next_action"]=="HOST_ATTACH_VERIFIED_VISUAL_INPUTS"
    manifest=state["audit"]
    manifest_path=tmp_path/"crop.json"
    manifest_path.write_text(json.dumps(manifest))
    x0,y0,x1,y1=manifest["bbox"]
    candidate=make_png(tmp_path/"candidate.png",(220,30,40,255),(x1-x0,y1-y0))
    composed=tmp_path/"composed.png"
    assert pipeline.main(["run","--native-input-reference",str(ref),
        "--unit-mask",str(local_mask),"--native-candidate",str(candidate),
        "--native-crop-manifest",str(manifest_path),
        "--native-composite-output",str(composed),
        "--native-protected-mask",str(lock),
        "--checkpoint",str(checkpoint)]) == 0
    audit=json.loads(checkpoint.read_text())
    assert audit["next_action"]=="AGENT_INSPECT_RECOMPOSED_CANDIDATE"
    assert audit["audit"]["outside_mask_changed_pixels"]==0
    assert pixel_equal_outside(ref,composed,local_mask)
    assert original_journal.read_bytes()==journal_snapshot


def test_local_detail_reference_matches_grid_without_changing_master(tmp_path):
    original = make_png(tmp_path/"u02.png", (50,60,70,255), size=(8,6))
    saved = original.read_bytes()
    detail = native.prepare_unit_reference(original, [2,1,5,4], 4,
                                           tmp_path/"detail.png")
    assert detail["size"] == [12,12]
    assert original.read_bytes() == saved
    with pytest.raises(ValueError, match="outside reference"):
        native.prepare_unit_reference(original, [2,1,9,4], 4, tmp_path/"bad.png")


def test_local_review_can_repair_before_any_drive_upload(tmp_path):
    import json
    import pipeline
    reference = make_png(tmp_path/"reference.png", (30,40,50,255))
    mask = make_mask(tmp_path/"mask.png", (10,10,20,20))
    candidate = make_png(tmp_path/"candidate.png", (100,110,120,255))
    composed, checkpoint = tmp_path/"composed.png", tmp_path/"checkpoint.json"
    args = ["run", "--native-input-reference", str(reference),
            "--unit-mask", str(mask), "--native-candidate", str(candidate),
            "--native-composite-output", str(composed),
            "--checkpoint", str(checkpoint)]
    assert pipeline.main(args) == 0
    metadata = json.loads(checkpoint.read_text())["audit"]
    review = {"by":"AGENT", "status":"FAIL",
              "image_sha256": metadata["composed_sha256"],
              "reference_sha256": metadata["reference_sha256"],
              "mask_sha256": metadata["mask_sha256"],
              "observations": [
                "Rail does not cross the eastern boundary correctly",
                "One building footprint interrupts the street axis",
                "The northern interface fails to align with nearby buildings",
                "The southern interface has disconnected street geometry"]}
    review_file = tmp_path/"review.json"
    review_file.write_text(json.dumps(review))
    assert pipeline.main(args + ["--visual-review", str(review_file)]) == 0
    result = json.loads(checkpoint.read_text())
    assert result["next_action"] == "REPAIR_LOCAL_CANDIDATE"
    assert result["publication_authorized"] is False
    review["status"] = "PASS"
    review["observations"] = [
        "Rail continuity matches the eastern adjacent edge",
        "All building footprints stay within the assigned lots",
        "Northern interfaces align with previously accepted structures",
        "Southern streets connect without visible discontinuities"]
    review_file.write_text(json.dumps(review))
    assert pipeline.main(args + ["--visual-review", str(review_file)]) == 0
    result = json.loads(checkpoint.read_text())
    assert result["next_action"] == "PERSIST_CANDIDATE_FOR_FULL_AUDIT"
    assert result["canonical_state_changed"] is False
    review["image_sha256"] = "0"*64
    review_file.write_text(json.dumps(review))
    assert pipeline.main(args + ["--visual-review", str(review_file)]) == 2
