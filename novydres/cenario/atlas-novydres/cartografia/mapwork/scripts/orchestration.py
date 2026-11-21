"""Deterministic attempt ledger and policy for the single Mapwork pipeline.

The Web agent, not this module, performs research, generation, correction and
visual inspection.  Each invocation records one *real* attempt and returns a
next action.  There is deliberately no retry loop here.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")).hexdigest()


def atomic_json(path, value):
    """Write-to-temp + fsync + replace: crash-safe on a single filesystem."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as writer:
            json.dump(value, writer, ensure_ascii=False, sort_keys=True, indent=2)
            writer.write("\n")
            writer.flush()
            os.fsync(writer.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def failure_signature(attempt):
    return tuple(sorted(k for k, check in attempt.get("checks", {}).items()
                        if isinstance(check, dict) and check.get("status") == "FAIL"))


def progress_policy(attempts):
    """No unbounded repeats of one method; never return PASS by exhaustion."""
    if not attempts:
        return "GENERATE_AND_AUDIT_CANDIDATE"
    last = attempts[-1]
    if last.get("verdict") == "PASS":
        return "ADVANCE_AFTER_ACCEPTANCE"
    if len(attempts) >= 6:
        # Six unsuccessful iterations require method/premise/decomposition audit.
        # A subsequent attempt must declare a materially new method generation.
        return "REASSESS_METHOD"
    if len(attempts) >= 3:
        recent = attempts[-3:]
        if all(a.get("verdict") != "PASS" and
               failure_signature(a) == failure_signature(last) and
               a.get("improvement_evidence") is None for a in recent):
            return "REPLAN_STAGE"
    return "REPAIR_AND_REGENERATE"


def record_attempt(ledger_path, attempt_path, *, criteria_sha256, reference_sha256,
                   schema, allowed_stages, active_stage):
    """Persist one candidate even when FAIL/incomplete; no false acceptance.

    Payloads must be real JSON files. A duplicate call is idempotent; changed
    input with a reused request id is rejected; reused geometry or preview is
    rejected. Remote GitHub/Drive CAS+readback is owned by the Web host.
    """
    ledger_path = Path(ledger_path)
    attempt_path = Path(attempt_path)
    attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
    if not isinstance(attempt, dict):
        raise ValueError("attempt must be object")
    stage = attempt.get("stage")
    if stage not in allowed_stages:
        raise ValueError("unknown stage")
    if stage != active_stage:
        raise ValueError("candidate stage differs from independently evaluated active stage")
    if attempt.get("reference_sha256") != reference_sha256:
        raise ValueError("attempt has wrong approved reference")
    if not isinstance(attempt.get("request_id"), str) or not attempt["request_id"]:
        raise ValueError("attempt request_id required for idempotency")
    # Material evidence can be incomplete, but its deficit can never confer PASS.
    if attempt.get("verdict") == "PASS":
        for kind in ("geometry", "preview"):
            p = attempt.get(kind + "_path")
            if not isinstance(p, str) or not p:
                raise ValueError("PASS candidate without " + kind + " bytes")
            f = Path(p)
            if not f.is_absolute():
                f = ledger_path.parent / f
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != attempt.get(kind + "_sha256"):
                raise ValueError("PASS candidate bytes unverified: " + kind)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.is_file() else {
        "schema": schema, "criteria_sha256": criteria_sha256,
        "reference_sha256": reference_sha256,
        "stages": {stage_id: {"attempts": []} for stage_id in allowed_stages}
    }
    if (ledger.get("schema") != schema or
        ledger.get("criteria_sha256") != criteria_sha256 or
        ledger.get("reference_sha256") != reference_sha256):
        raise ValueError("ledger authority mismatch: migrate/reaudit before append")
    groups = ledger.setdefault("stages", {})
    for predecessor in list(allowed_stages)[:list(allowed_stages).index(stage)]:
        previous = groups.get(predecessor, {}).get("attempts", [])
        if not previous or previous[-1].get("verdict") != "PASS":
            raise ValueError("cannot append to stage before predecessors accepted")
    attempts = groups.setdefault(stage, {"attempts": []})["attempts"]
    raw = dict(attempt)
    raw.pop("iteration", None)
    raw.pop("parent_attempt_sha256", None)
    raw.pop("attempt_sha256", None)
    payload_digest = digest(raw)
    for earlier in attempts:
        if earlier.get("request_id") == attempt["request_id"]:
            if earlier.get("payload_sha256") == payload_digest:
                return {"status": "IDEMPOTENT", "stage": stage,
                        "iteration": earlier["iteration"], "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest()}
            raise ValueError("request_id reused with different attempt")
    prior = attempts[-1] if attempts else None
    if prior:
        for kind in ("geometry_sha256", "preview_sha256"):
            if (attempt.get(kind) and any(attempt.get(kind) == item.get(kind)
                                         for item in attempts)):
                raise ValueError("new attempt reused old " + kind)
        # After a mandatory replan/method assessment, a new strategy must be documented.
        action = progress_policy(attempts)
        if action in ("REPLAN_STAGE", "REASSESS_METHOD"):
            if (not attempt.get("replan_evidence") or
                    len(str(attempt["replan_evidence"]).strip()) < 30 or
                    attempt.get("strategy_id") == prior.get("strategy_id")):
                raise ValueError("new construction strategy and evidence required")
    attempt["iteration"] = len(attempts) + 1
    attempt["payload_sha256"] = payload_digest
    attempt["parent_attempt_sha256"] = prior.get("attempt_sha256") if prior else None
    attempt["attempt_sha256"] = digest({k:v for k,v in attempt.items() if k != "attempt_sha256"})
    attempts.append(attempt)
    atomic_json(ledger_path, ledger)
    return {"status": "RECORDED", "stage": stage,
            "iteration": attempt["iteration"], "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest()}
