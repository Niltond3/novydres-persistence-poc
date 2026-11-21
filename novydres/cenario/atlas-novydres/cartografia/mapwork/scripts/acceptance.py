#!/usr/bin/env python3
"""Fail-closed, hash-bound semantic+deterministic acceptance for Mapwork .

This module NEVER generates images or pretends to inspect them. The external
host agent must render and visually inspect each full-reference candidate,
record FAIL/PASS evidence, repair failed stages, and re-invoke pipeline.py.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image

import infra_checks as infra
import orchestration as controller

STAGES = (
    "INF-01", "INF-02", "INF-03", "INF-04",
    "INF-05", "INF-06", "INF-07", "URB-08"
)
SCHEMA = "NOVYDRES_MAPWORK_ACCEPTANCE_LEDGER"
ROOT = Path(__file__).resolve().parents[1]
CRITERIA_DOC = ROOT / "docs" / "infra-acceptance.md"
_HEX = re.compile(r"^[0-9a-f]{64}$")


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def criteria_contract(doc_path=CRITERIA_DOC):
    """The Markdown is the binding source of rule IDs; Python never forks it."""
    raw = Path(doc_path).read_text(encoding="utf-8")
    stages = tuple(re.findall(r"^### ((?:INF|URB)-\d{2})\b", raw, re.M))
    if stages != STAGES:
        raise ValueError("acceptance Markdown has missing/reordered infrastructure stages")
    result = {}
    for stage in STAGES:
        rule_ids = tuple(re.findall(
            r"^- \[ \] \x60(" + re.escape(stage) + r"\.\d{2})\x60", raw, re.M
        ))
        if len(rule_ids) != 4 or len(set(rule_ids)) != len(rule_ids):
            raise ValueError(stage + ": acceptance Markdown must define 4 unique criteria")
        result[stage] = rule_ids
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", raw, re.S)
    profiles = [json.loads(s) for s in matches if
                '"NOVYDRES_MAPWORK_SPATIAL_PROFILE"' in s]
    if len(profiles) != 1 or set(profiles[0]["stage_modes"]) != set(STAGES):
        raise ValueError("Markdown executable spatial acceptance profile absent")
    return {"stages": result, "sha256": sha_file(doc_path),"profile":profiles[0]}


def _stage(stage, action, blockers, *, iteration=0, accepted=(), latest=None):
    invalid = {"REPAIR_UNVERIFIED_CANDIDATE", "REPAIR_AND_REGENERATE", "REPLAN_STAGE",
               "REPAIR_DIAGNOSTIC_AND_REGENERATE",
               "REGENERATE_DIFFERENT_CANDIDATE", "REPAIR_ACCEPTANCE_LEDGER",
               "REASSESS_METHOD",
               "INVALIDATE_AND_REAUDIT_STALE_EVIDENCE"}
    return {
        "status": "PASS" if action == "ADVANCE_AFTER_ACCEPTANCE" else
                  "FAIL" if action in invalid else "BLOCKED",
        "stage": stage,
        "next_action": action,
        "blockers": list(blockers),
        "attempts": iteration,
        "accepted_stages": list(accepted),
        "latest": latest,
        "allows_lots": action == "ADVANCE_AFTER_ACCEPTANCE" and stage == "INF-07",
    }


def _verify_artifact(path_value, digest_value, *, base, image=False,
                     source_sha256=None, expected_size=None, stage=None):
    if not isinstance(path_value, str) or not path_value.strip():
        return "artifact path absent"
    if not isinstance(digest_value, str) or not _HEX.fullmatch(digest_value):
        return "artifact SHA-256 absent or invalid"
    p = Path(path_value)
    if not p.is_absolute():
        p = base / p
    if not p.is_file() or not p.is_file():
        return "artifact bytes not materialized: " + path_value
    if sha_file(p) != digest_value:
        return "artifact SHA-256 differs from actual bytes: " + path_value
    if image:
        if digest_value == source_sha256:
            return "candidate is identical to approved reference"
        try:
            with Image.open(p) as im:
                if im.size != tuple(expected_size or ()):
                    return "candidate preview is not full reference dimensions"
                im.verify()
        except (OSError, SyntaxError, ValueError) as exc:
            return "candidate preview is not a valid image: " + str(exc)
    else:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(obj, dict):
                return "candidate geometry must be a JSON object"
            if obj.get("stage") != stage or obj.get("source_sha256") != source_sha256:
                return "candidate geometry stage/reference not bound"
            if not any(bool(obj.get(k)) for k in (
                    "transport", "territory", "vector_corridors",
                    "features", "network", "layers")):
                return "candidate geometry has no actual spatial objects"
        except (OSError, ValueError, UnicodeError) as exc:
            return "candidate geometry cannot be read as JSON: " + str(exc)
    return None


def evaluate(ledger_path, *, reference_file, reference_sha256, reference_size,
             require_urban=False, require_remote=False, criteria_path=CRITERIA_DOC,
             expected_target=None):
    """Read most recent attempt for each stage, in mandatory dependency order.

    No record, stale file, fabricated hash, missing check or FAIL can authorize
    downstream planning. Failed attempts trigger agent repair, not owner review.
    """
    try:
        spec = criteria_contract(criteria_path)
    except (OSError, ValueError) as exc:
        return _stage("INF-01", "FIX_ACCEPTANCE_CONTRACT", [str(exc)])
    required = STAGES if require_urban else STAGES[:-1]
    expected_size = tuple(reference_size)
    if not isinstance(reference_sha256, str) or not _HEX.fullmatch(reference_sha256):
        return _stage(required[0], "RESTORE_REFERENCE_AUTHORITY",
                      ["approved reference SHA-256 missing"])
    if not reference_file or not Path(reference_file).is_file():
        return _stage(required[0], "MATERIALIZE_ORIGINAL_REFERENCE",
                      ["U02 PNG must be local for self-review"])
    if sha_file(reference_file) != reference_sha256:
        return _stage(required[0], "RESTORE_ORIGINAL_REFERENCE",
                      ["reference byte SHA-256 mismatch"])
    try:
        with Image.open(reference_file) as im:
            if im.size != expected_size:
                return _stage(required[0], "RESTORE_ORIGINAL_REFERENCE",
                              ["reference pixel dimensions mismatch"])
            im.verify()
    except (OSError, ValueError) as exc:
        return _stage(required[0], "RESTORE_ORIGINAL_REFERENCE", [str(exc)])

    file = Path(ledger_path) if ledger_path else None
    if file is None or not file.is_file():
        return _stage(required[0], "GENERATE_AND_AUDIT_CANDIDATE",
                      ["acceptance ledger absent; start first independent candidate"])
    try:
        ledger = json.loads(file.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return _stage(required[0], "REPAIR_ACCEPTANCE_LEDGER", [str(exc)])
    if (not isinstance(ledger, dict) or ledger.get("schema") != SCHEMA or
            ledger.get("criteria_sha256") != spec["sha256"] or
            ledger.get("reference_sha256") != reference_sha256 or
            (expected_target is not None and ledger.get("target") != expected_target) or
            ledger.get("reference_dimensions_px") != list(reference_size)):
        return _stage(required[0], "INVALIDATE_AND_REAUDIT_STALE_EVIDENCE",
                      ["ledger schema/criteria/reference digest mismatch"])
    groups = ledger.get("stages")
    if not isinstance(groups, dict) or set(groups) - set(STAGES):
        return _stage(required[0], "REPAIR_ACCEPTANCE_LEDGER",
                      ["stage map invalid or contains unrecognized stage"])
    accepted = []
    accepted_candidate_pairs = set()
    for stage in required:
        block = groups.get(stage)
        attempts = block.get("attempts", []) if isinstance(block, dict) else []
        if not isinstance(attempts, list):
            return _stage(stage, "REPAIR_ACCEPTANCE_LEDGER",
                          ["attempts must be an ordered array"], accepted=accepted)
        if not attempts:
            diagnostics=[d for d in ledger.get("diagnostics", [])
                         if isinstance(d, dict) and d.get("stage") == stage and
                         d.get("status") == "FAIL"]
            if diagnostics:
                failed=diagnostics[-1]
                return _stage(stage, "REPAIR_DIAGNOSTIC_AND_REGENERATE",
                              [failed.get("finding", "unresolved diagnostic failure")],
                              accepted=accepted,
                              latest={"id": failed.get("id"), "verdict":"FAIL",
                                      "official_attempt":False})
            return _stage(stage, "GENERATE_AND_AUDIT_CANDIDATE",
                          ["no candidate yet for " + stage], accepted=accepted)
        prev = None
        for ordinal, attempt in enumerate(attempts, 1):
            if not isinstance(attempt, dict) or attempt.get("iteration") != ordinal:
                return _stage(stage, "REPAIR_ACCEPTANCE_LEDGER",
                              ["attempt order mismatch"], iteration=ordinal, accepted=accepted)
            if prev is not None and any(prev.get(key) and prev.get(key) == attempt.get(key)
                    for key in ("geometry_sha256", "preview_sha256")):
                return _stage(stage, "REGENERATE_DIFFERENT_CANDIDATE",
                              ["geometry or preview was reused, not materially regenerated"],
                              iteration=ordinal, accepted=accepted)
            # Declared PASS is not independently verified. An invalid one
            # must never prevent a later repaired candidate in the same stage.
            if attempt.get("request_id"):
                original={k:v for k,v in attempt.items()
                          if k not in ("iteration","parent_attempt_sha256",
                                      "attempt_sha256","payload_sha256",
                                      "verified_verdict")}
                expected_parent=prev.get("attempt_sha256") if prev else None
                if (attempt.get("parent_attempt_sha256") != expected_parent or
                    attempt.get("payload_sha256") != controller.digest(original) or
                    attempt.get("attempt_sha256") != controller.digest({
                       k:v for k,v in attempt.items() if k != "attempt_sha256"})):
                    return _stage(stage,"REPAIR_ACCEPTANCE_LEDGER",
                                  ["candidate hash chain or payload corrupted"],
                                  iteration=ordinal,accepted=accepted)
            prev = attempt
        last = attempts[-1]
        problems = []
        if last.get("stage") != stage:
            problems.append("attempt stage identity mismatch")
        pair = (last.get("geometry_sha256"), last.get("preview_sha256"))
        if pair in accepted_candidate_pairs:
            problems.append("same candidate reused for a different accepted stage")
        for key, visual in (("geometry", False), ("preview", True)):
            reason = _verify_artifact(
                last.get(key + "_path"), last.get(key + "_sha256"),
                base=file.parent, image=visual, source_sha256=reference_sha256,
                expected_size=expected_size, stage=stage
            )
            if reason:
                problems.append(key + ": " + reason)
        # Independent deterministic proof: bytes, entire cumulative multimodal
        # network, grade crossings, target mask, territorial exclusivity and
        # identity of the preceding approved stage. Agent text cannot replace it.
        try:
            geo = Path(last.get("geometry_path", ""))
            if not geo.is_absolute():
                geo = file.parent / geo
            preceding = None
            if accepted:
                prev = groups[accepted[-1]]["attempts"][-1]
                preceding = Path(prev["geometry_path"])
                if not preceding.is_absolute():
                    preceding = file.parent / preceding
            spatial = infra.validate(geo, source_sha=reference_sha256,
                                     dimensions=expected_size,
                                     profile=spec["profile"], prior=preceding)
            if spatial["stage"] != stage or spatial["geometry_sha256"] != last.get("geometry_sha256"):
                problems.append("deterministic spatial audit bound to different candidate")
        except (infra.InfraInvalid, OSError, ValueError, TypeError, KeyError) as exc:
            problems.append("deterministic geometry audit failed: " + str(exc))
        # Remote bytes must be read back by the host. This receipt checks
        # declared binding; actual connector traffic cannot be proven by Python.
        if require_remote:
            receipts=last.get("drive_receipts",{})
            preview=receipts.get("preview") if isinstance(receipts,dict) else None
            if (not isinstance(preview,dict) or
                not isinstance(preview.get("file_id"),str) or not preview["file_id"] or
                preview.get("sha256") != last.get("preview_sha256") or
                preview.get("readback_sha256") != last.get("preview_sha256")):
                problems.append("Drive image upload/readback receipt missing or inconsistent")
        # Host visual reports are a separate semantic judgment. A naked boolean
        # and long prose is never sufficient for a purported image inspection.
        observation = last.get("visual_observations")
        if (not isinstance(observation, dict) or
                observation.get("preview_sha256") != last.get("preview_sha256") or
                observation.get("geometry_sha256") != last.get("geometry_sha256")):
            problems.append("visual inspection receipt missing or stale")
        else:
            seen = set()
            region_checks = observation.get("regions", [])
            if not isinstance(region_checks,list):
                region_checks=[]
            imgpath=Path(last.get("preview_path", ""))
            if not imgpath.is_absolute():
                imgpath=file.parent/imgpath
            try:
                with Image.open(imgpath) as im:
                    for r in region_checks:
                        cid=r.get("criterion_id") if isinstance(r,dict) else None
                        box=r.get("bbox") if isinstance(r,dict) else None
                        if (cid not in spec["stages"][stage] or cid in seen or
                            not isinstance(box,list) or len(box)!=4 or
                            not all(isinstance(n,int) for n in box) or
                            not (0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height)):
                            continue
                        digest=hashlib.sha256(im.crop(tuple(box)).tobytes()).hexdigest()
                        if r.get("pixels_sha256")==digest:
                            seen.add(cid)
                if seen != set(spec["stages"][stage]):
                    problems.append("visual inspection lacks real image-bound regions for all criteria")
            except (OSError, ValueError) as exc:
                problems.append("visual inspection image cannot be opened: " + str(exc))
        if (last.get("reviewed_by") != "AGENT" or
                not isinstance(last.get("model"), str) or
                len(last["model"].strip()) < 3 or
                last.get("full_image_visually_inspected") is not True):
            problems.append("real host-agent full-image review evidence missing")
        if last.get("reference_sha256") != reference_sha256:
            problems.append("attempt not bound to original reference")
        checks = last.get("checks")
        expected_ids = set(spec["stages"][stage])
        if not isinstance(checks, dict) or set(checks) != expected_ids:
            problems.append("per-criterion review absent, extra or incomplete")
            checks = {}
        failed = []
        for cid in spec["stages"][stage]:
            check = checks.get(cid)
            if not isinstance(check, dict) or check.get("status") not in ("PASS", "FAIL"):
                problems.append(cid + ": PASS/FAIL decision absent")
                failed.append(cid)
                continue
            evidence = check.get("evidence")
            if not isinstance(evidence, str) or len(evidence.strip()) < 30:
                problems.append(cid + ": concrete visual/technical evidence required")
            if check["status"] == "FAIL":
                failed.append(cid)
        verdict = last.get("verdict")
        if verdict not in ("PASS", "FAIL"):
            problems.append("final verdict must be PASS/FAIL")
        if verdict == "PASS" and (
                failed or last.get("findings") != [] or last.get("repair_plan") not in (None, "")):
            problems.append("PASS conflicts with failing checks/open findings")
        if verdict == "FAIL" and (
                not failed or
                not isinstance(last.get("findings"), list) or not last["findings"] or
                not isinstance(last.get("repair_plan"), str) or
                len(last["repair_plan"].strip()) < 30):
            problems.append("FAIL must list failed checks, concrete findings and repair plan")
        if problems:
            action = controller.progress_policy(attempts)
            if action == "REPAIR_AND_REGENERATE":
                action = "REPAIR_UNVERIFIED_CANDIDATE"
            return _stage(stage, action,
                          problems, iteration=len(attempts), accepted=accepted,
                          latest={"declared_verdict": verdict,
                                  "verified_verdict": "FAIL", "failed": failed})
        if verdict == "FAIL":
            action = controller.progress_policy(attempts)
            return _stage(stage, action, failed, iteration=len(attempts),
                          accepted=accepted,
                          latest={"declared_verdict": "FAIL",
                                  "verified_verdict": "FAIL",
                                  "repair_plan": last["repair_plan"],
                                  "findings": last["findings"]})
        accepted_candidate_pairs.add(pair)
        accepted.append(stage)
    return _stage(required[-1], "ADVANCE_AFTER_ACCEPTANCE", [],
                  accepted=accepted)

def checkpoint_issues(checkpoint, *, ledger_path, reference_sha256,
                      criteria_sha256, expected_target):
    """Check exact remote-resumable state, not self-declared approval flags."""
    issues = []
    if not isinstance(checkpoint, dict):
        return ["checkpoint missing or unreadable"]
    if checkpoint.get("schema") != "NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT":
        issues.append("checkpoint schema mismatch")
    if checkpoint.get("target") != expected_target:
        issues.append("checkpoint target mismatch")
    if checkpoint.get("criteria_sha256") != criteria_sha256:
        issues.append("checkpoint Markdown contract SHA mismatch")
    if checkpoint.get("reference_sha256") != reference_sha256:
        issues.append("checkpoint original U02 SHA mismatch")
    ledger_file = Path(ledger_path)
    if not ledger_file.is_file():
        return issues + ["acceptance ledger bytes absent"]
    if checkpoint.get("ledger_sha256") != sha_file(ledger_file):
        issues.append("checkpoint and ledger SHA mismatch")
    try:
        ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
        stages = ledger.get("stages", {})
        # Claiming an accepted stage without a recorded PASS is never evidence.
        accepted = checkpoint.get("official_accepted_stages")
        if not isinstance(accepted, list) or any(
            stage not in stages or not isinstance(stages[stage], dict) or
            not stages[stage].get("attempts") or
            stages[stage]["attempts"][-1].get("verdict") != "PASS"
            for stage in accepted
        ):
            issues.append("checkpoint accepted stages not backed by ledger")
        if isinstance(accepted, list) and accepted != list(STAGES[:len(accepted)]):
            issues.append("checkpoint accepted stages out of order")
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        issues.append("ledger unreadable: " + str(exc))
    return issues
