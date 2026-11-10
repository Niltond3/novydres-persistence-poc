import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = [
    "D05_PLAYER_APPROVAL_QUEUE_V004.json", "AUDIT_D05_V005.json", "HANDOFF_D05_V006.json",
    "D06_CHRONICLE_BIBLE_V004.json", "D06_TRANSFORMATION_PATHS_V004.json",
    "D06_PLAYER_APPROVAL_QUEUE_V004.json", "AUDIT_D06_V004.json", "HANDOFF_D06_V004.json",
    "D07_PLAYER_APPROVAL_QUEUE_V004.json", "AUDIT_D12_V004.json",
    "HANDOFF_D12_V004.json", "D12_RELEASE_CANDIDATE_V004.json",
]
docs = {}
checks = 0

def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

for filename in FILES:
    path = ROOT / filename
    check(path.is_file(), f"missing artifact: {filename}")
    docs[filename] = json.loads(path.read_text(encoding="utf-8"))

d05 = docs["D05_PLAYER_APPROVAL_QUEUE_V004.json"]
a05 = docs["AUDIT_D05_V005.json"]
h05 = docs["HANDOFF_D05_V006.json"]
bible = docs["D06_CHRONICLE_BIBLE_V004.json"]
routes = docs["D06_TRANSFORMATION_PATHS_V004.json"]
q06 = docs["D06_PLAYER_APPROVAL_QUEUE_V004.json"]
a06 = docs["AUDIT_D06_V004.json"]
h06 = docs["HANDOFF_D06_V004.json"]
d07 = docs["D07_PLAYER_APPROVAL_QUEUE_V004.json"]
audit = docs["AUDIT_D12_V004.json"]
handoff = docs["HANDOFF_D12_V004.json"]
release = docs["D12_RELEASE_CANDIDATE_V004.json"]

check(d05["input_head"] == "c3bba6e1495bd76c0f967fe45727388b9de0fb86", "D05 input design head")
check(d05["decisions"][0]["status"] == "CURSOR_RECONCILED_TO_CYCLE_V0033", "D05 pointer decision")
check(d05["decisions"][0]["investigation_result"]["current_manifest"]["current_cycle"].endswith("CYCLE_V0033.json"), "manifest pointer evidence")
check(d05["decisions"][1]["status"] == "APPROVED_PENDING_GATES", "future promotion approval")
check(d05["decisions"][1]["promotion_performed"] is False, "promotion not performed")
check(d05["decisions"][2]["status"] == "COMMITMENT_RECORDED_BLOCKER_REMAINS", "secret handling remains blocked")
check(d05["decisions"][3]["status"] == "NOT_GRANTED", "scene permission not granted")
check(a05["finding"]["severity"] == "resolved", "D05 pointer finding resolved")
check(a05["result"] == "PASS_WITH_UNKNOWN", "D05 audit gate")
check(h05["master_head_sha_at_review"] == "735fe5d52e2761c4d492fe873a4b6bbcce17654a", "D05 master head")

decision = next(x for x in q06["decisions"] if x["id"] == "APPROVAL-D06-001")
check(decision["status"] == "AUTHORIAL_TARGET_RECORDED_BLOCKED_SOURCE_RECONCILIATION", "D06 decision status")
check("antes de 1970" in decision["selected_target"], "M3.01 retiming recorded")
check("mortal" in decision["selected_target"], "Bart mortal through M3.01")
check("1970-12-25" in decision["selected_target"], "Embrace cutoff")
check(decision["actual_event"] == "NOT_ESTABLISHED", "Embrace is not an established event")
check(decision["authorial_sequence"]["status"] == "CANDIDATE_DESIGN_NOT_EVENT", "future dramatic sequence remains design")
check(bible["player_intent"]["chronology_gate"] == "BLOCKED_CONFLICT", "D06 chronology gate")
check(bible["operational_target_gate"] == "BLOCKED_CONFLICT", "D06 operational gate")
check("antes de 1970" in routes["route_policy"], "route policy uses revised target")
route = next(x for x in routes["routes"] if x["id"] == "ROUTE-VAMPIRE-BY-2010")
check(route["status"] == "AUTHORIAL_TARGET_SELECTED_PENDING_SOURCE_RECONCILIATION", "route remains blocked")
check("scene permission" in route["if_unavailable"], "no permission inferred from target")
check(next(x for x in a06["findings"] if x["id"] == "D06-F-004")["classification"] == "RESOLVED", "D06 pointer finding closed")
check(next(x for x in a06["findings"] if x["id"] == "D06-F-006")["classification"] == "BLOCKED_CONFLICT", "D06 chronology finding remains")
check("M2.03" in audit["source_verification"]["character_state_ref"]["verified_text"], "state ref mismatch recorded")
check("fim dos anos 1970" in audit["source_verification"]["episode"]["verified_text"], "episode conflict evidence recorded")
check(h06["next_phase_boundary"].startswith("Documentary decision state only"), "D06 handoff boundary")

