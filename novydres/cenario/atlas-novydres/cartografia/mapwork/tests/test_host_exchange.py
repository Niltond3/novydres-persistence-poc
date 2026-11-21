"""Connector-host handoff: material files, CAS, replay, corruption and recovery."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import orchestration as o


def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def sync(tmp_path, journal, lease, head):
    payload=journal.read_bytes()
    remote=tmp_path/("git-readback-"+head+".json")
    remote.write_bytes(payload)  # host GET response materialized separately
    return {"branch":"mapwork/integration","lease_head":lease,
            "head":head,"ref_head":head,"commit_sha":head,
            "repo_path":"sessions/host-io-fixture.json",
            "commit_parent":lease,"tree_blob_sha":blob(payload),
            "blob_sha":blob(payload),"readback_path":str(remote)}


def setup(tmp_path, action="MATERIALIZE_INTENT"):
    journal=tmp_path/"journal.json"
    artifact=tmp_path/"intent.json"
    values={}
    def run():
        return {"next_action":"CHECKPOINT" if values.get("intent") else action,
                "phase":"INTENT","publication_authorized":False,
                "canonical_state_changed":False}
    def apply(updates, validate_only=False):
        if set(updates) - {"intent"}:
            raise ValueError("forbidden pipeline argument")
        if not validate_only:
            values.update(updates)
    def exchange(payload=None):
        f=tmp_path/"exchange.json"
        if payload is not None:
            f.write_text(json.dumps(payload))
        return o.run_host_exchange(run,journal,session_key="fixed-session",
                     source_commit="a"*40,branch="mapwork/integration",
                     expected_head="a"*40,
                     journal_repo_path="sessions/host-io-fixture.json",
                     exchange_path=f if payload is not None else None,
                     apply_arguments=apply)
    return journal,artifact,exchange


def receipt(tmp_path, artifact, op_id, body=b'{"intent":"real bytes"}'):
    artifact.write_bytes(body)
    remote=tmp_path/"provider-download.json"
    remote.write_bytes(body)
    return {"operation_id":op_id,"github_commits":[{
        "branch":"mapwork/integration","lease_head":"b"*40,
        "commit_parent":"b"*40,"head":"d"*40,"ref_head":"d"*40,
        "commit_sha":"d"*40,
        "files":{"candidates/intent.json":blob(body)}}],
        "artifacts":[{
        "path":str(artifact),"readback_path":str(remote),
        "provider":"github","remote_id":blob(body),
        "repo_path":"candidates/intent.json","blob_sha":blob(body),"sha256":hashlib.sha256(body).hexdigest()}],
        "arg_updates":{"intent":str(artifact)}}


def test_material_operation_sync_and_recovery(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    initial=invoke()
    assert initial["next_action"]=="SYNC_PENDING_JOURNAL"
    operation=initial["operation"]
    assert json.loads(journal.read_text())["steps"][0]["status"]=="PENDING"
    pending=sync(tmp_path,journal,"a"*40,"b"*40)
    assert invoke()["operation"]["operation_id"]==operation["operation_id"]
    delivered=receipt(tmp_path,artifact,operation["operation_id"])
    committed=invoke({"kind":"COMPLETE_OPERATION","operation_id":operation["operation_id"],
                      "pending_sync":pending,"result":delivered})
    assert committed["next_action"]=="SYNC_COMPLETED_JOURNAL"
    # Lost response is idempotent: no second provider upload / new id.
    repeated=invoke({"kind":"COMPLETE_OPERATION","operation_id":operation["operation_id"]})
    assert repeated["next_action"]=="SYNC_COMPLETED_JOURNAL"
    complete=sync(tmp_path,journal,"d"*40,"c"*40)
    fresh=tmp_path/"fresh-provider-download.json"
    fresh.write_bytes(artifact.read_bytes())
    done=invoke({"kind":"ACK_COMPLETE","operation_id":operation["operation_id"],
                 "completed_sync":complete,
                 "recovery_readbacks":[{"provider":"github",
                    "remote_id":blob(artifact.read_bytes()),"readback_path":str(fresh)}]})
    assert done["next_action"]=="CHECKPOINT"
    assert done["publication_authorized"] is False
    saved=json.loads(journal.read_text())
    assert saved["steps"][0]["status"]=="COMPLETED"


def test_journal_sync_requires_original_lease_and_independent_bytes(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    op=invoke()["operation"]
    r=receipt(tmp_path,artifact,op["operation_id"])
    p=sync(tmp_path,journal,"a"*40,"b"*40)
    p["commit_parent"]="f"*40
    with pytest.raises(ValueError,match="CAS/head/tree/blob"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})
    assert json.loads(journal.read_text())["steps"][0]["status"]=="PENDING"
    p["commit_parent"]="a"*40
    Path(p["readback_path"]).write_bytes(b"forged local echo")
    with pytest.raises(ValueError,match="readback bytes differ"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})


def test_fake_provider_receipt_or_replayed_bytes_rejected(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    op=invoke()["operation"]
    p=sync(tmp_path,journal,"a"*40,"b"*40)
    r=receipt(tmp_path,artifact,op["operation_id"])
    Path(r["artifacts"][0]["readback_path"]).write_bytes(b"corrupt provider data")
    with pytest.raises(ValueError,match="GitHub remote artifact must use"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})
    r=receipt(tmp_path,artifact,op["operation_id"])
    r["arg_updates"]={"_editorial_verified":True}
    with pytest.raises(ValueError,match="forbidden"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})


def test_generation_requires_real_png_and_hash_bound_review(tmp_path):
    journal,artifact,invoke=setup(tmp_path,action="GENERATE_AND_AUDIT_CANDIDATE")
    op=invoke()["operation"]
    p=sync(tmp_path,journal,"a"*40,"b"*40)
    r=receipt(tmp_path,artifact,op["operation_id"])
    with pytest.raises(ValueError,match="Drive PNG bytes"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})
    from PIL import Image
    image=tmp_path/"actual-image.png"
    Image.new("RGB",(16,16),(22,33,44)).save(image)
    remote=tmp_path/"downloaded-image.png"
    remote.write_bytes(image.read_bytes())
    body=image.read_bytes()
    r["artifacts"].append({"path":str(image),"readback_path":str(remote),
        "provider":"drive","remote_id":"drive-file-example","kind":"image",
        "sha256":hashlib.sha256(body).hexdigest()})
    with pytest.raises(ValueError,match="visual inspection"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})
    visual=tmp_path/"visual.json"
    visual.write_text(json.dumps({"image_sha256":hashlib.sha256(body).hexdigest(),
                   "observations":["source inspected","bounds inspected",
                                   "connections inspected","grade inspected"]}))
    vb=visual.read_bytes()
    vr=tmp_path/"downloaded-visual.json"
    vr.write_bytes(vb)
    r["artifacts"].append({"path":str(visual),"readback_path":str(vr),
        "provider":"github","remote_id":blob(vb),"blob_sha":blob(vb),
        "repo_path":"candidates/visual.json","kind":"visual-review","sha256":hashlib.sha256(vb).hexdigest()})
    r["github_commits"][0]["files"]["candidates/visual.json"]=blob(vb)
    assert invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                   "pending_sync":p,"result":r})["next_action"]=="SYNC_COMPLETED_JOURNAL"


def test_resume_denies_foreign_session_and_tampered_hash_chain(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    invoke()
    data=json.loads(journal.read_text())
    data["session_key"]="foreign"
    journal.write_text(json.dumps(data))
    with pytest.raises(ValueError,match="authority mismatch"):
        invoke()
    data["session_key"]="fixed-session"
    data["steps"][0]["action"]="fake PASS"
    journal.write_text(json.dumps(data))
    with pytest.raises(ValueError,match="hash chain"):
        invoke()


def test_host_journal_remote_path_is_bound_and_noncanonical(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    op=invoke()["operation"]
    p=sync(tmp_path,journal,"a"*40,"b"*40)
    p["repo_path"]="zones/cidade-velha/checkpoint.json"
    r=receipt(tmp_path,artifact,op["operation_id"])
    with pytest.raises(ValueError,match="CAS/head/tree/blob"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})


def test_pipeline_intent_cannot_pivot_to_different_district(capsys):
    import pipeline
    known=ROOT/"zones"/"cidade-velha"/"intent.json"
    code=pipeline.main(["run","--district","sulfok","--intent",str(known)])
    assert code==2
    assert "requested district and resolved intent target mismatch" in capsys.readouterr().err


def test_host_exchange_is_not_a_false_remote_checkpoint(capsys,tmp_path):
    import pipeline
    code=pipeline.main(["run","--request","Teste técnico sem mapa",
        "--district","sulfok","--session-key","io-fixture",
        "--autonomous-journal",str(tmp_path/"journal.json"),
        "--source-commit","a"*40,
        "--host-head","a"*40,"--host-branch","mapwork/integration",
        "--host-journal-path","sessions/test-only.json"])
    assert code==0
    payload=json.loads(capsys.readouterr().out)
    assert payload["status"]=="BLOCKED"
    assert payload["next_action"]=="SYNC_PENDING_JOURNAL"
    assert payload["retryable"] is True
