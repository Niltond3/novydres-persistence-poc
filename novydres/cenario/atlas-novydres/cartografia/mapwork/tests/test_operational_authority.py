"""Production paths must not interpret historical visuals as operational gates."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import acceptance
import pipeline
import mapwork


def test_kingswell_checkpoint_ledger_and_markdown_match():
    directory=ROOT/"zones"/"cidade-velha"
    cp=json.loads((directory/"checkpoint.json").read_text(encoding="utf-8"))
    ledger=json.loads((directory/"acceptance-ledger.json").read_text(encoding="utf-8"))
    assert acceptance.checkpoint_issues(
        cp,ledger_path=directory/"acceptance-ledger.json",
        reference_sha256=mapwork.load(ROOT/"config.json")["reference"]["sha256"],
        criteria_sha256=acceptance.criteria_contract()["sha256"],
        expected_target="kingswell") == []
    assert cp["official_accepted_stages"]==[]
    assert all(not block["attempts"] for block in ledger["stages"].values())
    assert len(ledger["diagnostics"])==5
    assert ledger["diagnostics"][-1]["remaining_untyped_crossings"]==217


def test_direct_renderer_cannot_use_obsolete_boolean():
    forged=SimpleNamespace(preflight_verified=True,district="kingswell")
    with pytest.raises(mapwork.Invalid,match="verified pipeline gate"):
        pipeline._run_verified(forged)


def test_direct_renderer_cannot_use_forged_editorial_proof_without_real_ledger_pass():
    forged=SimpleNamespace(_editorial_verified=True,
        _accepted_criteria_sha256=acceptance.criteria_contract()["sha256"],
        district="kingswell",zone=None,reference=None,
        acceptance_ledger=None,execute=False,recipe_unit=None,audit_unit=None)
    with pytest.raises(mapwork.Invalid,match="independent infrastructure acceptance"):
        pipeline._run_verified(forged)


def test_single_pipeline_status_schema_has_no_operational_drawing_promotion():
    schema=json.loads((ROOT/"schemas"/"zone.schema.json").read_text())
    assert "SKETCH_APPROVED" not in schema["properties"]["status"]["enum"]
    assert "sketch_approved" not in schema["properties"]
    for name in ("mapwork.py","pipeline.py","flow.py"):
        script=(ROOT/"scripts"/name).read_text(encoding="utf-8")
        assert "SKETCH_APPROVED" not in script
        assert "sketch_approved" not in script
        assert "PROMOTE_ZONE_TO_GENERATING_WITH_AUDIT" not in script
        assert "preflight_verified" not in script


def test_new_candidate_ledger_records_target_and_reference_geometry(tmp_path):
    import orchestration
    from test_orchestration import failed
    attempt=tmp_path/"attempt.json"
    attempt.write_text(json.dumps(failed(1)),encoding="utf-8")
    ledger=tmp_path/"ledger.json"
    options=dict(criteria_sha256="c"*64,reference_sha256="a"*64,
                 schema=acceptance.SCHEMA,allowed_stages=acceptance.STAGES,
                 active_stage="INF-01",target="sulfok",reference_size=[32,32])
    assert orchestration.record_attempt(ledger,attempt,**options)["status"]=="RECORDED"
    stored=json.loads(ledger.read_text(encoding="utf-8"))
    assert stored["target"]=="sulfok"
    assert stored["reference_dimensions_px"]==[32,32]
    with pytest.raises(ValueError,match="ledger authority mismatch"):
        orchestration.record_attempt(ledger,attempt,**dict(options,target="kingswell"))
