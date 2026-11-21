"""Connector-host handoff: material files, CAS, replay, corruption and recovery."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import orchestration as o
from native_fixture import fixture as native_fixture


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
    req,h,images,artifacts,review=native_fixture(tmp_path,op["operation_id"])
    r["artifacts"].append(next(a for a in artifacts if a["kind"]=="image"))
    with pytest.raises(ValueError,match="reference, mask, handoff and review"):
        invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                "pending_sync":p,"result":r})
    r["artifacts"].extend(a for a in artifacts if a["kind"]!="image")
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


def cold_proof(session, journal, readback_path, *, head, parent, artifacts=()):
    return {"schema":"NOVYDRES_MAPWORK_COLD_RECOVERY",
            "branch":session["branch"],
            "journal_repo_path":session["journal_repo_path"],
            "source_commit":session["source_commit"],
            "initial_head":session["initial_head"],
            "current_ref_head":head, "head_chain":[],
            "journal_readback_path":str(readback_path),
            "journal_commit":{"branch":session["branch"],
                "repo_path":session["journal_repo_path"],
                "head":head,"ref_head":head,"commit_sha":head,
                "commit_parent":parent,"tree_blob_sha":blob(journal.read_bytes()),
                "blob_sha":blob(journal.read_bytes())},
            "artifact_readbacks":list(artifacts)}


def test_cold_recovery_pending_from_other_session_reuses_original_operation(tmp_path):
    journal, artifact, invoke = setup(tmp_path)
    op = invoke()["operation"]
    second = tmp_path/"cold-host"
    second.mkdir()
    cold_journal = second/"restored-journal.json"
    cold_journal.write_bytes(journal.read_bytes())
    provider_get = second/"journal-provider-get.json"
    provider_get.write_bytes(cold_journal.read_bytes())
    doc = cold_proof(json.loads(cold_journal.read_text()),
                     cold_journal,provider_get,head="b"*40,parent="a"*40)
    recovery_file = second/"cold-proof.json"
    recovery_file.write_text(json.dumps(doc))
    def run():
        return {"next_action":"MATERIALIZE_INTENT", "phase":"INTENT",
                "publication_authorized":False,"canonical_state_changed":False}
    def apply(updates, validate_only=False):
        assert updates == {}
    result = o.run_host_exchange(
        run,cold_journal,session_key="fixed-session",source_commit="a"*40,
        branch="mapwork/integration",expected_head="a"*40,
        journal_repo_path="sessions/host-io-fixture.json",
        recovery_path=recovery_file,apply_arguments=apply)
    assert result["next_action"]=="EXECUTE_RECOVERED_PENDING_OPERATION"
    assert result["operation"]["operation_id"]==op["operation_id"]
    assert json.loads(cold_journal.read_text())["steps"][0]["status"]=="PENDING"
    doc["journal_commit"]["commit_parent"]="f"*40
    recovery_file.write_text(json.dumps(doc))
    with pytest.raises(ValueError,match="parent/lease"):
        o.run_host_exchange(
            run,cold_journal,session_key="fixed-session",source_commit="a"*40,
            branch="mapwork/integration",expected_head="a"*40,
            journal_repo_path="sessions/host-io-fixture.json",
            recovery_path=recovery_file,apply_arguments=apply)


def test_cold_recovery_completed_restores_portable_artifact_arguments(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    op=invoke()["operation"]
    pending=sync(tmp_path,journal,"a"*40,"b"*40)
    evidence=receipt(tmp_path,artifact,op["operation_id"])
    assert invoke({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                   "pending_sync":pending,"result":evidence})["next_action"]=="SYNC_COMPLETED_JOURNAL"
    second=tmp_path/"fresh-session"
    second.mkdir()
    cold=second/"journal.json"
    cold.write_bytes(journal.read_bytes())
    old=artifact.read_bytes()
    artifact.unlink()  # The previous host filesystem is no longer available.
    new_artifact=second/"restored-intent.json"
    new_artifact.write_bytes(old)
    get=second/"provider-get-intent.json"
    get.write_bytes(old)
    journal_get=second/"provider-get-journal.json"
    journal_get.write_bytes(cold.read_bytes())
    recovery=cold_proof(json.loads(cold.read_text()),cold,journal_get,
        head="c"*40,parent="d"*40,artifacts=[{
            "original_path":str(artifact),"materialized_path":str(new_artifact),
            "readback_path":str(get),"provider":"github",
            "remote_id":blob(old),"sha256":hashlib.sha256(old).hexdigest()}])
    recovery_file=second/"recovery.json"
    recovery_file.write_text(json.dumps(recovery))
    state={"intent":None}
    def run():
        return {"next_action":"CHECKPOINT" if state["intent"] else "MATERIALIZE_INTENT",
                "phase":"INTENT","publication_authorized":False,
                "canonical_state_changed":False}
    def apply(updates,validate_only=False):
        if not validate_only:
            state.update(updates)
    def call(exchange=None):
        exchange_path=None
        if exchange is not None:
            exchange_path=second/"exchange.json"
            exchange_path.write_text(json.dumps(exchange))
        return o.run_host_exchange(
            run,cold,session_key="fixed-session",source_commit="a"*40,
            branch="mapwork/integration",expected_head="a"*40,
            journal_repo_path="sessions/host-io-fixture.json",
            exchange_path=exchange_path,recovery_path=recovery_file,
            apply_arguments=apply)
    assert call()["next_action"]=="ACK_RECOVERED_COMPLETED_JOURNAL"
    complete=sync(second,cold,"d"*40,"c"*40)
    complete["repo_path"]="sessions/host-io-fixture.json"
    result=call({"kind":"ACK_COMPLETE","operation_id":op["operation_id"],
                 "completed_sync":complete,
                 "recovery_readbacks":[{"provider":"github",
                    "remote_id":blob(old),"readback_path":str(get)}]})
    assert result["next_action"]=="CHECKPOINT"
    assert state["intent"]==str(new_artifact)
    assert result["publication_authorized"] is False
    # An upload response or an unrelated GET is never enough for a cold restore.
    get.write_bytes(b"fabricated provider response")
    with pytest.raises(ValueError,match="artifact bytes differ"):
        call()


def test_cold_recovery_rejects_self_echoed_or_unbound_journal(tmp_path):
    journal, artifact, invoke = setup(tmp_path)
    invoke()
    session=json.loads(journal.read_text())
    proof=cold_proof(session,journal,journal,head="b"*40,parent="a"*40)
    with pytest.raises(ValueError,match="independent GitHub GET"):
        o._verify_cold_recovery(journal,session,proof)
    remote=tmp_path/"fresh-journal-get.json"
    remote.write_bytes(journal.read_bytes())
    proof["journal_readback_path"]=str(remote)
    proof["source_commit"]="f"*40
    with pytest.raises(ValueError,match="authority mismatch"):
        o._verify_cold_recovery(journal,session,proof)


def test_cold_recovery_rejects_head_move_without_verified_commit_chain(tmp_path):
    journal, _, invoke=setup(tmp_path)
    invoke()
    restored=tmp_path/"remote-journal.json"
    restored.write_bytes(journal.read_bytes())
    session=json.loads(journal.read_text())
    evidence=cold_proof(session,journal,restored,head="b"*40,parent="a"*40)
    evidence["current_ref_head"]="f"*40
    with pytest.raises(ValueError,match="latest GitHub HEAD"):
        o._verify_cold_recovery(journal,session,evidence)
    evidence["head_chain"]=[{"parent":"b"*40,"head":"f"*40,
                             "commit_sha":"f"*40,
                             "journal_blob_sha":blob(journal.read_bytes())}]
    aliases=o._verify_cold_recovery(journal,session,evidence)
    assert aliases=={}
    recovery_file=tmp_path/"recovery-with-upload.json"
    recovery_file.write_text(json.dumps(evidence))
    def run():
        return {"next_action":"MATERIALIZE_INTENT","publication_authorized":False,
                "canonical_state_changed":False}
    def apply(updates,validate_only=False):
        pass
    result=o.run_host_exchange(
        run,journal,session_key="fixed-session",source_commit="a"*40,
        branch="mapwork/integration",expected_head="a"*40,
        journal_repo_path="sessions/host-io-fixture.json",
        recovery_path=recovery_file,apply_arguments=apply)
    assert result["next_action"]=="RECONCILE_RECOVERED_REMOTE_WRITES"
    assert result["operation_id"]==session["steps"][-1]["operation_id"]
    assert result["current_ref_head"]=="f"*40
    assert json.loads(journal.read_text())==session
    evidence["head_chain"][0]["parent"]="e"*40
    with pytest.raises(ValueError,match="intervening Git HEAD chain"):
        o._verify_cold_recovery(journal,session,evidence)


def test_new_web_process_cannot_resume_from_local_journal_alone(tmp_path, monkeypatch):
    journal,artifact,invoke=setup(tmp_path)
    first=invoke()
    assert first["next_action"]=="SYNC_PENDING_JOURNAL"
    # This simulates a new isolated Python interpreter/Web host. A copied
    # local journal is not proof that it is GitHub's latest committed blob.
    monkeypatch.setattr(o,"_HOST_KNOWN_JOURNALS",{})
    with pytest.raises(ValueError,match="fresh connector cold recovery"):
        invoke()
    assert json.loads(journal.read_text())["steps"][0]["operation_id"]==first["operation"]["operation_id"]


def test_cold_recovery_after_upload_before_receipt_reconciles_without_reupload(tmp_path):
    journal,artifact,invoke=setup(tmp_path)
    op=invoke()["operation"]
    pending=sync(tmp_path,journal,"a"*40,"b"*40)
    result=receipt(tmp_path,artifact,op["operation_id"])
    # The GitHub artifact commit exists, but the original Web session crashed
    # before it could send COMPLETE_OPERATION to the canonical pipeline.
    second=tmp_path/"cold-after-upload"
    second.mkdir()
    cold=second/"journal.json"
    cold.write_bytes(journal.read_bytes())
    journal_get=second/"journal-provider-get.json"
    journal_get.write_bytes(cold.read_bytes())
    recovery=cold_proof(json.loads(cold.read_text()),cold,journal_get,
                         head="b"*40,parent="a"*40)
    recovery["current_ref_head"]="d"*40
    recovery["head_chain"]=[{
        "parent":"b"*40,"head":"d"*40,"commit_sha":"d"*40,
        "journal_blob_sha":blob(cold.read_bytes()),
        "operation_id":op["operation_id"],
        "files":result["github_commits"][0]["files"]}]
    proof_file=second/"recovery.json"
    proof_file.write_text(json.dumps(recovery))
    state={}
    def run():
        return {"next_action":"CHECKPOINT" if state.get("intent") else "MATERIALIZE_INTENT",
                "phase":"INTENT","publication_authorized":False,
                "canonical_state_changed":False}
    def apply(updates,validate_only=False):
        if not validate_only:
            state.update(updates)
    def call(exchange=None):
        exchanged=None
        if exchange:
            exchanged=second/"result.json"
            exchanged.write_text(json.dumps(exchange))
        return o.run_host_exchange(
            run,cold,session_key="fixed-session",source_commit="a"*40,
            branch="mapwork/integration",expected_head="a"*40,
            journal_repo_path="sessions/host-io-fixture.json",
            exchange_path=exchanged,recovery_path=proof_file,
            apply_arguments=apply)
    assert call()["next_action"]=="RECONCILE_RECOVERED_REMOTE_WRITES"
    invalid=json.loads(json.dumps(recovery))
    invalid["head_chain"][0]["operation_id"]="not-our-operation"
    proof_file.write_text(json.dumps(invalid))
    with pytest.raises(ValueError,match="cannot attribute external writes"):
        call({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
              "pending_sync":pending,"result":result})
    assert json.loads(cold.read_text())["steps"][-1]["status"]=="PENDING"
    proof_file.write_text(json.dumps(recovery))
    accepted=call({"kind":"COMPLETE_OPERATION","operation_id":op["operation_id"],
                   "pending_sync":pending,"result":result})
    assert accepted["next_action"]=="SYNC_COMPLETED_JOURNAL"
    assert accepted["lease_head"]=="d"*40
    saved=json.loads(cold.read_text())["steps"][-1]
    assert saved["operation_id"]==op["operation_id"] and saved["status"]=="COMPLETED"
    assert saved["operation_head"]=="d"*40


def test_cold_resume_allows_verified_code_only_commits_without_replaying_operation(tmp_path):
    journal, _, invoke = setup(tmp_path)
    op = invoke()["operation"]
    restored = tmp_path/"independent-journal-get.json"
    restored.write_bytes(journal.read_bytes())
    session = json.loads(journal.read_text())
    proof = cold_proof(session, journal, restored, head="b"*40, parent="a"*40)
    proof["current_ref_head"] = "d"*40
    proof["runtime_source_commit"] = "d"*40
    proof["head_chain"] = [{"parent":"b"*40, "head":"c"*40,
        "commit_sha":"c"*40, "journal_blob_sha":blob(journal.read_bytes()),
        "kind":"VERIFIED_SOURCE_CHANGE", "changed_paths":["scripts/pipeline.py"]},
        {"parent":"c"*40, "head":"d"*40, "commit_sha":"d"*40,
         "journal_blob_sha":blob(journal.read_bytes()),
         "kind":"VERIFIED_SOURCE_CHANGE", "changed_paths":["tests/test_host_exchange.py","WEB_RUNTIME.md"]}]
    proof_file = tmp_path/"verified-code-history.json"
    proof_file.write_text(json.dumps(proof))
    def run():
        return {"next_action":"NEW_STATE","publication_authorized":False,
                "canonical_state_changed":False}
    def apply(updates, validate_only=False):
        pass
    def call():
        return o.run_host_exchange(run, journal, session_key="fixed-session",
            source_commit="a"*40, branch="mapwork/integration",
            expected_head="a"*40, journal_repo_path="sessions/host-io-fixture.json",
            recovery_path=proof_file, apply_arguments=apply)
    fresh=call()
    assert fresh["next_action"] == "EXECUTE_RECOVERED_PENDING_OPERATION"
    assert fresh["operation"]["operation_id"] == op["operation_id"]
    assert json.loads(journal.read_text()) == session
    proof["head_chain"][-1]["changed_paths"].append("zones/kingswell/zone.json")
    proof_file.write_text(json.dumps(proof))
    with pytest.raises(ValueError, match="non-source writes"):
        call()


def test_cold_resume_rejects_fake_source_change_missing_runtime_pin(tmp_path):
    journal, _, invoke = setup(tmp_path)
    invoke()
    restored = tmp_path/"external-get.json"
    restored.write_bytes(journal.read_bytes())
    session = json.loads(journal.read_text())
    proof = cold_proof(session,journal,restored,head="b"*40,parent="a"*40)
    proof["current_ref_head"]="c"*40
    proof["head_chain"]=[{"parent":"b"*40,"head":"c"*40,"commit_sha":"c"*40,
        "journal_blob_sha":blob(journal.read_bytes()),
        "kind":"VERIFIED_SOURCE_CHANGE","changed_paths":["scripts/pipeline.py"]}]
    recovery=tmp_path/"without-runtime-pin.json"
    recovery.write_text(json.dumps(proof))
    def run():
        return {"next_action":"NEW_STATE","publication_authorized":False,
                "canonical_state_changed":False}
    got=o.run_host_exchange(run,journal,session_key="fixed-session",source_commit="a"*40,
        branch="mapwork/integration",expected_head="a"*40,
        journal_repo_path="sessions/host-io-fixture.json",
        recovery_path=recovery,apply_arguments=lambda changes,validate_only=False:None)
    assert got["next_action"] == "RECONCILE_RECOVERED_REMOTE_WRITES"
