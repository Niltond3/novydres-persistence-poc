#!/usr/bin/env python3
"""Seeded-state contract reducer for D11 V019; never plays or persists a scene."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
DEL = Path("novydres/runtime/narrative-architecture/program/deliverables")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def deep_merge(target, overlay):
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)
    return target


def initial(case):
    state = {
        "episode_m301_open": True,
        "m302_unlocked": False,
        "m302_story_entry_eligible": False,
        "next_scene": "C06",
        "scene_started": False,
        "scene_ready": False,
        "narrator_permission": False,
        "persistent_state_mutated": False,
        "event_log": [],
        "timeline_tick": 0,
        "invitation_count": 0,
        "new_invitation_emitted": False,
        "bart": {"mortal": True, "embrace_recorded": False},
        "pc_knowledge": {"box_contents": "UNKNOWN"},
        "npc_knowledge": {},
        "family": {"identity": "UNKNOWN", "location": "UNKNOWN", "response": "UNKNOWN"},
        "optional_story": {"status": "NOT_STARTED"},
        "route": "TARGET_PENDING",
        "alternate_route_selected": False,
        "npc_generation": "UNKNOWN",
        "npc_blood_potency": None,
        "transition": {"allowed": False, "reason": "NOT_ATTEMPTED"},
    }
    return deep_merge(state, case.get("initial_state", {}))


def knowledge_delta(before, after):
    delta = []

    def walk(a, b, prefix=""):
        for key in sorted(set(a) | set(b)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in a:
                delta.append({"path": path, "change": "ADDED"})
            elif key not in b:
                delta.append({"path": path, "change": "REMOVED"})
            elif isinstance(a[key], dict) and isinstance(b[key], dict):
                walk(a[key], b[key], path)
            elif a[key] != b[key]:
                delta.append({"path": path, "change": "CHANGED"})

    walk(before, after)
    return delta


def has_c06_admission(d04):
    """Read current D04, rather than treating an invitation or test fixture as admission."""
    for admission in d04.get("admissions", []):
        material = " ".join(
            str(admission.get(key, ""))
            for key in ("plot_id", "contract_ref", "decision")
        ).upper()
        decision = str(admission.get("decision", "")).upper()
        if (
            ("C06" in material or "ST-C06-REENTRY" in material)
            and decision.startswith("ADMITTED")
        ):
            return True
    return False


def reduce(state, event, d04_c06_admitted):
    s = copy.deepcopy(state)
    kind = event["type"]

    if kind == "contract_only":
        pass
    elif kind == "evaluate_kuthulun_presentation":
        evidence = event.get("evidence", {})
        delivered = evidence.get("actual_cause_action") is True and evidence.get("first_invitation_delivered") is True
        s["presentation"] = {
            "broad_basis_available": evidence.get("broad_trigger_present") is True,
            "actual_action": evidence.get("actual_cause_action") is True,
        }
        s["invitation"] = {"status": "DELIVERED" if delivered else "NOT_EMITTED"}
        s["story_entry_eligible"] = delivered and evidence.get("bart_attends") is True
        s["bart_attendance"] = "CHOSEN" if evidence.get("bart_attends") is True else "NOT_CHOSEN"
        s["scene_started"] = s["story_entry_eligible"]
    elif kind == "deliver_kuthulun_invitation":
        delivered = event.get("cause_action") is True and event.get("delivery_confirmed") is True
        attends = delivered and event.get("bart_attends") is True
        if delivered:
            s["invitation"] = {"status": "DELIVERED", "id": event["invitation_id"]}
            s["invitation_count"] = state.get("invitation_count", 0) + 1
        else:
            s["invitation"] = {"status": "NOT_EMITTED"}
        s["bart_attendance"] = "CHOSEN" if attends else "NOT_CHOSEN"
        s["presence_recorded"] = attends
        s["scene_started"] = attends and (
            event.get("invitation_kind") == "PRECEDENCE"
            or (event.get("invitation_kind") == "COERCION" and event.get("prior_story_closed") is True)
        )
        if event.get("invitation_kind") == "COERCION":
            s["coercion_story_started"] = s["scene_started"]
    elif kind == "settle_kuthulun_victory":
        outcome = event.get("actual_outcome")
        resolved = event.get("immediate_actions_resolved") is True
        active = event.get("other_conflict_active") is True
        s["local_conflict_resolution"] = {
            "status": "ONGOING_REAL_CONFLICT" if active else "CLOSED" if resolved else "UNRESOLVED",
            "actual_outcome": outcome,
        }
        s["route"] = state.get("route", "TARGET_PENDING")
        s["npc_action_generated"] = False
        s["post_victory_consequence_filed"] = False
    elif kind == "select_quiet_alternate_exit":
        evidence = event.get("evidence", {})
        selected = evidence.get("player_selected") is True
        reconciled = evidence.get("source_state_reconciled") is True
        if selected and reconciled:
            s["guided_creation_status"] = "ALTERNATE"
            s["route"] = "ROUTE-QUIET-ALTERNATE-EXIT"
            s["alternate_route_selected"] = True
        else:
            s["guided_creation_status"] = "PENDING"
            s["route"] = "PROVOCATION_CLOSURE_PENDING"
            s["alternate_route_selected"] = False
        s["episode_m301_open"] = True
        s["m302_unlocked"] = False
        s["scene_started"] = False
    elif kind == "classify_route_outcome":
        evidence = event.get("evidence", {})
        outcome = evidence.get("outcome")
        if evidence.get("irreversible") is not True:
            status, reason = "PENDING", "RECOVERABLE_DIVERGENCE"
            s["route"] = "TARGET_PENDING"
        elif not evidence.get("sources_reconciled") or not evidence.get("materially_blocks_target"):
            status, reason = "PENDING_REVIEW", "IRREVERSIBLE_RESULT_REQUIRES_RECONCILED_REVIEW"
            s["route"] = "TARGET_PENDING"
        elif evidence.get("player_selected_status") in ("ALTERNATE", "INCOMPLETE"):
            status, reason = evidence["player_selected_status"], "PLAYER_SELECTED_AFTER_MATERIAL_BLOCKAGE"
            s["route"] = status
        else:
            status, reason = "PENDING_REVIEW", "EXPLICIT_PLAYER_CHOICE_REQUIRED"
            s["route"] = "TARGET_PENDING"
        s["route_review"] = {"status": status, "reason": reason, "reviewed_outcome": outcome}
        if outcome == "FINAL_DEATH":
            s.setdefault("bart", {})["final_death"] = True
            s["bart"]["embrace_recorded"] = False
    elif kind == "box_search":
        s["pc_knowledge"]["box_contents"] = "UNKNOWN"
    elif kind == "unobserved_contact":
        s["invitation"] = {"status": "NOT_EMITTED", "reason": "NO_OBSERVATION"}
        s["location_disclosed"] = False
    elif kind == "relay_refused":
        s["delivery_attempt"]["status"] = "REFUSED"
        s["invitation"] = {"status": "NOT_EMITTED", "reason": "RELAY_REFUSED"}
        s["location_disclosed"] = False
    elif kind == "relay_delayed":
        s["delivery_attempt"]["status"] = "PENDING"
        s["invitation"] = {"status": "NOT_EMITTED_PENDING_RELAY", "reason": "RELAY_PENDING"}
        s["location_disclosed"] = False
    elif kind == "early_document_discovery":
        s["pc_knowledge"]["document_scope"] = "TEXTUAL_ASSOCIATION_ONLY"
    elif kind == "abandon_optional":
        s["optional_story"] = {"status": "CLOSED", "disposition": "ABANDONED"}
    elif kind == "decline_invitation":
        s["route"] = state.get("route", "TARGET_PENDING")
        s["scene_started"] = False
    elif kind == "leave_first_contact":
        s["route"] = "CONTACT_CLOSED"
        s["new_invitation_emitted"] = False
    elif kind == "attempt_transition":
        closure = event.get("closure", {})
        required = (
            "required_units_closed",
            "optional_started_closed",
            "player_confirmed",
            "sources_reconciled",
            "supported_cycle_transition",
            "c06_started",
            "c06_closed",
        )
        closure_flags_complete = all(closure.get(key) is True for key in required)
        ok = d04_c06_admitted and closure_flags_complete
        reason = (
            "ALL_FUTURE_GATES_MET"
            if ok
            else "MISSING_OR_UNSUPPORTED_EVIDENCE"
            if not closure_flags_complete
            else "NO_ADMITTED_C06_CAUSE"
        )
        s["transition"] = {
            "allowed": ok,
            "reason": reason,
        }
        s["m302_unlocked"] = ok
        if ok:
            s["episode_m301_open"] = False
    elif kind == "attempt_c06_offer":
        evidence = event.get("evidence", {})
        valid = (
            d04_c06_admitted
            and evidence.get("separate_player_authorization") is True
            and evidence.get("delivery_confirmed") is True
            and bool(evidence.get("offer_id"))
        )
        if valid:
            offer_id = evidence["offer_id"]
            s["c06"] = {
                "status": "OFFER_DELIVERED",
                "cause_admitted": True,
                "offer_made": True,
                "separately_authorized": True,
                "offer_delivered": True,
                "offer_id": offer_id,
                "played": False,
            }
            s["invitation"] = {"status": "DELIVERED", "id": offer_id}
            s["invitation_count"] = state.get("invitation_count", 0) + 1
            s["new_invitation_emitted"] = True
            s["transition"] = {"allowed": True, "reason": "VALID_ADMITTED_AUTHORIZED_OFFER"}
        else:
            s["transition"] = {"allowed": False, "reason": "NO_ADMITTED_CAUSE"}
            s["new_invitation_emitted"] = False
            s["scene_started"] = False
    elif kind == "attempt_alternate_closure":
        evidence = event.get("evidence", {})
        c06 = s.get("c06", {})
        required = (
            "started_units_closed",
            "unstarted_optional_quiet",
            "source_state_reconciled",
            "player_selected_alternate",
            "player_explicit_close",
            "critical_evidence_verified",
            "supported_cycle_transition",
        )
        no_cause = (
            not d04_c06_admitted
            and c06.get("status") == "NO_ADMITTED_CAUSE"
            and c06.get("cause_admitted") is False
            and c06.get("offer_made") is False
            and c06.get("played") is False
            and evidence.get("cause_absence_verified") is True
        )
        valid_decline = (
            d04_c06_admitted
            and c06.get("status") == "DECLINED_BEFORE_START"
            and c06.get("cause_admitted") is True
            and c06.get("offer_made") is True
            and c06.get("separately_authorized") is True
            and c06.get("offer_delivered") is True
            and bool(c06.get("offer_id"))
            and c06.get("played") is False
        )
        selected = evidence.get("player_selected_alternate") is True
        if selected:
            s["route"] = "ROUTE-M3-01-DECLINED-CONTINUATION"
            s["alternate_route_selected"] = True
        else:
            s["alternate_route_selected"] = False
        if evidence.get("critical_evidence_verified") is not True:
            reason = "CRITICAL_EVIDENCE_UNVERIFIED"
        elif not selected:
            reason = "ALTERNATE_ROUTE_NOT_SELECTED"
        elif c06.get("status") == "DECLINED_BEFORE_START" and not valid_decline:
            reason = "NO_VALID_ADMITTED_OFFER"
        elif c06.get("status") == "NO_ADMITTED_CAUSE" and not no_cause:
            reason = "NO_ADMITTED_CAUSE_NOT_VERIFIED"
        else:
            reason = "MISSING_OR_UNSUPPORTED_EVIDENCE"
        ok = (no_cause or valid_decline) and selected and all(evidence.get(key) is True for key in required)
        s["transition"] = {
            "allowed": ok,
            "reason": "ALL_FUTURE_GATES_MET" if ok else reason,
            "route": "ALTERNATE",
        }
        s["m302_story_entry_eligible"] = False
        s["m302_unlocked"] = False
        if ok:
            s["episode_m301_open"] = False
    elif kind == "decline_c06_before_start":
        c06 = s.get("c06", {})
        valid_offer = (
            d04_c06_admitted
            and c06.get("status") == "OFFER_DELIVERED"
            and c06.get("cause_admitted") is True
            and c06.get("offer_made") is True
            and c06.get("separately_authorized") is True
            and c06.get("offer_delivered") is True
            and bool(c06.get("offer_id"))
            and c06.get("played") is False
        )
        if valid_offer:
            c06["status"] = "DECLINED_BEFORE_START"
            s.setdefault("story_units", {})["ST-C06-REENTRY"] = {
                "status": "DECLINED_NOT_PLAYED",
                "played": False,
            }
            s["route"] = "ROUTE-M3-01-DECLINED-CONTINUATION"
            s["transition"] = {"allowed": True, "reason": "VALID_OFFER_DECLINED"}
        else:
            s["transition"] = {"allowed": False, "reason": "NO_VALID_ADMITTED_OFFER"}
        s["scene_started"] = False
        s["episode_m301_open"] = True
        s["new_invitation_emitted"] = False
    elif kind == "decline_existing_offer":
        invitation = s.get("invitation", {})
        if invitation.get("status") == "DELIVERED" and invitation.get("id"):
            invitation["status"] = "DECLINED"
        s["new_invitation_emitted"] = False
        s["scene_started"] = False
    elif kind == "evaluate_independent_cause":
        evidence = event.get("evidence", {})
        ready = (
            evidence.get("m301_closed") is True
            and evidence.get("supported_cycle_transition") is True
            and (evidence.get("local_boundary_cause") is True or evidence.get("explicit_request_transmitted") is True)
        )
        s["independent_entry"] = {
            "eligible": ready,
            "status": "ENTRY_CAUSE_PRESENT" if ready else "QUIET_NO_CAUSE",
        }
        s["m302_story_entry_eligible"] = ready
        s["invitation"] = {"status": "NOT_EMITTED"}
        s["new_invitation_emitted"] = False
        s["scene_started"] = False
    elif kind == "simulate_route_selection":
        s["route"] = event["route"]
        s["scene_started"] = False
    elif kind == "do_not_attend":
        s["route"] = state.get("route", "TARGET_PENDING")
        s["scene_started"] = False
    elif kind == "escape":
        s["route"] = "ESCAPED"
        s["bart"]["embrace_recorded"] = False
    elif kind == "mechanical_divergence":
        s["route"] = "DIVERGED"
        s["actual_outcome"] = event["actual_outcome"]
        s["bart"]["embrace_recorded"] = False
    elif kind == "generic_threat":
        s["family_threat"] = {
            "scope": "GENERIC_FAMILY",
            "names_added": [],
            "locations_added": [],
            "actions_added": [],
            "responses_added": [],
        }
    elif kind == "no_actual_embrace":
        s["bart"]["embrace_recorded"] = False
    elif kind == "family_unavailable":
        s["family_contact_attempt"] = {
            "attempted": True,
            "channel": event["channel"],
            "result": "NO_CONTACT_ESTABLISHED_THIS_ATTEMPT",
        }
    elif kind == "refuse_social_task":
        task = event.get("task_id", "unspecified")
        s.setdefault("story_task", {})[task] = {"status": "REFUSED", "local_scene_status": "CLOSED"}
        s["route_abandoned"] = False
        s["route_advanced"] = False
    elif kind == "refuse_optional_ethics":
        s.setdefault("optional_stories", {})["ST-ETHICAL-COST"] = {"status": "CLOSED", "disposition": "REFUSED"}
    elif kind == "uninformed_npc":
        pass
    elif kind == "review_with_optional_open":
        s["graduation_review_available"] = True
        evidence = event.get("evidence", {})
        required = (
            "route_critical_closures",
            "player_choice_recorded",
            "sheet_and_xp_reconciled",
        )
        optional_ok = evidence.get("optional_threads") in (
            "RESOLVED",
            "ABANDONED",
            "QUIET",
            "CARRIED_BY_PLAYER_CHOICE",
        )
        if evidence.get("player_chooses_principal_2010") is False:
            alternate_ok = all(evidence.get(key) is True for key in required) and optional_ok
            s["graduation_status"] = "ALTERNATE" if alternate_ok else "INCOMPLETE"
        elif evidence.get("player_chooses_principal_2010") is True:
            complete_ok = all(evidence.get(key) is True for key in required) and optional_ok
            s["graduation_status"] = "COMPLETE" if complete_ok else "INCOMPLETE"
        else:
            s["graduation_status"] = "INCOMPLETE"
    elif kind == "elide_to_2010":
        s["exact_intermediate_dates"] = "UNKNOWN"
        s["graduation_review_available"] = True
    elif kind == "xp_review":
        s["xp_review_available"] = True
        s["xp_awarded_delta"] = 0
        s["xp_spent_delta"] = 0
    elif kind == "narrator_attempt":
        s["transition"] = {"allowed": False, "reason": "NO_OPERATIONAL_PERMISSION"}
        s["scene_ready"] = False
        s["narrator_permission"] = False
        s["scene_started"] = False
    elif kind == "read_prospective_profile":
        s["npc_generation"] = "UNKNOWN"
        s["npc_blood_potency"] = event["blood_potency"]
    elif kind == "final_death_before_embrace":
        s["bart"]["final_death"] = True
        s["bart"]["embrace_recorded"] = False
        s["route"] = "DIVERGED"
    else:
        raise ValueError(f"Unknown reducer event: {kind}")

    s["npc_knowledge_delta"] = knowledge_delta(
        state.get("npc_knowledge", {}), s.get("npc_knowledge", {})
    )
    return s


MISSING = object()


def get_path(obj, path):
    current = obj
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return MISSING
        current = current[part]
    return current


def matches(actual, expected, before, path):
    if expected == "__MISSING__":
        return actual is MISSING
    if isinstance(expected, dict):
        if expected.get("$unchanged_from_initial") is True:
            return actual == get_path(before, path)
        if expected.get("$absent") is True:
            return actual is MISSING
        if "$in" in expected:
            return actual in expected["$in"]
        if "$equals" in expected:
            return actual == expected["$equals"]
    return actual == expected


def resolve_pointer(obj, pointer):
    if not pointer:
        return obj
    current = obj
    for token in pointer.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def markdown_section(text, anchor):
    lines = text.splitlines()
    start = None
    level = None
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        title = match.group(2)
        if (anchor.startswith("#") and line.strip() == anchor.strip()) or (not anchor.startswith("#") and anchor in title):
            start, level = index, len(match.group(1))
            break
    if start is None:
        for index, line in enumerate(lines):
            if anchor in line:
                start, level = index, 7
                break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = re.match(r"^(#{1,6})\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])


def resolve_contract(case):
    source, anchor = case["contract_ref"].split("#", 1)
    path = ROOT / DEL / source
    if not path.is_file() or len(case.get("pass_criterion", "").strip()) < 12:
        return False
    if path.suffix.lower() == ".md":
        return markdown_section(path.read_text(encoding="utf-8"), anchor) is not None
    if path.suffix.lower() == ".json":
        try:
            return resolve_pointer(read_json(path), anchor) is not None
        except Exception:
            return False
    return False


def check_contract_assertion(check):
    path = ROOT / DEL / check["source"]
    if not path.is_file():
        return False
    kind = check["kind"]
    if kind.startswith("json_pointer_"):
        try:
            target = resolve_pointer(read_json(path), check["pointer"])
        except Exception:
            return False
        if kind == "json_pointer_equals":
            return target == check.get("expected")
        if kind == "json_pointer_contains_all":
            return isinstance(target, str) and all(needle in target for needle in check.get("needles", []))
        return False
    if kind == "markdown_section_contains_all":
        section = markdown_section(path.read_text(encoding="utf-8"), check["section_anchor"])
        return section is not None and all(needle in section for needle in check.get("needles", []))
    return False


cases_path = ROOT / DEL / "D11_ADVERSARIAL_CASES_V019_GM_HIDDEN.json"
cases_raw = cases_path.read_bytes()
cases_blob = file_blob(cases_path)
runner_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
cases_doc = json.loads(cases_raw.decode("utf-8"))
if cases_doc.get("document_id") != "D11_ADVERSARIAL_CASES_V019_GM_HIDDEN" or cases_doc.get("version") != "V019":
    raise SystemExit("D11_V019_BLOCK: wrong case identity")
for source in cases_doc.get("source_refs", []):
    path = ROOT / source["path"]
    if not path.is_file() or file_blob(path) != source["blob_sha"]:
        raise SystemExit("D11_V019_BLOCK: stale source pin")
d04_path = ROOT / DEL / "D04_PLOT_ADMISSIONS_V010.json"
d04 = read_json(d04_path)
d04_c06_admitted = has_c06_admission(d04)
if d04_c06_admitted:
    raise SystemExit("D11_V019_BLOCK: current no-cause fixtures conflict with D04 admission")
cases = cases_doc["cases"]
if len({case.get("id") for case in cases}) != len(cases):
    raise SystemExit("D11_V019_BLOCK: duplicate case ID")
for case in cases:
    if not resolve_contract(case):
        raise SystemExit(f"D11_V019_BLOCK: unresolved contract or missing pass criterion: {case.get('id')}")
    if not isinstance(case.get("assert"), dict) or not case["assert"]:
        raise SystemExit(f"D11_V019_BLOCK: missing contract assertions: {case.get('id')}")
    for check in case.get("contract_checks", []):
        if not check_contract_assertion(check):
            raise SystemExit(f"D11_V019_BLOCK: contract text/pointer check failed: {case.get('id')} / {check.get('kind')}")
results = []
for case in cases:
    before = initial(case)
    actual = reduce(before, case["event"], d04_c06_admitted)
    failures = []
    for path, expected in case["assert"].items():
        if not matches(get_path(actual, path), expected, before, path):
            failures.append(path)
    results.append((case["id"], not failures, failures))
failed = sum(not ok for _, ok, _ in results)
report = {
    "document_id": "D11_TEST_RESULTS_V019_PLAYER_SAFE",
    "version": "V019",
    "status": "PASS" if failed == 0 else "FAIL",
    "execution_mode": "DETERMINISTIC_SEEDED_STATE_CONTRACT_REDUCER",
    "cases_total": len(results),
    "passed": len(results) - failed,
    "failed": failed,
    "current_d04_c06_admission_present": d04_c06_admitted,
    "scenes_played": 0,
    "dice_simulated": False,
    "persistent_state_mutated": False,
    "result_detail_disclosed": False,
    "input_artifact_refs": [
        {"path": str(cases_path.relative_to(ROOT)), "blob_sha": cases_blob},
        *cases_doc.get("source_refs", []),
    ],
    "runner_source_sha256": runner_sha256,
    "case_failures": [
        {"case_id": case_id, "failed_assertions": failures}
        for case_id, ok, failures in results
        if not ok
    ],
    "limitation": "The reducer checks seeded authored-contract transitions against pinned current D04-D09 sources. It is not the game engine and proves no live cycle transition, V5 roll result, time advancement, event persistence, or scene permission.",
}
print(json.dumps(report, ensure_ascii=False, indent=2))
if failed:
    raise SystemExit(1)
