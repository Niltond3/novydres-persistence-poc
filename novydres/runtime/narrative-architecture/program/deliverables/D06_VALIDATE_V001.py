#!/usr/bin/env python3
"""Reproducible documentary assertions for CHR-001 D06 V001.

This narrow phase check does not validate future play, canon truth, or semantic
quality beyond the explicit assertions below. Run from repository root.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
DELIVERABLES = ROOT / "novydres/runtime/narrative-architecture/program/deliverables"
BASE_COMMIT = "38ed1270d83a3fc31ab05fc881535849f3045211"

def load(name):
    return json.loads((DELIVERABLES / name).read_text(encoding="utf-8"))

def contains_key(value, wanted):
    if isinstance(value, dict):
        return any(str(k).lower() == wanted or contains_key(v, wanted) for k, v in value.items())
    if isinstance(value, list):
        return any(contains_key(v, wanted) for v in value)
    return False

def require(condition, message):
    if not condition:
        raise AssertionError(message)

bible = load("D06_CHRONICLE_BIBLE_V001.json")
paths = load("D06_TRANSFORMATION_PATHS_V001.json")
approvals = load("D06_PLAYER_APPROVAL_QUEUE_V001.json")
tests = load("D06_ADVERSARIAL_TESTS_V001.json")
audit = load("AUDIT_D06_V001.json")
handoff = load("HANDOFF_D06_V001.json")
routes = {item["id"]: item for item in paths["routes"]}
marks = {item["id"]: item for item in bible["milestones"]}
checks = [
    ("T-D06-001", bible["checkpoint"]["sequence"] == 33 and bible["checkpoint"]["last_event_id"] == "CHR001-M301-C05-22-20261109-001", "cycle sequence and event pinned"),
    ("T-D06-002", bible["checkpoint"]["recorded_state"]["M3.01_C05"] == "CLOSED" and bible["checkpoint"]["recorded_state"]["M3.01_C06"] == "NOT_STARTED", "checkpoint close/open states preserved"),
    ("T-D06-003", bible["checkpoint"]["recorded_state"]["Bartholomeu"] == "MORTAL" and bible["checkpoint"]["recorded_state"]["Embrace"] == "NOT_OCCURRED" and not contains_key(bible, "sire") and not contains_key(bible, "embrace_date"), "no Embrace or sire asserted"),
    ("T-D06-004", "unactivated preparation proposals" in bible["precedence"]["CH00_CH07"], "legacy proposal status preserved"),
    ("T-D06-005", "M3.01 C05/C06 não definem" in bible["structure"]["checkpoint_limit"], "operational M3.01 separated from macro milestones"),
    ("T-D06-006", "do not reopen" in marks["M1"]["limits"] and "closed history is immutable" in marks["M1"]["limits"], "closed M1 boundary preserved"),
    ("T-D06-007", "current status requires source-chain reconciliation" in marks["M2"]["recorded_status"], "older M2 status not promoted"),
    ("T-D06-008", "no character or mechanical change" in bible["frozen_boundaries"] and "D06 awards nothing" in bible["dependencies"]["mechanics"], "no mechanical or character grant"),
    ("T-D06-009", "creating future dialogue, action, NPC knowledge" in bible["scope"]["excludes"][2] and "each NPC fact needs recorded acquisition" in bible["dependencies"]["npc_knowledge"], "no future scene or unacquired NPC knowledge"),
    ("T-D06-010", not bible["central_plot_ids"] and "D06 creates no causal links" in bible["dependencies"]["causality"], "no central plot or causal link created"),
    ("T-D06-011", all(r["status"] in ("OPTION_NOT_SELECTED", "ALTERNATE_REQUIRES_APPROVAL", "VALID_REPORTING; NOT_A_SUCCESS_SHORTCUT", "PLAYER_DECISION_REQUIRED") for r in paths["routes"]), "no route selected by default"),
    ("T-D06-012", "Embrace is played and persisted" in routes["ROUTE-VAMPIRE-BY-2010"]["preconditions"] and any("meaningful post-Embrace experience" in item for item in routes["ROUTE-VAMPIRE-BY-2010"]["preconditions"]), "vampire route requires played transition and aftermath"),
    ("T-D06-013", any("player approves this alternate target" in item for item in routes["ROUTE-NONVAMPIRIC-2010"]["preconditions"]), "alternate target approval gated"),
    ("T-D06-014", routes["ROUTE-UNFINISHED-OR-EARLY-TERMINAL"]["status"] == "VALID_REPORTING; NOT_A_SUCCESS_SHORTCUT", "unfinished/refusal/failure states are not success shortcuts"),
    ("T-D06-015", bible["timeline_to_2010"]["precision"].startswith("soft horizon") and "no exact dates" in bible["timeline_to_2010"]["precision"], "2010 remains a soft horizon"),
    ("T-D06-016", "Coverage + Coherence + Consequence" in bible["sufficiency_model"]["marco_close"], "milestone sufficiency contract present"),
    ("T-D06-017", "each NPC fact needs recorded acquisition" in bible["dependencies"]["npc_knowledge"] and "M1-M5" in bible["structure"]["principle"], "epistemic boundary and macro structure explicit"),
    ("T-D06-018", "MANIFEST_V46 pointer conflict" in bible["checkpoint"]["limit"] and "truth-dependent work blocked" in bible["dependencies"]["secrets"], "D05 pointer and segregation blockers retained"),
]
source_refs = bible["source_refs"]
source_ok = True
for ref in source_refs:
    actual = subprocess.check_output(["git", "rev-parse", f"{BASE_COMMIT}:{ref['path']}"], text=True).strip()
    source_ok = source_ok and actual == ref["blob_sha"]
checks.append(("T-D06-019", len(source_refs) == 20 and source_ok, "20 declared source blob pins match input commit"))
checks.append(("T-D06-020", all(key in bible for key in ("scope", "milestones", "dependencies", "graduation_gate", "pending_approvals")) and len(tests["tests"]) == 20, "JSON parse and required keys"))
require([row[0] for row in checks] == [row["id"] for row in tests["tests"]], "test ids do not match executed check ids")
for test, (test_id, passed, description) in zip(tests["tests"], checks):
    require(passed, f"{test_id} failed: {description}")
    require(test["result"] == "PASS", f"{test_id} does not record PASS")
require(bible["gate"] == audit["gate"] == handoff["gate"] == "PASS_WITH_UNKNOWN", "D06 gate fields disagree")
require(audit["validation"]["json_parse"] == "PASS" and audit["validation"]["semantic_assertions"] == "PASS", "audit validation fields are not PASS")
require(audit["independent_review"]["status"] == "COMPLETED", "independent review not recorded completed")
print(json.dumps({"result": "PASS", "checks_passed": len(checks), "source_blob_refs_verified": len(source_refs), "tests": [{"id": tid, "result": "PASS", "assertion": desc} for tid, _, desc in checks]}, ensure_ascii=False, indent=2))
