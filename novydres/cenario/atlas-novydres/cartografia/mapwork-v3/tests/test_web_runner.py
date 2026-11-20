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