d07a = next(x for x in d07["decisions"] if x["id"] == "APPROVAL-D07-001")
check(d07a["status"] == "APPROVED_PENDING_SOURCE_RECONCILIATION", "D07 conditional decision preserved")
check(d07["no_scene_authorization"] is True or d07.get("no_scene_authorization") is None, "D07 queue schema")
check(d07.get("no_scene_authorization", d07.get("no_scene_authorization", True)) is True, "D07 no scene authorization")

c03 = next(x for x in audit["checks"] if x["id"] == "D12-03")
c19 = next(x for x in audit["checks"] if x["id"] == "D12-19")
c23 = next(x for x in audit["checks"] if x["id"] == "D12-23")
c17 = next(x for x in audit["checks"] if x["id"] == "D12-17")
check(c03["result"] == "PASS", "D12 current pointer gate")
check(c19["result"] == "BLOCKED_CONFLICT", "D12 chronology gate")
check(c23["result"] == "BLOCKED_CONFLICT", "D12 state provenance gate")
check(c17["result"] == "PENDING_READBACK", "remote readback pending before publication")
check(audit["operational_gate"] == "BLOCKED_CONFLICT", "D12 operational gate remains blocked")
check(audit["narrator_status"] == "NOT_READY_FOR_NARRATOR", "D12 narrator status")
check(audit["phase_gates"]["D06_TARGET"] == "BLOCKED_CONFLICT", "D06 target phase gate")
check(next(x for x in audit["checks"] if x["id"] == "D12-10")["result"] == "BLOCKED_EXTERNAL_DEPENDENCY", "ACL dependency gate")
check(next(x for x in audit["checks"] if x["id"] == "D12-21")["result"] == "BLOCKED_EXTERNAL_DEPENDENCY", "secret commitment is not ACL")
check(next(x for x in audit["checks"] if x["id"] == "D12-15")["result"] == "NOT_READY_FOR_NARRATOR", "no narrator readiness")
check(next(x for x in audit["checks"] if x["id"] == "D12-18")["result"] == "NOT_READY_FOR_NARRATOR", "no scene readiness")
check(release["status"] == "BLOCKED_CONFLICT", "release candidate remains blocked")
check(release["promotion_decision"] == "APPROVED_PENDING_GATES", "promotion only after gates")
check(release["promotion_performed"] is False, "promotion not performed")
check(release["authorizations"]["master_write"] is False, "master not modified")
check(release["authorizations"]["scene_execution"] is False, "no scene execution")
check(release["authorizations"]["narrator_permission"] is False, "no narrator permission")
check(release["input"]["current_manifest_path"] == "novydres/MANIFEST_V47.json", "current manifest captured")
check(handoff["status"] == "BLOCKED_CONFLICT" and handoff["narrator_release"] == "NOT_READY_FOR_NARRATOR", "handoff gate")
check("no Narrator prompt" in " ".join(handoff["restrictions"]), "handoff prohibits narrator prompt")
expected = set(FILES + ["D12_VALIDATE_V004.py"])
check(set(release["outputs"]) == expected, "release output inventory")
print(f"PASS: {checks}/{checks} D12 V004 assertions")
