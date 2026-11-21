"""Real-operation orchestration: bytes, remote readback, CAS, recovery, no fake PASS."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import orchestration as o
import pipeline


def harness(tmp_path):
    local = tmp_path / "evidence.json"
    remote = {}
    heads = [0]
    calls = []
    def pipeline_state():
        if not local.is_file():
            action = "MATERIALIZE_INTENT"
        else:
            action = "CHECKPOINT"
        return {"schema": "NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT",
                "phase": "INTENT", "next_action": action,
                "blockers": [], "publication_authorized": False,
                "canonical_state_changed": False}
    def perform(action, state, operation_id):
        assert action == "MATERIALIZE_INTENT"
        calls.append(operation_id)
        body = json.dumps({"request_id": operation_id, "target": "kingswell"}).encode()
        local.write_bytes(body)
        remote[("github", "intent-blob")] = body
        blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
        return {"operation_id": operation_id,
                "artifacts": [{"path": str(local), "provider": "github",
                               "remote_id": "intent-blob",
                               "sha256": hashlib.sha256(body).hexdigest(),
                               "blob_sha": blob}]}
    def fetch(provider, identifier):
        return remote[(provider, identifier)]
    def sync(path, sha):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
        previous = f"{heads[0]:040x}"
        heads[0] += 1
        written = path.read_bytes()
        remote[("github", "journal")] = written
        return {"provider": "github", "readback": remote[("github", "journal")],
                "lease_head": previous, "head": f"{heads[0]:040x}"}
    return local, remote, calls, pipeline_state, perform, fetch, sync


def test_real_material_action_and_independent_git_readback(tmp_path):
    local, remote, calls, run, perform, fetch, sync = harness(tmp_path)
    journal = tmp_path / "journal.json"
    result = o.run_autonomous(run, perform, fetch, sync, journal,
                              session_key="kingswell-source", max_operations=8)
    assert result["status"] == "HALTED_FOR_OWNER_OR_CAPABILITY"
    assert result["next_action"] == "CHECKPOINT"
    assert local.exists() and len(calls) == 1
    saved = json.loads(journal.read_text())
    assert saved["steps"][0]["status"] == "COMPLETED"
    assert saved["publication_authorized"] is False
    assert remote[("github", "journal")] == journal.read_bytes()
    # A new session does not redo work or allocate an unverified second attempt.
    again = o.run_autonomous(run, perform, fetch, sync, journal,
                             session_key="kingswell-source")
    assert again["next_action"] == "CHECKPOINT" and len(calls) == 1


def test_crash_after_pending_journal_reuses_same_operation_id(tmp_path):
    local, remote, calls, run, perform, fetch, sync = harness(tmp_path)
    journal = tmp_path / "journal.json"
    def interrupted(action, state, operation_id):
        calls.append(operation_id)
        raise ConnectionError("provider offline after pending persisted")
    with pytest.raises(ConnectionError):
        o.run_autonomous(run, interrupted, fetch, sync, journal,
                          session_key="stable")
    data = json.loads(journal.read_text())
    assert data["steps"][0]["status"] == "PENDING"
    restored = o.run_autonomous(run, perform, fetch, sync, journal,
                                session_key="stable")
    assert restored["next_action"] == "CHECKPOINT"
    assert calls[0] == calls[1]
    assert len(json.loads(journal.read_text())["steps"]) == 1


def test_readback_mismatch_refuses_completion_and_stage_progress(tmp_path):
    local, remote, _, run, perform, fetch, sync = harness(tmp_path)
    def tampered(action, state, operation_id):
        receipt = perform(action, state, operation_id)
        remote[("github", "intent-blob")] = b"not the uploaded bytes"
        return receipt
    with pytest.raises(ValueError, match="readback differs"):
        o.run_autonomous(run, tampered, fetch, sync, tmp_path / "journal.json",
                          session_key="kingswell")
    data = json.loads((tmp_path / "journal.json").read_text())
    assert data["steps"][0]["status"] == "PENDING"
    assert data["publication_authorized"] is False


def test_no_artifact_or_receipt_only_is_never_an_autonomous_operation(tmp_path):
    _, _, _, run, perform, fetch, sync = harness(tmp_path)
    def narrated_only(action, state, operation_id):
        return {"operation_id": operation_id, "artifacts": [],
                "statement": "Completed successful visual inspection"}
    with pytest.raises(ValueError, match="real material artifacts"):
        o.run_autonomous(run, narrated_only, fetch, sync,
                          tmp_path / "journal.json", session_key="no-text-fakes")


def test_new_candidate_requires_real_drive_png_not_json_only(tmp_path):
    _, _, _, _, _, fetch, sync = harness(tmp_path)
    p = tmp_path / "candidate.json"
    remote = {("github", "candidate"): b'{"generated":true}'}
    p.write_bytes(remote[("github", "candidate")])
    data = p.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    def run():
        return {"next_action": "REPAIR_DIAGNOSTIC_AND_REGENERATE",
                "publication_authorized": False, "canonical_state_changed": False}
    def perform(action, state, operation_id):
        return {"operation_id": operation_id, "artifacts": [
            {"path": str(p), "provider": "github", "remote_id": "candidate",
             "sha256": hashlib.sha256(data).hexdigest(), "blob_sha": blob}]}
    with pytest.raises(ValueError, match="Drive PNG bytes"):
        o.run_autonomous(run, perform, lambda provider, identifier: remote[(provider, identifier)],
                          sync, tmp_path / "journal.json", session_key="real-pixels")


def test_no_progress_cannot_loop_on_text_state(tmp_path):
    _, _, _, _, _, fetch, sync = harness(tmp_path)
    p = tmp_path / "a.json"
    body = b'{"changed":true}'
    p.write_bytes(body)
    digest = hashlib.sha256(body).hexdigest()
    blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
    def run():
        return {"next_action": "MATERIALIZE_INTENT",
                "publication_authorized": False, "canonical_state_changed": False}
    def perform(action, state, operation_id):
        return {"operation_id": operation_id, "artifacts": [
            {"path": str(p), "sha256": digest, "blob_sha": blob,
             "provider": "github", "remote_id": "a"}]}
    with pytest.raises(ValueError, match="no pipeline progress"):
        o.run_autonomous(run, perform, lambda p, i: body,
                          sync, tmp_path / "journal.json", session_key="stall")


def test_journal_chain_tampering_and_authority_mismatch_rejected(tmp_path):
    _, _, _, run, perform, fetch, sync = harness(tmp_path)
    journal = tmp_path / "journal.json"
    o.run_autonomous(run, perform, fetch, sync, journal, session_key="fixed")
    with pytest.raises(ValueError, match="authority mismatch"):
        o.run_autonomous(run, perform, fetch, sync, journal, session_key="other")
    obj = json.loads(journal.read_text())
    obj["steps"][0]["status"] = "PASS"
    journal.write_text(json.dumps(obj))
    with pytest.raises(ValueError, match="hash chain"):
        o.run_autonomous(run, perform, fetch, sync, journal, session_key="fixed")


def test_pipeline_autonomous_mode_refuses_missing_connector_hooks(capsys, tmp_path):
    code = pipeline.main(["run", "--request", "Construa Sulfok",
                          "--district", "sulfok", "--session-key", "s1",
                          "--autonomous-journal", str(tmp_path / "log.json")])
    assert code == 2
    assert "needs real host tools" in capsys.readouterr().err


def test_host_cannot_inject_pipeline_canonical_authority(tmp_path, monkeypatch):
    _, _, _, run, perform, fetch, sync = harness(tmp_path)
    def malicious(action, state, operation_id):
        value = perform(action, state, operation_id)
        value["arg_updates"] = {"_editorial_verified": True}
        return value
    # Validate the forbidden update before accepting it in the engine.
    def forbid(updates):
        if "_editorial_verified" in updates:
            raise ValueError("forbidden pipeline arguments")
    with pytest.raises(ValueError, match="forbidden"):
        o.run_autonomous(run, malicious, fetch, sync,
                          tmp_path / "journal.json", session_key="guard",
                          apply_arguments=forbid)
