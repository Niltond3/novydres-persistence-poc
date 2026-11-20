"""Web runner handoff regression: no client filesystem or private media assumed."""
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import web_runner
import mapwork as core


def test_hosted_bootstrap_emits_content_hashes_without_private_media(tmp_path,monkeypatch):
    monkeypatch.delenv("GITHUB_EVENT_NAME",raising=False)
    result=web_runner.run_request(district="sulfok",out=tmp_path)
    assert result["checkpoint"]["phase"]=="BOOTSTRAP"
    assert result["media_access"]=="NOT_PROVISIONED"
    assert result["checkpoint"]["publication_authorized"] is False
    checkpoint=tmp_path/"checkpoint.json"
    receipt=core.load(tmp_path/"readback.json")
    assert receipt["checkpoint_sha256"]==core.sha(checkpoint)


def test_browser_request_rejects_stale_parent_before_pipeline(tmp_path,monkeypatch):
    monkeypatch.setenv("GITHUB_EVENT_NAME","push")
    monkeypatch.setenv("GITHUB_SHA","c"*40)
    monkeypatch.setenv("GITHUB_ACTIONS","false")
    monkeypatch.setattr(web_runner,"parent_commit",lambda:"1"*40)
    monkeypatch.setattr(web_runner,"checked_path",lambda p,**kw:tmp_path/"request.json")
    core.save(tmp_path/"request.json",{
        "schema":web_runner.REQUEST_SCHEMA,
        "request_id":"stale-1",
        "expected_parent_sha":"0"*40,
        "district":"sulfok"})
    with pytest.raises(core.Invalid,match="stale or non-CAS"):
        web_runner.run_request(request="web-requests/stale.json",out=tmp_path/"out")


def test_browser_request_rejects_traversal(tmp_path):
    with pytest.raises(core.Invalid,match="relative"):
        web_runner.checked_path("../../world-state.json",prefix="web-requests")
    with pytest.raises(core.Invalid,match="web-requests"):
        web_runner.checked_path("zones/cidade-velha/zone.json",prefix="web-requests")


def test_push_request_discovery_uses_checked_out_git_diff(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    def fake_check_output(args,**kwargs):
        if "rev-parse" in args:
            return "b"*40+"\n"
        return ("novydres/cenario/atlas-novydres/cartografia/mapwork-v3/"
                "web-requests/kingswell.json\n")
    monkeypatch.setattr(web_runner.subprocess,"check_output",fake_check_output)
    assert web_runner.discover_request_from_push()=="web-requests/kingswell.json"


def test_push_request_rejects_mismatched_checkout(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    monkeypatch.setattr(web_runner.subprocess,"check_output",lambda *a,**kw:"a"*40+"\n")
    with pytest.raises(core.Invalid,match="checkout differs"):
        web_runner.discover_request_from_push()


def test_read_only_hosted_source_guard_still_blocks_image_generation():
    import mapwork as core
    import urban_architecture as urban
    p=core.load(ROOT/"fixtures"/"topology-v31-synthetic.json")
    p["fixture_mode"]=False
    cfg=core.load(ROOT/"config.json")
    p["source_sha256"]=cfg["reference"]["sha256"]
    r=urban.plan_city(p,cfg,reference_file=None)
    assert r["gates"]["source_bytes_verified"] is False
    assert r["generation_ready"] is False


def test_remote_branch_sha_lease_detects_stale_runner(monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS","true")
    monkeypatch.setenv("GITHUB_SHA","b"*40)
    monkeypatch.setenv("GITHUB_REF_NAME","mapwork-v3/candidate")
    monkeypatch.setenv("GITHUB_REF","refs/heads/mapwork-v3/candidate")
    def fake_git(*args):
        if args[:2]==("rev-parse","HEAD"):return "b"*40
        if args[0]=="ls-remote":return "a"*40+"\\trefs/heads/mapwork-v3/candidate"
        raise AssertionError(args)
    monkeypatch.setattr(web_runner,"_git",fake_git)
    with pytest.raises(core.Invalid,match="remote branch SHA changed"):
        web_runner.verify_remote_branch()


def test_resuming_verified_remote_checkpoint_is_idempotent(tmp_path,monkeypatch):
    monkeypatch.delenv("GITHUB_SHA",raising=False)
    monkeypatch.delenv("GITHUB_EVENT_NAME",raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS",raising=False)
    first=web_runner.run_request(district="sulfok",out=tmp_path/"first")
    cp=tmp_path/"first"/"checkpoint.json"
    folder=tmp_path/"web-checkpoints";folder.mkdir()
    original=folder/"restart.json"
    original.write_bytes(cp.read_bytes())
    request={
        "schema":web_runner.REQUEST_SCHEMA,
        "request_id":"resume-test",
        "expected_parent_sha":"1"*40,
        "district":"sulfok",
        "resume":{"checkpoint_path":"web-checkpoints/restart.json",
                  "checkpoint_sha256":core.sha(original)}
    }
    source=tmp_path/"request.json"
    core.save(source,request)
    def mock_path(p,**kw):
        if kw.get("prefix")=="web-requests":return source
        if kw.get("prefix")=="web-checkpoints":return original
        return web_runner.ROOT/p
    monkeypatch.setattr(web_runner,"checked_path",mock_path)
    result=web_runner.run_request(request="web-requests/request.json",out=tmp_path/"second")
    assert result["resumed_from"]["checkpoint_sha256"]==core.sha(original)
    assert result["input_fingerprints"]==first["input_fingerprints"]
    request["resume"]["checkpoint_sha256"]="0"*64
    core.save(source,request)
    with pytest.raises(core.Invalid,match="tampered"):
        web_runner.run_request(request="web-requests/request.json",out=tmp_path/"third")


def test_resume_rejects_changed_checkpoint_inputs(tmp_path):
    original={"schema":web_runner.OUTPUT_SCHEMA,"checkpoint":{"district":"sulfok",
              "phase":"RESEARCH","next_action":"RESEARCH_ANALOGUES"},
              "input_fingerprints":{"world_state_sha256":"old"}}
    folder=tmp_path/"web-checkpoints";folder.mkdir()
    cp=folder/"old.json"
    core.save(cp,original)
    from unittest.mock import patch
    new={"district":"sulfok","phase":"RESEARCH","next_action":"RESEARCH_ANALOGUES"}
    with patch.object(web_runner,"checked_path",return_value=cp):
        with pytest.raises(core.Invalid,match="inputs changed"):
            web_runner._check_resume({"resume":{"checkpoint_path":"web-checkpoints/old.json",
                "checkpoint_sha256":core.sha(cp)}},new,{"world_state_sha256":"new"})
