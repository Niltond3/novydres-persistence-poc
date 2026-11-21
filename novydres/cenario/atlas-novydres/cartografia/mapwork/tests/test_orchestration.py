"""Single-entry, host-driven retry: monotonic receipts, policy, replay safety."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import orchestration as o


def failed(i, *, key="INF-01.01", strategy="trace-roads", improvement=None):
    x = {
        "request_id": f"request-{i}", "stage": "INF-01",
        "reference_sha256": "a" * 64,
        "geometry_path": f"geometry-{i}.json", "geometry_sha256": f"{i:064x}",
        "preview_path": f"preview-{i}.png", "preview_sha256": f"{i+100:064x}",
        "strategy_id": strategy,
        "verdict": "FAIL", "checks": {key: {"status": "FAIL", "evidence": "failed"}},
        "findings": ["Road crosses wrong grade"], "repair_plan": "Change physical corridor",
    }
    if improvement:
        x["improvement_evidence"] = improvement
    return x


def submit(tmp_path, data):
    a = tmp_path / "candidate.json"
    a.write_text(json.dumps(data), encoding="utf-8")
    return o.record_attempt(tmp_path / "ledger.json", a,
        criteria_sha256="c"*64, reference_sha256="a"*64,
        schema="ACCEPTANCE_LEDGER", allowed_stages=("INF-01", "INF-02"),
        active_stage="INF-01" if data.get("stage")=="INF-01" else "INF-02")


def test_retry_and_replanning_measurable_and_no_false_pass(tmp_path):
    for n in (1, 2, 3):
        assert submit(tmp_path, failed(n))["iteration"] == n
    data = json.loads((tmp_path / "ledger.json").read_text())["stages"]["INF-01"]["attempts"]
    assert o.progress_policy(data) == "REPLAN_STAGE"
    with pytest.raises(ValueError, match="strategy"):
        submit(tmp_path, failed(4))
    for n in (4, 5, 6):
        x = failed(n, strategy=f"different-{n}", improvement="material corrections made")
        if n == 4:
            x["replan_evidence"] = "Split unstable road segment into verified 8px sectors"
        submit(tmp_path, x)
    data = json.loads((tmp_path / "ledger.json").read_text())["stages"]["INF-01"]["attempts"]
    assert o.progress_policy(data) == "REASSESS_METHOD"
    assert len(data) == 6
    assert all(x["verdict"] == "FAIL" for x in data)


def test_idempotent_retry_and_request_collision(tmp_path):
    a = failed(1)
    first = submit(tmp_path, a)
    raw = (tmp_path / "ledger.json").read_bytes()
    assert submit(tmp_path, a)["status"] == "IDEMPOTENT"
    assert (tmp_path / "ledger.json").read_bytes() == raw
    altered = dict(a, preview_sha256="f"*64)
    with pytest.raises(ValueError, match="request_id"):
        submit(tmp_path, altered)
    assert first["ledger_sha256"] == hashlib.sha256(raw).hexdigest()


def test_predecessor_gate_rejects_early_promotion(tmp_path):
    a = failed(1)
    a["stage"] = "INF-02"
    with pytest.raises(ValueError, match="predecessors"):
        submit(tmp_path, a)


def test_requires_new_both_geometry_and_pixels(tmp_path):
    submit(tmp_path, failed(1))
    next = failed(2)
    next["preview_sha256"] = failed(1)["preview_sha256"]
    with pytest.raises(ValueError, match="reused"):
        submit(tmp_path, next)


def test_partial_candidate_is_recorded_but_never_accepted(tmp_path):
    bad = failed(1)
    bad.pop("preview_sha256")
    assert submit(tmp_path, bad)["status"] == "RECORDED"
    ledger = json.loads((tmp_path / "ledger.json").read_text())
    assert ledger["stages"]["INF-01"]["attempts"][0]["verdict"] == "FAIL"
    assert not ledger["stages"]["INF-02"]["attempts"]


def test_invalid_pass_persisted_but_never_accepted_or_blocks_retry(tmp_path):
    a = failed(1)
    a["verdict"] = "PASS"
    assert submit(tmp_path, a)["iteration"] == 1
    ledger = json.loads((tmp_path/"ledger.json").read_text())
    assert ledger["stages"]["INF-01"]["attempts"][0]["verified_verdict"] == "UNVERIFIED"
    assert submit(tmp_path, failed(2))["iteration"] == 2


def test_host_must_execute_next_action_instead_of_terminating_on_failure():
    for action, expected in (
        ("REPAIR_DIAGNOSTIC_AND_REGENERATE","REPAIRABLE_FAILURE"),
        ("CORRECT_AND_REGENERATE_IMAGE","REPAIRABLE_FAILURE"),
        ("REPLAN_STAGE","REPLANNING"),
        ("REASSESS_METHOD_AND_REGENERATE_IMAGE","REPLANNING"),
        ("GENERATE_AND_AUDIT_CANDIDATE","WORK_IN_PROGRESS"),
    ):
        directive=o.execution_directive({"next_action":action,"audit":{"status":"FAIL"}})
        assert directive["classification"]==expected
        assert directive["continue_same_session"]
        assert directive["must_persist_and_readback"]
        assert directive["may_promote_stage"] is False
        assert directive["automatic_approval"] is False
    for action, expected in (
        ("ASK_OWNER_ONE_DECISION","EDITORIAL_DECISION"),
        ("RESTORE_REQUIRED_HOST_TOOLS","TOOL_UNAVAILABLE"),
        ("CHECKPOINT","CHECKPOINT"),
    ):
        directive=o.execution_directive({"next_action":action})
        assert directive["classification"]==expected
        assert not directive["continue_same_session"]
        assert directive["automatic_approval"] is False
