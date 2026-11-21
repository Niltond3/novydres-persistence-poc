"""Noncanonical fixture evaluator used ONLY by scripts/pipeline.py run.

This is not an executable pipeline or a second controller. All host operations,
remote journals, retries and CAS remain in the canonical orchestration module.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re

from PIL import Image

import mapwork as core
import contracts as contract
import acceptance
import orchestration as controller
import infra_checks as infra
import native_generation as native

ROOT=Path(__file__).resolve().parents[1]


def _load(path):
    return core.load(path) if path and Path(path).is_file() else None


def _checkpoint(phase, action, blockers, *, audit=None):
    return {"schema": "NOVYDRES_MAPWORK_PIPELINE_CHECKPOINT",
            "phase": phase, "next_action": action, "blockers": list(blockers),
            "audit": audit, "publication_authorized": False,
            "canonical_state_changed": False, "next_decision_id": None}


SYNTHETIC_SCHEMA = "NOVYDRES_MAPWORK_SYNTHETIC_TRIAL"
SYNTHETIC_LEDGER = "NOVYDRES_MAPWORK_SYNTHETIC_LEDGER"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def synthetic_contract(path, args):
    """Isolated, opt-in host trial; no canonical geometry or editorial authority."""
    trial = _load(path)
    contract.require(isinstance(trial, dict) and trial.get("schema") == SYNTHETIC_SCHEMA
        and trial.get("test_only") is True
        and trial.get("publication_authorized") is False
        and trial.get("canonical_state_changed") is False
        and trial.get("canonical_target") is None,
        "synthetic trial requires explicit noncanonical authority")
    scenario = trial.get("scenario_id")
    contract.require(isinstance(scenario, str) and re.fullmatch(
        r"synthetic-[a-z0-9][a-z0-9-]{2,63}", scenario),
        "synthetic trial needs an isolated scenario identity")
    contract.require(trial.get("criteria_sha256") == hashlib.sha256(
        (ROOT / "docs/infra-acceptance.md").read_bytes()).hexdigest(),
        "synthetic trial Markdown criteria hash differs")
    dimensions = trial.get("reference_size")
    contract.require(isinstance(trial.get("reference_sha256"), str)
        and HEX64.fullmatch(trial["reference_sha256"])
        and isinstance(dimensions, list) and len(dimensions) == 2
        and all(type(size) is int and 1 <= size <= 16384 for size in dimensions),
        "synthetic reference identity or dimensions missing")
    operation_id = trial.get("resume_operation_id")
    contract.require(isinstance(operation_id, str) and HEX64.fullmatch(operation_id),
        "synthetic trial must bind its existing pending operation")
    contract.require(getattr(args, "autonomous_journal", None)
        and getattr(args, "host_journal_path", None) == trial.get("journal_repo_path")
        and getattr(args, "host_branch", None) == trial.get("branch"),
        "synthetic trial requires its original GitHub journal and branch")
    journal = _load(args.autonomous_journal)
    contract.require(isinstance(journal, dict)
        and journal.get("schema") == controller.AUTONOMY_SCHEMA
        and journal.get("branch") == trial["branch"]
        and journal.get("journal_repo_path") == trial["journal_repo_path"]
        and journal.get("publication_authorized") is False
        and journal.get("steps")
        and any(step.get("operation_id") == operation_id for step in journal["steps"])
        and journal["steps"][-1]["status"] in ("PENDING", "COMPLETED"),
        "synthetic trial is not bound to a recovered operation")
    # An existing test-only request is allowed in the original journal. A real
    # region request can never be silently reinterpreted as synthetic.
    if getattr(args, "intent", None):
        intent = _load(args.intent)
        contract.require(isinstance(intent, dict) and intent.get("test_only") is True,
            "real canonical intent cannot enter synthetic trial")
    contract.require(not any((getattr(args, "execute", False),
        getattr(args, "zone", None), getattr(args, "reference", None),
        getattr(args, "before", None), getattr(args, "editable_mask", None),
        getattr(args, "assets", None), getattr(args, "recipe_unit", None),
        getattr(args, "audit_unit", None), getattr(args, "design_unit", None))),
        "synthetic trial cannot run canonical renderer or U02 modifications")
    return trial


def synthetic_output_path(path):
    """A trial may write outside the checkout, or only under sessions/ inside."""
    resolved = Path(path).resolve()
    checkout = ROOT.resolve()
    if resolved.is_relative_to(checkout) and not resolved.is_relative_to(checkout / "sessions"):
        raise contract.Blocked("synthetic output cannot overwrite canonical project files")
    return resolved


def _synthetic_state(trial, phase, action, blockers=(), audit=None):
    result = _checkpoint(phase, action, blockers, audit=audit)
    result.update(mode="SYNTHETIC_TRIAL", target=trial["scenario_id"],
                  request_sha256=contract.evidence_digest(trial),
                  synthetic_test_only=True)
    return result


def run(args):
    trial = synthetic_contract(args.synthetic_trial, args)
    if not getattr(args, "spatial", None):
        return _synthetic_state(trial, "SYNTHETIC_TOPOLOGY",
            "RECONCILE_SYNTHETIC_TOPOLOGY",
            ["Produce fixture-only topology by the existing pipeline; no U02, zone or INF acceptance"])
    spatial_file = Path(args.spatial)
    geometry = _load(spatial_file)
    contract.require(isinstance(geometry, dict)
        and geometry.get("fixture_mode") is True
        and geometry.get("schema") == "NOVYDRES_MAPWORK_INFRA_GEOMETRY"
        and geometry.get("target") == trial["scenario_id"]
        and geometry.get("reference_size") == trial.get("reference_size")
        and geometry.get("source_sha256") == trial["reference_sha256"],
        "synthetic geometry provenance/identity differs from isolated trial")
    try:
        technical = infra.validate(spatial_file,
            source_sha=trial["reference_sha256"],
            dimensions=tuple(trial["reference_size"]),
            profile=acceptance.criteria_contract()["profile"])
    except (infra.InfraInvalid, ValueError, TypeError, KeyError, OSError) as exc:
        technical = {"status": "FAIL", "reason": str(exc)}
    crossings = geometry.get("network", {}).get("crossings", [])
    if not any(item.get("kind") == "grade_separated" for item in crossings):
        technical = {"status": "FAIL", "reason": "synthetic grade-separated crossing absent"}
    if technical.get("status") != "PASS":
        return _synthetic_state(trial, "SYNTHETIC_TOPOLOGY",
            "REPAIR_SYNTHETIC_TOPOLOGY", [technical.get("reason", "fixture topology failed")],
            audit=technical)
    image_ref=trial.get("native_reference_sha256")
    edit_mask=trial.get("native_mask_sha256")
    goal=trial.get("native_edit_goal")
    if not all((image_ref,edit_mask,goal)):
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "MATERIALIZE_SYNTHETIC_REFERENCE_AND_MASK",
            ["Provide a real image reference from Drive, edit mask and explicit edit goal; "
             "topological source hash alone is not a native image reference"])
    request=native.edit_request(reference_sha256=image_ref,mask_sha256=edit_mask,
        goal=goal,scope="SYNTHETIC",job_id=trial["scenario_id"])
    if not getattr(args, "unit_receipt", None):
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "GENERATE_AND_AUDIT_CANDIDATE",
            ["Host must independently GET reference and mask from Drive, attach both "
             "as native edit visual inputs; never send a textual infographic prompt"],
            audit={"topology_status": "PASS", "geometry_sha256":
                   hashlib.sha256(spatial_file.read_bytes()).hexdigest(),
                   "native_edit_request":request,
                   "native_edit_request_sha256":native.json_digest(request)})
    receipt = _load(args.unit_receipt)
    contract.require(isinstance(receipt, dict) and receipt.get("provider") == "drive"
        and isinstance(receipt.get("remote_id"), str) and receipt["remote_id"]
        and receipt.get("native_generation") is True,
        "native Drive generation receipt absent")
    raw, remote = Path(receipt.get("path", "")), Path(receipt.get("readback_path", ""))
    contract.require(raw.is_file() and remote.is_file()
        and raw.resolve() != remote.resolve()
        and raw.read_bytes() == remote.read_bytes()
        and receipt.get("sha256") == hashlib.sha256(raw.read_bytes()).hexdigest(),
        "independent Drive image bytes/SHA mismatch")
    with Image.open(raw) as image:
        contract.require(image.format == "PNG", "native candidate is not PNG")
        image.verify()
    if not getattr(args, "native_handoff", None):
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "MATERIALIZE_NATIVE_EDIT_HANDOFF",
            ["Native input dispatch, reference/mask Drive GET and image result must be bound"])
    bound=native.verify_handoff(_load(args.native_handoff),request=request,
        output_sha256=receipt["sha256"])
    handoff = _load(args.native_handoff)
    contract.require(receipt["remote_id"] == handoff["output"]["remote_id"],
        "native image Drive receipt identity differs from handoff")
    if not getattr(args, "native_composed_receipt", None):
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "RECOMPOSE_NATIVE_MASK", ["Recompose native candidate over real reference "
             "using the authorized mask; upload PNG to Drive and independently GET it. "
             "Native candidate alone is never a pixel-preserving result."])
    composed = _load(args.native_composed_receipt)
    contract.require(isinstance(composed,dict) and
        composed.get("provider") == "drive" and
        isinstance(composed.get("remote_id"),str) and composed["remote_id"],
        "composed Drive receipt missing")
    composed_path=Path(composed.get("path",""))
    composed_readback=Path(composed.get("readback_path",""))
    contract.require(composed_path.is_file() and composed_readback.is_file() and
        composed_path.resolve()!=composed_readback.resolve() and
        composed_path.read_bytes()==composed_readback.read_bytes() and
        composed.get("sha256")==hashlib.sha256(composed_path.read_bytes()).hexdigest(),
        "composed image independent Drive readback mismatch")
    proof=native.verify_composed(
        handoff["inputs"]["reference-image"]["path"],
        handoff["inputs"]["edit-mask"]["path"],
        handoff["output"]["path"], composed_path,
        crop_bbox=composed.get("crop_bbox"))
    contract.require(proof["composed_sha256"] == composed["sha256"],
                     "masked composition identity mismatch")
    review = _load(getattr(args, "visual_review", None))
    if not review:
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "AGENT_INSPECT_IMAGE", ["Inspect the recomposed PNG, grade, interfaces and scene, not a text PASS"])
    observations = review.get("observations", [])
    required = {"grade", "continuity", "coherence", "format"}
    contract.require(review.get("by") == "AGENT"
        and review.get("image_sha256") == composed["sha256"]
        and review.get("reference_sha256") == bound["reference_sha256"]
        and review.get("mask_sha256") == bound["mask_sha256"]
        and review.get("status") in ("PASS", "FAIL")
        and isinstance(observations, list) and len(observations) == 4
        and all(isinstance(item, dict) and item.get("criterion") in required
            and item.get("status") in ("PASS", "FAIL")
            and isinstance(item.get("evidence"), str)
            and len(item["evidence"].strip()) >= 16 for item in observations)
        and {item["criterion"] for item in observations} == required
        and (review["status"] == "FAIL" or all(item["status"] == "PASS" for item in observations)),
        "synthetic review must inspect grade, continuity, coherence and format")
    if not getattr(args, "record_attempt", None) or not getattr(args, "ledger", None):
        return _synthetic_state(trial, "SYNTHETIC_IMAGE",
            "RECORD_SYNTHETIC_ATTEMPT", ["Persist attempt in existing deterministic retry ledger"])
    attempt = _load(args.record_attempt)
    contract.require(isinstance(attempt, dict)
        and attempt.get("stage") == "SYNTHETIC"
        and attempt.get("reference_sha256") == trial["reference_sha256"]
        and attempt.get("geometry_sha256") == hashlib.sha256(spatial_file.read_bytes()).hexdigest()
        and attempt.get("preview_sha256") == composed["sha256"]
        and attempt.get("verdict") == review["status"],
        "synthetic attempt differs from material geometry, pixels or visual verdict")
    synthetic_output_path(args.ledger)
    recorded = controller.record_attempt(args.ledger, args.record_attempt,
        criteria_sha256=trial["criteria_sha256"],
        reference_sha256=trial["reference_sha256"],
        schema=SYNTHETIC_LEDGER, allowed_stages=("SYNTHETIC",),
        active_stage="SYNTHETIC", target=trial["scenario_id"],
        reference_size=trial["reference_size"])
    ledger = core.load(args.ledger)
    attempts = ledger["stages"]["SYNTHETIC"]["attempts"]
    if review["status"] == "FAIL":
        return _synthetic_state(trial, "SYNTHETIC_REPAIR",
            controller.progress_policy(attempts),
            ["Visual FAIL remains unaccepted; regenerate independent native PNG bytes"],
            audit={"status": "FAIL", "record": recorded})
    # A test may pass only with genuine PNG bytes, Drive GET and an independent
    # model review. This cannot promote any INF or canonical stage.
    return _synthetic_state(trial, "SYNTHETIC_ACCEPTANCE", "CHECKPOINT",
        audit={"status": "PASS", "record": recorded,
               "topology_status": "PASS", "image_sha256": composed["sha256"],
               "canonical_acceptance": False})


