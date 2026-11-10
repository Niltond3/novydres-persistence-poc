#!/usr/bin/env python3
"""Validate the player-decision delta for CHR-001 D05-D12 V002.

This checks documentary decisions and source pins only. It does not read secret
truth files, validate canon generally, grant permissions, or simulate play.
Run from the repository root.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
DELIVERABLES = ROOT / "novydres/runtime/narrative-architecture/program/deliverables"
BASE_HEAD = "5d4f0841779a60591cd816b3363892fe33064f2a"
EXPECTED_MASTER = "124f9a9f43ed427d3db106d9187a875d74f60ac6"
EXPECTED_CYCLE_BLOB = "51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a"
checks = []

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def require(identifier, condition, detail):
    checks.append((identifier, bool(condition), detail))

def approval(doc, identifier):
    return next(x for x in doc["decisions"] if x["id"] == identifier)

def git_blob(path):
    return subprocess.check_output(
        ["git", "rev-parse", f"{BASE_HEAD}:{path}"], cwd=ROOT, text=True
    ).strip()

# Parse every versioned artifact produced by the D12 decision delta.
names = [
    "D05_PLAYER_APPROVAL_QUEUE_V002.json", "AUDIT_D05_V003.json",
    "HANDOFF_D05_V004.json", "D06_CHRONICLE_BIBLE_V002.json",
    "D06_TRANSFORMATION_PATHS_V002.json", "D06_PLAYER_APPROVAL_QUEUE_V002.json",
    "AUDIT_D06_V002.json", "HANDOFF_D06_V002.json",
    "D07_PLAYER_APPROVAL_QUEUE_V002.json", "AUDIT_D07_V002.json",
    "AUDIT_D12_V002.json", "D12_RELEASE_CANDIDATE_V002.json",
    "HANDOFF_D12_V002.json",
]
docs = {name: load(DELIVERABLES / name) for name in names}
require("D12V2-01", len(docs) == 13, "all new JSON artifacts parse")

d05 = docs["D05_PLAYER_APPROVAL_QUEUE_V002.json"]
d06q = docs["D06_PLAYER_APPROVAL_QUEUE_V002.json"]
d07 = docs["D07_PLAYER_APPROVAL_QUEUE_V002.json"]
a12 = docs["AUDIT_D12_V002.json"]
release = docs["D12_RELEASE_CANDIDATE_V002.json"]
handoff = docs["HANDOFF_D12_V002.json"]
bible = docs["D06_CHRONICLE_BIBLE_V002.json"]
paths = docs["D06_TRANSFORMATION_PATHS_V002.json"]

require("D12V2-02", approval(d05, "APPROVAL-D05-001")["status"] == "INVESTIGATED_BLOCKED_CONFLICT",
        "pointer decision records investigation and remaining conflict")
require("D12V2-03", "CYCLE_V0033" in approval(d05, "APPROVAL-D05-001")["investigation_result"]["current_cycle"]
        and "CYCLE_V0024" in approval(d05, "APPROVAL-D05-001")["investigation_result"]["conflict"],
        "cycle authority and stale manifest pointer both documented")
require("D12V2-04", approval(d05, "APPROVAL-D05-002")["status"] == "APPROVED_PENDING_GATES"
        and approval(d05, "APPROVAL-D05-002")["promotion_performed"] is False,
        "promotion authorized but not performed")
require("D12V2-05", approval(d05, "APPROVAL-D05-003")["status"] == "COMMITMENT_RECORDED_BLOCKER_REMAINS"
        and "nenhum segredo foi lido" in approval(d05, "APPROVAL-D05-003")["disposition"],
        "player commitment recorded without ACL or secret access")
require("D12V2-06", approval(d05, "APPROVAL-D05-004")["status"] == "NOT_GRANTED",
        "no scene permission recorded")
require("D12V2-07", approval(d06q, "APPROVAL-D06-001")["status"] == "DECIDED_TARGET_BLOCKED_CONFLICT"
        and approval(d06q, "APPROVAL-D06-001")["selected_target"] == "Embrace vampírico antes de 1970-12-25",
        "selected Embrace target and chronology blocker recorded")
require("D12V2-08", bible["player_intent"]["actual_event_date"] == "UNKNOWN"
        and bible["player_intent"]["status"] == "SELECTED_PLAYER_INTENT_NOT_CANON_EVENT",
        "player intent is not recorded as an occurred event")
require("D12V2-09", bible["operational_target_gate"] == "BLOCKED_CONFLICT"
        and paths["routes"][0]["status"] == "PLAYER_SELECTED_TARGET_BLOCKED_CONFLICT",
        "D06 operational route remains blocked")
require("D12V2-10", approval(d07, "APPROVAL-D07-001")["status"] == "APPROVED_PENDING_SOURCE_RECONCILIATION",
        "D07 operational consideration is approved conditionally")
require("D12V2-11", a12["operational_release"] == "AUTHORIZED_PENDING_GATES"
        and a12["operational_gate"] == "BLOCKED_CONFLICT",
        "D12 distinguishes authorization from release gate")
require("D12V2-12", release["promotion_performed"] is False
        and release["operational_release"] == "AUTHORIZED_PENDING_GATES",
        "no master promotion occurred")
require("D12V2-13", handoff["narrator_release"] == "NOT_READY_FOR_NARRATOR"
        and approval(d05, "APPROVAL-D05-004")["status"] == "NOT_GRANTED",
        "Narrator and scene permissions remain absent")

cycle_path = "novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json"
cycle = load(ROOT / cycle_path)
require("D12V2-14", git_blob(cycle_path) == EXPECTED_CYCLE_BLOB
        and cycle["sequence"] == 33 and cycle["next_role"] == "DRAMATURGO"
        and cycle["checkpoint"]["mortal"] is True
        and cycle["checkpoint"]["embrace_occurred"] is False,
        "current cycle source pin and checkpoint verified")

manifest = load(ROOT / "novydres/MANIFEST_V46.json")
current_cycle = manifest["runtime"]["orchestration"]["current_cycle"]
require("D12V2-15", current_cycle.endswith("CYCLE_V0024.json"),
        "manifest still points to CYCLE_V0024 and conflict is preserved")

episode_path = cycle["refs"]["episode"]["path"]
character_path = cycle["refs"]["character"]["path"]
require("D12V2-16", git_blob(episode_path) == cycle["refs"]["episode"]["blob_sha"]
        and git_blob(character_path) == cycle["refs"]["character"]["blob_sha"],
        "episode and character evidence match cycle pins")
character = (ROOT / character_path).read_text(encoding="utf-8")
require("D12V2-17", "fim dos anos 1970" in character.lower()
        and "Bartholomeu Krauser MORTAL" in character
        and "nenhum Abraço" in character,
        "linked character state confirms later mortal period without Embrace")
require("D12V2-18", "FUTURE_SIRE_PLAYER_SELECTION_V1.json" in character
        and "não ocorreu Abraço" in character,
        "sire selection is already recorded separately; no Embrace event inferred")

expected_paths = {f"novydres/runtime/narrative-architecture/program/deliverables/{n}" for n in names}
expected_paths.add("novydres/runtime/narrative-architecture/program/deliverables/D12_VALIDATE_V002.py")
changed = set(subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD"], cwd=ROOT, text=True
).splitlines())
untracked = set(subprocess.check_output(
    ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
).splitlines())
require("D12V2-19", changed | untracked == expected_paths,
        "working changes are limited to the 13 V002 JSON files and this validator")
require("D12V2-20", release["phase_gates"]["D06_TARGET"] == "BLOCKED_CONFLICT"
        and "D12-19" in [x["id"] for x in a12["checks"]],
        "D12 reports the chronology conflict as a gate")

failed = [item for item in checks if not item[1]]
result = {
    "result": "FAIL" if failed else "PASS",
    "checks_passed": len(checks) - len(failed),
    "checks_total": len(checks),
    "failures": [{"id": i, "detail": d} for i, ok, d in failed],
    "assertions": [{"id": i, "result": "PASS" if ok else "FAIL", "detail": d} for i, ok, d in checks],
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(1 if failed else 0)
