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
    for rel in sorted(["docs/infra-acceptance.md", "config.json", "scope-index.json",
                       "VISUAL_REVIEW_PROTOCOL.md", "PIPELINE.md"]+
                      ["scripts/"+p.name for p in (ROOT/"scripts").glob("*.py")]):
        data=(ROOT/rel).read_bytes()
        files.append({"path":rel,"provider":"github","sha256":w.sha256(data),
                      "blob_sha":w.git_blob_sha(data),"size_bytes":len(data)})
    manifest={"schema":w.FILE_MANIFEST_SCHEMA,"source_commit":"1"*40,"files":files}
    # A collection-time import from an unverified module cache is forbidden.
    local_names={p.stem for p in (ROOT/"scripts").glob("*.py")}
    saved={k:sys.modules.pop(k) for k in tuple(sys.modules)
           if k in local_names and k != "web_bridge"}
    try:
        remote_blobs={row["path"]:row["blob_sha"] for row in files}
        result=w.run_web(argv=["--district","kingswell"],file_manifest=manifest,
                         root=ROOT,source_commit="1"*40,remote_blobs=remote_blobs)
    finally:
        for k in local_names-{"web_bridge"}:
            sys.modules.pop(k,None)
        sys.modules.update(saved)
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


def _complete_manifest():
    records=[]
    for rel in sorted(["docs/infra-acceptance.md", "config.json", "scope-index.json",
                       "VISUAL_REVIEW_PROTOCOL.md", "PIPELINE.md"] +
                      ["scripts/"+p.name for p in (ROOT/"scripts").glob("*.py")]):
        data=(ROOT/rel).read_bytes()
        records.append({"path":rel,"provider":"github","sha256":w.sha256(data),
                        "blob_sha":w.git_blob_sha(data),"size_bytes":len(data)})
    return ({"schema":w.FILE_MANIFEST_SCHEMA,"source_commit":"1"*40,
             "files":records},
            {r["path"]:r["blob_sha"] for r in records})


def test_remote_tree_mismatch_rejected_before_import():
    manifest,remote=_complete_manifest()
    remote["scripts/contracts.py"]="f"*40
    with pytest.raises(w.WebBridgeError,match="remote Git commit blob"):
        w.run_web(argv=["--district","kingswell"],
                  file_manifest=manifest,root=ROOT,source_commit="1"*40,
                  remote_blobs=remote)


def test_stale_or_previously_loaded_local_module_rejected(monkeypatch):
    import types
    manifest,remote=_complete_manifest()
    stale=types.ModuleType("contracts")
    stale.__file__=str(ROOT/"scripts"/"contracts.py")
    stale._mapwork_verified_sha256="0"*64
    monkeypatch.setitem(sys.modules,"contracts",stale)
    with pytest.raises(w.WebBridgeError,match="stale/unverified cached"):
        w.run_web(argv=["--district","kingswell"],
                  file_manifest=manifest,root=ROOT,source_commit="1"*40,
                  remote_blobs=remote)


def test_missing_independent_remote_tree_rejected():
    manifest,_=_complete_manifest()
    with pytest.raises(w.WebBridgeError,match="remote Git tree blob map required"):
        w.run_web(argv=["--district","kingswell"],
                  file_manifest=manifest,root=ROOT,source_commit="1"*40,
                  remote_blobs={})


def test_web_entrypoint_dispatches_real_material_action_without_canon(tmp_path):
    """Full bridge -> pipeline.main -> controller -> file/readback -> next gate."""
    manifest, remote_blobs = _complete_manifest()
    remote = {}
    heads = [0]
    file = tmp_path / "intent.json"
    journal = tmp_path / "journal.json"
    canonical = (ROOT / "zones" / "cidade-velha" / "acceptance-ledger.json")
    unchanged = hashlib.sha256(canonical.read_bytes()).hexdigest()
    def execute(action, state, operation_id):
        assert action == "AGENT_RESOLVE_AND_RECORD_INTENT"
        assert state["agent_context"]["request"] == "Construa Kingswell"
        data = (ROOT / "zones" / "cidade-velha" / "intent.json").read_bytes()
        file.write_bytes(data)
        remote[("github", "material-intent")] = data
        blob = w.git_blob_sha(data)
        return {"operation_id": operation_id, "artifacts": [{
            "path": str(file), "sha256": w.sha256(data), "provider": "github",
            "remote_id": "material-intent", "blob_sha": blob
        }], "arg_updates": {"intent": str(file)}}
    def fetch(provider, identifier):
        return remote[(provider, identifier)]
    def sync(path, digest):
        data = path.read_bytes()
        assert w.sha256(data) == digest
        blob = w.git_blob_sha(data)
        old = f"{heads[0]:040x}"
        heads[0] += 1
        new = f"{heads[0]:040x}"
        remote[("github", blob)] = data
        remote[("github-ref", "mapwork/integration-test")] = new
        return {"provider": "github", "branch": "mapwork/integration-test",
                "blob_sha": blob, "head": new, "lease_head": old}
    local_names = {p.stem for p in (ROOT / "scripts").glob("*.py")}
    saved = {k: sys.modules.pop(k) for k in tuple(sys.modules)
             if k in local_names and k != "web_bridge"}
    try:
        response = w.run_web(
            argv=["--request", "Construa Kingswell", "--district", "kingswell",
                  "--session-key", "kingswell-source-commit",
                  "--autonomous-journal", str(journal),
                  "--max-operations", "1"],
            file_manifest=manifest, root=ROOT, source_commit="1"*40,
            remote_blobs=remote_blobs, action_executor=execute,
            remote_readback=fetch, journal_sync=sync)
    finally:
        for module in local_names - {"web_bridge"}:
            sys.modules.pop(module, None)
        sys.modules.update(saved)
    assert response["status"] == "CHECKPOINT"
    assert response["pipeline"]["result"]["completed_operations"] == 1
    assert response["pipeline"]["next_action"] == "PROVE_HOST_CAPABILITIES"
    assert journal.is_file() and file.is_file()
    assert hashlib.sha256(canonical.read_bytes()).hexdigest() == unchanged
    assert response["authorizes_canon"] is False


def test_web_adapter_requires_verified_canonical_index_and_config():
    manifest, remote = _complete_manifest()
    manifest["files"] = [f for f in manifest["files"]
                         if f["path"] != "scope-index.json"]
    with pytest.raises(w.WebBridgeError, match="canonical pipeline or binding"):
        w.run_web(argv=["--district", "kingswell"],
                  file_manifest=manifest, root=ROOT, source_commit="1"*40,
                  remote_blobs=remote)


def test_web_adapter_rejects_github_authority_replacement():
    manifest, remote = _complete_manifest()
    remote["scope-index.json"] = "f"*40
    with pytest.raises(w.WebBridgeError, match="remote Git commit blob"):
        w.run_web(argv=["--district", "kingswell"],
                  file_manifest=manifest, root=ROOT, source_commit="1"*40,
                  remote_blobs=remote)
