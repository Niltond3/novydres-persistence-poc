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
    """Next action from actual unsuccessful attempts, never declared PASS text."""
    if not attempts:
        return "GENERATE_AND_AUDIT_CANDIDATE"
    last = attempts[-1]
    if last.get("verified_verdict") == "PASS":
        return "ADVANCE_AFTER_ACCEPTANCE"
    # A documented method reassessment starts a new six-failure epoch. The
    # seventh attempt must be constructible instead of staying stuck forever.
    epoch = max([0] + [i+1 for i, a in enumerate(attempts)
                       if a.get("method_reassessment_evidence")])
    if len(attempts) - epoch >= 6:
        return "REASSESS_METHOD"
    if len(attempts) - epoch >= 3:
        recent = attempts[-3:]
        if (all(a.get("verified_verdict") != "PASS" and
                failure_signature(a) == failure_signature(last) and
                a.get("improvement_evidence") is None for a in recent) and
                len({a.get("strategy_id") for a in recent}) == 1):
            return "REPLAN_STAGE"
    return "REPAIR_AND_REGENERATE"


def record_attempt(ledger_path, attempt_path, *, criteria_sha256, reference_sha256,
                   schema, allowed_stages, active_stage, accepted_stages=(),
                   target=None, reference_size=None):
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
    # Invalid PASS declarations are evidence to audit, not authority to block
    # future repair. Artifact bytes are independently evaluated downstream.
    if attempt.get("verdict") not in ("PASS", "FAIL"):
        raise ValueError("declared candidate verdict must be PASS/FAIL")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.is_file() else {
        "schema": schema, "criteria_sha256": criteria_sha256,
        "reference_sha256": reference_sha256,
        **({"target":target,"reference_dimensions_px":list(reference_size)}
           if target is not None and reference_size is not None else {}),
        "stages": {stage_id: {"attempts": []} for stage_id in allowed_stages}
    }
    if (ledger.get("schema") != schema or
        ledger.get("criteria_sha256") != criteria_sha256 or
        ledger.get("reference_sha256") != reference_sha256 or
        (target is not None and
         (ledger.get("target") != target or
          ledger.get("reference_dimensions_px") != list(reference_size or [])))):
        raise ValueError("ledger authority mismatch: reconcile/reaudit before append")
    groups = ledger.setdefault("stages", {})
    for predecessor in list(allowed_stages)[:list(allowed_stages).index(stage)]:
        if predecessor not in accepted_stages:
            raise ValueError("cannot append to stage before predecessors independently accepted")
    # Validate the entire append-only chain before every mutation, including
    # idempotent calls, so forged hashes and forked histories cannot be replayed.
    for stage_id, group in groups.items():
        previous_sha = None
        for ordinal, old in enumerate(group.get("attempts", []), 1):
            if (old.get("iteration") != ordinal or
                old.get("parent_attempt_sha256") != previous_sha or
                old.get("attempt_sha256") != digest({
                    k:v for k,v in old.items() if k != "attempt_sha256"})):
                raise ValueError("attempt hash chain corrupt: " + stage_id)
            original = {k:v for k,v in old.items()
                        if k not in ("iteration", "parent_attempt_sha256",
                                     "attempt_sha256", "payload_sha256",
                                     "verified_verdict")}
            if old.get("payload_sha256") != digest(original):
                raise ValueError("attempt original payload hash corrupt: " + stage_id)
            previous_sha = old["attempt_sha256"]
    attempts = groups.setdefault(stage, {"attempts": []})["attempts"]
    raw = dict(attempt)
    raw.pop("iteration", None)
    raw.pop("parent_attempt_sha256", None)
    raw.pop("attempt_sha256", None)
    raw.pop("payload_sha256", None)
    raw.pop("verified_verdict", None)
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
            if action == "REASSESS_METHOD":
                if (not isinstance(attempt.get("method_reassessment_evidence"), str) or
                    len(attempt["method_reassessment_evidence"].strip()) < 30):
                    raise ValueError("explicit method reassessment required after six failures")
    attempt["iteration"] = len(attempts) + 1
    attempt["payload_sha256"] = payload_digest
    attempt["verified_verdict"] = "UNVERIFIED"
    attempt["parent_attempt_sha256"] = prior.get("attempt_sha256") if prior else None
    attempt["attempt_sha256"] = digest({k:v for k,v in attempt.items() if k != "attempt_sha256"})
    attempts.append(attempt)
    atomic_json(ledger_path, ledger)
    return {"status": "RECORDED", "stage": stage,
            "iteration": attempt["iteration"], "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest()}


# Host-facing executable instruction for the existing sole pipeline entrypoint.
# This is metadata, not a second pipeline or an autonomous Python image loop.
def execution_directive(result):
    action=result.get("next_action")
    if not isinstance(action,str) or not action.strip():
        raise ValueError("pipeline checkpoint missing actionable next_action")
    owner={"ASK_OWNER_ONE_DECISION","READY_FOR_OWNER_REVIEW"}
    capability={"RESTORE_REQUIRED_HOST_TOOLS","BLOCKED_CAPABILITY"}
    terminal={"CHECKPOINT","STOP_SESSION_CONFIRMED"}
    repairs={"REPAIR_UNVERIFIED_CANDIDATE","REPAIR_AND_REGENERATE",
             "REPAIR_DIAGNOSTIC_AND_REGENERATE","REGENERATE_DIFFERENT_CANDIDATE",
             "CORRECT_AND_REGENERATE_IMAGE","CORRECT_AND_RETEST",
             "INVALIDATE_AND_REAUDIT_STALE_EVIDENCE"}
    replans={"REPLAN_STAGE","REPLAN_AND_REGENERATE_IMAGE",
             "REASSESS_METHOD","REASSESS_METHOD_AND_REGENERATE_IMAGE"}
    if action in owner:
        classification="EDITORIAL_DECISION";operation="ASK_OWNER";continue_session=False
    elif action in capability:
        classification="TOOL_UNAVAILABLE";operation="RESTORE_CAPABILITY";continue_session=False
    elif action in terminal:
        classification="CHECKPOINT";operation="PERSIST_AND_READBACK";continue_session=False
    elif action in repairs or action.startswith(("REPAIR_","CORRECT_","REGENERATE_")):
        classification="REPAIRABLE_FAILURE";operation="REPAIR_GENERATE_AUDIT_PERSIST";continue_session=True
    elif action in replans:
        classification="REPLANNING";operation="CHANGE_METHOD_GENERATE_AUDIT_PERSIST";continue_session=True
    else:
        classification="WORK_IN_PROGRESS";operation="EXECUTE_NEXT_ACTION_AND_REENTER";continue_session=True
    # Saving a checkpoint never implies successful stage acceptance.
    return {"classification":classification,
            "operation":operation,
            "action":action,
            "continue_same_session":continue_session,
            "rerun_entrypoint":"scripts/pipeline.py run" if continue_session else None,
            "must_persist_and_readback":True,
            "may_request_owner":classification=="EDITORIAL_DECISION",
            "may_promote_stage":action=="ADVANCE_AFTER_ACCEPTANCE" and
                isinstance(result.get("audit"),dict) and
                result["audit"].get("status")=="PASS",
            "automatic_approval":False}



# The agent-facing, material-execution controller. The injected host functions
# MUST perform the semantic/visual work via actual connected tools. These are
# not Python replacements for an LLM, Drive, or GitHub. A bare declaration of
# completion never advances the pipeline.
AUTONOMY_SCHEMA = "NOVYDRES_MAPWORK_AUTONOMOUS_SESSION"
HEX64 = __import__("re").compile(r"^[0-9a-f]{64}$")
HEX40 = __import__("re").compile(r"^[0-9a-f]{40}$")


def _session_chain(steps):
    previous = None
    for entry in steps:
        if (not isinstance(entry, dict) or entry.get("parent_sha256") != previous
                or entry.get("entry_sha256") != digest({
                    k: v for k, v in entry.items() if k != "entry_sha256"
                })):
            raise ValueError("autonomous journal hash chain corrupt")
        previous = entry["entry_sha256"]


def _persist_session(journal_path, session, sync_journal):
    """The connector must CAS-write this file to GitHub and fetch it again."""
    atomic_json(journal_path, session)
    payload = Path(journal_path).read_bytes()
    proof = sync_journal(Path(journal_path), hashlib.sha256(payload).hexdigest())
    if (not isinstance(proof, dict) or proof.get("provider") != "github"
            or not isinstance(proof.get("readback"), bytes)
            or proof["readback"] != payload
            or not HEX40.fullmatch(str(proof.get("head", "")))
            or not HEX40.fullmatch(str(proof.get("lease_head", "")))
            or proof["head"] == proof["lease_head"]):
        raise ValueError("GitHub CAS write and independent journal readback required")


def _verify_operation(operation, receipt, remote_readback, old_entries):
    if not isinstance(receipt, dict) or receipt.get("operation_id") != operation["operation_id"]:
        raise ValueError("operation receipt identity mismatch")
    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("real material artifacts required before repeating pipeline")
    verified = []
    old = {(a["provider"], a["remote_id"], a["sha256"])
           for entry in old_entries if entry.get("status") == "COMPLETED"
           for a in entry.get("artifacts", [])}
    old_content = {(a["provider"], a["sha256"])
                   for entry in old_entries if entry.get("status") == "COMPLETED"
                   for a in entry.get("artifacts", [])}
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError("invalid artifact receipt")
        path = Path(item.get("path", ""))
        value = item.get("sha256")
        provider = item.get("provider")
        remote_id = item.get("remote_id")
        if (not path.is_file() or not HEX64.fullmatch(str(value)) or
                provider not in ("github", "drive") or
                not isinstance(remote_id, str) or not remote_id):
            raise ValueError("missing local artifact or external provider identity")
        local_bytes = path.read_bytes()
        if hashlib.sha256(local_bytes).hexdigest() != value:
            raise ValueError("local artifact SHA-256 differs from receipt")
        # This must be a separate connected-provider GET, not the upload response.
        recovered = remote_readback(provider, remote_id)
        if not isinstance(recovered, bytes) or recovered != local_bytes:
            raise ValueError("remote artifact readback differs from real local bytes")
        if provider == "github":
            blob = hashlib.sha1(b"blob " + str(len(recovered)).encode() +
                                b"\0" + recovered).hexdigest()
            if item.get("blob_sha") != blob:
                raise ValueError("Git blob identity not independently verified")
        if (provider, remote_id, value) in old or (provider, value) in old_content:
            raise ValueError("completed artifact replayed as a new operation")
        if item.get("kind") == "image":
            if provider != "drive":
                raise ValueError("binary image must reside in Drive")
            from PIL import Image
            with Image.open(path) as image:
                if image.format != "PNG":
                    raise ValueError("generated image must be a genuine PNG")
                image.verify()
        verified.append({"path": str(path), "sha256": value,
                         "provider": provider, "remote_id": remote_id,
                         **({"blob_sha": item["blob_sha"]} if provider == "github" else {}),
                         **({"kind": item["kind"]} if item.get("kind") else {})})
    action = operation["action"]
    if (action in ("GENERATE_AND_AUDIT_CANDIDATE", "REPAIR_AND_REGENERATE",
                   "REPAIR_UNVERIFIED_CANDIDATE",
                   "REPAIR_DIAGNOSTIC_AND_REGENERATE",
                   "REGENERATE_DIFFERENT_CANDIDATE",
                   "GENERATE_WITH_CHATGPT_NATIVE_IMAGE",
                   "CORRECT_AND_REGENERATE_IMAGE")
            or "REGENERATE_IMAGE" in action):
        if not any(a["provider"] == "drive" and a.get("kind") == "image"
                   for a in verified):
            raise ValueError("generation requires new verified Drive PNG bytes")
    return verified


def run_autonomous(run_once, execute_action, remote_readback, sync_journal,
                   journal_path, *, session_key, max_operations=16,
                   apply_arguments=None):
    """Perform real host operations until a legitimate stop, never text-only retries.

    Host dependencies are injected, not simulated: execute_action calls research,
    visual inspection, generation, topology correction or upload tools;
    remote_readback fetches bytes independently; sync_journal must perform a
    GitHub lease write followed by a fresh GET. The caller keeps pipeline.py as
    the sole state/acceptance engine. Crash recovery reuses the SAME operation_id.
    """
    if (not all(callable(fn) for fn in
                (run_once, execute_action, remote_readback, sync_journal))
            or not isinstance(session_key, str) or not session_key
            or not isinstance(max_operations, int) or max_operations < 1):
        raise ValueError("autonomous host callbacks, session key and budget required")
    journal_path = Path(journal_path)
    if journal_path.is_file():
        session = json.loads(journal_path.read_text(encoding="utf-8"))
        if (session.get("schema") != AUTONOMY_SCHEMA or
                session.get("session_key") != session_key or
                not isinstance(session.get("steps"), list)):
            raise ValueError("journal authority mismatch")
        _session_chain(session["steps"])
    else:
        session = {"schema": AUTONOMY_SCHEMA, "session_key": session_key, "steps": [],
                   "publication_authorized": False}
    completed_this_call = 0
    while completed_this_call < max_operations:
        state = run_once()
        if (not isinstance(state, dict) or not isinstance(state.get("next_action"), str)
                or state.get("publication_authorized") is not False
                or state.get("canonical_state_changed") is not False):
            raise ValueError("pipeline state lacks independent fail-closed authority")
        directive = execution_directive(state)
        action = state["next_action"]
        if directive["classification"] in ("EDITORIAL_DECISION", "TOOL_UNAVAILABLE",
                                           "CHECKPOINT") or action == "SHOW_COMPLETE_BEFORE_AFTER":
            return {"status": "HALTED_FOR_OWNER_OR_CAPABILITY",
                    "next_action": action, "state": state,
                    "completed_operations": completed_this_call,
                    "journal_sha256": hashlib.sha256(journal_path.read_bytes()).hexdigest()
                        if journal_path.is_file() else None}
        # A stage may only be promoted by the independent acceptance evaluator.
        if action == "ADVANCE_AFTER_ACCEPTANCE" and not directive["may_promote_stage"]:
            raise ValueError("unverified stage promotion refused")
        state_sha = digest(state)
        previous = session["steps"][-1] if session["steps"] else None
        if (previous and previous["status"] == "COMPLETED" and
                previous.get("state_sha256") == state_sha):
            # Crash between committing a completed operation and applying
            # its new input path flags: replay arguments, NOT provider writes.
            updates = previous.get("arg_updates", {})
            if updates and callable(apply_arguments):
                apply_arguments(updates)
                state = run_once()
                if digest(state) != state_sha:
                    continue
            raise ValueError("no pipeline progress after material action")
        if previous and previous["status"] == "PENDING":
            if previous["state_sha256"] != state_sha or previous["action"] != action:
                raise ValueError("pending operation conflicts with resumed pipeline state")
            operation = previous
        else:
            operation = {
                "operation_id": digest({"session": session_key, "action": action,
                                        "state_sha256": state_sha,
                                        "parent": previous["entry_sha256"] if previous else None}),
                "action": action, "state_sha256": state_sha,
                "status": "PENDING", "artifacts": [],
                "parent_sha256": previous["entry_sha256"] if previous else None
            }
            operation["entry_sha256"] = digest({
                k:v for k,v in operation.items() if k != "entry_sha256"})
            session["steps"].append(operation)
            _persist_session(journal_path, session, sync_journal)
        # A pending operation may already have uploaded before a crash.
        # Calling the host with the same operation_id is an idempotent replay.
        receipt = execute_action(action, state, operation["operation_id"])
        artifacts = _verify_operation(operation, receipt, remote_readback,
                                      session["steps"][:-1])
        updates = receipt.get("arg_updates", {})
        if not isinstance(updates, dict):
            raise ValueError("operation argument updates must be an object")
        operation.update(status="COMPLETED", artifacts=artifacts,
                         receipt_sha256=digest({k:v for k,v in receipt.items()
                                                if k != "artifacts"}),
                         arg_updates=updates)
        operation["entry_sha256"] = digest({
            k:v for k,v in operation.items() if k != "entry_sha256"})
        _persist_session(journal_path, session, sync_journal)
        if updates:
            if not callable(apply_arguments):
                raise ValueError("host must apply verified pipeline argument changes")
            apply_arguments(updates)
        completed_this_call += 1
    return {"status": "INTERRUPTED_REQUIRES_RESUME", "next_action": run_once().get("next_action"),
            "completed_operations": completed_this_call,
            "journal_sha256": hashlib.sha256(journal_path.read_bytes()).hexdigest(),
            "publication_authorized": False}
