"""No terminal, network or Git CLI: same canonical pipeline invoked in Web adapter."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "scripts"))
import web_bridge as w


def fake_source(tmp_path):
    p=tmp_path/"scripts"/"some_source.py"
    p.parent.mkdir(exist_ok=True)
    p.write_bytes(b"print('real bytes')\n")
    raw=p.read_bytes()
    rec={"path":"scripts/some_source.py", "provider":"github",
         "sha256":w.sha256(raw),"blob_sha":w.git_blob_sha(raw),"size_bytes":len(raw)}
    return {"schema":w.FILE_MANIFEST_SCHEMA,"source_commit":"1"*40,"files":[rec]}


def test_verified_git_blob_bytes_no_git_command(tmp_path):
    manifest=fake_source(tmp_path)
    result=w.verify_files(manifest,root=tmp_path,expected_commit="1"*40)
    assert result["status"]=="PASS" and result["file_count"]==1


def test_forged_sha_and_git_blob_and_missing_bytes(tmp_path):
    manifest=fake_source(tmp_path)
    manifest["files"][0]["sha256"]="f"*64
    with pytest.raises(w.WebBridgeError,match="SHA-256"):
        w.verify_files(manifest,root=tmp_path)
    manifest=fake_source(tmp_path)
    manifest["files"][0]["blob_sha"]="f"*40
    with pytest.raises(w.WebBridgeError,match="GitHub Git blob"):
        w.verify_files(manifest,root=tmp_path)
    (tmp_path/"scripts"/"some_source.py").unlink()
    with pytest.raises(w.WebBridgeError,match="missing"):
        w.verify_files(manifest,root=tmp_path)


def test_wrong_source_commit_never_passes(tmp_path):
    with pytest.raises(w.WebBridgeError,match="does not match"):
        w.verify_files(fake_source(tmp_path),root=tmp_path,expected_commit="2"*40)


def test_canonical_pipeline_is_in_process_and_remains_blocked(tmp_path):
    files=[]
    for rel in ("scripts/pipeline.py", "scripts/mapwork.py", "scripts/flow.py",
                "scripts/contracts.py", "scripts/acceptance.py",
                "docs/infra-acceptance.md", "scripts/web_bridge.py"):
        data=(ROOT/rel).read_bytes()
        files.append({"path":rel,"provider":"github","sha256":w.sha256(data),
                      "blob_sha":w.git_blob_sha(data),"size_bytes":len(data)})
    manifest={"schema":w.FILE_MANIFEST_SCHEMA,"source_commit":"1"*40,"files":files}
    result=w.run_web(argv=["--district","kingswell"],file_manifest=manifest,
                     root=ROOT,source_commit="1"*40)
    assert result["status"]=="BLOCKED"
    assert result["pipeline"]["result"]["phase"]=="INTENT"
    assert not result["authorizes_canon"]


def test_canonical_cli_propagates_fail_instead_of_blocked(monkeypatch,capsys):
    import pipeline
    monkeypatch.setattr(pipeline,"run",lambda _: {
        "phase":"INFRASTRUCTURE_ACCEPTANCE", "audit":{"status":"FAIL"},
        "blockers":["candidate geometry failed mathematical audit"]})
    rc=pipeline.main(["run","--district","kingswell"])
    result=json.loads(capsys.readouterr().out)
    assert rc==2 and result["status"]=="FAIL"
