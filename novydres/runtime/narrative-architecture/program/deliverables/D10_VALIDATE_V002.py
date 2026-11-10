#!/usr/bin/env python3
"""D10 V002 proof verifier. Documentary only; never mutates narrative state."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent
V1_PATH = BASE / "D10_VALIDATE_V001.py"
spec = importlib.util.spec_from_file_location("d10_v1", V1_PATH)
v1 = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(v1)

BRANCH = "design/chr001-narrative-program-d01"
CYCLE_DIR = "novydres/chronicles/CHR-001/orchestration"
DELIVERABLES = "novydres/runtime/narrative-architecture/program/deliverables"
SHA1 = re.compile(r"^[0-9a-f]{40}$")
GATE_OK = {"PASS", "PASS_WITH_UNKNOWN"}
APPROVAL_RESOLUTION_KINDS = {
    "APPROVED": "PLAYER_APPROVAL_GRANTED",
    "DECLINED": "PLAYER_APPROVAL_DECLINED",
    "NOT_REQUIRED": "PLAYER_APPROVAL_NOT_REQUIRED",
}
APPROVAL_PENDING_STATUSES = {None, "PENDING_PLAYER_APPROVAL", "BLOCKED_EXTERNAL_DEPENDENCY", "NOT_GRANTED"}
HANDOFFS = {
    "D01": f"{DELIVERABLES}/HANDOFF_D01_V001.json",
    "D02": f"{DELIVERABLES}/HANDOFF_D02_V011.json",
    "D03": f"{DELIVERABLES}/HANDOFF_D03_V001.json",
    "D04": f"{DELIVERABLES}/HANDOFF_D04_V001.json",
    "D05": f"{DELIVERABLES}/HANDOFF_D05_V002.json",
    "D06": f"{DELIVERABLES}/HANDOFF_D06_V001.json",
    "D07": f"{DELIVERABLES}/HANDOFF_D07_V001.json",
    "D08": f"{DELIVERABLES}/HANDOFF_D08_V001.json",
    "D09": f"{DELIVERABLES}/HANDOFF_D09_V001.json",
    "D10": f"{DELIVERABLES}/HANDOFF_D10_V002.json",
    "D11": f"{DELIVERABLES}/HANDOFF_D11_V001.json",
}


def run(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.decode("utf-8").strip()


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git_blob(root: Path, rev: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def tree_blob(root: Path, rev: str, path: str) -> str:
    return run(root, "rev-parse", f"{rev}:{path}")


def git_tree_entry(root: Path, rev: str, path: str) -> tuple[str, str, str] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-z", rev, "--", f":(literal){path}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    for record in result.split(b"\0"):
        if not record:
            continue
        metadata, entry_path = record.split(b"\t", 1)
        if entry_path.decode("utf-8") != path:
            continue
        mode, object_type, object_sha = metadata.decode("ascii").split(" ", 2)
        return mode, object_type, object_sha
    return None


def git_regular_blob(root: Path, rev: str, path: str) -> bytes:
    entry = git_tree_entry(root, rev, path)
    if entry is None or entry[0] not in {"100644", "100755"} or entry[1] != "blob":
        raise ValueError(f"{path} is not a regular tracked file (symlink, submodule or other tree entry)")
    raw = git_blob(root, rev, path)
    if blob_sha(raw) != entry[2]:
        raise ValueError(f"{path} content differs from its Git tree object")
    return raw


def latest_cycle(root: Path, master_head: str) -> tuple[str, str, dict[str, Any]]:
    run(root, "fetch", "--no-tags", "origin", "refs/heads/master:refs/remotes/origin/master")
    if run(root, "rev-parse", "refs/remotes/origin/master") != master_head:
        raise ValueError("origin/master differs from the independently supplied master HEAD")
    names = run(root, "ls-tree", "-r", "--name-only", master_head, "--", CYCLE_DIR).splitlines()
    versions = []
    for name in names:
        match = re.fullmatch(re.escape(CYCLE_DIR) + r"/CYCLE_V(\d+)\.json", name)
        if match:
            versions.append((int(match.group(1)), name))
    if not versions:
        raise ValueError("authoritative master contains no numeric CHR-001 cycle")
    path = max(versions)[1]
    raw = git_regular_blob(root, master_head, path)
    cycle = json.loads(raw)
    last_event = cycle.get("checkpoint", {}).get("last_event_id")
    if not isinstance(last_event, str) or not last_event:
        raise ValueError("latest authoritative cycle has no checkpoint.last_event_id")
    return path, blob_sha(raw), cycle


def json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("source json_pointer must be an RFC 6901 pointer")
    current = value
    for raw in pointer[1:].split("/"):
        if re.search(r"~(?![01])", raw):
            raise ValueError("source json_pointer contains an invalid RFC 6901 escape")
        part = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", part):
                raise ValueError("array indices in a JSON pointer must be canonical non-negative integers")
            index = int(part)
            if index >= len(current):
                raise IndexError("JSON pointer array index is out of range")
            current = current[index]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise ValueError("source json_pointer does not resolve")
    return current


def cycle_source_map(cycle: dict[str, Any]) -> dict[str, str]:
    refs: dict[str, str] = {}
    for ref in cycle.get("refs", {}).values():
        if isinstance(ref, dict) and isinstance(ref.get("path"), str) and isinstance(ref.get("blob_sha"), str):
            refs[ref["path"]] = ref["blob_sha"]
    return refs


def approval_request_sha256(decision: dict[str, Any]) -> str | None:
    """Fingerprint the exact player-facing request, excluding status/resolution metadata."""
    text = decision.get("decision")
    if not isinstance(text, str) or not text.strip():
        return None
    payload = {key: value for key, value in decision.items() if key not in {"id", "status", "resolution"}}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def verify_semantic_ref(
    root: Path,
    source_head: str,
    cycle: dict[str, Any],
    ref: Any,
    record_type: str,
    fields: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(ref, dict):
        return ["semantic source ref is required"]
    path = ref.get("path")
    if path not in cycle_source_map(cycle):
        return ["semantic source is not one of the exact latest-cycle refs"]
    if ref.get("blob_sha") != cycle_source_map(cycle)[path]:
        return ["semantic source blob SHA differs from the blob pinned by latest-cycle refs"]
    try:
        raw = git_regular_blob(root, source_head, path)
        if blob_sha(raw) != ref.get("blob_sha"):
            return ["semantic source blob does not match the pinned source HEAD"]
        doc = json.loads(raw)
        record = json_pointer(doc, ref.get("json_pointer"))
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError, IndexError, TypeError, json.JSONDecodeError):
        return ["semantic source JSON pointer does not resolve in the pinned source blob"]
    if not isinstance(record, dict) or record.get("record_type") != record_type:
        errors.append(f"source pointer must resolve to a {record_type} record")
    else:
        for key, expected in fields.items():
            if record.get(key) != expected:
                errors.append(f"source {record_type} record does not prove {key}")
    if ref.get("anchor") != ref.get("json_pointer"):
        errors.append("structured source anchor must equal its exact JSON pointer")
    return errors


def validate_bundle_v2(
    bundle: dict[str, Any], root: Path, expected_source_head: str, expected_master_head: str
) -> list[str]:
    errors = v1.validate_bundle(bundle, v1.load_registry()[1], root, expected_source_head)
    try:
        if run(root, "rev-parse", "HEAD") != expected_source_head:
            return errors + ["working source HEAD differs from independent source HEAD"]
        cycle_path, cycle_sha, cycle = latest_cycle(root, expected_master_head)
    except (ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return errors + [f"authoritative checkpoint cannot be verified: {exc}"]
    cycle_ref = bundle.get("cycle_ref", {})
    if cycle_ref.get("path") != cycle_path or cycle_ref.get("blob_sha") != cycle_sha:
        errors.append("bundle checkpoint ref is not the numerically latest cycle on origin/master")
    if cycle_ref.get("verification") != "VERIFIED":
        errors.append("latest cycle ref must be independently verified")
    event = cycle.get("checkpoint", {}).get("last_event_id")
    if not event_ids_match_cycle(bundle, cycle):
        errors.append("event_ids must be derived exactly from latest cycle checkpoint; older or invented IDs remain UNKNOWN")

    acquisitions = {a.get("acquisition_id"): a for a in bundle.get("acquisition_records", []) if isinstance(a, dict) and isinstance(a.get("acquisition_id"), str)}
    for item in bundle.get("artifacts", []):
        if isinstance(item, dict) and item.get("type") == "knowledge" and isinstance(item.get("data"), dict):
            knowledge = item["data"]
            if not knowledge_fact_matches_acquisition(knowledge, acquisitions):
                errors.append(f"knowledge {knowledge.get('knowledge_id', 'UNKNOWN')}: fact_ref must equal the exact source-backed acquisition fact_ref")
    for record in bundle.get("acquisition_records", []):
        if not isinstance(record, dict):
            continue
        fields = {key: record.get(key) for key in ("acquisition_id", "knower_id", "event_id", "method", "evidence_id", "fact_ref")}
        errors.extend(f"acquisition {record.get('acquisition_id')}: {e}" for e in verify_semantic_ref(root, expected_source_head, cycle, record.get("source"), "ACQUISITION", fields))

    for record in bundle.get("decision_records", []):
        if not isinstance(record, dict):
            continue
        fields = {key: record.get(key) for key in ("decision_id", "decision_maker", "decision_kind", "scope", "affected_refs", "event_id", "evidence_id")}
        errors.extend(f"decision {record.get('decision_id')}: {e}" for e in verify_semantic_ref(root, expected_source_head, cycle, record.get("source"), "PLAYER_DECISION", fields))

    for item in bundle.get("artifacts", []):
        if not isinstance(item, dict) or not isinstance(item.get("data"), dict):
            continue
        data = item["data"]
        prov = data.get("provenance", {})
        if isinstance(prov, dict) and prov.get("record_kind") == "CANON_EVENT":
            event_id = prov.get("as_of_event_id") or data.get("as_of_event_id")
            refs = prov.get("source_refs", [])
            if not refs:
                errors.append("CANON_EVENT claim lacks an exact event source record")
            for ref in refs:
                errors.extend(verify_semantic_ref(root, expected_source_head, cycle, ref, "CANON_EVENT", {"event_id": event_id}))
        if item.get("type") == "plot":
            for link in data.get("plot_links", []):
                if link.get("kind") == "CAUSAL":
                    for ref in link.get("sources", []):
                        errors.extend(verify_semantic_ref(root, expected_source_head, cycle, ref, "CAUSAL_LINK", {"from_id": data.get("plot_id"), "to_id": link.get("target_id"), "kind": "CAUSAL"}))
        if item.get("type") == "retcon" and data.get("status") in {"PLAYER_APPROVED", "APPLIED_VERSIONED"}:
            approved = [r for r in bundle.get("decision_records", []) if isinstance(r, dict) and r.get("decision_id") == data.get("approval_decision_id")]
            if not approved:
                errors.append(f"retcon {data.get('change_id')} has no source-backed exact player decision")
    return errors


def event_ids_match_cycle(bundle: dict[str, Any], cycle: dict[str, Any]) -> bool:
    event = cycle.get("checkpoint", {}).get("last_event_id")
    return isinstance(event, str) and bundle.get("event_ids") == [event]


def knowledge_fact_matches_acquisition(knowledge: dict[str, Any], acquisitions: dict[str, dict[str, Any]]) -> bool:
    acquisition = acquisitions.get(knowledge.get("acquisition_ref"))
    return acquisition is not None and acquisition.get("fact_ref") == knowledge.get("fact_ref")


def verify_publication(
    record: dict[str, Any], root: Path, expected_input_head: str, expected_master_head: str
) -> list[str]:
    errors: list[str] = []
    if record.get("remote") != "origin" or record.get("target_branch") != BRANCH:
        return ["publication must target origin's authorized documentary branch"]
    if record.get("force_push") is not False:
        errors.append("force push is prohibited")
    commit = record.get("commit", "")
    if not isinstance(commit, str) or not SHA1.fullmatch(commit):
        return errors + ["published commit must be an actual 40-character Git object"]
    if record.get("input_head") != expected_input_head or not SHA1.fullmatch(str(expected_input_head)):
        errors.append("publication input HEAD differs from independently supplied input HEAD")
    if record.get("master_head") != expected_master_head or not SHA1.fullmatch(str(expected_master_head)):
        errors.append("publication master HEAD differs from independently supplied master HEAD")
    try:
        run(root, "fetch", "--no-tags", "origin", f"refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}", "refs/heads/master:refs/remotes/origin/master")
        remote_head = run(root, "rev-parse", f"refs/remotes/origin/{BRANCH}")
        remote_master = run(root, "rev-parse", "refs/remotes/origin/master")
        if remote_master != expected_master_head:
            errors.append("remote master changed from independently supplied checkpoint")
        if remote_head != record.get("remote_head_after"):
            errors.append("remote documentary branch HEAD does not match publication record")
        run(root, "merge-base", "--is-ancestor", commit, remote_head)
        actual_parent = run(root, "rev-list", "--parents", "-n", "1", commit).split()
        if len(actual_parent) != 2 or actual_parent[1] != expected_input_head:
            errors.append("actual published commit parent differs from expected input HEAD")
        actual_tree = run(root, "rev-parse", f"{commit}^{{tree}}")
        if actual_tree != record.get("tree"):
            errors.append("actual Git tree SHA differs from publication record")
        changed = run(root, "diff-tree", "--no-commit-id", "--name-status", "-r", expected_input_head, commit).splitlines()
        changed_paths = []
        for line in changed:
            cols = line.split("\t")
            if len(cols) != 2 or cols[0] != "A" or not cols[1].startswith(DELIVERABLES + "/"):
                errors.append("publication commit must add only new deliverable artifacts")
            elif ".." in Path(cols[-1]).parts:
                errors.append("publication path escapes deliverables")
            changed_paths.append(cols[-1])
        artifacts = record.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append("publication requires an explicit artifact path/blob manifest")
        else:
            expected_paths = set()
            for artifact in artifacts:
                path, sha = artifact.get("path"), artifact.get("blob_sha")
                if path not in changed_paths or not isinstance(sha, str) or not SHA1.fullmatch(sha):
                    errors.append("artifact manifest must list each added path with a Git blob SHA")
                    continue
                expected_paths.add(path)
                entry = git_tree_entry(root, commit, path)
                if entry is None or entry[0] not in {"100644", "100755"} or entry[1] != "blob":
                    errors.append(f"published artifact is not a regular tracked file: {path}")
                    continue
                actual = entry[2]
                raw = git_regular_blob(root, commit, path)
                if actual != sha or blob_sha(raw) != sha:
                    errors.append(f"remote commit blob/content mismatch: {path}")
                if re.search(rb"gh[oprsu]_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", raw):
                    errors.append(f"credential pattern detected in published artifact: {path}")
            if expected_paths != set(changed_paths):
                errors.append("artifact manifest does not exactly cover the new-file diff")
    except (subprocess.CalledProcessError, OSError, ValueError):
        errors.append("actual Git remote/readback verification failed")
    return errors


def resolve_handoff_gate(root: Path, head: str, phase: str, ref: dict[str, Any]) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    path = HANDOFFS.get(phase)
    if not path or ref.get("path") != path:
        return None, [f"{phase} must cite its authoritative versioned handoff path"]
    try:
        raw = git_regular_blob(root, head, path)
        sha = blob_sha(raw)
        if sha != ref.get("blob_sha"):
            return None, [f"{phase} handoff blob does not match pinned Git tree"]
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return None, [f"{phase} handoff is not readable at verified HEAD"]
    except ValueError as exc:
        if "regular tracked file" in str(exc) or "differs from its Git tree object" in str(exc):
            return None, [f"{phase} handoff Git entry is invalid: {exc}"]
        return None, [f"{phase} handoff is not readable at verified HEAD"]
    except (subprocess.CalledProcessError, OSError):
        return None, [f"{phase} handoff is not readable at verified HEAD"]
    status = doc.get("gate", doc.get("status")) if phase == "D01" else doc.get("gate")
    if status not in GATE_OK:
        errors.append(f"{phase} handoff gate is not approved: {status}")
    return status, errors


def collect_pending_approvals(root: Path, head: str, expected_master_head: str) -> tuple[list[str], list[str]]:
    paths = run(root, "ls-tree", "-r", "--name-only", head, "--", DELIVERABLES).splitlines()
    entries_by_id: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    pending: list[str] = []
    errors: list[str] = []
    try:
        _, _, cycle = latest_cycle(root, expected_master_head)
    except (ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return ["CHECKPOINT_UNVERIFIED"], [f"approval resolution checkpoint cannot be verified: {exc}"]
    latest_event = cycle.get("checkpoint", {}).get("last_event_id")
    for path in paths:
        if not re.search(r"D\d+_PLAYER_APPROVAL_QUEUE_V\d+\.json$", path):
            continue
        try:
            doc = json.loads(git_regular_blob(root, head, path))
        except (json.JSONDecodeError, subprocess.CalledProcessError, ValueError):
            pending.append(f"UNREADABLE:{path}")
            errors.append(f"approval queue is unreadable: {path}")
            continue
        decisions = doc.get("decisions")
        if not isinstance(decisions, list):
            pending.append(f"INVALID_QUEUE:{path}")
            errors.append(f"approval queue decisions must be an array: {path}")
            continue
        for decision in decisions:
            if not isinstance(decision, dict) or not isinstance(decision.get("id"), str) or not decision["id"]:
                pending.append(f"INVALID_DECISION:{path}")
                errors.append(f"approval queue contains an entry without a stable decision id: {path}")
                continue
            entries_by_id.setdefault(decision["id"], []).append((path, decision))

    for ident, entries in sorted(entries_by_id.items()):
        verified_resolutions: list[tuple[str, str]] = []
        invalid_resolution = False
        request_hashes = {approval_request_sha256(decision) for _, decision in entries}
        if None in request_hashes:
            pending.append(f"{ident}:REQUEST_UNVERIFIABLE")
            if any(decision.get("status") in APPROVAL_RESOLUTION_KINDS or decision.get("resolution") is not None for _, decision in entries):
                errors.append(f"{ident}: terminal resolution cannot apply because a repeated request lacks a verifiable decision statement")
            continue
        if len(request_hashes) != 1:
            pending.append(f"{ident}:REQUEST_CONFLICT")
            if any(decision.get("status") in APPROVAL_RESOLUTION_KINDS or decision.get("resolution") is not None for _, decision in entries):
                errors.append(f"{ident}: terminal resolution cannot apply to divergent repeated request content")
            continue
        request_hash = next(iter(request_hashes))
        for path, decision in entries:
            status = decision.get("status")
            resolution = decision.get("resolution")
            if isinstance(status, str) and status in APPROVAL_RESOLUTION_KINDS:
                if not isinstance(resolution, dict) or resolution.get("status") != status:
                    errors.append(f"{ident}: terminal status {status} lacks a matching source-backed resolution")
                    invalid_resolution = True
                    continue
                if resolution.get("request_sha256") != request_hash:
                    errors.append(f"{ident}: terminal resolution is not bound to the exact repeated request fingerprint")
                    invalid_resolution = True
                    continue
                source = resolution.get("source")
                expected_fields = {
                    "decision_id": ident,
                    "decision_maker": "PLAYER",
                    "decision_kind": APPROVAL_RESOLUTION_KINDS[status],
                    "scope": f"APPROVAL_RESOLUTION:{ident}",
                    "affected_refs": [f"approval:{ident}"],
                    "event_id": latest_event,
                    "approval_request_sha256": request_hash,
                }
                source_errors = verify_semantic_ref(root, head, cycle, source, "PLAYER_DECISION", expected_fields)
                record: Any = None
                if not source_errors and isinstance(source, dict):
                    try:
                        source_doc = json.loads(git_regular_blob(root, head, source["path"]))
                        record = json_pointer(source_doc, source.get("json_pointer"))
                    except (subprocess.CalledProcessError, OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError):
                        source_errors.append("player decision evidence pointer does not resolve")
                if not source_errors and (not isinstance(record, dict) or not isinstance(record.get("evidence_id"), str) or not record["evidence_id"]):
                    source_errors.append("player decision evidence_id must be present and non-empty")
                if source_errors:
                    errors.extend(f"{ident}: {item}" for item in source_errors)
                    invalid_resolution = True
                    continue
                signature = json.dumps({"status": status, "request_sha256": request_hash, "source": source}, sort_keys=True, separators=(",", ":"))
                verified_resolutions.append((status, signature))
            elif resolution is not None:
                errors.append(f"{ident}: a resolution object requires a matching terminal status")
                invalid_resolution = True
            elif not (status is None or isinstance(status, str) and status in APPROVAL_PENDING_STATUSES):
                errors.append(f"{ident}: unsupported approval queue status {status!r}")
                invalid_resolution = True

        distinct = {signature for _, signature in verified_resolutions}
        if len(distinct) > 1:
            errors.append(f"{ident}: conflicting source-backed approval resolutions exist")
            invalid_resolution = True
        if invalid_resolution or not verified_resolutions:
            statuses = sorted({str(decision.get("status") or "STATUS_UNRECORDED") for _, decision in entries})
            pending.append(f"{ident}:{'/'.join(statuses)}")

    return sorted(set(pending)), errors


def passing_audit_findings_safe(report: dict[str, Any]) -> list[str]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        return ["review report must include an explicit findings list"]
    result = report.get("result")
    errors: list[str] = []
    allowed_severity = {"INFO", "LOW", "MEDIUM", "HIGH", "MATERIAL", "BLOCKER", "CRITICAL"}
    allowed_disposition = {"OPEN", "RESOLVED", "BOUNDED_UNKNOWN", "NON_MATERIAL"}
    finding_ids: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"finding {index} must have structured severity and disposition")
            continue
        severity = finding.get("severity")
        disposition = finding.get("disposition")
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not finding_id.strip():
            errors.append(f"finding {index} must have a stable non-empty id")
        elif finding_id in finding_ids:
            errors.append(f"finding {index} duplicates finding id {finding_id!r}")
        else:
            finding_ids.add(finding_id)
        if severity not in allowed_severity or disposition not in allowed_disposition:
            errors.append(f"finding {index} must declare a recognized severity and disposition")
            continue
        if disposition == "OPEN":
            errors.append(f"finding {index} remains open and cannot support a passing review")
        if severity in {"MATERIAL", "BLOCKER", "CRITICAL"} and disposition != "RESOLVED":
            errors.append(f"material finding {index} must be resolved before a passing review")
        resolution_evidence = finding.get("resolution_evidence")
        if disposition == "RESOLVED":
            if not isinstance(resolution_evidence, list) or not resolution_evidence:
                errors.append(f"resolved finding {index} must cite one or more structured remediation records")
                continue
            for record_index, record in enumerate(resolution_evidence):
                if not isinstance(record, dict) or set(record) != {"finding_id", "remediation", "refs"}:
                    errors.append(f"resolved finding {index} record {record_index} must contain exactly finding_id, remediation and refs")
                    continue
                if record.get("finding_id") != finding_id:
                    errors.append(f"resolved finding {index} record {record_index} must bind its exact finding id")
                if not isinstance(record.get("remediation"), str) or not record["remediation"].strip():
                    errors.append(f"resolved finding {index} record {record_index} must describe the remediation")
                refs = record.get("refs")
                if not isinstance(refs, list) or not refs:
                    errors.append(f"resolved finding {index} record {record_index} must cite one or more source refs")
                    continue
                for ref_index, ref in enumerate(refs):
                    if not isinstance(ref, dict) or set(ref) != {"path", "blob_sha", "anchor_kind", "anchor"}:
                        errors.append(f"resolved finding {index} record {record_index} ref {ref_index} must have exactly path, blob_sha, anchor_kind and anchor")
                        continue
                    if not isinstance(ref.get("path"), str) or not ref["path"].startswith(DELIVERABLES + "/") or ".." in Path(ref["path"]).parts:
                        errors.append(f"resolved finding {index} record {record_index} ref {ref_index} must target a deliverable")
                    if not isinstance(ref.get("blob_sha"), str) or not SHA1.fullmatch(ref["blob_sha"]):
                        errors.append(f"resolved finding {index} record {record_index} ref {ref_index} must include a Git blob SHA")
                    if ref.get("anchor_kind") not in {"JSON_POINTER", "TEXT_LITERAL"} or not isinstance(ref.get("anchor"), str) or not ref["anchor"].strip():
                        errors.append(f"resolved finding {index} record {record_index} ref {ref_index} must include a typed, non-empty anchor")
        if disposition == "BOUNDED_UNKNOWN" and result != "PASS_WITH_UNKNOWN":
            errors.append(f"bounded unknown finding {index} requires PASS_WITH_UNKNOWN")
    return errors


def verify_resolution_evidence_refs(root: Path, head: str, report_path: str, report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        report_blob_sha = blob_sha(git_regular_blob(root, head, report_path))
    except (subprocess.CalledProcessError, OSError, ValueError):
        report_blob_sha = None
    for index, finding in enumerate(report.get("findings", [])):
        if not isinstance(finding, dict) or finding.get("disposition") != "RESOLVED":
            continue
        records = finding.get("resolution_evidence")
        if not isinstance(records, list):
            continue  # The structural checker reports the missing typed records.
        for record_index, record in enumerate(records):
            if not isinstance(record, dict) or set(record) != {"finding_id", "remediation", "refs"} or record.get("finding_id") != finding.get("id"):
                continue  # The structural checker reports malformed or mismatched remediation records.
            refs = record.get("refs")
            if not isinstance(refs, list):
                continue
            for ref_index, ref in enumerate(refs):
                if not isinstance(ref, dict) or set(ref) != {"path", "blob_sha", "anchor_kind", "anchor"}:
                    continue  # The structural checker reports malformed refs.
                path = ref["path"]
                label = f"finding {index} remediation {record_index} evidence ref {ref_index}"
                if path == report_path or ref["blob_sha"] == report_blob_sha:
                    errors.append(f"{label} cannot cite the review report itself or a byte-identical copy")
                    continue
                try:
                    raw = git_regular_blob(root, head, path)
                    if blob_sha(raw) != ref["blob_sha"]:
                        errors.append(f"{label} blob is not pinned to the exact review HEAD")
                        continue
                    anchor = ref["anchor"]
                    if ref["anchor_kind"] == "JSON_POINTER":
                        if not anchor.startswith("/"):
                            raise ValueError("JSON evidence anchor must be a non-root RFC 6901 pointer")
                        json_pointer(json.loads(raw), anchor)
                    elif ref["anchor_kind"] == "TEXT_LITERAL":
                        if anchor.encode("utf-8") not in raw:
                            errors.append(f"{label} text anchor is absent from its pinned blob")
                except ValueError as exc:
                    if "regular tracked file" in str(exc) or "differs from its Git tree object" in str(exc):
                        errors.append(f"{label} cannot use an invalid Git tree entry: {exc}")
                    else:
                        errors.append(f"{label} anchor does not resolve in its pinned blob")
                except (subprocess.CalledProcessError, OSError, KeyError, TypeError, IndexError):
                    errors.append(f"{label} anchor does not resolve in its pinned blob")
    return errors


def verify_audit_evidence(root: Path, head: str, phase: str, role: str, entry: dict[str, Any]) -> list[str]:
    ref = entry.get("report_ref", {})
    path = ref.get("path")
    if not isinstance(path, str) or not path.startswith(DELIVERABLES + "/") or ".." in Path(path).parts:
        return [f"{role} review must reference a tracked report inside deliverables"]
    try:
        raw = git_regular_blob(root, head, path)
        if blob_sha(raw) != ref.get("blob_sha"):
            return [f"{role} review report blob is not verified at the pinned HEAD"]
        report = json.loads(raw)
    except json.JSONDecodeError:
        return [f"{role} review report cannot be read at the pinned HEAD"]
    except ValueError as exc:
        if "regular tracked file" in str(exc) or "differs from its Git tree object" in str(exc):
            return [f"{role} review report has an invalid Git entry: {exc}"]
        return [f"{role} review report cannot be read at the pinned HEAD"]
    except (subprocess.CalledProcessError, OSError):
        return [f"{role} review report cannot be read at the pinned HEAD"]
    errors = []
    if report.get("phase") != phase or report.get("review_role") != role:
        errors.append(f"{role} report does not identify this exact phase and review role")
    if report.get("reviewer_id") != entry.get("reviewer_id") or report.get("reviewer_id") == report.get("author_id"):
        errors.append(f"{role} report lacks a distinct reviewer identity")
    acceptable = GATE_OK | ({"NOT_APPLICABLE"} if phase == "D10" and role == "literary" else set())
    if report.get("result") != entry.get("status") or report.get("result") not in acceptable:
        errors.append(f"{role} report result does not support its declared gate")
    if report.get("result") in GATE_OK:
        errors.extend(f"{role} {item}" for item in passing_audit_findings_safe(report))
        errors.extend(f"{role} {item}" for item in verify_resolution_evidence_refs(root, head, path, report))
    elif not isinstance(report.get("findings"), list):
        errors.append(f"{role} report must include an explicit findings list")
    return errors


def verify_test_report(root: Path, head: str, phase: str, ref: dict[str, Any]) -> list[str]:
    path = ref.get("path")
    if not isinstance(path, str) or not path.startswith(DELIVERABLES + "/") or ".." in Path(path).parts:
        return ["validation must reference a tracked test report inside deliverables"]
    try:
        raw = git_regular_blob(root, head, path)
        if blob_sha(raw) != ref.get("blob_sha"):
            return ["test report blob is not verified at pinned HEAD"]
        report = json.loads(raw)
        catalog = json.loads((BASE / "D10_HARDENING_TESTS_V002.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["test report cannot be read at pinned HEAD"]
    except ValueError as exc:
        if "regular tracked file" in str(exc) or "differs from its Git tree object" in str(exc):
            return [f"test report has an invalid Git entry: {exc}"]
        return ["test report cannot be read at pinned HEAD"]
    except (subprocess.CalledProcessError, OSError):
        return ["test report cannot be read at pinned HEAD"]
    expected_ids = [case["id"] for case in catalog["test_cases"]]
    tests = report.get("tests", [])
    errors = []
    if report.get("phase") != phase or report.get("status") != "PASS":
        errors.append("test report is not a passing report for this exact phase")
    if [case.get("id") for case in tests] != expected_ids or any(case.get("result") != "PASS" for case in tests):
        errors.append("test report does not contain the exact executable catalog with all cases passing")
    if report.get("catalog_matches_runner") is not True:
        errors.append("test runner did not confirm exact catalog-to-assertion alignment")
    if report.get("passed") != len(expected_ids) or report.get("total") != len(expected_ids):
        errors.append("test report totals do not match the executable catalog")
    return errors


def validate_final_gates(root: Path, head: str, expected_master_head: str, prior: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(prior) != {f"D{i:02d}" for i in range(1, 12)}:
        return ["D12 requires evidence refs for every handoff D01 through D11"]
    for phase, ref in prior.items():
        _, phase_errors = resolve_handoff_gate(root, head, phase, ref)
        errors.extend(phase_errors)
    pending, queue_errors = collect_pending_approvals(root, head, expected_master_head)
    errors.extend(queue_errors)
    if pending:
        errors.append("D12 remains pending while player approval queues are unresolved or contain unverified terminal statuses")
    return errors


def validate_prior_handoff(root: Path, head: str, phase: str, ref: dict[str, Any]) -> list[str]:
    prior_phase = f"D{int(phase[1:])-1:02d}"
    if phase == "D05":
        prior_phase = "D04"
    if phase not in {f"D{i:02d}" for i in range(5, 13)}:
        return []
    _, errors = resolve_handoff_gate(root, head, prior_phase, ref)
    return errors


def validate_phase_envelope_v2(
    envelope: dict[str, Any], root: Path, source_head: str, expected_input_head: str, expected_master_head: str
) -> list[str]:
    schema_path = BASE / "D10_PHASE_ENVELOPE_SCHEMA_V002.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    from jsonschema import Draft202012Validator
    errors = [e.message for e in Draft202012Validator(schema).iter_errors(envelope)]
    phase = envelope.get("phase")
    gate = envelope.get("gate")
    transition = envelope.get("next_phase") is not None
    ready_gate = gate in GATE_OK
    for role in ("technical", "literary"):
        entry = envelope.get("audit", {}).get(role, {})
        errors.extend(verify_audit_evidence(root, source_head, phase, role, entry))
    errors.extend(verify_test_report(root, source_head, phase, envelope.get("validation_report_ref", {})))
    if ready_gate or transition or phase == "D12":
        for role, entry in envelope.get("audit", {}).items():
            acceptable = GATE_OK | ({"NOT_APPLICABLE"} if phase == "D10" and role == "literary" else set())
            if entry.get("status") not in acceptable:
                errors.append(f"{role} review is not complete")
        record_errors = verify_publication(envelope.get("publication_record", {}), root, expected_input_head, expected_master_head)
        errors.extend(f"publication: {e}" for e in record_errors)
        errors.extend(validate_prior_handoff(root, source_head, phase, envelope.get("previous_handoff_ref", {})))
    if phase == "D12" and ready_gate:
        errors.extend(validate_final_gates(root, source_head, expected_master_head, envelope.get("prior_phase_gates", {})))
    if phase == "D12" and gate == "PENDING_PLAYER_APPROVAL":
        prior = envelope.get("prior_phase_gates", {})
        if set(prior) != {f"D{i:02d}" for i in range(1, 12)}:
            errors.append("D12 pending envelope still requires evidence refs for every prior handoff")
        else:
            for prior_phase, ref in prior.items():
                _, phase_errors = resolve_handoff_gate(root, source_head, prior_phase, ref)
                errors.extend(phase_errors)
        pending, queue_errors = collect_pending_approvals(root, source_head, expected_master_head)
        errors.extend(queue_errors)
        if not pending:
            errors.append("PENDING_PLAYER_APPROVAL requires at least one unresolved source-backed approval")
    if envelope.get("narrator_ready") is not False:
        errors.append("D10 proposal cannot grant narrator readiness")
    if transition:
        expected = {f"D{i:02d}": f"D{i+1:02d}" for i in range(5, 12)}.get(phase)
        if envelope.get("next_phase") != expected or gate not in GATE_OK:
            errors.append("phase transition must advance exactly one gate-approved step")
    return errors


def self_test(report_path: Path | None = None) -> int:
    tests: list[tuple[str, Any]] = []
    def check(name: str, fn: Any) -> None:
        try:
            fn()
            tests.append((name, "PASS"))
        except Exception as exc:
            tests.append((name, f"FAIL: {exc}"))
    with tempfile.TemporaryDirectory(prefix="novydres-d10-v2-") as temp:
        root = Path(temp) / "repo"
        remote = Path(temp) / "remote.git"
        root.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "master", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "D10 Fixture"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
        cycle_dir = root / CYCLE_DIR
        cycle_dir.mkdir(parents=True)
        cycle = {"sequence": 1, "checkpoint": {"last_event_id": "E1"}, "refs": {"knowledge": {"path": "evidence/ledger.json", "blob_sha": ""}}}
        approval_request = {"id": "A1", "decision": "Approve request A."}
        request_hash = approval_request_sha256(approval_request)
        assert request_hash
        ledger = {"acquisitions": [{"record_type": "ACQUISITION", "acquisition_id": "A1", "knower_id": "N1", "event_id": "E1", "method": "OBSERVED", "evidence_id": "EV1", "fact_ref": "F1"}], "decisions": [{"record_type": "PLAYER_DECISION", "decision_id": "P1", "decision_maker": "PLAYER", "decision_kind": "RETCON_APPROVAL", "scope": "EXACT_RETCON", "affected_refs": ["R1"], "event_id": "E1", "evidence_id": "EV1"}, {"record_type": "PLAYER_DECISION", "decision_id": "A1", "decision_maker": "PLAYER", "decision_kind": "PLAYER_APPROVAL_GRANTED", "scope": "APPROVAL_RESOLUTION:A1", "affected_refs": ["approval:A1"], "event_id": "E1", "evidence_id": "EV2", "approval_request_sha256": request_hash}], "events": [{"record_type": "CANON_EVENT", "event_id": "E1"}], "links": [{"record_type": "CAUSAL_LINK", "from_id": "PLOT1", "to_id": "PLOT2", "kind": "CAUSAL"}]}
        ledger_path = root / "evidence/ledger.json"
        ledger_path.parent.mkdir(parents=True)
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        cycle["refs"]["knowledge"]["blob_sha"] = blob_sha(ledger_path.read_bytes())
        queue_path = root / DELIVERABLES / "D05_PLAYER_APPROVAL_QUEUE_V001.json"
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        queue_path.write_text(json.dumps({"decisions":[{**approval_request,"status":"PENDING_PLAYER_APPROVAL"}]}),encoding="utf-8")
        inherited_queue = root / DELIVERABLES / "D06_PLAYER_APPROVAL_QUEUE_V001.json"
        inherited_queue.write_text(json.dumps({"decisions":[{**approval_request}]}),encoding="utf-8")
        resolution_evidence_path = root / DELIVERABLES / "D10_REVIEW_EVIDENCE_FIXTURE.json"
        resolution_evidence_path.write_text('{"checks":[{"id":"fix-1","status":"PASS"}]}\n', encoding="utf-8")
        resolution_evidence_copy = root / DELIVERABLES / "D10_REVIEW_EVIDENCE_COPY_FIXTURE.json"
        resolution_evidence_copy.write_bytes(resolution_evidence_path.read_bytes())
        resolution_evidence_symlink = root / DELIVERABLES / "D10_REVIEW_EVIDENCE_SYMLINK_FIXTURE.json"
        resolution_evidence_symlink.symlink_to(resolution_evidence_path.name)
        regular_report_fixture = root / DELIVERABLES / "D10_REGULAR_REPORT_FIXTURE.json"
        test_catalog = json.loads((BASE / "D10_HARDENING_TESTS_V002.json").read_text(encoding="utf-8"))
        test_ids = [case["id"] for case in test_catalog["test_cases"]]
        regular_report = {
            "phase": "D10",
            "review_role": "adversarial",
            "reviewer_id": "independent",
            "author_id": "author",
            "result": "PASS_WITH_UNKNOWN",
            "findings": [],
            "status": "PASS",
            "tests": [{"id": case_id, "result": "PASS"} for case_id in test_ids],
            "catalog_matches_runner": True,
            "passed": len(test_ids),
            "total": len(test_ids),
            "gate": "PASS_WITH_UNKNOWN",
        }
        regular_report_fixture.write_text(json.dumps(regular_report) + "\n", encoding="utf-8")
        audit_report_symlink = root / DELIVERABLES / "D10_ADVERSARIAL_REVIEW_V002.json"
        audit_report_symlink.symlink_to(regular_report_fixture.name)
        test_report_symlink = root / DELIVERABLES / "D10_TEST_RESULTS_V002.json"
        test_report_symlink.symlink_to(regular_report_fixture.name)
        regular_handoff = root / HANDOFFS["D05"]
        regular_handoff.parent.mkdir(parents=True, exist_ok=True)
        regular_handoff.write_text('{"gate":"PASS_WITH_UNKNOWN"}\n', encoding="utf-8")
        cyc_path = cycle_dir / "CYCLE_V0001.json"
        cyc_path.write_text(json.dumps(cycle), encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)
        regular_head = run(root, "rev-parse", "HEAD")
        regular_handoff.unlink()
        regular_handoff.symlink_to(regular_report_fixture.name)
        subprocess.run(["git", "-C", str(root), "add", HANDOFFS["D05"]], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "symlink handoff fixture"], check=True)
        master = run(root, "rev-parse", "HEAD")
        remote.mkdir()
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
        subprocess.run(["git", "-C", str(root), "push", "-q", "origin", "master"], check=True)
        subprocess.run(["git", "-C", str(root), "fetch", "-q", "origin"], check=True)
        path, sha, cycle_doc = latest_cycle(root, master)
        good_ref = {"path": "evidence/ledger.json", "blob_sha": tree_blob(root, master, "evidence/ledger.json"), "json_pointer": "/acquisitions/0", "anchor": "/acquisitions/0", "verification": "VERIFIED"}
        def source_symlink_sha(path: Path) -> str:
            return tree_blob(root, master, path.relative_to(root).as_posix())
        regular_report_sha = source_symlink_sha(regular_report_fixture)
        regular_handoff_ref = {"path": HANDOFFS["D05"], "blob_sha": tree_blob(root, regular_head, HANDOFFS["D05"])}
        regular_audit_ref = {"reviewer_id": "independent", "status": "PASS_WITH_UNKNOWN", "report_ref": {"path": regular_report_fixture.relative_to(root).as_posix(), "blob_sha": regular_report_sha}}
        regular_test_ref = {"path": regular_report_fixture.relative_to(root).as_posix(), "blob_sha": regular_report_sha}
        def assert_regular_then_symlink_rejected(label: str, verify_regular: Any, regular_ref: dict[str, Any], verify_symlink: Any, symlink_ref: dict[str, Any], symlink_path: str) -> None:
            regular_errors = verify_regular(regular_ref)
            if regular_errors:
                raise AssertionError(f"valid regular {label} report rejected: {regular_errors}")
            try:
                git_regular_blob(root, master, symlink_path)
            except ValueError as exc:
                if "regular tracked file" not in str(exc):
                    raise AssertionError(f"{label} fixture failed for an unrelated tree-entry reason: {exc}") from exc
            else:
                raise AssertionError(f"{label} symlink passed the Git regular-file check")
            symlink_errors = verify_symlink(symlink_ref)
            if not any("regular tracked file" in error for error in symlink_errors):
                raise AssertionError(f"{label} consumer did not reject the Git tree mode: {symlink_errors}")
        regular_handoff_verify = lambda ref: resolve_handoff_gate(root, regular_head, "D05", ref)[1]
        symlink_handoff_verify = lambda ref: resolve_handoff_gate(root, master, "D05", ref)[1]
        audit_verify = lambda ref: verify_audit_evidence(root, master, "D10", "adversarial", ref)
        test_verify = lambda ref: verify_test_report(root, master, "D10", ref)
        check("handoff gate rejects a symlink document", lambda: assert_regular_then_symlink_rejected("handoff", regular_handoff_verify, regular_handoff_ref, symlink_handoff_verify, {"path": HANDOFFS["D05"], "blob_sha": tree_blob(root, master, HANDOFFS["D05"])}, HANDOFFS["D05"]))
        check("audit evidence rejects a symlink report", lambda: assert_regular_then_symlink_rejected("audit", audit_verify, regular_audit_ref, audit_verify, {"reviewer_id": "independent", "status": "PASS_WITH_UNKNOWN", "report_ref": {"path": audit_report_symlink.relative_to(root).as_posix(), "blob_sha": source_symlink_sha(audit_report_symlink)}}, audit_report_symlink.relative_to(root).as_posix()))
        check("test evidence rejects a symlink report", lambda: assert_regular_then_symlink_rejected("test", test_verify, regular_test_ref, test_verify, {"path": test_report_symlink.relative_to(root).as_posix(), "blob_sha": source_symlink_sha(test_report_symlink)}, test_report_symlink.relative_to(root).as_posix()))
        check("event IDs derive from latest master checkpoint", lambda: (_ for _ in ()).throw(AssertionError("derived cursor rejected")) if not event_ids_match_cycle({"event_ids":["E1"]}, cycle_doc) else None)
        check("fabricated or older event IDs are rejected", lambda: (_ for _ in ()).throw(AssertionError("caller event IDs accepted")) if event_ids_match_cycle({"event_ids":["E1","E2"]}, cycle_doc) or event_ids_match_cycle({"event_ids":["E0"]}, cycle_doc) else None)
        check("exact acquisition source binds actor/event/method/fact", lambda: (_ for _ in ()).throw(AssertionError(verify_semantic_ref(root, master, cycle_doc, good_ref, "ACQUISITION", {"acquisition_id":"A1","knower_id":"N1","event_id":"E1","method":"OBSERVED","evidence_id":"EV1","fact_ref":"F1"}))) if verify_semantic_ref(root, master, cycle_doc, good_ref, "ACQUISITION", {"acquisition_id":"A1","knower_id":"N1","event_id":"E1","method":"OBSERVED","evidence_id":"EV1","fact_ref":"F1"}) else None)
        check("mismatched acquisition claim is rejected", lambda: (_ for _ in ()).throw(AssertionError("mismatch accepted")) if not verify_semantic_ref(root, master, cycle_doc, good_ref, "ACQUISITION", {"acquisition_id":"A1","knower_id":"OTHER","event_id":"E1","method":"OBSERVED","evidence_id":"EV1","fact_ref":"F1"}) else None)
        decision_ref = {**good_ref,"json_pointer":"/decisions/0","anchor":"/decisions/0"}
        check("exact player-decision authority is source-bound", lambda: (_ for _ in ()).throw(AssertionError(verify_semantic_ref(root, master, cycle_doc, decision_ref, "PLAYER_DECISION", {"decision_id":"P1","decision_maker":"PLAYER","decision_kind":"RETCON_APPROVAL","scope":"EXACT_RETCON","affected_refs":["R1"],"event_id":"E1","evidence_id":"EV1"}))) if verify_semantic_ref(root, master, cycle_doc, decision_ref, "PLAYER_DECISION", {"decision_id":"P1","decision_maker":"PLAYER","decision_kind":"RETCON_APPROVAL","scope":"EXACT_RETCON","affected_refs":["R1"],"event_id":"E1","evidence_id":"EV1"}) else None)
        check("event claims require exact event source record", lambda: (_ for _ in ()).throw(AssertionError(verify_semantic_ref(root, master, cycle_doc, {**good_ref,"json_pointer":"/events/0","anchor":"/events/0"}, "CANON_EVENT", {"event_id":"E1"}))) if verify_semantic_ref(root, master, cycle_doc, {**good_ref,"json_pointer":"/events/0","anchor":"/events/0"}, "CANON_EVENT", {"event_id":"E1"}) else None)
        check("causal links require exact typed source record", lambda: (_ for _ in ()).throw(AssertionError(verify_semantic_ref(root, master, cycle_doc, {**good_ref,"json_pointer":"/links/0","anchor":"/links/0"}, "CAUSAL_LINK", {"from_id":"PLOT1","to_id":"PLOT2","kind":"CAUSAL"}))) if verify_semantic_ref(root, master, cycle_doc, {**good_ref,"json_pointer":"/links/0","anchor":"/links/0"}, "CAUSAL_LINK", {"from_id":"PLOT1","to_id":"PLOT2","kind":"CAUSAL"}) else None)
        bad_ref = {**good_ref, "path": "test/unreferenced.json"}
        check("unreferenced generic fixture is rejected", lambda: (_ for _ in ()).throw(AssertionError("unreferenced source accepted")) if not verify_semantic_ref(root, master, cycle_doc, bad_ref, "ACQUISITION", {}) else None)
        check("source blob differing from exact cycle ref is rejected", lambda: (_ for _ in ()).throw(AssertionError("cycle-pinned blob mismatch accepted")) if not verify_semantic_ref(root, master, cycle_doc, {**good_ref,"blob_sha":"0"*40}, "ACQUISITION", {}) else None)

        # Build a real, non-forced documentary publication on the local bare remote.
        subprocess.run(["git", "-C", str(root), "checkout", "-qb", BRANCH], check=True)
        subprocess.run(["git", "-C", str(root), "push", "-q", "origin", f"HEAD:refs/heads/{BRANCH}"], check=True)
        target = root / DELIVERABLES / "D10_FIXTURE_V001.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('{"fixture":true}\n', encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(target.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture publication"], check=True)
        commit = run(root, "rev-parse", "HEAD")
        subprocess.run(["git", "-C", str(root), "push", "-q", "origin", f"HEAD:refs/heads/{BRANCH}"], check=True)
        subprocess.run(["git", "-C", str(root), "fetch", "-q", "origin"], check=True)
        record = {"remote":"origin","target_branch":BRANCH,"force_push":False,"commit":commit,"input_head":master,"master_head":master,"remote_head_after":commit,"tree":run(root,"rev-parse",f"{commit}^{{tree}}"),"artifacts":[{"path":target.relative_to(root).as_posix(),"blob_sha":tree_blob(root,commit,target.relative_to(root).as_posix())}]}
        check("real remote commit/tree/blob/content readback passes", lambda: (_ for _ in ()).throw(AssertionError(verify_publication(record, root, master, master))) if verify_publication(record, root, master, master) else None)
        check("synthetic commit SHA is rejected", lambda: (_ for _ in ()).throw(AssertionError("fake SHA accepted")) if not verify_publication({**record,"commit":"a"*40}, root, master, master) else None)
        check("fabricated blob SHA is rejected", lambda: (_ for _ in ()).throw(AssertionError("fake blob accepted")) if not verify_publication({**record,"artifacts":[{"path":target.relative_to(root).as_posix(),"blob_sha":"b"*40}]}, root, master, master) else None)
        check("master target is rejected", lambda: (_ for _ in ()).throw(AssertionError("master accepted")) if not verify_publication({**record,"target_branch":"master"}, root, master, master) else None)
        check("caller booleans cannot substitute for artifact manifest", lambda: (_ for _ in ()).throw(AssertionError("boolean-only publication accepted")) if not verify_publication({**record,"artifacts":[],"readback":{"all_contents_match":True}}, root, master, master) else None)
        check("handoff enum without pinned source is rejected", lambda: (_ for _ in ()).throw(AssertionError("status enum accepted")) if not resolve_handoff_gate(root, commit, "D05", {"path":HANDOFFS["D05"],"blob_sha":"c"*40})[1] else None)
        pending, approval_errors = collect_pending_approvals(root, commit, master)
        check("duplicated pending approval remains unresolved", lambda: (_ for _ in ()).throw(AssertionError(f"pending approval not preserved: {pending}; {approval_errors}")) if not any(item.startswith("A1:") for item in pending) or approval_errors else None)
        divergent_pending = root / DELIVERABLES / "D13_PLAYER_APPROVAL_QUEUE_V001.json"
        divergent_pending.write_text(json.dumps({"decisions":[{**approval_request,"request_prompt":"This copy refers to a different approval scope."}]}), encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(divergent_pending.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "divergent request fixture"], check=True)
        divergent_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, divergent_head, master)
        check("divergent repeated approval requests remain pending", lambda: (_ for _ in ()).throw(AssertionError(f"divergent requests were not held pending: {pending}; {approval_errors}")) if "A1:REQUEST_CONFLICT" not in pending or approval_errors else None)
        divergent_terminal = root / DELIVERABLES / "D14_PLAYER_APPROVAL_QUEUE_V001.json"
        approval_source = {"path":"evidence/ledger.json","blob_sha":tree_blob(root, master, "evidence/ledger.json"),"json_pointer":"/decisions/1","anchor":"/decisions/1","verification":"VERIFIED"}
        divergent_terminal.write_text(json.dumps({"decisions":[{**approval_request,"status":"APPROVED","resolution":{"status":"APPROVED","request_sha256":request_hash,"source":approval_source}}]}), encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(divergent_terminal.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "resolution against divergent request fixture"], check=True)
        divergent_terminal_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, divergent_terminal_head, master)
        check("one approval cannot clear divergent repeated request content", lambda: (_ for _ in ()).throw(AssertionError(f"approval cleared divergent request copies: {pending}; {approval_errors}")) if "A1:REQUEST_CONFLICT" not in pending or not any("cannot apply to divergent repeated request content" in error for error in approval_errors) else None)
        divergent_pending.unlink()
        divergent_terminal.unlink()
        subprocess.run(["git", "-C", str(root), "add", "-u", DELIVERABLES], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "remove divergent approval fixtures"], check=True)
        unverified_queue = root / DELIVERABLES / "D12_PLAYER_APPROVAL_QUEUE_V001.json"
        unverified_queue.write_text(json.dumps({"decisions":[{**approval_request,"status":"APPROVED"}]}),encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(unverified_queue.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "unverified queue fixture"], check=True)
        unverified_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, unverified_head, master)
        check("unverified terminal approval status is rejected", lambda: (_ for _ in ()).throw(AssertionError(f"unverified terminal status accepted: {pending}; {approval_errors}")) if not pending or not any("lacks a matching source-backed resolution" in error for error in approval_errors) else None)
        unverified_queue.write_text(json.dumps({"decisions":[{**approval_request,"status":"APPROVED","resolution":{"status":"APPROVED","request_sha256":request_hash,"source":approval_source}}]}),encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(unverified_queue.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "verified queue resolution fixture"], check=True)
        resolved_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, resolved_head, master)
        check("source-backed approval resolution supersedes duplicated pending copies", lambda: (_ for _ in ()).throw(AssertionError(f"verified resolution did not supersede pending copies: {pending}; {approval_errors}")) if pending or approval_errors else None)
        forged_queue = root / DELIVERABLES / "D13_PLAYER_APPROVAL_QUEUE_V001.json"
        forged_source = {**approval_source,"json_pointer":"/decisions/0","anchor":"/decisions/0"}
        forged_queue.write_text(json.dumps({"decisions":[{**approval_request,"status":"APPROVED","resolution":{"status":"APPROVED","request_sha256":request_hash,"source":forged_source}}]}),encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", str(forged_queue.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "forged queue resolution fixture"], check=True)
        forged_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, forged_head, master)
        check("approval resolution cannot use a different source decision", lambda: (_ for _ in ()).throw(AssertionError(f"mismatched decision source accepted: {pending}; {approval_errors}")) if not pending or not approval_errors else None)
        queue_symlink = root / DELIVERABLES / "D07_PLAYER_APPROVAL_QUEUE_V001.json"
        queue_symlink.symlink_to(queue_path.name)
        subprocess.run(["git", "-C", str(root), "add", str(queue_symlink.relative_to(root))], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "symlink approval queue fixture"], check=True)
        queue_symlink_head = run(root, "rev-parse", "HEAD")
        pending, approval_errors = collect_pending_approvals(root, queue_symlink_head, master)
        check("approval queue rejects a symlink document", lambda: (_ for _ in ()).throw(AssertionError(f"symlink queue was accepted: {pending}; {approval_errors}")) if not any(item.startswith("UNREADABLE:") for item in pending) or not approval_errors else None)
        queue_symlink.unlink()
        subprocess.run(["git", "-C", str(root), "add", "-u", DELIVERABLES], check=True)
        subprocess.run(["git", "-C", str(root), "commit", "-qm", "remove symlink approval queue fixture"], check=True)
        check("D12 rejects missing prior handoff evidence", lambda: (_ for _ in ()).throw(AssertionError("D12 passed despite missing handoffs")) if not validate_final_gates(root, commit, master, {}) else None)
        check("material review finding cannot hide under PASS", lambda: (_ for _ in ()).throw(AssertionError("open blocker finding accepted")) if not passing_audit_findings_safe({"result":"PASS","findings":[{"id":"F1","severity":"BLOCKER","disposition":"OPEN"}]}) else None)
        evidence_path = resolution_evidence_path.relative_to(root).as_posix()
        evidence_ref = {"path":evidence_path,"blob_sha":tree_blob(root, commit, evidence_path),"anchor_kind":"JSON_POINTER","anchor":"/checks/0/status"}
        remediation_record = {"finding_id":"F1","remediation":"Bind resolution to the exact request fingerprint and verified source decision.","refs":[evidence_ref]}
        valid_review = {"result":"PASS","findings":[{"id":"F1","severity":"BLOCKER","disposition":"RESOLVED","resolution_evidence":[remediation_record]}]}
        def review_evidence_is_tracked_and_pinned() -> None:
            if passing_audit_findings_safe(valid_review):
                raise AssertionError("valid typed ref failed structural checks")
            if verify_resolution_evidence_refs(root, commit, f"{DELIVERABLES}/D10_REVIEW_REPORT_FIXTURE.json", valid_review):
                raise AssertionError("tracked source blob and resolving JSON pointer were rejected")
            for bad_ref in (
                {"path":evidence_path,"blob_sha":"0"*40,"anchor_kind":"JSON_POINTER","anchor":"/checks/0/status"},
                {"path":evidence_path,"blob_sha":evidence_ref["blob_sha"],"anchor_kind":"JSON_POINTER","anchor":"/checks/99/status"},
                {"path":f"{DELIVERABLES}/D10_MISSING_FIXTURE.json","blob_sha":evidence_ref["blob_sha"],"anchor_kind":"JSON_POINTER","anchor":"/checks/0/status"},
            ):
                report = {"result":"PASS","findings":[{"id":"F1","severity":"BLOCKER","disposition":"RESOLVED","resolution_evidence":[{**remediation_record,"refs":[bad_ref]}]}]}
                if not verify_resolution_evidence_refs(root, commit, f"{DELIVERABLES}/D10_REVIEW_REPORT_FIXTURE.json", report):
                    raise AssertionError(f"unverifiable typed evidence ref accepted: {bad_ref}")
            plain_text_report = {"result":"PASS","findings":[{"id":"F1","severity":"BLOCKER","disposition":"RESOLVED","resolution_evidence":"resolved"}]}
            if not passing_audit_findings_safe(plain_text_report):
                raise AssertionError("declarative plain text resolution was accepted")
        check("resolved material finding has tracked linked remediation evidence", review_evidence_is_tracked_and_pinned)
        def remediation_record_binds_exact_finding_id() -> None:
            mismatched = json.loads(json.dumps(valid_review))
            mismatched["findings"][0]["resolution_evidence"][0]["finding_id"] = "OTHER-FINDING"
            if not passing_audit_findings_safe(mismatched):
                raise AssertionError("remediation record for a different finding was accepted")
        check("resolved evidence is bound to the exact finding ID", remediation_record_binds_exact_finding_id)
        def duplicate_review_finding_ids_are_rejected() -> None:
            duplicated = json.loads(json.dumps(valid_review))
            second = json.loads(json.dumps(duplicated["findings"][0]))
            second["summary"] = "A distinct blocker with a different issue but a reused stable ID."
            duplicated["findings"].append(second)
            errors = passing_audit_findings_safe(duplicated)
            if not any("duplicates finding id 'F1'" in error for error in errors):
                raise AssertionError(f"duplicate stable finding ID was accepted: {errors}")
        check("duplicate review finding IDs are rejected", duplicate_review_finding_ids_are_rejected)
        def review_evidence_rejects_self_copy_and_missing_paths() -> None:
            same_path = json.loads(json.dumps(valid_review))
            same_path["findings"][0]["resolution_evidence"][0]["refs"][0]["path"] = evidence_path
            if not verify_resolution_evidence_refs(root, commit, evidence_path, same_path):
                raise AssertionError("review report self-reference by path was accepted")
            copy_path = resolution_evidence_copy.relative_to(root).as_posix()
            copied_blob = json.loads(json.dumps(valid_review))
            copied_blob["findings"][0]["resolution_evidence"][0]["refs"][0]["path"] = copy_path
            if not verify_resolution_evidence_refs(root, commit, evidence_path, copied_blob):
                raise AssertionError("byte-identical review report copy was accepted")
        check("review evidence rejects report self-copy", review_evidence_rejects_self_copy_and_missing_paths)
        def review_evidence_rejects_symlink_tree_entries() -> None:
            symlink_path = resolution_evidence_symlink.relative_to(root).as_posix()
            symlink_ref = {
                "path": symlink_path,
                "blob_sha": tree_blob(root, commit, symlink_path),
                "anchor_kind": "TEXT_LITERAL",
                "anchor": resolution_evidence_path.name,
            }
            report = {"result":"PASS","findings":[{"id":"F1","severity":"BLOCKER","disposition":"RESOLVED","resolution_evidence":[{**remediation_record,"refs":[symlink_ref]}]}]}
            errors = verify_resolution_evidence_refs(root, commit, f"{DELIVERABLES}/D10_REVIEW_REPORT_FIXTURE.json", report)
            if not any("regular tracked file" in error for error in errors):
                raise AssertionError(f"symlink tree entry was accepted as document evidence: {errors}")
        check("review evidence rejects symlink tree entries", review_evidence_rejects_symlink_tree_entries)
        def rfc6901_rejects_noncanonical_array_and_escape_segments() -> None:
            fixture = json.loads(resolution_evidence_path.read_text(encoding="utf-8"))
            for pointer in ("/checks/-1/status", "/checks/00/status", "/checks/0/status~2"):
                try:
                    json_pointer(fixture, pointer)
                except (ValueError, IndexError, KeyError):
                    continue
                raise AssertionError(f"non-RFC JSON pointer was accepted: {pointer}")
        check("RFC 6901 rejects invalid array indexes and escapes", rfc6901_rejects_noncanonical_array_and_escape_segments)
        acquisitions = {"A1":{"acquisition_id":"A1","fact_ref":"F1"}}
        check("knowledge fact matches its acquisition", lambda: (_ for _ in ()).throw(AssertionError("matching fact was rejected")) if not knowledge_fact_matches_acquisition({"acquisition_ref":"A1","fact_ref":"F1"}, acquisitions) else None)
        check("knowledge cannot claim a different acquired fact", lambda: (_ for _ in ()).throw(AssertionError("different fact was accepted")) if knowledge_fact_matches_acquisition({"acquisition_ref":"A1","fact_ref":"F2"}, acquisitions) else None)
        cli_input = Path(temp) / "invalid-cli-input.json"
        cli_input.write_text("{}\n", encoding="utf-8")
        def cli_rejects(mode: str) -> None:
            result = subprocess.run([sys.executable, str(BASE / "D10_VALIDATE_V002.py"), "--repo-root", str(root), "--expected-source-head", commit, "--expected-master-head", master, mode, str(cli_input)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = json.loads(result.stdout.decode("utf-8"))
            if result.returncode != 1 or output.get("status") != "FAIL" or not output.get("errors"):
                raise AssertionError(f"CLI mode {mode} did not execute and fail closed: rc={result.returncode}; stderr={result.stderr.decode('utf-8')}")
        check("CLI bundle mode runs and fails closed", lambda: cli_rejects("--bundle"))
        check("CLI envelope mode runs and fails closed", lambda: cli_rejects("--envelope"))
        check("CLI publication mode runs and fails closed", lambda: cli_rejects("--publication-record"))
        valid_record = Path(temp) / "valid-publication-record.json"
        valid_record.write_text(json.dumps(record), encoding="utf-8")
        def cli_accepts_publication() -> None:
            result = subprocess.run(
                [sys.executable, str(BASE / "D10_VALIDATE_V002.py"), "--repo-root", str(root),
                 "--expected-source-head", commit, "--expected-input-head", master,
                 "--expected-master-head", master, "--publication-record", str(valid_record)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            output = json.loads(result.stdout.decode("utf-8"))
            if result.returncode != 0 or output.get("status") != "PASS_WITH_UNKNOWN" or output.get("errors"):
                raise AssertionError(f"CLI publication mode rejected valid readback: rc={result.returncode}; output={output}; stderr={result.stderr.decode('utf-8')}")
        check("CLI publication mode accepts a verified readback", cli_accepts_publication)
        def publication_rejects_symlink_artifact() -> None:
            input_head = run(root, "rev-parse", "HEAD")
            subprocess.run(["git", "-C", str(root), "push", "-q", "origin", f"HEAD:refs/heads/{BRANCH}"], check=True)
            symlink_artifact = root / DELIVERABLES / "D10_PUBLISHED_SYMLINK_FIXTURE.json"
            symlink_artifact.symlink_to(target.name)
            subprocess.run(["git", "-C", str(root), "add", str(symlink_artifact.relative_to(root))], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "symlink publication fixture"], check=True)
            symlink_commit = run(root, "rev-parse", "HEAD")
            subprocess.run(["git", "-C", str(root), "push", "-q", "origin", f"HEAD:refs/heads/{BRANCH}"], check=True)
            subprocess.run(["git", "-C", str(root), "fetch", "-q", "origin"], check=True)
            symlink_record = {"remote":"origin","target_branch":BRANCH,"force_push":False,"commit":symlink_commit,"input_head":input_head,"master_head":master,"remote_head_after":symlink_commit,"tree":run(root,"rev-parse",f"{symlink_commit}^{{tree}}"),"artifacts":[{"path":symlink_artifact.relative_to(root).as_posix(),"blob_sha":tree_blob(root,symlink_commit,symlink_artifact.relative_to(root).as_posix())}]}
            errors = verify_publication(symlink_record, root, input_head, master)
            if not any("not a regular tracked file" in error for error in errors):
                raise AssertionError(f"symlink publication artifact was accepted: {errors}")
        check("publication readback rejects a symlink artifact", publication_rejects_symlink_artifact)

    catalog_matches = False
    try:
        catalog = json.loads((BASE / "D10_HARDENING_TESTS_V002.json").read_text(encoding="utf-8"))
        expected_ids = [case["id"] for case in catalog["test_cases"]]
        actual_ids = [name for name, _ in tests]
        catalog_matches = expected_ids == actual_ids
    except (OSError, KeyError, json.JSONDecodeError):
        catalog_matches = False
    for name, result in tests:
        print(f"{name}: {result}")
    failed = sum(not result.startswith("PASS") for _, result in tests) + (0 if catalog_matches else 1)
    if not catalog_matches:
        print("CATALOG ALIGNMENT: FAIL")
    print(f"RESULT {len(tests)-failed}/{len(tests)}; gate={'PASS_WITH_UNKNOWN' if not failed else 'FAIL'}")
    if report_path:
        report_path.write_text(json.dumps({"phase":"D10","status":"PASS" if not failed else "FAIL","passed":len(tests)- (0 if catalog_matches else 1),"total":len(tests),"catalog_matches_runner":catalog_matches,"tests":[{"id":name,"result":"PASS" if result == "PASS" else "FAIL","detail":None if result == "PASS" else result} for name,result in tests]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--expected-source-head")
    parser.add_argument("--expected-input-head")
    parser.add_argument("--expected-master-head")
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--publication-record", type=Path)
    parser.add_argument("--envelope", type=Path)
    parser.add_argument("--report-out", type=Path)
    args = parser.parse_args()
    if args.self_test:
        return self_test(args.report_out)
    if not args.repo_root or not args.expected_source_head or not args.expected_master_head:
        parser.error("verified repository root, source HEAD, and master HEAD are required")
    if args.publication_record:
        errors = verify_publication(json.loads(args.publication_record.read_text()), args.repo_root, args.expected_input_head or args.expected_source_head, args.expected_master_head)
    elif args.envelope:
        errors = validate_phase_envelope_v2(json.loads(args.envelope.read_text()), args.repo_root, args.expected_source_head, args.expected_input_head or args.expected_source_head, args.expected_master_head)
    elif args.bundle:
        errors = validate_bundle_v2(json.loads(args.bundle.read_text()), args.repo_root, args.expected_source_head, args.expected_master_head)
    else:
        parser.error("choose --bundle or --publication-record")
    print(json.dumps({"status":"FAIL" if errors else "PASS_WITH_UNKNOWN","errors":errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
