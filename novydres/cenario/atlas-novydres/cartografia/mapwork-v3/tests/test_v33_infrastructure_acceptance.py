"""Tests for fail-closed iterative infrastructure acceptance in the single V3.3 pipeline."""
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import v33_acceptance as a


def write_json(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return a.sha_file(path)


def fixture(tmp_path, *, stages=7):
    source = tmp_path / "u02.png"
    Image.new("RGB", (32, 32), (12, 25, 32)).save(source)
    source_sha = a.sha_file(source)
    spec = a.criteria_contract()
    record = {
        "schema": a.SCHEMA,
        "criteria_sha256": spec["sha256"],
        "reference_sha256": source_sha,
        "stages": {}
    }
    zone = tmp_path / "zone-mask.png"
    Image.new("L",(32,32),255).save(zone)
    territory = {}
    for label in a.criteria_contract()["profile"]["territory_classes"]:
        file = tmp_path / ("territory-"+label+".png")
        Image.new("L",(32,32),255 if label == "urban" else 0).save(file)
        territory[label]={"path":file.name,"sha256":a.sha_file(file)}
    roads=[]
    nodes=[]
    for mode,y,level in (("road",1,0),("rail",5,0),("tram",9,0),("metro",13,-1)):
        left, right = mode+"-start",mode+"-end"
        nodes.extend([{"id":left,"point":[1,y],"level":level},
                      {"id":right,"point":[10,y],"level":level}])
        roads.append({"id":mode,"from":left,"to":right,"points":[[1,y],[10,y]],
                      "mode":mode,"level":level,"width_units":1})
    prior = None
    for i, stage in enumerate(a.STAGES[:stages]):
        geometry = tmp_path / (stage + ".json")
        preview = tmp_path / (stage + ".png")
        geo_data = {
            "schema":"NOVYDRES_MAPWORK_V33_INFRA_GEOMETRY_2",
            "stage":stage,"source_sha256":source_sha,"reference_size":[32,32],
            "zone_mask":{"path":zone.name,"sha256":a.sha_file(zone)},
            "network":{"nodes":nodes,"edges":roads,"crossings":[]},
            "territory":{"class_masks":territory},
        }
        if prior is not None:
            geo_data["previous_stage_sha256"]=a.sha_file(prior)
        geo_sha=write_json(geometry,geo_data)
        Image.new("RGB", (32, 32), (i * 18 + 1, 55, 72)).save(preview)
        with Image.open(preview) as im:
            regions=[{"criterion_id":cid,"bbox":[0,0,8,8],
                      "pixels_sha256":hashlib.sha256(im.crop((0,0,8,8)).tobytes()).hexdigest()}
                     for cid in spec["stages"][stage]]
        record["stages"][stage] = {"attempts": [{
            "stage": stage, "iteration": 1,
            "geometry_path": geometry.name, "geometry_sha256": geo_sha,
            "preview_path": preview.name, "preview_sha256": a.sha_file(preview),
            "reference_sha256": source_sha,
            "reviewed_by": "AGENT", "model": "GPT-6",
            "full_image_visually_inspected": True,
            "visual_observations":{"preview_sha256":a.sha_file(preview),
                                   "geometry_sha256":geo_sha,"regions":regions},
            "checks": {
                cid: {
                    "status": "PASS",
                    "evidence": "Imagem integral conferida; eixo, conexões, níveis e coerência examinados."
                }
                for cid in spec["stages"][stage]
            },
            "verdict": "PASS", "findings": [], "repair_plan": ""
        }]}
        prior=geometry
    path = tmp_path / "acceptance-ledger-v33.json"
    write_json(path, record)
    kwargs = {
        "ledger_path": path, "reference_file": source,
        "reference_sha256": source_sha, "reference_size": [32, 32]
    }
    return path, record, kwargs


def evaluation(kw, **changes):
    params = dict(kw, **changes)
    return a.evaluate(**params)


def test_contract_reads_32_rules_and_order():
    spec = a.criteria_contract()
    assert tuple(spec["stages"]) == a.STAGES
    assert all(len(value) == 4 for value in spec["stages"].values())


def test_no_ledger_demands_first_real_candidate(tmp_path):
    _, _, kw = fixture(tmp_path, stages=0)
    assert evaluation(kw)["next_action"] == "GENERATE_AND_AUDIT_CANDIDATE"


def test_seven_full_stage_acceptances_allow_lots_but_no_urban_art(tmp_path):
    _, _, kw = fixture(tmp_path, stages=7)
    ok = evaluation(kw)
    assert ok["status"] == "PASS"
    assert ok["allows_lots"] is True
    assert len(ok["accepted_stages"]) == 7
    urban = evaluation(kw, require_urban=True)
    assert urban["status"] == "BLOCKED"
    assert urban["stage"] == "URB-08"


def test_eight_stage_acceptances_authorize_downstream_gates_not_canon(tmp_path):
    _, _, kw = fixture(tmp_path, stages=8)
    ok = evaluation(kw, require_urban=True)
    assert ok["status"] == "PASS"
    assert len(ok["accepted_stages"]) == 8


def test_negative_missing_image_bytes_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    (tmp_path / "INF-01.png").unlink()
    assert evaluation(kw)["next_action"] == "REPAIR_UNVERIFIED_CANDIDATE"


def test_negative_forged_image_hash_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    record["stages"]["INF-01"]["attempts"][0]["preview_sha256"] = "a" * 64
    write_json(path, record)
    assert evaluation(kw)["status"] == "FAIL"


def test_negative_missing_one_rule_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    record["stages"]["INF-01"]["attempts"][0]["checks"].pop("INF-01.03")
    write_json(path, record)
    assert evaluation(kw)["next_action"] == "REPAIR_UNVERIFIED_CANDIDATE"


def test_negative_generic_evidence_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    record["stages"]["INF-01"]["attempts"][0]["checks"]["INF-01.01"]["evidence"] = "ok"
    write_json(path, record)
    assert evaluation(kw)["status"] == "FAIL"


def test_negative_repeated_unsuccessful_candidate_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    stage = record["stages"]["INF-01"]["attempts"]
    previous = stage[0]
    previous["verdict"] = "FAIL"
    previous["checks"]["INF-01.01"]["status"] = "FAIL"
    previous["findings"] = ["Duplicated aerial centerlines have unverified grade."]
    previous["repair_plan"] = "Regenerate the street geometry and inspect actual road beds."
    stage.append(dict(copy.deepcopy(previous), iteration=2))
    write_json(path, record)
    assert evaluation(kw)["next_action"] == "REGENERATE_DIFFERENT_CANDIDATE"


def test_real_failure_orders_repair_before_next_stage(tmp_path):
    path, record, kw = fixture(tmp_path)
    attempt = record["stages"]["INF-02"]["attempts"][0]
    attempt["verdict"] = "FAIL"
    attempt["checks"]["INF-02.02"]["status"] = "FAIL"
    attempt["findings"] = ["Trevo sem rampas nem níveis." ]
    attempt["repair_plan"] = "Desenhar a rampa e observar cada união de pista por imagem."
    write_json(path, record)
    result = evaluation(kw)
    assert result["stage"] == "INF-02"
    assert result["next_action"] == "REPAIR_AND_REGENERATE"
    assert result["accepted_stages"] == ["INF-01"]


def test_negative_stale_markdown_digest_never_pass(tmp_path):
    path, record, kw = fixture(tmp_path)
    record["criteria_sha256"] = "f" * 64
    write_json(path, record)
    assert evaluation(kw)["next_action"] == "INVALIDATE_AND_REAUDIT_STALE_EVIDENCE"


def test_negative_geometry_without_spatial_features_rejected(tmp_path):
    path, record, kw = fixture(tmp_path)
    geometry = tmp_path / "INF-01.json"
    new_sha = write_json(geometry, {
        "stage": "INF-01", "source_sha256": kw["reference_sha256"]
    })
    record["stages"]["INF-01"]["attempts"][0]["geometry_sha256"] = new_sha
    write_json(path, record)
    assert evaluation(kw)["next_action"] == "REPAIR_UNVERIFIED_CANDIDATE"


def test_negative_misbound_geometry_stage_rejected(tmp_path):
    path, record, kw = fixture(tmp_path)
    geometry = tmp_path / "INF-03.json"
    geo = json.loads(geometry.read_text())
    geo["stage"] = "INF-04"
    new_sha = write_json(geometry, geo)
    record["stages"]["INF-03"]["attempts"][0]["geometry_sha256"] = new_sha
    write_json(path, record)
    assert evaluation(kw)["stage"] == "INF-03"
    assert evaluation(kw)["status"] == "FAIL"


def test_negative_missing_reference_file_blocks_everything(tmp_path):
    _, _, kw = fixture(tmp_path)
    kw["reference_file"] = tmp_path / "U02-missing.png"
    assert evaluation(kw)["next_action"] == "MATERIALIZE_ORIGINAL_REFERENCE"


def test_three_stagnant_rejections_replan_instead_of_owner_override(tmp_path):
    path, record, kw = fixture(tmp_path)
    attempts = record["stages"]["INF-01"]["attempts"]
    first = attempts[0]
    first["verdict"] = "FAIL"
    first["checks"]["INF-01.01"]["status"] = "FAIL"
    first["findings"] = ["The east sector has unexplained highway gaps."]
    first["repair_plan"] = "Change drafting strategy and repair roadbeds and intersections."
    for i in (2, 3):
        new = copy.deepcopy(first)
        new["iteration"] = i
        preview = tmp_path / ("INF-01-attempt%d.png" % i)
        geometry = tmp_path / ("INF-01-attempt%d.json" % i)
        Image.new("RGB", (32, 32), (35 + i, 60, 95)).save(preview)
        new["preview_path"] = preview.name
        new["preview_sha256"] = a.sha_file(preview)
        new["geometry_path"] = geometry.name
        original = json.loads((tmp_path / "INF-01.json").read_text())
        original["test_attempt_unique"] = i
        new["geometry_sha256"] = write_json(geometry, original)
        with Image.open(preview) as im:
            pix=hashlib.sha256(im.crop((0,0,8,8)).tobytes()).hexdigest()
        new["visual_observations"] = {
            "preview_sha256":new["preview_sha256"],
            "geometry_sha256":new["geometry_sha256"],
            "regions":[{"criterion_id":cid,"bbox":[0,0,8,8],"pixels_sha256":pix}
                       for cid in a.criteria_contract()["stages"]["INF-01"]]
        }
        attempts.append(new)
    write_json(path, record)
    result = evaluation(kw)
    assert result["stage"] == "INF-01"
    assert result["next_action"] == "REPLAN_STAGE"


def test_negative_reuse_same_preview_across_stages(tmp_path):
    path, record, kw = fixture(tmp_path)
    original = record["stages"]["INF-01"]["attempts"][0]
    other = record["stages"]["INF-02"]["attempts"][0]
    for key in ("geometry_sha256", "preview_sha256", "geometry_path", "preview_path"):
        other[key] = original[key]
    write_json(path, record)
    assert evaluation(kw)["stage"] == "INF-02"
    assert evaluation(kw)["status"] == "FAIL"