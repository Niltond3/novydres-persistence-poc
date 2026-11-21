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


def test_host_connector_results_are_translated_without_callbacks(tmp_path):
    from PIL import Image
    img = tmp_path/"native-original.png"
    Image.new("RGB", (16, 16), (15, 25, 35)).save(img)
    downloaded = tmp_path/"drive-get-independent.png"
    downloaded.write_bytes(img.read_bytes())
    review = tmp_path/"review.json"
    review.write_text(json.dumps({
        "image_sha256": w.sha256(img.read_bytes()),
        "observations": ["source region checked","road crossings checked",
                         "rail grade checked","peer continuity checked"],
        "by":"AGENT","status":"FAIL"
    }))
    review_get = tmp_path/"review-drive-get.json"
    review_get.write_bytes(review.read_bytes())
    operation = {"operation_id":"op-real-image-transport","action":"GENERATE_AND_AUDIT_CANDIDATE",
                 "status":"PENDING"}
    result = w.materialize_host_exchange(
        operation=operation,pending_sync={"branch":"mapwork/noncanon"},
        provider_results=[
            {"provider":"drive","kind":"image","path":str(img),
             "readback_path":str(downloaded),
             "upload":{"success":True,"id":"actual-provider-id"},
             "readback":{"id":"actual-provider-id"}},
            {"provider":"drive","kind":"visual-review","path":str(review),
             "readback_path":str(review_get),
             "upload":{"success":True,"id":"independent-review-id"},
             "readback":{"id":"independent-review-id"}}
        ],github_commits=[],arg_updates={},
        output_path=tmp_path/"host-exchange.json")
    data=json.loads((tmp_path/"host-exchange.json").read_text())
    assert result["artifacts"]==2
    assert data["kind"]=="COMPLETE_OPERATION"
    assert data["result"]["operation_id"]=="op-real-image-transport"
    assert data["result"]["artifacts"][0]["sha256"]==w.sha256(img.read_bytes())
    assert data["result"]["artifacts"][0]["remote_id"]=="actual-provider-id"
    import orchestration
    checked=orchestration._host_artifacts(operation,data["result"],[])
    assert len(checked)==2 and any(a.get("kind")=="image" for a in checked)


def test_host_connector_adapter_rejects_forged_provider_ids_and_bytes(tmp_path):
    local=tmp_path/"original.json"
    remote=tmp_path/"get.json"
    local.write_bytes(b'{"source":"real"}')
    remote.write_bytes(local.read_bytes())
    kwargs={"operation":{"operation_id":"stable","status":"PENDING",
                         "action":"RESEARCH_REAL_WORLD_ANALOGUES"},
            "pending_sync":{"branch":"mapwork/noncanon"},
            "github_commits":[],"arg_updates":{},
            "output_path":tmp_path/"exchange.json"}
    item={"provider":"drive","path":str(local),"readback_path":str(remote),
          "upload":{"success":True,"id":"uploaded-1"},
          "readback":{"id":"other-id"}}
    with pytest.raises(w.WebBridgeError,match="provider IDs differ"):
        w.materialize_host_exchange(provider_results=[item],**kwargs)
    item["readback"]["id"]="uploaded-1"
    remote.write_bytes(b'{"source":"tampered"}')
    with pytest.raises(w.WebBridgeError,match="GET bytes differ"):
        w.materialize_host_exchange(provider_results=[item],**kwargs)
    remote.write_bytes(local.read_bytes())
    item["readback_path"]=str(local)
    with pytest.raises(w.WebBridgeError,match="separate local and GET"):
        w.materialize_host_exchange(provider_results=[item],**kwargs)


def test_host_connector_adapter_rejects_fake_github_blob_claim(tmp_path):
    local=tmp_path/"a.json"
    remote=tmp_path/"download.json"
    local.write_bytes(b'{"research":"observed"}')
    remote.write_bytes(local.read_bytes())
    record={"provider":"github","kind":"research","path":str(local),
            "readback_path":str(remote),"repo_path":"sessions/research.json",
            "upload":{"sha":"0"*40},
            "readback":{"sha":w.git_blob_sha(local.read_bytes())}}
    with pytest.raises(w.WebBridgeError,match="GitHub blob/readback"):
        w.materialize_host_exchange(
            operation={"operation_id":"op","status":"PENDING","action":"RESEARCH_REAL_WORLD_ANALOGUES"},
            pending_sync={"branch":"mapwork/noncanon"},provider_results=[record],
            github_commits=[],arg_updates={},output_path=tmp_path/"exchange.json")


def test_host_exchange_supports_real_github_create_file_commit_only_response(tmp_path):
    source=tmp_path/"research.json"
    fetched=tmp_path/"research-get.json"
    raw=b'{"observations":["verified source"],"test_only":true}'
    source.write_bytes(raw)
    fetched.write_bytes(raw)
    path="novydres/cenario/atlas-novydres/cartografia/mapwork/sessions/research.json"
    blob=w.git_blob_sha(raw)
    receipt={"provider":"github","kind":"research",
             "path":str(source),"readback_path":str(fetched),
             "repo_path":path,
             "upload":{"commit_sha":"a"*40},  # GitHub create_file action
             "readback":{"sha":blob}}  # independent fetch_file action
    github_commits=[{"commit_sha":"a"*40,"files":{path:blob}}]
    result=w.materialize_host_exchange(
        operation={"operation_id":"op","status":"PENDING",
                   "action":"RESEARCH_REAL_WORLD_ANALOGUES"},
        pending_sync={"branch":"mapwork/noncanon"},
        provider_results=[receipt],github_commits=github_commits,
        arg_updates={"research_file":str(source)},
        output_path=tmp_path/"exchange.json")
    saved=json.loads(Path(result["path"]).read_text())
    assert saved["result"]["artifacts"][0]["blob_sha"]==blob
    github_commits[0]["files"][path]="f"*40
    with pytest.raises(w.WebBridgeError,match="GitHub blob/readback"):
        w.materialize_host_exchange(
            operation={"operation_id":"op","status":"PENDING",
                       "action":"RESEARCH_REAL_WORLD_ANALOGUES"},
            pending_sync={"branch":"mapwork/noncanon"},
            provider_results=[receipt],github_commits=github_commits,
            arg_updates={},output_path=tmp_path/"exchange.json")


def test_host_exchange_materializer_does_not_preload_unverified_controller(tmp_path,monkeypatch):
    source=tmp_path/"intent.json"; downloaded=tmp_path/"github-get.json"
    body=b'{"test_only":true}'
    source.write_bytes(body);downloaded.write_bytes(body)
    blob=w.git_blob_sha(body)
    monkeypatch.delitem(sys.modules,"orchestration",raising=False)
    output=tmp_path/"exchange.json"
    w.materialize_host_exchange(
        operation={"operation_id":"independent","status":"PENDING",
                   "action":"AGENT_RESOLVE_AND_RECORD_INTENT"},
        pending_sync={"branch":"technical"},
        provider_results=[{"provider":"github","path":str(source),
            "readback_path":str(downloaded),"repo_path":"sessions/intent.json",
            "upload":{"sha":blob},"readback":{"sha":blob}}],
        github_commits=[],arg_updates={"intent":str(source)},output_path=output)
    assert "orchestration" not in sys.modules
    assert json.loads(output.read_text())["result"]["operation_id"]=="independent"
